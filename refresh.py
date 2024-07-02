from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

client_id = 'YOUR_CLIENT_ID'
refresh_url = 'https://api.etsy.com/v3/public/oauth/token'
protected_url = 'https://api.etsy.com/v3/application/protected_endpoint'

# Your initial token object
token = {
    'access_token': '12345678.O1zLuwveeKjpIqCQFfmR-PaMMpBmagH6DljRAkK9qt05OtRKiANJOyZlMx3WQ_o2FdComQGuoiAWy3dxyGI4Ke_76PR',
    'token_type': 'Bearer',
    'expires_in': 3600,
    'refresh_token': '12345678.JNGIJtvLmwfDMhlYoOJl8aLR1BWottyHC6yhNcET-eC7RogSR5e1GTIXGrgrelWZalvh3YvvyLfKYYqvymd-u37Sjtx'
}

extra = {
    'client_id': client_id,
    'grant_type': 'refresh_token'
}

def token_saver(new_token):
    global token
    token = new_token
    # Save the new token as needed, e.g., to a file or database

try:
    oauth = OAuth2Session(client_id, token=token)
    r = oauth.get(protected_url)
except TokenExpiredError as e:
    token = oauth.refresh_token(refresh_url, **extra)
    token_saver(token)
    oauth = OAuth2Session(client_id, token=token)
    r = oauth.get(protected_url)

print(r.json())
