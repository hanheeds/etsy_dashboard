import os
from dotenv import load_dotenv
from etsy_shop_id import get_shop_id
from etsy_initial_token import load_token
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

token = load_token()
shop_id = get_shop_id(etsy_keystring, token)

# new_tags = ["funny tshirt"]

def update_tags(listing_id, new_tags):
      
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"x-api-key": etsy_keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(etsy_keystring, token=token, auto_refresh_url=refresh_url, token_updater=token_saver)
    
    url = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}"
    data = {
        'tags': ','.join(new_tags)
    }
    
    response = etsy_auth.patch(url, headers=headers, data=data)
    
    if response.status_code == 200:
        print('Listing tags updated successfully!')
    else:
        print(f'Error: {response.status_code} - {response.text}')

if __name__ == "__main__":

    listing_id = 1633310510
    new_tags = ['minecraft', 'minecraft shirt', 'minecraft warden', 'minecraft tshirt', 'minecraft teeshirt', 'minecraft birthday', 'minecrafter', 'minecraft merch', 'minecraft party', 'skeleton shirt', 'vintage shirt', 'minecraft lover gift', 'minecraft skeleton']
    # Example usage
    update_tags(listing_id, new_tags)
    

