"""
run_demo.py
SyncPulse AI · Master 1-Click Launcher for Hackathon Kurukshetra
Starts the Web Dashboard and Telegram Bot Listener together in one unified process.
Automatically opens your browser to http://127.0.0.1:5000.
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def print_banner():
    print(r"""
=============================================================================
   _____                      ____        _              ___    ____
  / ___/__  ______  _____    / __ \__  __/ /_______     /   |  /  _/
  \__ \/ / / / __ \/ ___/   / /_/ / / / / // ___/ _ \   / /| |  / /  
 ___/ / /_/ / / / / /__    / ____/ /_/ / /(__  )  __/  / ___ |_/ /   
/____/\__, /_/ /_/\___/   /_/    \__,_/_//____/\___/  /_/  |_/___/   
     /____/                                                           
       Autonomous AI Group Project Coordinator · Track W-PS-1
       Hackathon Kurukshetra · Dr. D.Y. Patil Institute, Pune
=============================================================================
""")

def start_flask():
    """Runs the Flask web dashboard on port 5000."""
    try:
        import app
        app.app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Web Dashboard error: {e}")

def start_telegram_bot():
    """Runs the Telegram Bot listener in a background thread."""
    bot_script = os.path.join(os.path.dirname(__file__), "backend", "bot_service.py")
    if os.path.exists(bot_script):
        try:
            print("🤖 Starting Telegram Bot Listener (@syncpulse_solver_bot)...")
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
            from bot_service import run_bot
            run_bot()
        except Exception as e:
            print(f"⚠️ Telegram Bot background listener notice: {e}")
            print("👉 You can also interact via the Web Dashboard presets!")

def main():
    print_banner()
    print("⏳ Initializing SyncPulse AI Workspace...")
    
    # 1. Start Flask Dashboard in background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    time.sleep(1.5)
    print("✅ Web Dashboard running at: http://127.0.0.1:5000")

    # 2. Automatically open web browser
    try:
        print("🌐 Opening Executive Dashboard in your browser...")
        webbrowser.open("http://127.0.0.1:5000")
    except Exception:
        pass

    print("-" * 75)
    print("✨ SyncPulse AI is LIVE and READY FOR JUDGE DEMONSTRATION!")
    print("📌 Open Dashboard: http://127.0.0.1:5000")
    print("📌 Telegram Bot:   https://t.me/syncpulse_solver_bot")
    print("-" * 75)
    print("Press Ctrl + C at any time to shut down the server.")
    print("=" * 75 + "\n")

    # 3. Start Telegram Bot in main thread with auto-reconnect
    start_telegram_bot()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 SyncPulse AI gracefully stopped. Goodbye!")
        sys.exit(0)
