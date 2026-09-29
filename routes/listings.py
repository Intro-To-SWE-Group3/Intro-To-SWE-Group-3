# routes/listings.py
# Contains API routes related to marketplace listings.
# Handles requests for creating listings, retrieving all listings,
# and retrieving information about a specific listing.

import base64
import binascii

import flask
from uuid import uuid4
from database.db import get_db_connection
from database.azure_storage import AzureBlobStorage
from database.queries.listing import insert_listing, get_all_listings

app = flask.Blueprint('listings', __name__)

@app.route('/listings', methods=['POST'])
def create_listing():
    """
    Create a new marketplace listing.
    Expects JSON data with listing details in the request body.
    Returns the created listing as JSON.
    """

    # Extract listing data from the request
    data = flask.request.get_json(silent=True)
    required_fields = (
        'item_name',
        'item_description',
        'item_price',
        'item_type',
        'seller_id',
        'image_data',
    )
    if not isinstance(data, dict):
        return flask.jsonify({"error": "JSON request body is required"}), 400

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return flask.jsonify({"error": "Missing required fields", "fields": missing_fields}), 400

    if not isinstance(data['image_data'], str) or not data['image_data']:
        return flask.jsonify({"error": "image_data must be a non-empty string"}), 400

    encoded_image = data['image_data']
    if encoded_image.startswith('data:') and ',' in encoded_image:
        encoded_image = encoded_image.split(',', 1)[1]
    try:
        image_bytes = base64.b64decode(encoded_image, validate=True)
    except (binascii.Error, ValueError):
        return flask.jsonify({"error": "image_data must be valid Base64"}), 400

    azure_storage = AzureBlobStorage()
    
    item_name = data.get('item_name')
    item_description = data.get('item_description')
    item_price = data.get('item_price')
    item_type = data.get('item_type')
    seller_id = data.get('seller_id')
    image_blob_name = f"{uuid4()}.jpg"
    image_url = azure_storage.upload_image(image_blob_name, image_bytes)

    # Insert the listing into the database
    insert_listing(item_name, item_description, item_price, item_type, seller_id, image_url, image_blob_name)

    # Return the created listing as JSON
    return flask.jsonify({
        "item_name": item_name,
        "item_description": item_description,
        "item_price": item_price,
        "item_type": item_type,
        "seller_id": seller_id,
        "image_url": image_url,
        "image_blob_name": image_blob_name
    }), 201 

    

@app.route('/listings', methods=['GET'])
def return_all_listings():
    """
    Retrieve all marketplace listings.
    Returns a list of listings as JSON.
    """
    return flask.jsonify(get_all_listings()), 200