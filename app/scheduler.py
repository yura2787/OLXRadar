import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

from app.config import settings
from app.db import AsyncSessionFactory, get_all_active_subscribers
from app.services.monobank import fetch_rates, format_digest

logger = logging.getLogger(__name__)


async def send_daily_digest(bot: Bot) -> None:
    logger.info("Running daily digest job")

    try:
        rates = await fetch_rates()
    except Exception:
        logger.error("Failed to fetch rates for digest")
        return

    text = format_digest(rates)

    async with AsyncSessionFactory() as session:
        subscribers = await get_all_active_subscribers(session)

    logger.info("Sending digest to %d subscribers", len(subscribers))

    for sub in subscribers:
        try:
            await bot.send_message(sub.chat_id, text, parse_mode="HTML")
        except Exception as e:
            logger.warning("Failed to send digest to chat_id=%d: %s", sub.chat_id, e)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=settings.timezone)

    scheduler.add_job(
        send_daily_digest,
        trigger=CronTrigger(
            hour=settings.digest_hour,
            minute=settings.digest_minute,
            timezone=settings.timezone,
        ),
        kwargs={"bot": bot},
        id="daily_digest",
        replace_existing=True,
    )

    return scheduler
