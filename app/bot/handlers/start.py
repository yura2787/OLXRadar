from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards import currencies_keyboard

router = Router()

WELCOME_TEXT = (
    "👋 <b>Hello!</b> I'm a currency rate bot.\n\n"
    "I show live exchange rates from <b>monobank</b>.\n\n"
    "Choose a currency 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=currencies_keyboard())
