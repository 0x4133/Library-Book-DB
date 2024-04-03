import requests
from bs4 import BeautifulSoup
import sqlite3


def google_upc(upc):
    # Perform Google search
    search_url = f"https://www.google.com/search?q={upc}"
    headers = {
        "User-Agent": "Your User-Agent"
    }  # Replace 'Your User-Agent' with your actual User-Agent string
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


def main(upc):
    html_content = google_upc(upc)
    if html_content:
        result = parse_first_result(html_content)
        if result:
            save_to_db(result, upc)
        else:
            print("No results found.")
    else:
        print("Failed to fetch search results.")


# Main program loop
while True:
    upc = input("Scan a UPC (or press Enter to quit): ")
    if upc == "":
        main(upc)
        break
    main(upc)
