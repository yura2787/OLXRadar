from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards import currencies_keyboard

router = Router()

WELCOME_TEXT = (
    "👋 <b>Привіт!</b> Я бот курсу валют.\n\n"
    "Показую актуальні курси з <b>monobank</b>.\n\n"
    "Обери валюту 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=currencies_keyboard())
