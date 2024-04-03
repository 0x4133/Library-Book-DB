import requests
from bs4 import BeautifulSoup
import sqlite3
import tkinter as tk
from tkinter import ttk


def google_upc(upc):
    # Perform Google search
    search_url = f"https://www.google.com/search?q={upc}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_first_result(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    # Assuming the first search result can be identified with the 'h3' tag
    result = soup.find("h3")
    if result:
        title = result.text
        url = result.find_parent("a")["href"]
        return [(title, url)]
    else:
        return []


def save_to_db(results, upc):
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS upc_results
        (upc TEXT, title TEXT, url TEXT)"""
    )
    # Insert result into the database
    for title, url in results:
        cursor.execute(
            "INSERT INTO upc_results (upc, title, url) VALUES (?, ?, ?)",
            (upc, title, url),
        )
    # Commit changes and close the connection
    conn.commit()
    conn.close()


def search_upc():
    upc = upc_entry.get()
    if upc:
        html_content = google_upc(upc)
        if html_content:
            result = parse_first_result(html_content)
            if result:
                save_to_db(result, upc)
                result_text.delete("1.0", tk.END)
                result_text.insert(
                    tk.END, f"Title: {result[0][0]}\nURL: {result[0][1]}"
                )
            else:
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, "No results found.")
        else:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Failed to fetch search results.")
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a UPC.")


# Create the main window
window = tk.Tk()
window.title("UPC Search")

# Create and pack the widgets
upc_label = ttk.Label(window, text="Enter UPC:")
upc_label.pack()

upc_entry = ttk.Entry(window)
upc_entry.pack()

search_button = ttk.Button(window, text="Search", command=search_upc)
search_button.pack()

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

# Start the main event loop
window.mainloop()
