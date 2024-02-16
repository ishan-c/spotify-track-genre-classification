import base64
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
AUTH_URL = 'https://accounts.spotify.com/api/token'
TOKEN_FILE_PATH = Path(os.getenv('PROJECT_ROOT', '.')) / 'spotify_token.json'


def save_token(token, expires):
    data = {
        'access_token': token,
        'expires': expires.isoformat()
    }
    with open(TOKEN_FILE_PATH, 'w') as f:
        json.dump(data, f)


def load_token():
    if TOKEN_FILE_PATH.exists():
        with open(TOKEN_FILE_PATH, 'r') as f:
            data = json.load(f)
            return data['access_token'], datetime.fromisoformat(data['expires'])
    return None, None


def request_access_token():
    access_token, expires = load_token()
    if access_token and expires and datetime.now() < (expires - timedelta(seconds=300)):
        return access_token

    credentials = base64.b64encode(f'{os.getenv("CLIENT_ID")}: {os.getenv("CLIENT_SECRET")}'.encode()).decode()
    auth_headers = {
        'Authorization': f'Basic {credentials}'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    try:
        auth_response = requests.post(AUTH_URL, headers=auth_headers, data=auth_data)
        auth_response.raise_for_status()
        auth_response_json = auth_response.json()
        expires = datetime.now() + timedelta(seconds=auth_response_json['expires_in'])
        access_token = auth_response_json['access_token']
        save_token(access_token, expires)
        return access_token
    except requests.RequestException as e:
        print(f"Error requesting access token: {e}")
        raise
