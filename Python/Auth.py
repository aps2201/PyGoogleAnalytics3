from google.oauth2 import service_account
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
def gauth(**creds):
    credentials = None
    if 'cred_dict' in creds:
        credentials = service_account.Credentials.from_service_account_info(creds.get('cred_dict'))
    elif 'json_file' in creds:
        credentials = service_account.Credentials.from_service_account_file(creds.get('json_file'))
    return credentials