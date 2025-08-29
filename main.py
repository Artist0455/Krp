import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import InputStream, AudioPiped
import yt_dlp
from datetime import datetime

# Environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Pyrogram Clients
bot = Client("ArtistBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("ArtistUser", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# PyTgCalls
pytgcalls = PyTgCalls(user)

# In-memory queues
queues = {}

# Helper: download from yt-dlp
def yt_download(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info["title"], info["duration"], ydl.prepare_filename(info)

# Commands
@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text("✨ **Welcome to Artist Music Bot** 🎶\n\nUse /play <song name or link> to stream music!")

@bot.on_message(filters.command("play"))
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("❌ Please provide a song name or YouTube URL.")
    query = " ".join(m.command[1:])
    await m.reply("🔎 Searching...")
    title, duration, filename = yt_download(query)

    chat_id = m.chat.id
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append((title, filename))

    if not pytgcalls.active_calls.get(chat_id):
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(
                AudioPiped(filename)
            )
        )
        await m.reply_photo(
            "https://i.ibb.co/YRgt0ZT/music.jpg",
            caption=f"🎶 **Artist Music Streaming**\n\n▶️ Now Playing: **{title}**\n🕒 Duration: {duration} sec\n📌 Requested by: {m.from_user.mention}"
        )
    else:
        await m.reply(f"➕ Added to queue: **{title}**")

@bot.on_message(filters.command("skip"))
async def skip(_, m: Message):
    chat_id = m.chat.id
    if chat_id in queues and queues[chat_id]:
        queues[chat_id].pop(0)
        if queues[chat_id]:
            title, filename = queues[chat_id][0]
            await pytgcalls.change_stream(
                chat_id,
                InputStream(AudioPiped(filename))
            )
            await m.reply(f"⏭ Skipped! Now playing: **{title}**")
        else:
            await pytgcalls.leave_group_call(chat_id)
            await m.reply("✅ Queue empty, left VC.")
    else:
        await m.reply("❌ No songs in queue.")

@bot.on_message(filters.command("pause"))
async def pause(_, m: Message):
    await pytgcalls.pause_stream(m.chat.id)
    await m.reply("⏸ Paused!")

@bot.on_message(filters.command("resume"))
async def resume(_, m: Message):
    await pytgcalls.resume_stream(m.chat.id)
    await m.reply("▶️ Resumed!")

# Auto Artist Check every 1 min
async def artist_check():
    while True:
        await asyncio.sleep(60)
        try:
            await bot.send_message(OWNER_ID, "✅ Artist check successful ✨")
        except:
            pass

async def main():
    await bot.start()
    await user.start()
    await pytgcalls.start()
    asyncio.create_task(artist_check())
    print("✅ Artist Music Bot Started")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
    
