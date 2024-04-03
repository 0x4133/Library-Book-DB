import sqlite3
from colorama import Fore, Back, Style


def step_through_db():
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()

    # Select all records from the upc_results table
    cursor.execute("SELECT * FROM upc_results")

    # Fetch all rows
    rows = cursor.fetchall()

    # Iterate through the rows
    for row in rows:
        # Print the current row's details
        print(
            f"{Fore.CYAN}UPC:{Fore.GREEN}{row[0]}{Fore.RED} | {Fore.WHITE}{Style.DIM}Title:{Style.NORMAL}{Fore.LIGHTYELLOW_EX} {row[1]}{Fore.RED} | {Fore.WHITE}{Style.DIM} URL: {row[2]} {Style.NORMAL}"
        )

        # Wait for the user to press Enter before continuing
        input("Press Enter to continue to the next entry...")

    # Close the connection
    conn.close()


# Call the function to step through the database entries
step_through_db()
