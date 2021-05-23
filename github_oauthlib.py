'''
This script shows how one can use 
Oauthlib client library to authorize 
a github user
'''
from oauthlib.oauth2 import WebApplicationClient
import json
import requests 

config = json.loads(open("config.json").read())
client_id = config['github_client_id']
client_secret = config['github_client_secret']
auth_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
user_url = "https://api.github.com/user"
redirect_uri ="https://localhost:5000"
scopes = ["user"]
state = "1234"

def api_headers(access_token):
    headers = {'Accept':'application/vnd.github.v3+json',
                'Authorization':f'token {access_token}'}
    return headers

if __name__=="__main__":
    github = WebApplicationClient(client_id=client_id)
    url,headers,body=github.prepare_authorization_request(authorization_url=auth_url,
                                        state='1234',
                                        redirect_url=redirect_uri,
                                        scope=scopes)
    print(f"url is :{url}")
    print("visit this url and paste the url once you are logged in and have accepted the premissions this app desires")
    url = input("Paste the url here:")
    resp=github.parse_request_uri_response(url,state)
    code = resp['code']
    token_uri = github.prepare_request_uri(uri=token_url,
                                client_secret=client_secret,
                                code=code)
    headers = {"Accept": "application/json"}
    resp = requests.post(url = token_uri,headers=headers)
    access_token = resp.json()['access_token']
    user_resp = requests.get(url = user_url,
                             headers = api_headers(access_token))
    if user_resp.status_code==200:
        user_name = user_resp.json()['login']
    else:
        user_name = "Request failed, response code is not 200"
    print(user_name)
    

