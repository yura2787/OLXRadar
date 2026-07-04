from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards import back_keyboard, currencies_keyboard
from app.services.monobank import fetch_rates, format_rate

router = Router()


@router.callback_query(F.data.startswith("rate:"))
async def show_rate(callback: CallbackQuery) -> None:
    currency = callback.data.split(":")[1]
    await callback.answer()

    try:
        rates = await fetch_rates()
    except Exception:
        await callback.message.edit_text(
            "⚠️ Не вдалося отримати курс. Спробуй пізніше.",
            reply_markup=back_keyboard(),
        )
        return

    rate = rates.get(currency)
    if not rate:
        await callback.message.edit_text(
            f"❌ Курс для {currency} недоступний.",
            reply_markup=back_keyboard(),
        )
        return

    await callback.message.edit_text(
        format_rate(rate),
        reply_markup=back_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back:menu")
async def back_to_menu(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(
        "Обери валюту 👇",
        reply_markup=currencies_keyboard(),
    )
