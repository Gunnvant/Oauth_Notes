import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json
scopes = ['https://www.googleapis.com/auth/calendar.readonly',
         'https://www.googleapis.com/auth/calendar.events.readonly']
config = json.loads(open("../config.json").read())
if __name__=="__main__":

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        '../client_secret.json',
        scopes=scopes)
    flow.redirect_uri = config['google_redirect_url']
    auth_url,state = flow.authorization_url(access_type='offline',
                                      include_granted_scopes='true')
    print(f"Visit this url: {auth_url}")
    redirect_url = input("Enter the redirect url:")
    flow.fetch_token(authorization_response=redirect_url)
    credentials = flow.credentials
    calendar = build('calendar', 'v3', credentials=credentials)
    calendar_list = calendar.calendarList().list(pageToken=None).execute()
    print(calendar_list)
    


    
