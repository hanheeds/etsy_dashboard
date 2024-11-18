import requests

def exchange_code_for_token(code, client_id, client_secret, redirect_uri, token_url):
    # Exchange the authorization code for an access token
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        # Successfully received the token
        token_info = response.json()
        print("Access token:", token_info['access_token'])
        return token_info['access_token']
    else:
        # Handle errors
        print("Failed to retrieve access token:", response.status_code, response.text)
        return None

def handle_webhook(event):
    # Extract the authorization code from the query parameters
    code = event['query']['code']
    print("Authorization code received:", code)
    
    # Define your OAuth2 credentials
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    redirect_uri = 'YOUR_REDIRECT_URI'
    token_url = 'https://oauth2.example.com/token'
    
    # Exchange the authorization code for an access token
    token = exchange_code_for_token(code, client_id, client_secret, redirect_uri, token_url)
    
    return token

# Assuming 'event' is the incoming webhook data
event = {
    'query': {
        'code': 'example_authorization_code'
    }
}

# Handle the webhook and process the authorization code
access_token = handle_webhook(event)
