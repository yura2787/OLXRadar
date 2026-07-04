from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.monobank import SUPPORTED_CURRENCIES

CURRENCY_FLAGS = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "CHF": "🇨🇭",
    "PLN": "🇵🇱",
}


def currencies_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=f"{CURRENCY_FLAGS.get(c, '')} {c}",
            callback_data=f"rate:{c}",
        )
        for c in SUPPORTED_CURRENCIES
    ]
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="◀️ Back", callback_data="back:menu")
    ]])
