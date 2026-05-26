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
        "location": "The fitness corner in Jurong West St 64, Boon Lay, beside Block 685A",
        "time": "6pm to 8pm",
        "image": "https://i.imgur.com/tlnktiR.jpg",
        "session_image": "https://i.imgur.com/j54XpmW.jpg",
    },
    1: {
        "location": "The fitness corner beside Hillion Mall, Bukit Panjang",
        "time": "6pm to 8pm",
        "image": "https://i.imgur.com/tx5F3UY.jpg",
        "session_image": "https://i.imgur.com/M4DbOOv.jpg",
    },
    2: {
        "location": "The calisthenics park along Punggol Waterway Point",
        "time": "6pm to 8pm",
        "image": "https://i.imgur.com/gXITNTF.jpg",
        "session_image": "https://i.imgur.com/ugsSZRB.jpg",
    },
    3: {
        "location": "The fitness corner opposite Redhill MRT",
        "time": "6pm to 8pm",
        "image": "https://i.imgur.com/1saAz2U.jpg",
        "session_image": "https://i.imgur.com/JcLnaMV.jpg",
    },
    4: {
        "location": "The fitness corner opposite Ubi MRT",
        "time": "6pm to 8pm",
        "image": "https://i.imgur.com/qWJddaT.jpg",
        "session_image": "https://i.imgur.com/Lb8nbtc.jpg",
    },
    5: {
        "location": "Bukit Canberra ActiveSG Gym",
        "time": "2pm to 4pm",
        "image": "https://i.imgur.com/5wgCJOh.jpg",
        "session_image": "https://i.imgur.com/TvmnXZH.jpg",
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

    caption = (
        f"Hey everyone! The details for the training session on {date_str} are as follows:\n\n"
        f"⏰ Time: {session['time']}\n"
        f"📍 Location: {session['location']}\n"
        f"👕 Attire: Caliversity T-shirt\n\n"
        f"See you there fellow Caliversity athletes! 👋\n"
        f"⬆️ Click on the latest pinned message to view our schedule for the week"
    )

    async with Bot(token=BOT_TOKEN) as bot:
        image_url = session.get("image")
        if image_url:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=image_url,
                caption=caption
            )
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=caption)

async def send_session_started():
    now = datetime.datetime.now(TIMEZONE)
    today_weekday = now.weekday()

    if today_weekday not in SESSIONS:
        return

    session = SESSIONS[today_weekday]
    caption = (
        f"Our session at {session['location']} has begun! 🏃🏻‍♂️\n"
        f"See you if you're coming to train 🙌!"
    )
    async with Bot(token=BOT_TOKEN) as bot:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=session["session_image"],
            caption=caption
        )

async def send_weekly_schedule():
    now = datetime.datetime.now(TIMEZONE)

    monday   = now + datetime.timedelta(days=1)
    tuesday  = now + datetime.timedelta(days=2)
    wednesday= now + datetime.timedelta(days=3)
    thursday = now + datetime.timedelta(days=4)
    friday   = now + datetime.timedelta(days=5)
    saturday = now + datetime.timedelta(days=6)
    sunday   = now + datetime.timedelta(days=7)

    def fmt(d):
        return d.strftime("%-d %B")

    wed_date = fmt(wednesday)
    sat_date = fmt(saturday)

    message = (
        f"✅ 🅒🅐🅛🅘🅥🅔🅡🅢🅘🅣🅨 ✅\n"
        f"🗓 This Week's Training Schedule 🕓\n\n"

        f"⏩ Monday, {fmt(monday)}\n"
        f"📌 Location: Boon Lay (641685)\n"
        f"🚂 Nearest Station: Boon Lay MRT (EW27)\n"
        f"🔔 Time: 6pm - 8pm\n\n"

        f"⏩ Tuesday, {fmt(tuesday)}\n"
        f"📌 Location: Hillion Mall (671180)\n"
        f"🚂 Nearest Station: Petir LRT (BP7)\n"
        f"🔔 Time: 6pm - 8pm\n\n"

        f"⏩ Wednesday, {fmt(wednesday)}\n"
        f"📌 Location: Punggol (829899)\n"
        f"🚂 Nearest Station: Punggol MRT (NE17)\n"
        f"🔔 Time: 6pm - 8pm\n\n"

        f"⏩ Thursday, {fmt(thursday)}\n"
        f"📌 Location: Redhill (151074)\n"
        f"🚂 Nearest Station: Redhill MRT (EW18)\n"
        f"🔔 Time: 6pm - 8pm\n\n"

        f"⏩ Friday, {fmt(friday)}\n"
        f"📌 Location: Ubi (403358)\n"
        f"🚂 Nearest Station: Ubi MRT (DT27)\n"
        f"🔔 Time: 6pm - 8pm\n\n"

        f"⏩ Saturday, {fmt(saturday)}\n"
        f"📌 Location: Bukit Canberra ActiveSG Gym\n"
        f"🚂 Nearest Station: Sembawang MRT (NS11)\n"
        f"🔔 Time: 2pm - 4pm\n"
        f"💰 Gym Entry Fee: $2.50\n"
        f"❕ Bring a towel + Wear shoes!\n\n"

        f"❌ Sunday, {fmt(sunday)} - No Session\n\n"

        f"🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n\n"

        f"📢 AF Classes for the week!\n\n"

        f"➡️ AF Kovan ({wed_date} 7pm - 8pm)\n\n"

        f"➡️ AF Jurong Point ({sat_date} 11am - 12pm)\n\n"

        f"🖥 Slots are limited! DM the respective AF on Instagram to register your interest!\n\n"

        f"1) anytimefitnessjurongpoint - IG\n\n"

        f"2) anytimefitnesskovan - IG"
    )

    async with Bot(token=BOT_TOKEN) as bot:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)

async def main():
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    # Nightly reminder at 10:00 PM
    scheduler.add_job(
        send_reminder,
        trigger="cron",
        hour=20,
        minute=0,
    )

    # Session started — weekdays at 6:00 PM
    scheduler.add_job(
        send_session_started,
        trigger="cron",
        day_of_week="mon,tue,wed,thu,fri",
        hour=18,
        minute=0,
    )

    # Session started — Saturday at 2:00 PM
    scheduler.add_job(
        send_session_started,
        trigger="cron",
        day_of_week="sat",
        hour=14,
        minute=0,
    )

    # Weekly schedule — every Sunday at 12:00 PM
    scheduler.add_job(
        send_weekly_schedule,
        trigger="cron",
        day_of_week="sun",
        hour=12,
        minute=0,
    )

    scheduler.start()
    print("Bot is running. All messages scheduled.")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
