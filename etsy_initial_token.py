import os
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import json
import time
from util.get_env import get_env_variables

TOKEN_FILE = 'token.json'

etsy_keystring, etsy_authcode, etsy_code_verifier, callback_url, etsy_state = get_env_variables()

print(etsy_state)

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

def refresh_access_token(keystring, refresh_token, redirect_url, scopes):
    """
    Function to refresh the access token using the refresh token.
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": keystring,
    }
    oauth = OAuth2Session(
        keystring, redirect_uri=redirect_url, scope=scopes
    )
    token = oauth.refresh_token(
        "https://api.etsy.com/v3/public/oauth/token",
        refresh_token=refresh_token,
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

def get_valid_token(keystring, auth_code, code_verifier, redirect_url, scopes):
    token = load_token()
    
    if token is None:
        token = get_access_token(keystring, auth_code, code_verifier, redirect_url, scopes)
        save_token(token)
    elif time.time() >= token['expires_at']:
        token = refresh_access_token(keystring, token['refresh_token'], redirect_url, scopes)
        save_token(token)
    
    return token

if __name__ == "__main__":
    # This code will not run when the module is imported
    # print("This file is being run directly")

    load_dotenv()
    etsy_scope = ["transactions_w", "transactions_r", "listings_r", "listings_w"]
    token = get_valid_token(etsy_keystring, etsy_authcode, etsy_code_verifier, callback_url, etsy_scope)
    print(token)