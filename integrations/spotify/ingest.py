import csv
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from integrations.spotify.auth import request_access_token

load_dotenv()

ACCESS_HEADER = None
root = Path(os.getenv('PROJECT_ROOT', '.'))
TRACK_ID_FILE_PATH = root / 'data' / 'spotify_track_ids.csv'
TRACK_FEATURES_FILE_PATH = root / 'data' / 'spotify_track_features.csv'
DATASET_SIZE_THRESHOLD = 10
SPOTIFY_WEB_API = 'https://api.spotify.com/v1/'
TRACK_DATA_ENDPOINT = 'tracks/'
AUDIO_FEATURES_ENDPOINT = 'audio-features/'
AUDIO_ANALYSIS_ENDPOINT = 'audio-analysis/'


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
        print("Access forbidden. Check permissions and scope of access token.")
        return None
    else:
        print(f"Failed to fetch audio features for track ID {track_id}")
        return None


def collect_track_data(track_id: str) -> dict:
    """
    Placeholder
    """
    track_data = call_spotify_endpoint(TRACK_DATA_ENDPOINT, track_id)
    audio_features = call_spotify_endpoint(AUDIO_FEATURES_ENDPOINT, track_id)
    audio_analysis = call_spotify_endpoint(AUDIO_ANALYSIS_ENDPOINT, track_id)
    if not track_data:
        return {}
    track_features = {

    }
    if audio_features:
        track_features.update({
            'track_id': track_id,
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'mode': audio_features['mode'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo'],
        })
    if audio_analysis:
        track_features.update({

        })
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
