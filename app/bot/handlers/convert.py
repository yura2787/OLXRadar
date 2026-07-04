from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.monobank import SUPPORTED_CURRENCIES, fetch_rates

router = Router()

USAGE = "Використання: /convert <сума> <валюта>\nПриклад: /convert 100 USD"


@router.message(Command("convert"))
async def cmd_convert(message: Message) -> None:
    parts = message.text.strip().split()

    if len(parts) != 3:
        await message.answer(USAGE)
        return

    _, raw_amount, currency = parts
    currency = currency.upper()

    try:
        amount = float(raw_amount.replace(",", "."))
    except ValueError:
        await message.answer(f"❌ <b>{raw_amount}</b> — не число.\n{USAGE}", parse_mode="HTML")
        return

    if currency not in SUPPORTED_CURRENCIES:
        supported = ", ".join(SUPPORTED_CURRENCIES)
        await message.answer(f"❌ Валюта <b>{currency}</b> не підтримується.\nДоступні: {supported}", parse_mode="HTML")
        return

    try:
        rates = await fetch_rates()
    except Exception:
        await message.answer("⚠️ Не вдалося отримати курс. Спробуй пізніше.")
        return

    rate = rates.get(currency)
    if not rate:
        await message.answer(f"❌ Курс для {currency} тимчасово недоступний.")
        return

    result_buy = amount * rate.buy
    result_sell = amount * rate.sell

    await message.answer(
        f"💱 <b>{amount:,.2f} {currency}</b>\n\n"
        f"За курсом купівлі:  <b>{result_buy:,.2f} ₴</b>\n"
        f"За курсом продажу: <b>{result_sell:,.2f} ₴</b>\n\n"
        f"<i>Курс: {rate.buy:.2f} / {rate.sell:.2f}</i>",
        parse_mode="HTML",
    )
