from google.oauth2 import service_account
import google_auth_oauthlib.flow
import webbrowser

# Rather than using the oauth2 method, this method needs a service account json formatted as a dict
# example:
# service_account = dict({
#   "type": "service_account",
#   "project_id": "fivestones",
#   "private_key_id": "xxxx",
#   "private_key": "[private_key]",
#   "client_email": "fivestones@*.iam.gserviceaccount.com",
#   "client_id": "xxxx",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/fivestones"
# }
def gauth(*login,**creds):
    credentials = None
    if 'cred_dict' in creds:
        credentials = service_account.Credentials.from_service_account_info(creds.get('cred_dict'))
    elif 'json_file' in creds:
        credentials = service_account.Credentials.from_service_account_file(creds.get('json_file'))
    elif 'web' in login:
        oauth_cred = {"web":
                          {"client_id": "354355303396-7qvcftio0hkt74pvqdufb53dl20n5mfs.apps.googleusercontent.com",
                           "project_id": "fivestones-ga-automated-audit",
                           "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                           "token_uri": "https://oauth2.googleapis.com/token",
                           "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                           "client_secret": "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"}
                      }

        flow = google_auth_oauthlib.flow.Flow.from_client_config(oauth_cred,
                                                                 scopes=[
                                                                     'https://www.googleapis.com/auth/drive',
                                                                     'https://www.googleapis.com/auth/spreadsheets',
                                                                     'https://www.googleapis.com/auth/drive.metadata.readonly',
                                                                     'https://www.googleapis.com/auth/analytics',
                                                                     'https://www.googleapis.com/auth/analytics.readonly'
                                                                 ]
                                                                 )
        flow.redirect_uri = 'https://fivestones.net/contact-us'
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        open_browser = webbrowser.get(using='google-chrome')
        open_browser.open_new_tab(authorization_url)
        authorization_response = input('authorization_response')
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

    return credentials
# TODO: add user oauth