import customtkinter as ctk
from models import Task

class WeeklyKanbanView(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color="transparent")
        self.app_controller = app_controller
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=1)
        self.columns_data = [
            ("Jāsāk", "Jāsāk"),
            ("Daru", "Daru"),
            ("Pabeidzu", "Pabeidzu")
        ]
        self.column_frames = {}
        for i, (col_title, col_status) in enumerate(self.columns_data):
            col_frame = ctk.CTkFrame(self, corner_radius=8)
            col_frame.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
            col_frame.grid_rowconfigure(1, weight=1)
            col_frame.grid_columnconfigure(0, weight=1)
            header_lbl = ctk.CTkLabel(col_frame, text=col_title, font=ctk.CTkFont(size=14, weight="bold"))
            header_lbl.grid(row=0, column=0, pady=10)
            scroll_frame = ctk.CTkScrollableFrame(col_frame, label_text="")
            scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
            self.column_frames[col_status] = scroll_frame

    def refresh(self):
        for scroll_frame in self.column_frames.values():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
        weekly_tasks = [t for t in self.app_controller.tasks if t.in_weekly]
        for task in weekly_tasks:
            scroll_frame = self.column_frames.get(task.status)
            if scroll_frame:
                self._create_task_card(scroll_frame, task)

    def _create_task_card(self, parent, task: Task):
        card = ctk.CTkFrame(parent, fg_color=("gray90", "gray20"), corner_radius=6)
        card.pack(fill="x", padx=5, pady=5)
        title_lbl = ctk.CTkLabel(card, text=task.title, font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
        title_lbl.pack(anchor="w", padx=10, pady=(8, 2))
        info_text = f"Prioritāte: {task.priority} | Termiņš: {task.deadline}"
        info_lbl = ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(size=11), text_color="gray")
        info_lbl.pack(anchor="w", padx=10, pady=(0, 5))
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=5, pady=(0, 8))
        if task.status == "Jāsāk":
            ctk.CTkButton(btn_frame, text="Darīt", height=24, font=ctk.CTkFont(size=11),
                          command=lambda: self.change_status(task, "Daru")).pack(side="right", padx=2)

        elif task.status == "Daru":
            ctk.CTkButton(btn_frame, text="Atlikt", height=24, width=60, font=ctk.CTkFont(size=11),
                          command=lambda: self.change_status(task, "Jāsāk")).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="Gatavs", height=24, font=ctk.CTkFont(size=11),
                          command=lambda: self.change_status(task, "Pabeidzu")).pack(side="right", padx=2)

        elif task.status == "Pabeidzu":
            ctk.CTkButton(btn_frame, text="Darīt", height=24, font=ctk.CTkFont(size=11),
                          command=lambda: self.change_status(task, "Daru")).pack(side="left", padx=2)
        remove_btn = ctk.CTkButton(btn_frame, text="x", width=24, height=24, fg_color="transparent",
                                   text_color="red", hover_color=("gray80", "gray30"),
                                   command=lambda: self.remove_from_weekly(task))
        remove_btn.pack(side="right" if task.status != "Jāsāk" else "left", padx=2)

    def change_status(self, task: Task, new_status: str):
        task.status = new_status
        self.app_controller.refresh_all_views()

    def remove_from_weekly(self, task: Task):
        task.in_weekly = False
        self.app_controller.refresh_all_views()