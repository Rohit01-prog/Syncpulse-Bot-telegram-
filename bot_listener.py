"""
bot_listener.py
Telegram Bot Listener & Event Dispatcher for SyncPulse AI.
Track W-PS-1 · Hackathon Kurukshetra 2026 · CIMAGE Professional College, Patna
Listens to user commands (/tasks, /status, /blocker, /unblock, /team, /checkin, /admin)
and natural language messages, routing them through Agent Core & Supabase.
Includes an interactive console fallback mode for local testing.
"""

import os
import sys
import argparse
from typing import Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure backend directory is in Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

# Load environment variables safely
try:
    from dotenv import load_dotenv
    load_dotenv()
    backend_env = os.path.join(os.path.dirname(__file__), "backend", ".env")
    if os.path.exists(backend_env):
        load_dotenv(backend_env)
except ImportError:
    pass

from agent_brain import AgentBrain

def format_telegram_task_list(tasks, title_prefix="Track W-PS-1 Sprint Pipelines"):
    """Format tasks list with emoji badges and model specs."""
    if not tasks:
        return f"📋 <b>{title_prefix}</b>\nNo tasks found."
    
    text = f"📋 <b>{title_prefix} ({len(tasks)} AI Models)</b>\n\n"
    for t in tasks:
        status = t.get("status", "todo")
        is_blocked = t.get("is_blocked", False)
        if is_blocked:
            icon = "🛑"
            badge = f"BLOCKED ({t.get('blocker_reason', 'Dependency')})"
        elif status == "completed":
            icon = "✅"
            badge = "COMPLETED"
        elif status == "in_progress":
            icon = "⏳"
            badge = "IN PROGRESS"
        else:
            icon = "📋"
            badge = "TODO"

        progress = t.get("progress", 100 if status == "completed" else 50)
        prio = t.get("priority", "medium").upper()
        
        text += f"{icon} <code>[{t.get('task_code', t.get('id', 'AI'))}]</code> <b>{t.get('title')}</b>\n"
        text += f"   • Assigned: <b>{t.get('assigned_to', t.get('assigned_to_name', 'Engineer'))}</b> ({t.get('role', 'Developer')})\n"
        text += f"   • Status: <b>{badge}</b> | Progress: {progress}%\n"
        if t.get("specs"):
            text += f"   • Specs: <i>{t.get('specs')}</i>\n"
        if t.get("student_phone"):
            text += f"   • Contact: {t.get('student_phone')} | {t.get('student_email')}\n"
        text += "\n"
    return text.strip()

