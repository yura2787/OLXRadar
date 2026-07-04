from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db import AsyncSessionFactory, add_subscriber, get_subscriber, remove_subscriber

router = Router()


@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message) -> None:
    async with AsyncSessionFactory() as session:
        existing = await get_subscriber(session, message.from_user.id)
        if existing and existing.is_active:
            await message.answer("✅ Ти вже підписаний на щоранкову розсилку о 9:00.")
            return

        await add_subscriber(session, message.from_user.id, message.chat.id)

    await message.answer(
        "🔔 Підписку оформлено!\n"
        "Щоранку о <b>9:00</b> надсилатиму курс USD та EUR.",
        parse_mode="HTML",
    )


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message) -> None:
    async with AsyncSessionFactory() as session:
        removed = await remove_subscriber(session, message.from_user.id)

    if removed:
        await message.answer("🔕 Підписку скасовано.")
    else:
        await message.answer("ℹ️ Ти не підписаний на розсилку.")
