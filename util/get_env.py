import os
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

def get_env_variables():

    load_dotenv()

    etsy_keystring = os.getenv("etsy-keystring")
    callback_url = os.getenv("callback-url")
    etsy_state = os.getenv("etsy-state")
    etsy_code_verifier = os.getenv("code-verifier")
    etsy_auth_code = os.getenv("etsy-code")

    return etsy_keystring, etsy_auth_code, etsy_code_verifier, callback_url, etsy_state