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
        "start_hour": 18,
    },
    1: {
        "location": "Fitness corner beside Hillion Mall, Bukit Panjang",
        "time": "6pm to 8pm",
        "start_hour": 18,
    },
    2: {
        "location": "Fitness corner along Waterway Park, Punggol",
        "time": "6pm to 8pm",
        "start_hour": 18,
    },
    3: {
        "location": "Fitness corner opposite Redhill MRT",
        "time": "6pm to 8pm",
        "start_hour": 18,
    },
    4: {
        "location": "Fitness corner opposite Ubi MRT",
        "time": "6pm to 8pm",
        "start_hour": 18,
    },
    5: {
        "location": "Bukit Canberra ActiveSG",
        "time": "2pm to 4pm",
        "start_hour": 14,
    },
}

async def send_reminder():
    now = datetime.datetime.now(TIMEZONE)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday()

    if tomorrow_weekday not in SESSIONS:
        return  # No session on Sunday

    session = SESSIONS[tomorrow_weekday]
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
        await bot.send_message(chat_id=CHANNEL_ID, text=message)

async def send_session_started():
    now = datetime.datetime.now(TIMEZONE)
    today_weekday = now.weekday()

    if today_weekday not in SESSIONS:
        return  # No session on Sunday

    session = SESSIONS[today_weekday]
    message = (
        f"Our session at {session['location']} has begun! 🏃🏻‍♂️\n"
        f"See you if you're coming to train 🙌!"
    )
    async with Bot(token=BOT_TOKEN) as bot:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)

async def main():
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    # Nightly reminder at 10:00 PM
    scheduler.add_job(
        send_reminder,
        trigger="cron",
        hour=22,
        minute=0,
    )

    # Session started message — weekdays at 6:00 PM
    scheduler.add_job(
        send_session_started,
        trigger="cron",
        day_of_week="mon,tue,wed,thu,fri",
        hour=18,
        minute=0,
    )

    # Session started message — Saturday at 2:00 PM
    scheduler.add_job(
        send_session_started,
        trigger="cron",
        day_of_week="sat",
        hour=14,
        minute=0,
    )

    scheduler.start()
    print("Bot is running. Reminders scheduled at 10:00 PM SGT nightly. Session start messages scheduled.")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
