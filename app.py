import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


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
        # Retrieve the star rating for the current entry
        cursor.execute("SELECT rating FROM ratings WHERE upc = ?", (row[0],))
        rating_row = cursor.fetchone()
        rating = rating_row[0] if rating_row else 0
        # Retrieve the chili rating for the current entry
        cursor.execute("SELECT rating FROM chili_ratings WHERE upc = ?", (row[0],))
        chili_rating_row = cursor.fetchone()
        chili_rating = chili_rating_row[0] if chili_rating_row else 0
        # Format the current row's details
        result = {
            "upc": row[0],
            "title": row[1],
            "url": row[2],
            "rating": rating,
            "chiliRating": chili_rating,
        }
        current_index += 1
    else:
        result = {"message": "No more entries."}
    # Close the connection
    conn.close()
    return json.dumps(result)


def reset_index():
    global current_index
    current_index = 0
    return "Press 'Next Entry' to start stepping through the entries."


def save_rating(upc, rating):
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    # Create the ratings table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            upc TEXT PRIMARY KEY,
            rating INTEGER
        )
    """
    )
    # Insert or update the rating for the given UPC
    cursor.execute(
        """
        INSERT OR REPLACE INTO ratings (upc, rating)
        VALUES (?, ?)
    """,
        (upc, rating),
    )
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def save_chili_rating(upc, rating):
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    # Create the chili_ratings table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chili_ratings (
            upc TEXT PRIMARY KEY,
            rating INTEGER
        )
    """
    )
    # Insert or update the chili rating for the given UPC
    cursor.execute(
        """
        INSERT OR REPLACE INTO chili_ratings (upc, rating)
        VALUES (?, ?)
    """,
        (upc, rating),
    )
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def get_comments(upc):
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    # Create the comments table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            upc TEXT,
            comment TEXT
        )
    """
    )
    # Retrieve comments for the given UPC
    cursor.execute("SELECT comment FROM comments WHERE upc = ?", (upc,))
    comments = [row[0] for row in cursor.fetchall()]
    # Close the connection
    conn.close()
    return json.dumps(comments)


def add_comment(upc, comment):
    # Connect to SQLite database
    conn = sqlite3.connect("search_results.db")
    cursor = conn.cursor()
    # Create the comments table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            upc TEXT,
            comment TEXT
        )
    """
    )
    # Insert the comment for the given UPC
    cursor.execute(
        """
        INSERT INTO comments (upc, comment)
        VALUES (?, ?)
    """,
        (upc, comment),
    )
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/step":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(step_through_db().encode())
        elif self.path == "/reset":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(reset_index().encode())
        elif self.path.startswith("/comments"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            upc = query_params.get("upc", [""])[0]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(get_comments(upc).encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/rating":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            upc = data["upc"]
            rating = data["rating"]
            save_rating(upc, rating)
            self.send_response(200)
            self.end_headers()
        elif self.path == "/chili-rating":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            upc = data["upc"]
            rating = data["rating"]
            save_chili_rating(upc, rating)
            self.send_response(200)
            self.end_headers()
        elif self.path == "/comments":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            upc = data["upc"]
            comment = data["comment"]
            add_comment(upc, comment)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(404)


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()


# Initialize the current index
current_index = 0

if __name__ == "__main__":
    run_server()
