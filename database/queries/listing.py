from database.db import get_db_connection

sql = "INSERT INTO listings (Item_Name, Item_Description, Item_Price, Item_Type, Seller_ID, Image_URL, Image_Blob_Name) VALUES (?, ?, ?, ?, ?, ?, ?)"


def insert_listing(item_name, item_description, item_price, item_type, seller_id, image_url, image_blob_name):
    """
    Insert a new listing into the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (item_name, item_description, item_price, item_type, seller_id, image_url, image_blob_name))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_listings():
    """
    Retrieve all listings from the database.
    Returns a list of listings.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM listings")
    columns = [column[0] for column in cursor.description]
    listings = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return listings