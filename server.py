from flask import Flask
import threading
import main  # <-- yaha tumhara bot ka code import hoga

app = Flask(__name__)

@app.route("/")
def home():
    return "🎶 Artist Music Bot is Alive on Render!"

def run_bot():
    main.run_bot()  # is function ko main.py me define karenge

if __name__ == "__main__":
    # Thread me bot start karo
    threading.Thread(target=run_bot).start()
    # Web server start karo
    app.run(host="0.0.0.0", port=10000)
    
