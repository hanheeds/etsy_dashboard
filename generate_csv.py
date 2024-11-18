import os
from dotenv import load_dotenv
from etsy_shop_id import get_shop_id
from etsy_initial_token import load_token, save_token
from requests_oauthlib import OAuth2Session
import json
import pandas as pd
import math

# Load all the environment variables
# load_dotenv()

etsy_keystring = os.getenv("etsy-keystring")

token = load_token()
shop_id = get_shop_id(etsy_keystring, token)

# def get_listings(keystring, token, limit=100):
      
#     headers = {
# 		"Accept": "application/json",
# 		"Content-Type": "application/x-www-form-urlencoded",
# 		"x-api-key": keystring,
#     	      }
    
#     refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
#     etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=token_saver)
    
#     r = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/active?limit={limit}", headers=headers)


#     return json.loads(r.text)

def get_listings(keystring, token, limit=100):
    """
    Is the limit only 100? I can't get older listings, and there's an error when that happens
    """
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"x-api-key": keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=save_token)
    
    r = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/active?limit={limit}", headers=headers)
    r_json = json.loads(r.text)

    # The limit is 100 but we need to get more but we need to get them all
    num_listings = r_json['count']
    times_to_run = math.ceil(num_listings/limit)

    # Store the combined results
    all_results = r_json['results']

    # Iterate to fetch the rest of the listings
    offset = limit # start offset at the limit since the first batch is already fetched

    for i in range(1, times_to_run):
        r_sub = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/active?limit={limit}&offset={offset}", headers=headers)
        r_sub_json = json.loads(r_sub.text)
        
        # Combine the listings
        all_results += r_sub_json['results']

        # Update the offset for the next batch
        offset += 100

    # Return all the listings
    return all_results


def shorten(input_string):
    """Return the first 20 characters of the title."""
    return input_string[:20]

def generate_listings_csv():
    listings = get_listings(etsy_keystring, token)

    # print(listings)

    # Convert list of dictionaries to DataFrame
    listings_df = pd.DataFrame(listings)
    
    # Export DataFrame to CSV
    listings_file = 'data/listings.csv'
    listings_df.to_csv(listings_file, index=False)

    print('Updated listings successfully!')

def get_transactions(keystring, token, limit=100):
      
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"x-api-key": keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=save_token)
    
    r = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/transactions?limit={limit}", headers=headers)

    r_json = json.loads(r.text)

    # print(r_json)
    # The limit is 100 but we need to get more but we need to get them all
    num_transactions = r_json['count']
    times_to_run = math.ceil(num_transactions/limit)

    # Store the combined results
    all_results = r_json['results']

    # Iterate to fetch the rest of the listings
    offset = limit # start offset at the limit since the first batch is already fetched

    for i in range(1, times_to_run):
        r_sub = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/transactions?limit={limit}&offset={offset}", headers=headers)
        r_sub_json = json.loads(r_sub.text)
        
        # Combine the listings
        all_results += r_sub_json['results']

        # Update the offset for the next batch
        offset += 100

    # Return all the transactions
    return all_results

def generate_transactions_csv():
    transactions = get_transactions(etsy_keystring, token, limit=99)

    # Convert list of dictionaries to DataFrame
    transactions_df = pd.DataFrame(transactions)

    # Export DataFrame to CSV
    transactions_file = 'data/transactions.csv'
    transactions_df.to_csv(transactions_file, index=False)

    print('Updated transactions successfully!')

if __name__ == "__main__":
    # Create the listings.csv and transactions.csv
    generate_listings_csv()
    generate_transactions_csv()
