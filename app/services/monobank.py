import logging
from dataclasses import dataclass
from datetime import datetime

import aiohttp

from app.services.cache import cache_get, cache_set

logger = logging.getLogger(__name__)

MONOBANK_URL = "https://api.monobank.ua/bank/currency"
CACHE_KEY = "monobank:rates"

# ISO 4217 numeric codes
_CODE_MAP = {
    840: "USD",
    978: "EUR",
    826: "GBP",
    756: "CHF",
    985: "PLN",
}
UAH_CODE = 980

SUPPORTED_CURRENCIES = list(_CODE_MAP.values())


@dataclass
class CurrencyRate:
    currency: str
    buy: float
    sell: float
    updated_at: datetime


async def fetch_rates() -> dict[str, CurrencyRate]:
    cached = await cache_get(CACHE_KEY)
    if cached:
        return _parse_cached(cached)

    async with aiohttp.ClientSession() as session:
        async with session.get(MONOBANK_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            data = await resp.json()

    await cache_set(CACHE_KEY, data)
    logger.info("Fetched fresh rates from monobank")
    return _parse_raw(data)


def _parse_raw(data: list[dict]) -> dict[str, CurrencyRate]:
    rates: dict[str, CurrencyRate] = {}
    for item in data:
        code_a = item.get("currencyCodeA")
        code_b = item.get("currencyCodeB")
        if code_b != UAH_CODE or code_a not in _CODE_MAP:
            continue
        currency = _CODE_MAP[code_a]
        rates[currency] = CurrencyRate(
            currency=currency,
            buy=item.get("rateBuy", item.get("rateCross", 0)),
            sell=item.get("rateSell", item.get("rateCross", 0)),
            updated_at=datetime.fromtimestamp(item["date"]),
        )
    return rates


def _parse_cached(data: list[dict]) -> dict[str, CurrencyRate]:
    return _parse_raw(data)


def format_rate(rate: CurrencyRate) -> str:
    return (
        f"💵 <b>{rate.currency}/UAH</b>\n"
        f"Купівля:  <b>{rate.buy:.2f} ₴</b>\n"
        f"Продаж:   <b>{rate.sell:.2f} ₴</b>\n"
        f"Оновлено: {rate.updated_at.strftime('%d.%m.%Y %H:%M')}"
    )


def format_digest(rates: dict[str, CurrencyRate]) -> str:
    lines = ["🌅 <b>Курс валют на сьогодні</b>\n"]
    for currency in ("USD", "EUR"):
        if currency in rates:
            r = rates[currency]
            lines.append(
                f"<b>{r.currency}</b>  купівля <b>{r.buy:.2f}</b> | продаж <b>{r.sell:.2f}</b>"
            )
    return "\n".join(lines)
