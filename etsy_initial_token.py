import os
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import json
import time
import requests

TOKEN_FILE = 'token.json'

def get_access_token(keystring, auth_code, code_verifier, redirect_url, scopes):
    """
    Function to get the access token. 
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": keystring,
    }
    oauth = OAuth2Session(
        keystring, redirect_uri=redirect_url, scope=scopes
    )
    token = oauth.fetch_token(
        "https://api.etsy.com/v3/public/oauth/token",
        code=auth_code,
        code_verifier=code_verifier,
        include_client_id=True,
        headers=headers,
    )
    return json.loads(json.dumps(token))

def save_token(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)
    
    # Check if token is expired
    if time.time() >= token_data['expires_at']:
        return None
    
    return token_data



if __name__ == "__main__":
    # This code will not run when the module is imported
    # print("This file is being run directly")

    load_dotenv()

    etsy_keystring = os.getenv("etsy-keystring")
    callback_url = os.getenv("callback-url")
    etsy_state = os.getenv("etsy-state")
    etsy_code_verifier = os.getenv("code-verifier")
    etsy_auth_code = os.getenv("etsy-code")
    etsy_scope = ["transactions_w", "transactions_r", "listings_r", "listings_w"]

    token = get_access_token(etsy_keystring, etsy_auth_code, etsy_code_verifier, callback_url, etsy_scope)
    print(token)
    
    # save the token to json file to call it later
    save_token(token)

