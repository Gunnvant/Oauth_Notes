'''
This contains code for Authorization Grant flow using
Requests Oauthlib
'''
from requests_oauthlib import OAuth2Session
import requests 
import json

config = json.loads(open("../config.json").read())
client_id = config['github_client_id']
client_secret = config['github_client_secret']
auth_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
user_url = "https://api.github.com/user"
redirect_uri ="https://localhost:5000"
scopes = ["user"]
state = "1234"

if __name__=="__main__":
    github = OAuth2Session(client_id=client_id,
                           redirect_uri=redirect_uri,
                           scope=scopes)
    auth_uri = github.authorization_url(auth_url,
                                       state=state)[0]
    print(f"Visit this url: {auth_uri}")
    print("After you consent to permissions, copy the redirect url")
    redirect_url = input("And paste it here:")
    tokens = github.fetch_token(token_url=token_url,
                        authorization_response = redirect_url,
                        client_secret=client_secret)
    access_token = tokens['access_token']
    print(github.get(user_url).json())


