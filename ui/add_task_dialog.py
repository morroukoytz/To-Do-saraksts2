import customtkinter as ctk
from models import Task


class AddTaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.app_controller = app_controller

        self.title("Pievienot jaunu uzdevumu")
        self.geometry("400x350")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Uzdevuma nosaukums:").pack(anchor="w", padx=20, pady=(20, 5))
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Ievadiet nosaukumu...")
        self.title_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self, text="Prioritāte:").pack(anchor="w", padx=20, pady=(0, 5))
        self.priority_var = ctk.StringVar(value="Vidēja")
        self.priority_menu = ctk.CTkOptionMenu(
            self,
            values=["Augsta", "Vidēja", "Zema"],
            variable=self.priority_var
        )
        self.priority_menu.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(self, text="Izpildes termiņš:").pack(anchor="w", padx=20, pady=(0, 5))
        self.deadline_entry = ctk.CTkEntry(self, placeholder_text="2026-12-31")
        self.deadline_entry.pack(fill="x", padx=20, pady=(0, 20))

        save_btn = ctk.CTkButton(self, text="Pievienot", command=self.save_task)
        save_btn.pack(fill="x", padx=20, pady=10)

    def save_task(self):
        title = self.title_entry.get().strip()
        priority = self.priority_var.get()
        deadline = self.deadline_entry.get().strip()
        if not title:
            return
        if not deadline:
            deadline = "2026-12-31"
        new_task = Task(title=title, priority=priority, deadline=deadline, status="Jāsāk", in_weekly=True)
        self.app_controller.tasks.append(new_task)
        self.app_controller.refresh_all_views()
        self.destroy()