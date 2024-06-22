from requests_oauthlib import OAuth2Session
oauth = OAuth2Session(client_id, token=token, auto_refresh_url=refresh_url,
    auto_refresh_kwargs=extra, token_updater=token_saver)
r = oauth.get(protected_url)