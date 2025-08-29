# FILE: handlers.py
from pyrogram.types import Message
from config import SUPPORT_CHAT, UPDATE_CHANNEL

async def start_handler(client, message: Message):
    text = f"""
👋 Welcome **{message.from_user.first_name}** to **Artist Music Bot** 🎶  

✨ Fast play • Pause • Resume • Seek • Result • Nowplaying  

🔔 Support: {SUPPORT_CHAT or 'Not set'}  
📢 Updates: {UPDATE_CHANNEL or 'Not set'}  
"""
    await message.reply_text(text)

async def play_handler(client, message: Message):
    await message.reply_text("🎶 **Artist Music strimming...**")

async def pause_handler(client, message: Message):
    await message.reply_text("⏸️ Paused")

async def resume_handler(client, message: Message):
    await message.reply_text("▶️ Resumed")

async def nowplaying_handler(client, message: Message):
    await message.reply_text("🎧 Now Playing: Example Song")

async def seek_handler(client, message: Message):
    await message.reply_text("⏩ Seeked to new position")

async def set_player(player):
    # Future use for player object
    pass
