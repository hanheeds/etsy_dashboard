import os
from authentication import AuthHelper
from dotenv import load_dotenv
from util.update_env_file import update_env

def make_etsylink():

    """
    Generates the link to approve app. 
    This function doesn't return. 
    This function just writes the authorization code into the 'etsy_auth.txt' file. 
    """

    # load .env file
    load_dotenv()

    # set variables
    etsy_keystring = os.getenv("etsy-keystring")
    callback_url = os.getenv("callback-url")
    etsy_scope = ["transactions_w", "transactions_r", "listings_w", "listings_r"]

    # start AuthHelper class
    auth = AuthHelper(etsy_keystring, callback_url)

    # set more variables
    update_env("etsy-state", auth.state)
    update_env("code-verifier", auth.code_verifier)

    etsy_state = auth.state
    etsy_code_verifier = auth.code_verifier

    # Save the etsy auth link into a file.
    etsy_auth = AuthHelper(etsy_keystring, callback_url, etsy_scope, etsy_code_verifier, etsy_state)

    etsy_oauth_link = etsy_auth.get_auth_code()[0]
    file_path = "etsy_auth.txt"

    with open(file_path, "w") as file:
        file.write(etsy_oauth_link)

def get_etsylink(file_path):
    # Reading web link from file
    with open(file_path, "r") as file:
        link = file.read()

    return link

if __name__ == "__main__":
    # Make a link to use
    make_etsylink()
    link = get_etsylink("etsy_auth.txt")
    print(link)
