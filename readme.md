# **OAuth2.0 Python Examples**

This repository contains the examples to authenticate on services such as `google` and `github` using clients such as `oauthlib`, `Requests-Oauthlib` and google's `SDKs`

## **Github Oauth2.0 flow**

### [**Web application Flow**](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps)

This is the traditional authorization grant flow. The major tasks in the workflow are:

1. Request the user's consent

```
GET https://github.com/login/oauth/authorize

Parameters:
- client_id
- redirect_uri	
- login
- scope
- state
- allow_signup
```

2. After user consents one will receive an `authorization code`
3. Use the `authorization code` to request the access token using a `post` request

```
 
POST
https://github.com/login/oauth/access_token

Parameters:
- client_id 
- client_secret
- code
- redirect_uri
- state
```

4. The `access token` will be used to make api calls
git
```shell
Authorization: token OAUTH-TOKEN
GET https://api.github.com/user
```
You can find a demo code in the file called `github_requests.py`