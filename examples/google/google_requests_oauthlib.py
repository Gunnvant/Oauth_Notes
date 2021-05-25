from requests_oauthlib import OAuth2Session
import json

config = json.loads(open("../config.json").read())
client_id = config['google_client_id']
client_secret = config['google_client_secret']
redirect_url = config['google_redirect_url']

auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"
## ref: https://developers.google.com/calendar/auth
scopes = ["https://www.googleapis.com/auth/calendar.readonly",
          "https://www.googleapis.com/auth/calendar.events.readonly"]
api_url = "https://www.googleapis.com/calendar/v3/colors"
state = "1234"

if __name__=="__main__":
    google = OAuth2Session(client_id=client_id,
                           redirect_uri=redirect_url,
                           scope=scopes)
    auth_uri = google.authorization_url(auth_url,
                                       state=state)[0]
    print(f"Visit this url: {auth_uri}")
    print("After you consent to permissions, copy the redirect url")
    redirect_url = input("And paste it here:")
    tokens = google.fetch_token(token_url=token_url,
                        authorization_response = redirect_url,
                        client_secret=client_secret)
    access_token = tokens['access_token']
    print(google.get(api_url).json())
