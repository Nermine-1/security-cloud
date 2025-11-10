from flask import Flask, request, abort
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
ADMIN_KEY = os.getenv("ADMIN_KEY")

@app.route("/")
def home():
    return "Welcome! Try /admin?key=YOUR_KEY"

@app.route("/admin")
def admin():
    key = request.args.get("key")
    if key != ADMIN_KEY:
        abort(403)
    return "Secret admin area!"

if __name__ == "__main__":
    app.run()
