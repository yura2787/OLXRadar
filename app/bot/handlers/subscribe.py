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
            await message.answer("✅ You are already subscribed to the daily digest at 9:00.")
            return

        await add_subscriber(session, message.from_user.id, message.chat.id)

    await message.answer(
        "🔔 Subscribed!\n"
        "Every morning at <b>9:00</b> I'll send you USD and EUR rates.",
        parse_mode="HTML",
    )


@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message) -> None:
    async with AsyncSessionFactory() as session:
        removed = await remove_subscriber(session, message.from_user.id)

    if removed:
        await message.answer("🔕 Unsubscribed successfully.")
    else:
        await message.answer("ℹ️ You are not subscribed to the digest.")
