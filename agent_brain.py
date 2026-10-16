"""
agent_brain.py
Core AI Intelligence & Task Coordination Engine for Project Coordinator.
Manages tasks.json, executes natural language reasoning, and supports
OpenAI, Google Gemini, and offline rule-based heuristic parsing.
"""

import os
import sys
import re
import json
import threading
from datetime import datetime
from typing import List, Dict, Optional, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Load environment variables safely
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Basic fallback if python-dotenv is not installed
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

class AgentBrain:
    def __init__(self, tasks_file: Optional[str] = None):
        """Initialize the Agent Brain with storage configuration and AI settings."""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tasks_file = tasks_file or os.getenv("TASKS_FILE", os.path.join(self.base_dir, "tasks.json"))
        if not os.path.isabs(self.tasks_file):
            self.tasks_file = os.path.join(self.base_dir, self.tasks_file)
        
        self.lock = threading.Lock()
        self._ensure_storage()

        # AI Configuration
        self.ai_provider = os.getenv("AI_PROVIDER", "mistral").lower()
        self.mistral_key = os.getenv("MISTRAL_API_KEY", "")
        self.mistral_model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
        self.groq_key = os.getenv("GROQ_API_KEY", "")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def _ensure_storage(self):
        """Ensure tasks.json exists with valid JSON array."""
        with self.lock:
            if not os.path.exists(self.tasks_file):
                with open(self.tasks_file, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
            else:
                try:
                    with open(self.tasks_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if not isinstance(data, list):
                        with open(self.tasks_file, "w", encoding="utf-8") as f:
                            json.dump([], f, indent=2)
                except Exception:
                    with open(self.tasks_file, "w", encoding="utf-8") as f:
                        json.dump([], f, indent=2)

    # =========================================================================
    # Task Storage Operations (CRUD)
    # =========================================================================

    def load_tasks(self) -> List[Dict[str, Any]]:
        """Thread-safe read of all tasks from storage."""
        with self.lock:
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[AgentBrain] Error loading tasks: {e}")
                return []

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        """Thread-safe write of all tasks to storage."""
        with self.lock:
            try:
                with open(self.tasks_file, "w", encoding="utf-8") as f:
                    json.dump(tasks, f, indent=2, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"[AgentBrain] Error saving tasks: {e}")
                return False

    def generate_next_id(self, tasks: Optional[List[Dict[str, Any]]] = None) -> str:
        """Generate the next task ID, e.g. TASK-107."""
        if tasks is None:
            tasks = self.load_tasks()
        
        max_id = 100
        for task in tasks:
            tid = task.get("id", "")
            match = re.search(r"\d+", str(tid))
            if match:
                num = int(match.group())
                if num > max_id:
                    max_id = num
        return f"TASK-{max_id + 1}"

    def get_tasks(self, status: Optional[str] = None, priority: Optional[str] = None, 
                  search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve tasks with optional filtering."""
        tasks = self.load_tasks()
        filtered = tasks

        if status and status.lower() != "all":
            filtered = [t for t in filtered if t.get("status", "").lower() == status.lower()]

        if priority and priority.lower() != "all":
            filtered = [t for t in filtered if t.get("priority", "").lower() == priority.lower()]

        if search:
            query = search.lower()
            filtered = [
                t for t in filtered 
                if query in t.get("title", "").lower() 
                or query in t.get("description", "").lower()
                or query in t.get("assigned_to", "").lower()
                or query in t.get("id", "").lower()
                or any(query in tag.lower() for tag in t.get("tags", []))
            ]

        return filtered

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single task by ID."""
        tasks = self.load_tasks()
        for task in tasks:
            if task.get("id", "").upper() == task_id.upper().strip():
                return task
        return None

    def add_task(self, title: str, description: str = "", priority: str = "medium",
                 assigned_to: str = "Unassigned", due_date: Optional[str] = None,
                 tags: Optional[List[str]] = None, subtasks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Add a new task to tasks.json."""
        tasks = self.load_tasks()
        now = datetime.now().isoformat(timespec="seconds")

        new_task = {
            "id": self.generate_next_id(tasks),
            "title": title.strip(),
            "description": description.strip(),
            "status": "todo",
            "priority": priority.lower() if priority.lower() in ["low", "medium", "high", "urgent"] else "medium",
            "assigned_to": assigned_to.strip() if assigned_to else "Unassigned",
            "due_date": due_date or datetime.now().strftime("%Y-%m-%d"),
            "created_at": now,
            "updated_at": now,
            "tags": tags or ["general"],
            "subtasks": subtasks or []
        }

        tasks.append(new_task)
        self.save_tasks(tasks)
        return new_task

    def update_task(self, task_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update fields of an existing task."""
        tasks = self.load_tasks()
        target_idx = None
        for idx, task in enumerate(tasks):
            if task.get("id", "").upper() == task_id.upper().strip():
                target_idx = idx
                break

        if target_idx is None:
            return None

        task = tasks[target_idx]
        allowed_keys = ["title", "description", "status", "priority", "assigned_to", "due_date", "tags", "subtasks"]
        for key, val in kwargs.items():
            if key in allowed_keys and val is not None:
                if key == "status":
                    task[key] = val.lower()
                elif key == "priority":
                    task[key] = val.lower()
                else:
                    task[key] = val

        task["updated_at"] = datetime.now().isoformat(timespec="seconds")
        tasks[target_idx] = task
        self.save_tasks(tasks)
        return task

    def update_status(self, task_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        """Quick status updater (todo, in_progress, completed, cancelled)."""
        valid_statuses = {
            "done": "completed",
            "complete": "completed",
            "completed": "completed",
            "in progress": "in_progress",
            "inprogress": "in_progress",
            "in_progress": "in_progress",
            "todo": "todo",
            "to-do": "todo",
            "pending": "todo",
            "cancelled": "cancelled"
        }
        normalized = valid_statuses.get(new_status.lower().strip(), new_status.lower().strip())
        return self.update_task(task_id, status=normalized)

    def delete_task(self, task_id: str) -> bool:
        """Delete task by ID."""
        tasks = self.load_tasks()
        orig_len = len(tasks)
        tasks = [t for t in tasks if t.get("id", "").upper() != task_id.upper().strip()]
        if len(tasks) < orig_len:
            self.save_tasks(tasks)
            return True
        return False

    def get_summary(self) -> Dict[str, Any]:
        """Compute aggregated project statistics and metrics."""
        tasks = self.load_tasks()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
        todo = sum(1 for t in tasks if t.get("status") == "todo")
        cancelled = sum(1 for t in tasks if t.get("status") == "cancelled")

        completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0

        # High priority pending tasks
        high_priority = [
            {"id": t.get("id"), "title": t.get("title"), "status": t.get("status"), "assigned_to": t.get("assigned_to")}
            for t in tasks if t.get("priority") in ["high", "urgent"] and t.get("status") != "completed"
        ]

        # Workload per member
        workload: Dict[str, int] = {}
        for t in tasks:
            assignee = t.get("assigned_to", "Unassigned")
            workload[assignee] = workload.get(assignee, 0) + 1

        return {
            "total_tasks": total,
            "completed": completed,
            "in_progress": in_progress,
            "todo": todo,
            "cancelled": cancelled,
            "completion_rate": completion_rate,
            "high_priority_pending": high_priority,
            "workload": workload
        }

    # =========================================================================
    # Natural Language Understanding & AI Reasoning
    # =========================================================================

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user's instruction or question.
        Uses OpenAI or Gemini if configured; falls back to robust local heuristic NLP.
        """
        cleaned_query = query.strip()
        if not cleaned_query:
            return {
                "success": False,
                "intent": "empty",
                "response": "Please provide an instruction or question.",
                "action_taken": False
            }

        # Check if valid external AI provider can be called
        has_mistral = bool(self.mistral_key and not self.mistral_key.startswith("your_"))
        has_groq = bool(self.groq_key and not self.groq_key.startswith("your_"))
        has_openai = bool(self.openai_key and not self.openai_key.startswith("your_"))
        has_gemini = bool(self.gemini_key and not self.gemini_key.startswith("your_"))

        if self.ai_provider == "mistral" and has_mistral:
            try:
                res = self._call_mistral_agent(cleaned_query)
                if res:
                    return res
            except Exception as e:
                print(f"[AgentBrain] Mistral error: {e}. Falling back to heuristic NLP.")

        elif self.ai_provider == "groq" and has_groq:
            try:
                res = self._call_groq_agent(cleaned_query)
                if res:
                    return res
            except Exception as e:
                print(f"[AgentBrain] Groq error: {e}. Falling back to heuristic NLP.")

        elif self.ai_provider == "openai" and has_openai:
            try:
                return self._call_openai_agent(cleaned_query)
            except Exception as e:
                print(f"[AgentBrain] OpenAI error: {e}. Falling back to heuristic NLP.")

        elif self.ai_provider == "gemini" and has_gemini:
            try:
                return self._call_gemini_agent(cleaned_query)
            except Exception as e:
                print(f"[AgentBrain] Gemini error: {e}. Falling back to heuristic NLP.")

        # Default / Fallback: Fast, reliable rule-based heuristic parsing
        return self._heuristic_nlp_reasoning(cleaned_query)

    def _heuristic_nlp_reasoning(self, text: str) -> Dict[str, Any]:
        """
        Intelligent rule-based parsing for task management commands,
        supporting English and Hindi/Hinglish phrasing.
        """
        lower = text.lower()

        # 1. Summary / Status intent
        if any(w in lower for w in ["summary", "status", "overview", "kaisa chal raha", "project report", "kya status hai", "progress"]):
            summary = self.get_summary()
            msg = (
                f"📊 **Project Status Summary**\n"
                f"• Total Tasks: {summary['total_tasks']}\n"
                f"• ✅ Completed: {summary['completed']} ({summary['completion_rate']}%)\n"
                f"• ⏳ In Progress: {summary['in_progress']}\n"
                f"• 📋 Todo: {summary['todo']}\n\n"
            )
            if summary["high_priority_pending"]:
                msg += "⚠️ **High Priority Pending:**\n"
                for item in summary["high_priority_pending"][:3]:
                    msg += f"- [{item['id']}] {item['title']} ({item['assigned_to']})\n"
            else:
                msg += "🎉 No urgent or high priority pending tasks!"
            return {
                "success": True,
                "intent": "summary",
                "response": msg,
                "action_taken": False,
                "data": summary
            }

        # 2. Mark task completed / done
        complete_match = re.search(r"(?:complete|done|finish|khatam|mark as done)\s+(?:task\s+)?(TASK-\d+|\d+)", lower, re.IGNORECASE)
        if complete_match:
            raw_id = complete_match.group(1).upper()
            task_id = raw_id if raw_id.startswith("TASK-") else f"TASK-{raw_id}"
            updated = self.update_status(task_id, "completed")
            if updated:
                return {
                    "success": True,
                    "intent": "complete_task",
                    "response": f"✅ Great job! Task **{task_id}** ('{updated['title']}') is now marked as **Completed**.",
                    "action_taken": True,
                    "data": updated
                }
            return {
                "success": False,
                "intent": "complete_task",
                "response": f"❌ Could not find task with ID {task_id}.",
                "action_taken": False
            }

        # 3. Mark in progress
        inprogress_match = re.search(r"(?:start|in progress|working on|chalu karo)\s+(?:task\s+)?(TASK-\d+|\d+)", lower, re.IGNORECASE)
        if inprogress_match:
            raw_id = inprogress_match.group(1).upper()
            task_id = raw_id if raw_id.startswith("TASK-") else f"TASK-{raw_id}"
            updated = self.update_status(task_id, "in_progress")
            if updated:
                return {
                    "success": True,
                    "intent": "update_task",
                    "response": f"⏳ Task **{task_id}** ('{updated['title']}') status changed to **In Progress**.",
                    "action_taken": True,
                    "data": updated
                }
            return {
                "success": False,
                "intent": "update_task",
                "response": f"❌ Task {task_id} not found.",
                "action_taken": False
            }

        # 4. Delete task
        delete_match = re.search(r"(?:delete|remove|hata do|hatao)\s+(?:task\s+)?(TASK-\d+|\d+)", lower, re.IGNORECASE)
        if delete_match:
            raw_id = delete_match.group(1).upper()
            task_id = raw_id if raw_id.startswith("TASK-") else f"TASK-{raw_id}"
            if self.delete_task(task_id):
                return {
                    "success": True,
                    "intent": "delete_task",
                    "response": f"🗑️ Task **{task_id}** has been removed from the project.",
                    "action_taken": True
                }
            return {
                "success": False,
                "intent": "delete_task",
                "response": f"❌ Task {task_id} not found.",
                "action_taken": False
            }

        # 5. List tasks
        if any(w in lower for w in ["list tasks", "show tasks", "all tasks", "kya tasks hai", "tasks dikhao", "view tasks", "pending tasks"]):
            status_filter = "todo" if "pending" in lower else None
            tasks = self.get_tasks(status=status_filter)
            if not tasks:
                return {
                    "success": True,
                    "intent": "list_tasks",
                    "response": "No matching tasks found in the project.",
                    "action_taken": False,
                    "data": []
                }
            msg = f"📋 **Found {len(tasks)} Tasks:**\n"
            for t in tasks[:8]:
                icon = "✅" if t.get("status") == "completed" else ("⏳" if t.get("status") == "in_progress" else "📋")
                msg += f"• {icon} `[{t.get('id')}]` **{t.get('title')}** | Assigned: {t.get('assigned_to')} | Priority: {t.get('priority').upper()}\n"
            if len(tasks) > 8:
                msg += f"... and {len(tasks) - 8} more. Use the dashboard to view all."
            return {
                "success": True,
                "intent": "list_tasks",
                "response": msg,
                "action_taken": False,
                "data": tasks
            }

        # 6. Add / Create new task
        add_match = re.search(r"(?:add task|create task|new task|naya task banao|naya task|add:)\s*(.*)", text, re.IGNORECASE)
        if add_match or lower.startswith("add ") or lower.startswith("create "):
            raw_content = add_match.group(1) if add_match else text.split(" ", 1)[1]
            title = raw_content.strip()

            # Priority extraction
            priority = "medium"
            if re.search(r"\b(high|urgent|zaroori)\b", title, re.IGNORECASE):
                priority = "high"
                title = re.sub(r"\b(priority\s*:?\s*(high|urgent)|high priority)\b", "", title, flags=re.IGNORECASE).strip()
            elif re.search(r"\b(low)\b", title, re.IGNORECASE):
                priority = "low"
                title = re.sub(r"\b(priority\s*:?\s*low|low priority)\b", "", title, flags=re.IGNORECASE).strip()

            # Assignee extraction
            assignee = "Unassigned"
            assign_match = re.search(r"(?:assigned to|assign to|for)\s+([A-Za-z0-9_-]+)", title, re.IGNORECASE)
            if assign_match:
                assignee = assign_match.group(1)
                title = title[:assign_match.start()] + title[assign_match.end():]
                title = title.strip()

            # Clean trailing and leading symbols
            title = re.sub(r"^[:\s\-]+", "", title)
            title = re.sub(r"[\.,;]+$", "", title).strip()
            if not title:
                title = "New Unspecified Task"

            new_task = self.add_task(
                title=title,
                description=f"Created via coordinator command from: '{text}'",
                priority=priority,
                assigned_to=assignee
            )
            return {
                "success": True,
                "intent": "add_task",
                "response": f"✨ Created new task **[{new_task['id']}]**: '{new_task['title']}'\n• Priority: {new_task['priority'].upper()}\n• Assigned to: {new_task['assigned_to']}",
                "action_taken": True,
                "data": new_task
            }

        # 7. Help / Capabilities
        if any(w in lower for w in ["help", "madad", "kya kar sakte ho", "commands"]):
            help_text = (
                "🤖 **Project Coordinator Agent Brain**\n"
                "I can coordinate, assign, track, and summarize your project tasks.\n\n"
                "💡 **Try commands like:**\n"
                "• *'Status'* or *'Summary'* - View completion rate and metrics\n"
                "• *'List tasks'* - Show current active tasks\n"
                "• *'Add task: Build OAuth login assigned to Rahul priority high'*\n"
                "• *'Mark TASK-102 completed'*\n"
                "• *'Start TASK-103'*\n"
                "• *'Delete TASK-105'*"
            )
            return {
                "success": True,
                "intent": "help",
                "response": help_text,
                "action_taken": False
            }

        # 8. Conversational fallback
        return {
            "success": True,
            "intent": "chat",
            "response": f"Understood: '{text}'. If this was meant as a task, try saying: 'Add task: {text}'. Otherwise, type 'help' to see what I can do!",
            "action_taken": False
        }

    def _call_mistral_agent(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Mistral AI with structured instructions for project coordination."""
        import requests
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.mistral_key}",
            "Content-Type": "application/json"
        }
        tasks_summary = json.dumps(self.load_tasks()[:8], indent=2)
        system_prompt = (
            "You are SyncPulse AI, the Project Coordinator Brain. You manage project tasks stored in tasks.json.\n"
            f"Current tasks overview: {tasks_summary}\n\n"
            "Analyze the user's message. Output a valid JSON object strictly matching:\n"
            "{\n"
            '  "intent": "add_task" | "complete_task" | "update_task" | "delete_task" | "summary" | "list_tasks" | "chat",\n'
            '  "task_data": { "id": "TASK-XXX", "title": "...", "priority": "high|medium|low", "assigned_to": "..." },\n'
            '  "response": "User-friendly answer or confirmation message"\n'
            "}"
        )
        payload = {
            "model": self.mistral_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=12)
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return self._execute_parsed_action(parsed)
        return None

    def _call_groq_agent(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Groq Cloud with fast Llama 3 model."""
        import requests
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        tasks_summary = json.dumps(self.load_tasks()[:8], indent=2)
        system_prompt = (
            "You are SyncPulse AI, the Project Coordinator Brain. Output valid JSON strictly:\n"
            "{\n"
            '  "intent": "add_task" | "complete_task" | "update_task" | "delete_task" | "summary" | "list_tasks" | "chat",\n'
            '  "task_data": { "id": "TASK-XXX", "title": "...", "priority": "high|medium|low", "assigned_to": "..." },\n'
            '  "response": "User-friendly answer or confirmation message"\n'
            "}"
        )
        payload = {
            "model": self.groq_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=8)
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return self._execute_parsed_action(parsed)
        return None

    def _execute_parsed_action(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Apply parsed intent and task updates to storage."""
        intent = parsed.get("intent", "chat")
        tdata = parsed.get("task_data", {})
        action_taken = False
        result_data = None

        if intent == "add_task" and tdata.get("title"):
            result_data = self.add_task(
                title=tdata.get("title"),
                description=tdata.get("description", ""),
                priority=tdata.get("priority", "medium"),
                assigned_to=tdata.get("assigned_to", "Unassigned")
            )
            action_taken = True
        elif intent == "complete_task" and tdata.get("id"):
            result_data = self.update_status(tdata.get("id"), "completed")
            action_taken = bool(result_data)
        elif intent == "delete_task" and tdata.get("id"):
            action_taken = self.delete_task(tdata.get("id"))

        return {
            "success": True,
            "intent": intent,
            "response": parsed.get("response", "Request processed."),
            "action_taken": action_taken,
            "data": result_data or tdata
        }

    def _call_openai_agent(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI with system instructions to interpret project coordination requests."""
        import openai
        client = openai.OpenAI(api_key=self.openai_key)

        tasks_summary = json.dumps(self.load_tasks()[:10], indent=2)
        system_prompt = (
            "You are the AI Project Coordinator Brain. You manage project tasks stored in tasks.json.\n"
            f"Current tasks overview: {tasks_summary}\n\n"
            "Analyze the user's message. Output a valid JSON object strictly matching:\n"
            "{\n"
            '  "intent": "add_task" | "complete_task" | "update_task" | "delete_task" | "summary" | "list_tasks" | "chat",\n'
            '  "task_data": { "id": "TASK-XXX", "title": "...", "priority": "high|medium|low", "assigned_to": "..." },\n'
            '  "response": "User-friendly answer or confirmation message"\n'
            "}"
        )

        response = client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} if "gpt-4o" in self.openai_model else None,
            temperature=0.3
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        intent = parsed.get("intent", "chat")
        tdata = parsed.get("task_data", {})
        action_taken = False
        result_data = None

        if intent == "add_task" and tdata.get("title"):
            result_data = self.add_task(
                title=tdata.get("title"),
                description=tdata.get("description", ""),
                priority=tdata.get("priority", "medium"),
                assigned_to=tdata.get("assigned_to", "Unassigned")
            )
            action_taken = True
        elif intent == "complete_task" and tdata.get("id"):
            result_data = self.update_status(tdata.get("id"), "completed")
            action_taken = bool(result_data)
        elif intent == "delete_task" and tdata.get("id"):
            action_taken = self.delete_task(tdata.get("id"))

        return {
            "success": True,
            "intent": intent,
            "response": parsed.get("response", "Request processed."),
            "action_taken": action_taken,
            "data": result_data or tdata
        }

    def _call_gemini_agent(self, prompt: str) -> Dict[str, Any]:
        """Call Google GenAI client if configured."""
        from google import genai
        client = genai.Client(api_key=self.gemini_key)
        
        system_instruction = (
            "You are an AI Project Coordinator. Analyze user commands regarding task management, "
            "and provide concise, helpful project coordination answers."
        )
        response = client.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config={"system_instruction": system_instruction}
        )
        return {
            "success": True,
            "intent": "gemini_response",
            "response": response.text,
            "action_taken": False
        }

# =============================================================================
# CLI Testing & Demonstration
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧠 Project Coordinator - Agent Brain Diagnostic Test")
    print("=" * 60)
    brain = AgentBrain()
    
    summary = brain.get_summary()
    print(f"📁 Loaded tasks from: {brain.tasks_file}")
    print(f"📊 Total Tasks: {summary['total_tasks']} | Completed: {summary['completed']} ({summary['completion_rate']}%)")
    print(f"⚙️ Active AI Provider: {brain.ai_provider} (Fallback: Heuristic NLP active)")
    print("-" * 60)

    # Test sample command
    sample_queries = [
        "What is the status of our project?",
        "Add task: Implement user password reset assigned to Alex priority high",
        "Show tasks"
    ]

    for q in sample_queries:
        print(f"\n💬 Test Query: '{q}'")
        res = brain.process_query(q)
        print(f"🤖 Response:\n{res['response']}")
    print("\n" + "=" * 60)
    print("✅ Agent Brain is fully operational.")
