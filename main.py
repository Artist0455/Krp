import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL

# Env variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")

# Bot client
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# User session (for VC join)
user = Client(
    STRING_SESSION,
    api_id=API_ID,
    api_hash=API_HASH
)

# PyTgCalls setup
pytgcalls = PyTgCalls(user)


# --- YT-DLP Options ---
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(id)s.%(ext)s",
    "quiet": True,
    "no_warnings": True,
}


async def download_song(query):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        return ydl.prepare_filename(info), info.get("title")


# --- Commands ---
@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("👋 Welcome to **Artist Music Bot** 🎶")


@bot.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please give a song name or URL.")

    query = " ".join(message.command[1:])
    m = await message.reply("⏳ Downloading...")

    file_path, title = await download_song(query)

    chat_id = message.chat.id
    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(file_path)
    )

    await m.edit_text(f"▶️ Playing **{title}**\n\nArtist Music streaming ✨")


# --- Run bot ---
async def main():
    await bot.start()
    await user.start()
    await pytgcalls.start()
    print("✅ Bot started.")
    await idle()
    await bot.stop()
    await user.stop()

if __name__ == "__main__":
    asyncio.run(main())
    
