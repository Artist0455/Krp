import os
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

# CONFIG
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# CLIENTS
bot = Client("artist_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client(session_string=STRING_SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(user)

# FLASK SERVER FOR RENDER
flask_app = Flask(__name__)
@flask_app.route("/")
def home():
    return "✅ Artist Music Bot is running!"

# YT-DLP OPTIONS
ydl_opts = {"format": "bestaudio/best", "outtmpl": "downloads/%(title)s.%(ext)s", "quiet": True}

queues = {}

# HANDLERS
@bot.on_message(filters.command("start"))
async def start_handler(_, message):
    await message.reply(f"👋 Hello {message.from_user.mention}!\n🎵 I am Artist Music Bot. Use /play <song> to stream music!")

@bot.on_message(filters.command("play") & filters.group)
async def play_handler(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Provide a song name or YouTube link.")
    query = " ".join(message.command[1:])
    m = await message.reply("⏳ Downloading song...")
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        file_path = ydl.prepare_filename(info)
        title = info.get("title", "Unknown")
    chat_id = message.chat.id
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append((title, file_path))
    if len(queues[chat_id]) == 1:
        await pytgcalls.join_group_call(chat_id, AudioPiped(file_path))
        await m.edit(f"🎶 Now Playing: {title}\n💡 Requested by: {message.from_user.mention}")
    else:
        await m.edit(f"➕ Added to queue: {title}")

# ARTIST CHECK LOOP
async def artist_check():
    while True:
        await asyncio.sleep(60)
        try:
            await bot.send_message(OWNER_ID, "✅ Artist check successful ✨")
        except: pass

# MAIN
async def main():
    await bot.start()
    await user.start()
    await pytgcalls.start()
    asyncio.create_task(artist_check())
    print("✅ Artist Music Bot started!")
    await idle()
    await bot.stop()
    await user.stop()

# RUN
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
