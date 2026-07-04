

## Features

- 📊 Live exchange rates — USD, EUR, GBP, CHF, PLN vs UAH
- 💱 Currency converter — `/convert 100 USD`
- 🔔 Daily digest — subscribe to get USD & EUR rates every morning at 9:00
- ⚡ Redis caching — respects monobank rate limit (1 req/min)
- 🐘 PostgreSQL — stores subscribers for the daily digest

## Stack

| Technology | Purpose |
|---|---|
| aiogram 3 | Telegram bot framework |
| aiohttp | Async HTTP requests to monobank API |
| PostgreSQL + SQLAlchemy | Storing digest subscribers |
| Redis | Caching exchange rates |
| APScheduler | Daily digest at 9:00 Kyiv time |
| Docker Compose | One-command deploy |
| uv | Fast Python package manager |

## How to run

```bash
# 1. Clone the repo
git clone https://github.com/your-username/currency-bot
cd currency-bot

# 2. Create .env from example
cp .env.example .env
# Add your BOT_TOKEN to .env

# 3. Start
docker compose up --build
```

## Project structure

```
app/
├── bot/
│   ├── handlers/       # /start, rates, /convert, /subscribe
│   └── keyboards.py    # Inline currency buttons
├── db/
│   ├── models.py       # Subscriber model
│   ├── repository.py   # DB queries
│   └── session.py      # Async SQLAlchemy engine
├── services/
│   ├── monobank.py     # API client + response parser
│   └── cache.py        # Redis cache wrapper
├── scheduler.py        # APScheduler daily digest job
├── config.py           # Pydantic settings
└── main.py             # Entry point
```

## Commands

| Command | Description |
|---|---|
| `/start` | Show currency menu |
| `/convert <amount> <currency>` | Convert to UAH |
| `/subscribe` | Subscribe to daily digest |
| `/unsubscribe` | Unsubscribe |
