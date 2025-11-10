from flask import Flask, request, abort, jsonify
import os

app = Flask(__name__)

ADMIN_KEY = os.environ.get("ADMIN_KEY")      # <- must be set in Render (not in code)
DATABASE_URL = os.environ.get("DATABASE_URL")  # <- provided by Render Postgres or set manually

@app.route("/")
def index():
    return """
    <h1>Render PaaS Security Demo</h1>
    <p>Home page — public.</p>
    <p>Try /admin (requires ADMIN_KEY) and /dbinfo (shows env-driven DB URL presence).</p>
    """

# Simple header-based admin protection (demo only)
@app.route("/admin")
def admin():
    # Client sends key in header X-ADMIN-KEY or ?key=...
    key = request.headers.get("X-ADMIN-KEY") or request.args.get("key")
    if not ADMIN_KEY:
        abort(500, "ADMIN_KEY is not configured (server misconfiguration).")
    if not key or key != ADMIN_KEY:
        abort(401, "Unauthorized: missing or invalid admin key.")
    return "<h2>Admin area — secret info</h2><p>Congrats, you used the admin key stored in env vars.</p>"

@app.route("/dbinfo")
def dbinfo():
    if DATABASE_URL:
        return jsonify({"database_url_present": True, "short_preview": DATABASE_URL[:50] + "..."})
    else:
        return jsonify({"database_url_present": False})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
