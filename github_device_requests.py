'''
Implements a device flow using
vanilla python requests library
using github api
'''
import requests 
import json
import datetime
import time

from requests.models import guess_json_utf

auth_url = "https://github.com/login/device/code"
token_url = "https://github.com/login/oauth/access_token"
config = json.loads(open("config.json").read())
client_id = config['github_client_id']
scopes = ['user']
def send_auth_request(auth_url,client_id,scopes):
    auth_headers = {'Accept':'application/json'}
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
    auth_url += f"?client_id={client_id}&scope={scopes}"
    resp = requests.post(url=auth_url,headers = auth_headers)
    return resp

def get_token(token_url,client_id,device_code):
    token_url+=f"?client_id={client_id}&device_code={device_code}&grant_type=urn:ietf:params:oauth:grant-type:device_code"
    auth_headers = {'Accept':'application/json'}
    try:
        resp = requests.post(url=token_url,headers=auth_headers)
    except:
        resp = None
    return resp

def poll_api(expires_in,interval,token_url,client_id,device_code):
    poll = True 
    current_time = datetime.datetime.now()
    delta_end = datetime.timedelta(0,expires_in)
    terminate_time = current_time+delta_end 
    while poll:
        print("Polling for access token")
        if datetime.datetime.now()<terminate_time:
            time.sleep(interval)
            resp = get_token(token_url,client_id,device_code)
            if resp is not None and "error" in resp:
                poll=True
            elif resp is not None and "access_token" in resp.json():
                poll=False 
        else:
            poll=False
    return resp 

        



if __name__=="__main__":
    resp = send_auth_request(auth_url,client_id,scopes)
    if resp.status_code==200:
        resp = resp.json()
        user_code = resp['user_code']
        verification_url = resp['verification_uri']
        device_code = resp['device_code']
        interval = int(resp['interval'])
        expires_in = int(resp['expires_in'])
        print(f"Visit {verification_url} and enter code: {user_code}")
        resp = poll_api(expires_in,interval,token_url,client_id,device_code)
        print(resp.json())
    else:
        print("Request failed!!!")