from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Subscriber


async def get_subscriber(session: AsyncSession, user_id: int) -> Subscriber | None:
    result = await session.execute(
        select(Subscriber).where(Subscriber.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def add_subscriber(session: AsyncSession, user_id: int, chat_id: int) -> Subscriber:
    existing = await get_subscriber(session, user_id)
    if existing:
        existing.is_active = True
        await session.commit()
        return existing

    subscriber = Subscriber(user_id=user_id, chat_id=chat_id)
    session.add(subscriber)
    await session.commit()
    return subscriber


async def remove_subscriber(session: AsyncSession, user_id: int) -> bool:
    subscriber = await get_subscriber(session, user_id)
    if not subscriber or not subscriber.is_active:
        return False
    subscriber.is_active = False
    await session.commit()
    return True


async def get_all_active_subscribers(session: AsyncSession) -> list[Subscriber]:
    result = await session.execute(
        select(Subscriber).where(Subscriber.is_active == True)  # noqa: E712
    )
    return list(result.scalars().all())
