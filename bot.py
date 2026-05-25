import os
import asyncio
import datetime
import pytz
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

TIMEZONE = pytz.timezone("Asia/Singapore")

SESSIONS = {
    0: {
        "location": "Fitness corner in Jurong West St 64, Boon Lay, beside Block 685A",
        "time": "6pm to 8pm",
    },
    1: {
        "location": "Fitness corner beside Hillion Mall, Bukit Panjang",
        "time": "6pm to 8pm",
    },
    2: {
        "location": "Fitness corner along Waterway Park, Punggol",
        "time": "6pm to 8pm",
    },
    3: {
        "location": "Fitness corner opposite Redhill MRT",
        "time": "6pm to 8pm",
    },
    4: {
        "location": "Fitness corner opposite Ubi MRT",
        "time": "6pm to 8pm",
    },
    5: {
        "location": "Bukit Canberra ActiveSG",
        "time": "2pm to 4pm",
    },
}

async def send_reminder():
    now = datetime.datetime.now(TIMEZONE)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday()

    if tomorrow_weekday not in SESSIONS:
        return  # No session on Sunday

    session = SESSIONS[tomorrow_weekday]

    # Format date as e.g. "27 May 2026"
    date_str = tomorrow.strftime("%-d %B %Y")

    message = (
        f"Hey everyone! The details for the training session on {date_str} are as follows:\n\n"
        f"⏰ Time: {session['time']}\n"
        f"📍 Location: {session['location']}\n"
        f"👕 Attire: Caliversity T-shirt\n\n"
        f"See you there fellow Caliversity athletes! 👋\n"
        f"⬆️ Click on the latest pinned message to view our schedule for the week"
    )
    async with Bot(token=BOT_TOKEN) as bot:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=message
        )

async def main():
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        send_reminder,
        trigger="cron",
        hour=22,
        minute=0,
    )
    scheduler.start()
    print("Bot is running. Reminders scheduled at 10:00 PM SGT nightly.")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
