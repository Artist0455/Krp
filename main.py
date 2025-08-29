import os
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

# ------------------ CONFIG ------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ------------------ CLIENTS ------------------
# Bot for commands
bot = Client("artist_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# User session for VC
user = Client(session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(user)

# ------------------ FLASK SERVER ------------------
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Artist Music Bot is running!"

# ------------------ YT-DLP OPTIONS ------------------
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "quiet": True
}

# ------------------ QUEUE ------------------
queues = {}  # chat_id -> [(title, file_path)]

# ------------------ HANDLERS ------------------
@bot.on_message(filters.command("start"))
async def start_handler(_, message):
    welcome_text = f"""
👋 Hello {message.from_user.mention}!

🎵 I am **Artist Music Bot**,  
I can play music directly in your group's voice chat.  

✨ Commands:
- `/play <song name or YouTube link>` → Play music
- `/ping` → Check bot status

🚀 Add me to your group and enjoy nonstop music!
"""
    await message.reply(welcome_text)

@bot.on_message(filters.command("ping"))
async def ping_handler(_, message):
    await message.reply("🏓 Pong! I am alive.")

@bot.on_message(filters.command("play") & filters.group)
async def play_handler(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a song name or YouTube link.")

    query = " ".join(message.command[1:])
    m = await message.reply("⏳ Downloading song...")

    # YT-DLP download
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        file_path = ydl.prepare_filename(info)
        title = info.get("title", "Unknown")

    chat_id = message.chat.id

    # Queue setup
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append((title, file_path))

    # VC join and play
    if len(queues[chat_id]) == 1:  # first song
        await pytgcalls.join_group_call(chat_id, AudioPiped(file_path))
        await m.edit(f"🎶 Now Playing: **{title}**\n💡 Requested by: {message.from_user.mention}")
    else:
        await m.edit(f"➕ Added to queue: **{title}**")

# ------------------ ARTIST CHECK LOOP ------------------
async def artist_check():
    while True:
        await asyncio.sleep(60)
        try:
            await bot.send_message(OWNER_ID, "✅ Artist check successful ✨")
        except:
            pass

# ------------------ MAIN ------------------
async def main():
    await bot.start()
    await user.start()
    await pytgcalls.start()
    asyncio.create_task(artist_check())
    print("✅ Artist Music Bot started!")
    await idle()
    await bot.stop()
    await user.stop()

# ------------------ RUN ------------------
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    
