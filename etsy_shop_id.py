import os
import json
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from etsy_initial_token import get_access_token

# load_dotenv()

# etsy_keystring = os.getenv("etsy-keystring")
# callback_url = os.getenv("callback-url")
# etsy_state = os.getenv("etsy-state")
# etsy_code_verifier = os.getenv("code-verifier")
# etsy_auth_code = os.getenv("etsy-code")
# etsy_scope = ["transactions_w", "transactions_r"]

# # Getting the token
# token = get_access_token(etsy_keystring, etsy_auth_code, etsy_code_verifier, callback_url, etsy_scope)

# # Define the token_saver function to handle updating the token
def token_saver(new_token):
    # Save the new token somewhere you can retrieve it later
    print("New token:", new_token)

token = {'access_token': '879431180.OMrKT6-sq4VaqLJDaYY7GhH9NBXTll45Pa2-vLNLPrariJcPF4Wdcipcz4bNGnGjRiKlee286zr-O0_pdcLCrU8ocF', 'token_type': 'Bearer', 'expires_in': 3600, 'refresh_token': '879431180.B39jjZEwM9XuEioQwT6mX9iF9yyCep6yRMAZUxSGrZ1BsyG1d5G2h2FLTczoDps5VwL845AZzOsEiawszogUXUoUNZ', 'expires_at': 1719036733.2370784}

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

# shop_id = get_shop_id(etsy_keystring, token)

# os.environ["shop-id"] = str(shop_id)

# shop_id2 = os.getenv("shop-id")
# print(shop_id2)

if __name__ == "__main__":
    # This code will not run when the module is imported
    print("This file is being run directly")