from app import app
from flask import jsonify, request
import pandas as pd

@app.route('/get-listings', methods=['GET'])
def get_listings():
    df = pd.read_csv('data/listings.csv')
    data = df[['title', 'listing_id', 'tags']].to_dict(orient='records')
    return jsonify(data)

@app.route('/submit-tags', methods=['POST'])
def submit_tags():
    edited_data = request.json
    with open('edited_tags.txt', 'w') as f:
        for item in edited_data:
            f.write(f"{item['listing_id']}: {item['tags']}\n")
    return jsonify({"status": "success"}), 200
