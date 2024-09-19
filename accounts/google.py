
from google.auth.transport import requests
from google.oauth2 import id_token

GOOGLE_CLIENT_ID = ""

def verify_google_token(token):
    try:
        # Verify the integrity of the token
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        # If the token is valid, return the user's information
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        return id_info
    except ValueError:
        # Invalid token
        return None
