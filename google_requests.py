'''
This script demonstrates how to authorize 
a google service using oauth2 and vanilla
requests library
'''
import requests 
import json

config = json.loads(open("config.json").read())
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

def create_auth_url(auth_url,
                    client_id,
                    redirect_uri,
                    scopes,
                    state):
    if len(scopes)==1:
        scopes = scopes[0]
    else:
        s = ""
        for idx,scope in enumerate(scopes):
            if idx==0:
                s+=scope
            else:
                s+=f"%20{scope}"
        scopes = s

    auth_url+=f"?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scopes}&state={state}&prompt=select_account"
    return auth_url

def create_token_url(token_url,client_id,client_secret,code,redirect_uri):
    token_url+=f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}"
    return token_url 

def get_token(token_url):
    headers = {"Content-Type":'application/json'} 
    res = requests.post(url=token_url,headers=headers)
    return res

def get_calender_details(access_token,api_url):
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type":'application/json'}
    resp = requests.get(api_url,headers=headers)
    return resp 

if __name__=="__main__":
    url = create_auth_url(auth_url,client_id,redirect_url,scopes,state)
    print(f"Visit this url: {url}")
    print("Once you are visited this page and authenticated copy the authorization code below")
    code = input("Copy the authorization code here:")
    url = create_token_url(token_url,client_id,client_secret,code,redirect_url)
    res = get_token(url)
    if res.status_code==200:
        access_token = res.json()['access_token']
        resp = get_calender_details(access_token,api_url)
        print(resp.status_code,resp.text)
    else:
        print("Haawww")
