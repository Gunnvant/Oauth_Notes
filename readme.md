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
Below are the list of code files you can refer to `examples/github`:

1. `github_requests.py` uses vanilla requests library to implement oauth2 Authorization flow
2. `github_oauthlib.py` uses `OAuthlib`. `OAuthlib` provides utilities to generate relevant urls
3. `github_requests_oauthlib.py` uses`Reqeuests Oauthlib` and has the least code footprint.


### [**Device Flow**](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps#device-flow)

Device flow is used when one doesn't have access to a browser. This usually is the case when one is trying to use applications in devices such as smart tv or xbox.

The major steps in this flow are as follows:

1. Request device and user verification codes by making a post request as given below:

```shell
POST https://github.com/login/device/code

Parameters:
- client_id
- scope
```

This request results in the following response:

```json
{
  "device_code":        "3584d83530557fdd1f46af8289938c8ef79f9dc5",
  "user_code": "WDJB-MJHT",
  "verification_uri": "https://github.com/login/device",
  "verification_uri": "https://github.com/login/device",
  "expires_in": 900,
  "interval": 5
}
```

2. The user inputs `user_code` at the `verification_uri`

3. While the user is giving consent, the client polls the following endpoint for `auth_token`

```shell
POST https://github.com/login/oauth/access_token

Parameters:
- client_id
- device_code
- grant_type (The grant type must be urn:ietf:params:oauth:grant-type:device_code.
)
```

The file `examples/github/github_device_requests.py` has a sample code that illustrates how `device flow` works.

## **Google Oauth2.0 flow**

### [**Web application Flow**](https://developers.google.com/identity/protocols/oauth2/web-server#httprest)

For google's services the oauth flow is very similar to that of github's flow.

Here are the major steps one might need to undertake to authorize an app:

1. Get consent from the owner of the resource by hitting the following endpoint using a browser

```shell
GET https://accounts.google.com/o/oauth2/v2/auth

Parmeters:
- client_id
- redirect_uri
- response_type: (Set to 'code')
- scope
- state
- prompt (Optional, values can be none, consent, select_account)
```

2. Once the user gives the consent then the google oauth service will redirect to `redirect_uri` from where the `authorization code` can be obtained

3. Now request for an `access token` by making the following request:

```shell
POST https://oauth2.googleapis.com/token

Parameters:
- client_id
- client_secret
- code
- grant_type (Set to 'authorization_code')
- redirect_uri

Headers:
Host: oauth2.googleapis.com
Content-Type: application/x-www-form-urlencoded    
```
4. If the request succeeds you will see a response as shown below:

```json
{
  "access_token": "1/fFAGRNJru1FTz70BzhT3Zg",
  "expires_in": 3920,
  "token_type": "Bearer",
  "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
  "refresh_token": "1//xEoDL4iW3cxlI7yDbSRFYNG01kVKM2C-259HOF2aQbI"
}
```

Google services also return a refresh token which can be used to generate an access token without revisiting the whole `Authorization Grant Flow`

5. To make calls to the secured resources one can either do a get request with `access token` passed in the header as `bearer` token or send the token as a `query parameter`


**Send `access token` as a header**
```shell
GET /drive/v2/files HTTP/1.1
Host: www.googleapis.com
Authorization: Bearer access_token
```
**Send `access token` as a query parameter**

```shell
GET https://www.googleapis.com/drive/v2/files?access_token=access_token
```

6. To get an access token back using refresh token you can hit the following end-point:

```shell
POST /token HTTP/1.1
Host: oauth2.googleapis.com
Content-Type: application/x-www-form-urlencoded

client_id=your_client_id&
client_secret=your_client_secret&
refresh_token=refresh_token&
grant_type=refresh_token
```
**Http/Rest** 

```shell
POST https://oauth2.googleapis.com/token

Parameters:
- client_id
- client_secret
- grant_type (Pass value "refresh_token")
- refresh_token
```

You can refer to the files placed in `examples/google`:

1. `google_requests.py` for an example on how oauth2 flow works using vanilla `requests` library
2. `google_requests_oauthlib.py` for an example on how to use `requests-oauthlib` package. 
3. `google_sdk.py` this uses google official sdk for authorization and api access.

This repo is a work in progress.