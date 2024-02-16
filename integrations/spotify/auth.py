"""
This module allows for authentication with the Spotify Web API using the Client Credentials Flow. It handles requesting,
saving, and refreshing access tokens to ensure uninterrupted access to the API for server-to-server applications.

The module uses environment variables to manage sensitive information such as the
client ID and client secret required for the authentication process.

Requirements:
- A `.env` file or environment variables `CLIENT_ID`, `CLIENT_SECRET`, and `PROJECT_ROOT`
  must be set for the module to function correctly.
- The `requests` library is used to make HTTP requests to the Spotify API.
- The `dotenv` library is used to load environment variables from the `.env` file.
"""
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


def save_token(token: str, expires: datetime):
    """
    Saves the access token and its expiration time to a JSON file in the project root

    Parameters:
    - token (str): spotify access token
    - expires (datetime): expiration time of access token
    """
    data = {
        'access_token': token,
        'expires': expires.isoformat()
    }
    with open(TOKEN_FILE_PATH, 'w') as f:
        json.dump(data, f)


def load_token() -> tuple:
    """
    Loads the access token and its expiration time from a JSON file

    Returns:
    - tuple: tuple containing the access token (str) and its expiration time (datetime), or (None, None) if the token
      does not exist or the file is not found
    """
    if TOKEN_FILE_PATH.exists():
        with open(TOKEN_FILE_PATH, 'r') as f:
            data = json.load(f)
            return data['access_token'], datetime.fromisoformat(data['expires'])
    return None, None


def package_access_token(token: str) -> dict:
    """
    Creates a dictionary containing the authorization headers required for Spotify API requests

    Parameters:
    - token (str): the Spotify access token

    Returns:
    - dict: dictionary with `Authorization` header, ready for use in requests
    """
    return {
        'Authorization': f'Bearer {token}',
    }


def request_access_token() -> dict:
    """
    Requests a new Spotify access token using the Client Credentials Flow. If an existing token is not expired, it
    returns the existing token. Otherwise, it requests a new token, saves it, and returns it.

    Returns:
    - dict: headers dictionary containing the Spotify access token used for authentication

    Raises:
    - requests.RequestException: if there is an error making the request to the Spotify API.
    """
    access_token, expires = load_token()
    if access_token and expires and datetime.now() < (expires - timedelta(seconds=300)):
        return package_access_token(access_token)

    credentials = base64.b64encode(f'{os.getenv("CLIENT_ID")}: {os.getenv("CLIENT_SECRET")}'.encode()).decode()
    auth_headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
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
        return package_access_token(access_token)
    except requests.RequestException as e:
        print(f"Error requesting access token: {e}")
        raise
