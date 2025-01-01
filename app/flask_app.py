import math
from flask import Flask, jsonify, render_template, request
import os
from services.csv_handler import process_performance_tables, convert_nan_to_null
# from dotenv import load_dotenv
# from util.authentication import AuthHelper
# from util.update_env_file import update_env

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
        transactions_csv_path = os.path.join(data_folder, 'transactions.csv')
        if not os.path.exists(listings_csv_path):
            return jsonify({'error': 'Listings file not found'}), 404

        # Process performance tables
        performance_tables = process_performance_tables(listings_csv_path, transactions_csv_path)
        performance_tables = convert_nan_to_null(performance_tables)

        # Return only the performance tables
        return jsonify({'performance_tables': performance_tables})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/finances')
def finances():
    return render_template('finances.html')

# # Route to generate Etsy OAuth link
# @app.route('/generate_etsy_auth', methods=['GET'])
# def generate_etsy_auth():
#     try:
#         # Get environment variables
#         etsy_keystring = os.getenv("etsy-keystring")
#         callback_url = os.getenv("callback-url")  # Dynamically read callback URL from .env
#         etsy_scope = ["transactions_w", "transactions_r", "listings_w", "listings_r"]

#         # Initialize AuthHelper
#         auth = AuthHelper(etsy_keystring, callback_url)
#         update_env("etsy-state", auth.state)
#         update_env("code-verifier", auth.code_verifier)

#         # Generate authorization link
#         etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, auth.code_verifier, auth.state)
#         etsy_oauth_link = etsy_auth.get_auth_code()[0]

#         return jsonify({'auth_link': etsy_oauth_link})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Route to handle Etsy OAuth callback
# @app.route('/callback', methods=['GET'])
# def handle_callback():
#     try:
#         # Extract query parameters
#         auth_code = request.args.get('code')
#         state = request.args.get('state')

#         if auth_code:
#             # Save auth code to .env or use it directly
#             update_env("etsy-code", auth_code)
#             return "Authorization successful. You can close this page."
#         else:
#             return "Authorization failed or incomplete.", 400

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)