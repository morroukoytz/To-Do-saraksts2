import json
import os

TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, title: str, priority: str, deadline: str, status: str = "Jāsāk", in_weekly: bool = False):
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.status = status
        self.in_weekly = in_weekly

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
            "in_weekly": self.in_weekly
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            title=data.get("title", ""),
            priority=data.get("priority", "Vidēja"),
            deadline=data.get("deadline", ""),
            status=data.get("status", "Jāsāk"),
            in_weekly=data.get("in_weekly", False)
        )


def get_sample_tasks() -> list:
    return [
        Task("Sagatavot gada pārskatu", "Augsta", "2026-10-25", status="Jāsāk", in_weekly=True),
        Task("Nopirkt pārtiku nedēļai", "Zema", "2026-10-21", status="Daru", in_weekly=True),
        Task("Projekta dokumentācija", "Vidēja", "2026-11-01", status="Pabeidzu", in_weekly=True),
        Task("Atjaunināt projekta atkarības", "Zema", "2026-10-28", status="Jāsāk", in_weekly=False)
    ]


def load_tasks() -> list:
    if not os.path.exists(TASKS_FILE):
        initial_tasks = get_sample_tasks()
        save_tasks(initial_tasks)
        return initial_tasks

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data]
    except Exception as e:
        print(f"Kļūda ielādējot datus: {e}")
        return get_sample_tasks()


def save_tasks(tasks: list):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Kļūda saglabājot datus: {e}")