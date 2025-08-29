from flask import Flask
import threading, os

app = Flask(__name__)

@app.route('/')
def home():
    return "Artist Music Bot is running!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run).start()
    
