import customtkinter as ctk
from models import load_tasks, save_tasks
from ui.weekly_view import WeeklyKanbanView
from ui.all_tasks_view import AllTasksView


class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("To Do saraksts")
        self.geometry("1000x650")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.tasks = load_tasks()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabview.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.tab_weekly_name = "Šīs nedēļas skats"
        self.tab_all_name = "Visi uzdevumi"
        self.tabview.add(self.tab_weekly_name)
        self.tabview.add(self.tab_all_name)

        weekly_container = ctk.CTkFrame(self.tabview.tab(self.tab_weekly_name))
        weekly_container.pack(fill="both", expand=True, padx=5, pady=5)
        all_container = ctk.CTkFrame(self.tabview.tab(self.tab_all_name))
        all_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.weekly_kanban = WeeklyKanbanView(weekly_container, self)
        self.weekly_kanban.pack(fill="both", expand=True)

        self.all_tasks_view = AllTasksView(all_container, self)
        self.all_tasks_view.pack(fill="both", expand=True)

        self.refresh_all_views()

    def refresh_all_views(self):
        save_tasks(self.tasks)
        self.weekly_kanban.refresh()
        self.all_tasks_view.refresh()

    def on_tab_change(self):
        selected_tab = self.tabview.get()
        if self.tab_weekly_name in selected_tab:
            self.weekly_kanban.refresh()
        elif self.tab_all_name in selected_tab:
            self.all_tasks_view.refresh()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
