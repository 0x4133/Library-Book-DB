import sqlite3
import tkinter as tk
from tkinter import ttk

import os

os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"


def step_through_db():
    global current_index
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    # Select all records from the upc_results table
    cursor.execute("SELECT * FROM upc_results")
    # Fetch all rows
    rows = cursor.fetchall()
    # Check if there are more rows to display
    if current_index < len(rows):
        row = rows[current_index]
        # Update the result text widget with the current row's details
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"UPC: {row[0]}\nTitle: {row[1]}\nURL: {row[2]}")
        current_index += 1
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No more entries.")
    # Close the connection
    conn.close()


def reset_index():
    global current_index
    current_index = 0
    result_text.delete("1.0", tk.END)
    result_text.insert(
        tk.END, "Press 'Next Entry' to start stepping through the entries."
    )


# Create the main window
window = tk.Tk()
window.title("Database Entries")

# Initialize the current index
current_index = 0

# Create and pack the widgets
next_button = ttk.Button(window, text="Next Entry", command=step_through_db)
next_button.pack()

reset_button = ttk.Button(window, text="Back to the Top", command=reset_index)
reset_button.pack()

result_text = tk.Text(window, height=10, width=80)
result_text.pack()

# Set initial text in the result text widget
result_text.insert(tk.END, "Press 'Next Entry' to start stepping through the entries.")

# Start the main event loop
window.mainloop()
