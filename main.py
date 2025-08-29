# FILE: main.py
import asyncio
import logging
from pyrogram import Client, filters, idle
from config import BOT_TOKEN, API_ID, API_HASH, OWNER_ID, ARTIST_CHECK_CHAT
from handlers import (
    start_handler,
    play_handler,
    pause_handler,
    resume_handler,
    nowplaying_handler,
    seek_handler,
    set_player
)
from player import Player

logging.basicConfig(level=logging.INFO)

app = Client(
    "artist-music-bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# ===================== COMMAND HANDLERS =====================

@app.on_message(filters.command("start"))
async def _start(client, message):
    await start_handler(client, message)

@app.on_message(filters.command("play"))
async def _play(client, message):
    await play_handler(client, message)

@app.on_message(filters.command("pause"))
async def _pause(client, message):
    await pause_handler(client, message)

@app.on_message(filters.command("resume"))
async def _resume(client, message):
    await resume_handler(client, message)

@app.on_message(filters.command("nowplaying"))
async def _nowplaying(client, message):
    await nowplaying_handler(client, message)

@app.on_message(filters.command("seek"))
async def _seek(client, message):
    await seek_handler(client, message)

# ===================== BACKGROUND TASK =====================

async def artist_check_task(client: Client):
    while True:
        try:
            target = ARTIST_CHECK_CHAT or OWNER_ID
            await client.send_message(target, "Artist check successful ✨")
        except Exception as e:
            logging.warning("Artist check failed: %s", e)
        await asyncio.sleep(60)

# ===================== MAIN =====================

async def main():
    await app.start()
    pl = Player(app)
    await pl.start()
    await set_player(pl)

    asyncio.create_task(artist_check_task(app))

    print("✅ Bot started. Press Ctrl+C to stop.")
    try:
        await idle()
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
    
