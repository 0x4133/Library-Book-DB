import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("product_database.db")
cursor = conn.cursor()

# Create the product table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS products (
        upc TEXT PRIMARY KEY,
        name TEXT,
        description TEXT
    )
"""
)


# Function to add a new product to the database
def add_product(upc, name, description):
    cursor.execute(
        """
        INSERT INTO products (upc, name, description)
        VALUES (?, ?, ?)
    """,
        (upc, name, description),
    )
    conn.commit()
    print("New product added successfully.")


# Function to look up a product by UPC
def lookup_product(upc):
    cursor.execute(
        """
        SELECT * FROM products WHERE upc = ?
    """,
        (upc,),
    )
    product = cursor.fetchone()
    if product:
        print("Product found:")
        print("UPC:", product[0])
        print("Name:", product[1])
        print("Description:", product[2])
    else:
        print("Product not found.")
        name = input("Enter the product name: ")
        description = input("Enter the product description: ")
        add_product(upc, name, description)


# Main program loop
while True:
    upc = input("Scan a UPC (or press Enter to quit): ")
    if upc == "":
        break
    lookup_product(upc)

# Close the database connection
conn.close()
