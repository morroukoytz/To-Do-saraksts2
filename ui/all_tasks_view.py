import customtkinter as ctk
from models import Task
from ui.add_task_dialog import AddTaskDialog


class AllTasksView(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        self.app_controller = app_controller
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(filter_frame, text="Šķirošana:").pack(side="left", padx=(0, 10))
        self.sort_var = ctk.StringVar(value="Alfabēta secībā")
        self.sort_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=["Alfabēta secībā", "Pēc prioritātes", "Pēc statusa"],
            variable=self.sort_var,
            command=lambda _: self.refresh()
        )
        self.sort_menu.pack(side="left", padx=5)

        add_btn = ctk.CTkButton(filter_frame, text="Pievienot", width=120, command=self.open_add_dialog)
        add_btn.pack(side="right", padx=5)

        self.tasks_scroll_frame = ctk.CTkScrollableFrame(self, label_text="Visi uzdevumi")
        self.tasks_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.refresh()

    def open_add_dialog(self):
        AddTaskDialog(self, self.app_controller)

    def refresh(self):
        for widget in self.tasks_scroll_frame.winfo_children():
            widget.destroy()
        sort_type = self.sort_var.get()
        sorted_tasks = list(self.app_controller.tasks)
        if sort_type == "Alfabēta secībā":
            sorted_tasks.sort(key=lambda x: x.title.lower())
        elif sort_type == "Pēc prioritātes":
            priority_weight = {"Augsts": 1, "Vidējais": 2, "Zems": 3}
            sorted_tasks.sort(key=lambda x: priority_weight.get(x.priority, 4))
        elif sort_type == "Pēc statusa":
            sorted_tasks.sort(key=lambda x: x.status)
        for task in sorted_tasks:
            self._create_task_row(self.tasks_scroll_frame, task)

    def _create_task_row(self, parent, task: Task):
        row_frame = ctk.CTkFrame(parent, fg_color=("gray85", "gray25"))
        row_frame.pack(fill="x", padx=5, pady=5)

        info_text = f"{task.title} | Prioritāte: {task.priority} | Termiņš: {task.deadline} | Statuss: {task.status}"
        lbl = ctk.CTkLabel(row_frame, text=info_text, anchor="w")
        lbl.pack(side="left", padx=10, pady=8, fill="x", expand=True)

        delete_btn = ctk.CTkButton(
            row_frame,
            text="Dzēst",
            width=70,
            fg_color="transparent",
            text_color="red",
            hover_color=("gray80", "gray30"),
            border_width=1,
            border_color="red",
            command=lambda t=task: self.delete_task(t)
        )
        delete_btn.pack(side="right", padx=5)

        weekly_btn_text = "Nedēļā" if task.in_weekly else "Pievienot nedēļai"
        weekly_btn = ctk.CTkButton(
            row_frame,
            text=weekly_btn_text,
            width=130,
            fg_color="green" if task.in_weekly else "transparent",
            border_width=1,
            command=lambda t=task: self.toggle_weekly(t)
        )
        weekly_btn.pack(side="right", padx=5)

    def toggle_weekly(self, task: Task):
        task.in_weekly = not task.in_weekly
        self.app_controller.refresh_all_views()

    def delete_task(self, task: Task):
        if task in self.app_controller.tasks:
            self.app_controller.tasks.remove(task)
            self.app_controller.refresh_all_views()
