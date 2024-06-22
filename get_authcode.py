import os
from authentication import AuthHelper
from dotenv import load_dotenv

# load .env file
load_dotenv()

# set variables
etsy_keystring = os.getenv("etsy-keystring")
callback_url = os.getenv("callback-url")
etsy_scope = ["transactions_w", "transactions_r"]

# start AuthHelper class
auth = AuthHelper(etsy_keystring, callback_url)

os.environ["etsy-state"] = auth.state
os.environ["code-verifier"] = auth.code_verifier

# set more variables
etsy_state = os.getenv("etsy-state")
etsy_code_verifier = os.getenv("code-verifier")

# Print the state and code verifiers
print("state: ", etsy_state)
print("verifier: ", etsy_code_verifier)

etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state)
print(etsy_auth.get_auth_code())
