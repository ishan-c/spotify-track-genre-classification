import csv
import os
import time
from pathlib import Path
from typing import List, Optional

import requests
from dotenv import load_dotenv

from integrations.spotify.auth import request_access_token
from integrations.spotify.endpoint_fields import *

load_dotenv()

ACCESS_HEADER = None
root = Path(os.getenv('PROJECT_ROOT', '.'))
TRACK_ID_FILE_PATH = root / 'data' / 'spotify_track_ids.csv'
TRACK_FEATURES_FILE_PATH = root / 'data' / 'spotify_track_features.csv'
DATASET_SIZE_THRESHOLD = 10
SPOTIFY_WEB_API = 'https://api.spotify.com/v1/'


def get_track_ids():
    return []


def get_existing_track_ids() -> tuple:
    """
    Reads existing track ids from the TRACK_ID_FILE_PATH and returns them in a tuple containing a set of track ids and
    the integer number of tracks

    Returns:
    - tuple: A tuple containing two elements, the set of track_id strings and the integer number of tracks in the file
    """
    seen_ids = set()
    if os.path.exists(TRACK_ID_FILE_PATH):
        with open(TRACK_ID_FILE_PATH, mode='r', newline='', encoding='utf-8') as id_file:
            reader = csv.reader(id_file)
            seen_ids = {line[0] for line in reader}
    return seen_ids, len(seen_ids)


def call_spotify_endpoint(endpoint: str, track_id: str):
    """Calls a Spotify endpoint for a given track or playlist ID and handles various HTTP responses."""
    global ACCESS_HEADER
    url = SPOTIFY_WEB_API + endpoint + track_id
    response = requests.get(url, headers=ACCESS_HEADER)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f'Rate limit exceeded. Retrying after {retry_after} seconds.')
        time.sleep(retry_after)
        return call_spotify_endpoint(endpoint, track_id)
    elif response.status_code == 401:
        ACCESS_HEADER = request_access_token()
        return call_spotify_endpoint(endpoint, track_id)
    elif response.status_code == 403:
        print(f'Access forbidden attempting to fetch {endpoint[:-1]} for track {track_id}. '
              f'Check permissions and scope of access token.')
        return None
    else:
        print(f'Failed to fetch {endpoint[:-1]} for track: {track_id} due to unhandled response {response.status_code}')
        return None


def parse_track_responses(track_data, audio_features) -> dict:
    return {}


def collect_track_data(track_id: str) -> Optional[dict]:
    """
    Placeholder
    """
    track_data = call_spotify_endpoint(TRACK_DATA_ENDPOINT, track_id)
    audio_features = call_spotify_endpoint(AUDIO_FEATURES_ENDPOINT, track_id)
    if not track_data and audio_features:
        print(f'Missing data for {track_id}, skipping...')
        return
    track_features = parse_track_responses(track_data, audio_features)

    return track_features


def main():
    global ACCESS_HEADER
    ACCESS_HEADER = request_access_token()
    track_ids = get_track_ids()
    processed_ids, n = get_existing_track_ids()
    new_track_ids = [track for track in track_ids if track not in processed_ids]

    if len(new_track_ids) + n >= DATASET_SIZE_THRESHOLD:
        print(f'Attempting to add {len(new_track_ids)} tracks, which will exceed threshold {DATASET_SIZE_THRESHOLD}. '
              f'Increase threshold to ingest.\nCancelling ingest.)')
        return

    track_counter = 0

    with (open(TRACK_ID_FILE_PATH, mode='a', newline='', encoding='utf-8') as id_file,
          open(TRACK_FEATURES_FILE_PATH, mode='a', newline='', encoding='utf-8') as data_file):

        id_writer = csv.writer(id_file)
        data_writer = csv.DictWriter(data_file)

        if n == 0:
            data_writer.writeheader()

        for track_id in new_track_ids:
            track_features = collect_track_data(track_id)
            if track_features:
                data_writer.writerow(track_features)
                id_writer.writerow([track_id])
                track_counter += 1


if __name__ == '__main__':
    main()
