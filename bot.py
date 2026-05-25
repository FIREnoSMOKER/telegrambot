import os
import asyncio
import datetime
import pytz
from telegram import Bot
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

TIMEZONE = pytz.timezone("Asia/Singapore")

SESSIONS = {
    0: {
        "day": "Monday",
        "location": "📍 Fitness corner in Jurong West St 64, Boon Lay, beside Block 685A",
        "time": "🕕 6:00 PM – 8:00 PM",
    },
    1: {
        "day": "Tuesday",
        "location": "📍 Fitness corner beside Hillion Mall, Bukit Panjang",
        "time": "🕕 6:00 PM – 8:00 PM",
    },
    2: {
        "day": "Wednesday",
        "location": "📍 Fitness corner along Waterway Park, Punggol",
        "time": "🕕 6:00 PM – 8:00 PM",
    },
    3: {
        "day": "Thursday",
        "location": "📍 Fitness corner opposite Redhill MRT",
        "time": "🕕 6:00 PM – 8:00 PM",
    },
    4: {
        "day": "Friday",
        "location": "📍 Fitness corner opposite Ubi MRT",
        "time": "🕕 6:00 PM – 8:00 PM",
    },
    5: {
        "day": "Saturday",
        "location": "📍 Bukit Canberra ActiveSG",
        "time": "🕑 2:00 PM – 4:00 PM",
    },
}

async def send_reminder(bot: Bot):
    now = datetime.datetime.now(TIMEZONE)
    tomorrow_weekday = (now.weekday() + 1) % 7

    if tomorrow_weekday not in SESSIONS:
        return  # No session on Sunday

    session = SESSIONS[tomorrow_weekday]
    message = (
        f"🏋️ *Train with us on {session['day']}!*\n\n"
        f"{session['location']}\n"
        f"{session['time']}\n"
        f"👕 Attire: Caliversity T-shirt\n\n"
        f"See you there!"
    )
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        send_reminder,
        trigger="cron",
        hour=22,
        minute=0,
        args=[app.bot],
    )

    async def run():
        await app.initialize()
        await app.start()
        scheduler.start()
        print("Bot is running. Reminders scheduled at 10:00 PM SGT nightly.")
        while True:
            await asyncio.sleep(3600)

    asyncio.run(run())

if __name__ == "__main__":
    main()
