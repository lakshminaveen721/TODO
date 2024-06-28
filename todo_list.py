import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import pickle
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")

        self.tasks = self.load_tasks()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(
            self.frame, 
            width=50, 
            height=10, 
            selectmode=tk.SINGLE
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.priority_var = tk.StringVar(value="Low")
        self.priority_dropdown = ttk.Combobox(
            root, 
            textvariable=self.priority_var, 
            values=["Low", "Medium", "High"],
            state="readonly",
            width=48
        )
        self.priority_dropdown.pack(pady=5)

        self.date_entry = DateEntry(root, width=48, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.date_entry.pack(pady=5)

        self.add_button = tk.Button(
            root, 
            text="Add Task", 
            width=48, 
            command=self.add_task
        )
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(
            root, 
            text="Delete Task", 
            width=48, 
            command=self.delete_task
        )
        self.delete_button.pack(pady=5)

        self.complete_button = tk.Button(
            root, 
            text="Complete Task", 
            width=48, 
            command=self.complete_task
        )
        self.complete_button.pack(pady=5)

        self.update_task_listbox()

    def add_task(self):
        task = self.entry.get()
        priority = self.priority_var.get()
        due_date = self.date_entry.get_date().strftime("%Y-%m-%d")
        if task != "":
            self.tasks.append({"task": task, "priority": priority, "due_date": due_date, "completed": False})
            self.update_task_listbox()
            self.entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def complete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks[selected_task_index]["completed"] = True
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to complete.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_str = f"{task['task']} (Priority: {task['priority']}, Due: {task['due_date']})"
            if task["completed"]:
                task_str += " - Completed"
            self.task_listbox.insert(tk.END, task_str)

    def save_tasks(self):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as f:
                tasks = pickle.load(f)
        except FileNotFoundError:
            tasks = []
        return tasks

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
