import os
from dotenv import load_dotenv
from etsy_shop_id import get_shop_id
from etsy_initial_token import load_token, save_token
from requests_oauthlib import OAuth2Session
import requests
import json
import math

load_dotenv()

etsy_keystring = os.getenv("etsy-keystring")

token = load_token()
shop_id = get_shop_id(etsy_keystring, token)

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

# Dictionary of all listings
listings = get_listings(etsy_keystring, token)

# Need a function to get the current price of the listing ID
def get_current_price(listings, listing_id):
    for listing in listings:
        if listing['listing_id']==listing_id:
            # error checking
            curr_price = listing['price']['amount']
            return listing['price']['amount']

print("curr price:", get_current_price(listings, 1646570917))

def update_price(listing_id, new_price_amount):
      
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"x-api-key": etsy_keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(etsy_keystring, token=token, auto_refresh_url=refresh_url, token_updater=save_token)
    
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}"
    data = {
        'price': {
            'amount': new_price_amount,
            'divisor': 100,  # Price given in cents
            'currency_code': 'USD'
        }
    }

    # Convert the data to JSON
    json_data = json.dumps(data)
    
    response = etsy_auth.patch(url, headers=headers, data=json_data)
    
    if response.status_code == 200:
        print('Price updated successfully!')
    else:
        print(f'Error: {response.status_code} - {response.text}')

def add_to_current_price(listing_id, add_amount):
    """
    Amount to add (add it in dollars)
    """
    add_amount *= 100
    current_price = get_current_price(listings, listing_id)
    print('hi')
    new_price = current_price + add_amount
    update_price(listing_id, new_price)
    print("The previous price was: ", current_price)
    print("The new price is: ", new_price)

if __name__ == "__main__":

    listing_id = 1646570917
    amount_to_add = 2

    add_to_current_price(listing_id, amount_to_add)

