from pyrogram import Client
import os

API_ID = int(input("Enter API_ID: "))
API_HASH = input("Enter API_HASH: ")

with Client("ArtistGen", api_id=API_ID, api_hash=API_HASH) as app:
    print("\nHere is your STRING_SESSION:\n")
    print(app.export_session_string())
