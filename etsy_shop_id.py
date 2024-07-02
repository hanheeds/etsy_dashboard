import os
import json
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from etsy_initial_token import load_token

def token_saver(new_token):
    # Save the new token somewhere you can retrieve it later
    print("New token:", new_token)

def get_shop_id(keystring, token):
  
    headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"x-api-key": keystring,
    	      }
    
    refresh_url = "https://api.etsy.com/v3/public/oauth/token"
    
    etsy_auth = OAuth2Session(keystring, token=token, auto_refresh_url=refresh_url, token_updater=token_saver)
    
    r = etsy_auth.get("https://api.etsy.com/v3/application/shops?shop_name=DesignTeesCentral", headers=headers)

    return json.loads(r.text)['results'][0]['shop_id']

if __name__ == "__main__":
    # This code will not run when the module is imported
    load_dotenv()

    print('hi1')

    etsy_keystring = os.getenv("etsy-keystring")
    callback_url = os.getenv("callback-url")
    etsy_state = os.getenv("etsy-state")
    etsy_code_verifier = os.getenv("code-verifier")
    etsy_auth_code = os.getenv("etsy-code")
    etsy_scope = ["transactions_w", "transactions_r"]

    print('hi')

    # Getting the token
    token = load_token()

    print(token)

    # Define the token_saver function to handle updating the token
    shop_id = get_shop_id(etsy_keystring, token)

    os.environ["shop-id"] = str(shop_id)

    shop_id2 = os.getenv("shop-id")
    print(shop_id2)