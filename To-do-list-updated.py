import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database Setup
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date TEXT NOT NULL)''')
conn.commit()

# Function to Add Task
def add_task():
    task = task_entry.get()
    priority = priority_var.get()
    due_date = due_date_entry.get()
    
    if task and priority and due_date:
        cursor.execute("INSERT INTO tasks (task, priority, due_date) VALUES (?, ?, ?)", 
                       (task, priority, due_date))
        conn.commit()
        load_tasks()
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please fill in all fields!")

# Function to Delete Selected Task
def delete_task():
    try:
        selected_item = task_tree.selection()[0]
        task_id = task_tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        task_tree.delete(selected_item)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete!")

# Function to Load Tasks from Database
def load_tasks():
    task_tree.delete(*task_tree.get_children())
    cursor.execute("SELECT * FROM tasks ORDER BY priority DESC, due_date ASC")
    for row in cursor.fetchall():
        task_tree.insert("", "end", values=row)

# GUI Setup
root = tk.Tk()
root.title("Enhanced To-Do List App")
root.geometry("500x600")
root.configure(bg="#f4f4f4")

# Custom Styling
title_label = tk.Label(root, text="To-Do List App", font=("Arial", 16, "bold"), bg="#f4f4f4", fg="#333")
title_label.pack(pady=10)

# Task Entry Field
task_entry = tk.Entry(root, width=50, font=("Arial", 12))
task_entry.pack(pady=5)

# Priority Dropdown
priority_var = tk.StringVar(value="Medium")
priority_label = tk.Label(root, text="Priority:", bg="#f4f4f4")
priority_label.pack()
priority_dropdown = ttk.Combobox(root, textvariable=priority_var, values=["High", "Medium", "Low"])
priority_dropdown.pack()

# Due Date Entry
due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):", bg="#f4f4f4")
due_date_label.pack()
due_date_entry = tk.Entry(root, width=20)
due_date_entry.pack()

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, bg="#FF5733", fg="white", font=("Arial", 12, "bold"))
delete_button.pack(pady=5)

# Task List Table
task_tree = ttk.Treeview(root, columns=("ID", "Task", "Priority", "Due Date"), show="headings")
task_tree.heading("ID", text="ID")
task_tree.heading("Task", text="Task")
task_tree.heading("Priority", text="Priority")
task_tree.heading("Due Date", text="Due Date")
task_tree.pack(pady=10)

# Load Tasks on Start
load_tasks()

# Run the Application
root.mainloop()