def run_interactive_console(brain: AgentBrain):
    """Fallback interactive CLI mode to test bot capabilities without Telegram connection."""
    print("=" * 70)
    print("🤖 SyncPulse AI - Interactive Terminal Coordinator (Track W-PS-1)")
    print("🏛️ CIMAGE Professional College, Patna · Hackathon Kurukshetra 2026")
    print("=" * 70)
    print("Type bot commands or natural language project requests.")
    print("Supported commands: /tasks, /status, /blocker, /unblock, /team, /help, exit")
    print("-" * 70)

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Exiting bot coordinator.")
                break

            # Process command
            if user_input.startswith("/tasks") or user_input.startswith("/list"):
                parts = user_input.split()
                status_filter = parts[1] if len(parts) > 1 else None
                tasks = brain.get_tasks(status=status_filter)
                print(f"\n🤖 Bot:\n{format_telegram_task_list(tasks)}")

            elif user_input.startswith("/status") or user_input.startswith("/summary"):
                tasks = brain.get_tasks()
                blocked = [t for t in tasks if t.get("is_blocked")]
                print("\n🤖 Bot:")
                print(f"📊 Sprint Velocity: {len(tasks)} AI Models Tracked")
                print(f"🛡️ Health Status: {'🟢 OPTIMAL (100%)' if not blocked else '🔴 CRITICAL BLOCKER (75%)'}")
                if blocked:
                    print(f"⚠️ Active Blocker on {blocked[0].get('assigned_to', 'Kabir')}: {blocked[0].get('blocker_reason')}")
                    print("💡 Tip: Type /unblock to simulate Meera releasing the GPU keys!")

            elif user_input.startswith("/blocker") or user_input.startswith("/radar"):
                print("\n🤖 Bot:")
                print("🚨 CRITICAL BLOCKER RADAR: AI-103")
                print("• Model: Llama-3 8B Instruction Fine-Tuning")
                print("• Engineer: Kabir Verma (CIMAGE-BCA-2026-103)")
                print("• Blocker: Waiting for GPU Cluster API Key & S3 Weights from Meera Sharma")
                print("• Autonomous Action: AgentCore logged blocker and dispatched urgent escalation to Meera.")

            elif user_input.startswith("/unblock") or user_input.startswith("/resolve"):
                tasks = brain.get_tasks()
                for t in tasks:
                    if t.get("id") == "AI-103" or t.get("task_code") == "AI-103":
                        t["status"] = "completed"
                        t["is_blocked"] = False
                        t["progress"] = 100
                        t.pop("blocker_reason", None)
                        t.pop("blocked_by_member_name", None)
                brain.save_tasks(tasks)
                print("\n🤖 Bot:")
                print("⚡ AUTONOMOUS UNBLOCK EXECUTED!")
                print("👩‍💻 Meera Sharma has provided the A100 GPU cluster API key & S3 weights.")
                print("👨‍💻 Kabir Verma's Llama-3 8B pipeline is now 100% COMPLETED.")
                print("Sprint health restored to 100% velocity!")

            elif user_input.startswith("/team") or user_input.startswith("/students"):
                print("\n🤖 Bot:")
                print("👨‍💻 CIMAGE Hackathon Student Team Dossier:")
                print("1. Meera Sharma · NLP Lead · CIMAGE-BCA-2026-101 · meera.sharma26@cimage.in · +91 98350 41201")
                print("2. Sumit Kumar · CV Engineer · CIMAGE-BCA-2026-102 · sumit.kumar26@cimage.in · +91 94712 88302")
                print("3. Kabir Verma · LLM Engineer · CIMAGE-BCA-2026-103 · kabir.verma26@cimage.in · +91 91234 56789")
                print("4. Jaswant Singh · Audio ML · CIMAGE-BCA-2026-104 · jaswant.singh26@cimage.in · +91 97890 12345")
                print("👑 Rohit · Chief Admin · CIMAGE-BCA-2025-30916 · rohit.bcastudent25.30916@cimage.in · +91 93041 24508")

            elif user_input.startswith("/help") or user_input.startswith("/start"):
                print("\n🤖 Bot:")
                print("Available commands:")
                print("• /tasks - List all 4 AI model pipelines")
                print("• /status - View overall sprint health and blockers")
                print("• /blocker - Deep-dive into Kabir Verma's GPU blocker")
                print("• /unblock - Resolve blocker autonomously")
                print("• /team - View official student contact dossier")
                print("• Or type any natural language question!")

            else:
                # Direct natural language agent query
                res = brain.process_query(user_input)
                print(f"\n🤖 Bot:\n{res.get('response', '')}")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 Bot listener terminated.")
            break
        except Exception as e:
            print(f"\n❌ Error processing command: {e}")

def main():
    parser = argparse.ArgumentParser(description="SyncPulse AI Bot Listener")
    parser.add_argument("--interactive", action="store_true", help="Force interactive terminal mode")
    args = parser.parse_args()

    token = os.getenv("TELEGRAM_BOT_TOKEN", "8936095048:AAHGBEacdNgFe-xCLPc42JPH6oymu9z9cmo").strip()

    if args.interactive:
        brain = AgentBrain()
        run_interactive_console(brain)
    else:
        try:
            from bot_service import run_bot
            run_bot()
        except ImportError as e:
            print(f"⚠️ Notice importing bot_service: {e}. Falling back to interactive console.")
            brain = AgentBrain()
            run_interactive_console(brain)
        except Exception as e:
            print(f"❌ Telegram Bot service encountered an error: {e}")
            brain = AgentBrain()
            run_interactive_console(brain)

if __name__ == "__main__":
    main()
