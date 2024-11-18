import os
from etsy_shop_id import get_shop_id
from etsy_initial_token import load_token
from requests_oauthlib import OAuth2Session
import requests
import json
import pandas as pd
from util.get_env import get_env_variables

etsy_keystring, etsy_authcode, etsy_code_verifier, callback_url, etsy_state = get_env_variables()

# Define the token_saver function to handle updating the token
def token_saver(new_token):
    # Save the new token somewhere you can retrieve it later
    print("New token:", new_token)

token = load_token()
shop_id = get_shop_id(etsy_keystring, token)

def get_listings(keystring, token):
      
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"x-api-key": keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=token_saver)
    
    r = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/active", headers=headers)


    return json.loads(r.text)

def shorten(input_string):
    """Return the first 20 characters of the title."""
    return input_string[:20]

listings = get_listings(etsy_keystring, token)

# names = shorten(listings["results"][0]["title"])

# print(listings["results"][0]["num_favorers"])

# print(listings["results"][0]["tags"])

# Convert list of dictionaries to DataFrame
# listings_df = pd.DataFrame(listings['results'])

# print(listings_df.shape)

# Export DataFrame to CSV
# listings_file = 'listings.csv'
# listings_df.to_csv(listings_file, index=False)

##################

def get_transactions(keystring, token, limit=99):
      
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"x-api-key": keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=token_saver)
    
    r = etsy_auth.get(f"https://openapi.etsy.com/v3/application/shops/{shop_id}/transactions?limit={limit}", headers=headers)


    return json.loads(r.text)

transactions = get_transactions(etsy_keystring, token, limit=99)

# print(transactions)


# I'm going to analyze when these
print(transactions["results"][0]["created_timestamp"])



# Convert list of dictionaries to DataFrame
# transactions_df = pd.DataFrame(transactions['results'])

# print(listings_df.shape)

# Export DataFrame to CSV
# transactions_file = 'transactions.csv'
# transactions_df.to_csv(transactions_file, index=False)
