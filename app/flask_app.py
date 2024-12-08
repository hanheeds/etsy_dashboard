import math
from flask import Flask, jsonify, render_template
import os
from services.csv_handler import process_performance_tables

app = Flask(__name__)

# Add a root route to render a homepage or redirect
@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html is in the templates folder

@app.route('/get_performance_data', methods=['GET'])
def get_performance_data():
    try:
        # Define the data folder
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        print("data_folder", data_folder)

        # Validate that the listings.csv file exists
        listings_csv_path = os.path.join(data_folder, 'listings.csv')
        if not os.path.exists(listings_csv_path):
            return jsonify({'error': 'Listings file not found'}), 404

        # Process performance tables
        performance_tables = process_performance_tables(listings_csv_path)
        performance_tables = convert_nan_to_null(performance_tables)

        # Return only the performance tables
        return jsonify({'performance_tables': performance_tables})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def convert_nan_to_null(data):
    if isinstance(data, dict):  # If the data is a dictionary
        return {key: convert_nan_to_null(value) for key, value in data.items()}
    elif isinstance(data, list):  # If the data is a list
        return [convert_nan_to_null(item) for item in data]
    elif isinstance(data, float) and math.isnan(data):  # If the value is NaN
        return None
    else:
        return data

if __name__ == '__main__':
    app.run(debug=True)