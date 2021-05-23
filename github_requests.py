'''
Examples on accessing API resources using 
Oauth2 Authorization Grant Flow using vanilla
requests package
'''
import requests
import json 
config = json.loads(open("config.json").read()) 
auth_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"
client_secret = config['client_secret']
client_id = config['client_id']
user_url = "https://api.github.com/user"
redirect_uri ="https://localhost:5000"
scopes = ["user"]
state = "1234"

def gen_auth_uri(auth_url,client_id,redirect_uri,scopes,state):
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
    auth_url+=f'''?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}&state={state}'''
    return auth_url

def get_access_token(token_url,client_id,client_secret,code):
    headers = {"Accept": "application/json"}
    token_url+=f'''?client_id={client_id}&client_secret={client_secret}&code={code}'''
    resp = requests.post(url=token_url,headers=headers)
    return resp

def create_header(access_token):
    headers = {'Accept':'application/vnd.github.v3+json',
                'Authorization':f'token {access_token}'}
    return headers
def get_user_info(access_token,url):
    headers = create_header(access_token)
    return requests.get(url=url,headers=headers).json()

# def get_count_starred_respos(access_token,url,user_name):
#     headers = create_header(access_token)
#     resp = requests.get(url=url.format(user_name),headers=headers)
#     return resp


if __name__=="__main__":
    url = gen_auth_uri(auth_url,client_id,redirect_uri,scopes,state)
    print(f"Visit the following url authorize the app and copy the code: {url.strip()}")
    code = input("Paste code here:")
    resp = get_access_token(token_url,client_id,client_secret,code)
    access_token = resp.json()['access_token']
    user = get_user_info(access_token,user_url)
    user_name = user['login']
    print(user_name)
    
    
