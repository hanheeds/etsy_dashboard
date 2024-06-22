import os
from dotenv import load_dotenv
from etsy_shop_id import get_shop_id
from requests_oauthlib import OAuth2Session
import requests
import json
import pandas as pd

load_dotenv()

etsy_keystring = os.getenv("etsy-keystring")

# Define the token_saver function to handle updating the token
def token_saver(new_token):
    # Save the new token somewhere you can retrieve it later
    print("New token:", new_token)

token = {'access_token': '879431180.e4at_iGAt16y44w0YFxTcMNn2u8r1Xg4gSbQqnZnoIQEF-RzdOsKZA__9wtzdSQWl2n4gT9QweTr7_ZCBgZzPBxIac', 'token_type': 'Bearer', 'expires_in': 3600, 'refresh_token': '879431180.IfHB7VLg_ZGffot3l31JiEKbScwS5r81HJjCCMs5UAuFUlwHEjs0EiczCidVp6HrHLNJg2pD0NTwLax-TfYJ9115-r', 'expires_at': 1719037222.0221074}
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

names = shorten(listings["results"][0]["title"])

# Convert list of dictionaries to DataFrame
listings_df = pd.DataFrame(listings['results'])

print(listings_df.shape)

# Export DataFrame to CSV
listings_file = 'listings.csv'
listings_df.to_csv(listings_file, index=False)

def get_transactions(keystring, token, limit=25):
      
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

# print(transactions["count"])

# print(list(transactions["results"][0].keys()))


# Let's try to find the most tags in the recent transactions
# I will make the list of the count of the transactions.

# First, we need to join the transactions dataset with the listings dataset. 
# We need to find the join key. 




# keys_to_print = ['title', "listing_id", "product_id", "price", "product_data"]
# # Get the listing id and product id

# print(transactions["results"][0])


# count = 0
# # Total profit
# for transaction in transactions["results"]:
#     count +=1

# print(count)