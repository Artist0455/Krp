# FILE: player.py
class Player:
    def __init__(self, client):
        self.client = client

    async def start(self):
        print("🎵 Player initialized successfully.")
