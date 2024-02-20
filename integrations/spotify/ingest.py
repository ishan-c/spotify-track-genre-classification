import csv
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from integrations.spotify.auth import request_access_token

load_dotenv()

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
    seen_ids = set()
    num_seen = 0
    if os.path.exists(TRACK_ID_FILE_PATH):
        with open(TRACK_ID_FILE_PATH, mode='r') as id_file:
            reader = csv.reader(id_file)
            seen_ids = {track for track in reader}
        num_seen = len(seen_ids)
    return seen_ids, num_seen


def call_spotify_endpoint(endpoint: str, track_id: str, access_header: dict):
    """Fetches audio features for a given track ID."""
    url = SPOTIFY_WEB_API + endpoint + track_id
    response = requests.get(url, headers=access_header)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        pass
    elif response.status_code == 401:
        pass
    elif response.status_code == 403:
        pass
    else:
        print(f"Failed to fetch audio features for track ID {track_id}")
        return None


def collect_track_data(track_id: str, access_header: dict):
    """
    Placeholder
    """
    track_data = call_spotify_endpoint(TRACK_DATA_ENDPOINT, track_id, access_header)
    audio_features = call_spotify_endpoint(AUDIO_FEATURES_ENDPOINT, track_id, access_header)
    audio_analysis = call_spotify_endpoint(AUDIO_ANALYSIS_ENDPOINT, track_id, access_header)
    track_features = {}
    if track_data:
        track_features = {}
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
    access_header = request_access_token()
    track_ids = get_track_ids()
    processed_ids, n = get_existing_track_ids()

    if n >= DATASET_SIZE_THRESHOLD:
        print(f'Dataset size of {n} equals or exceeds threshold {DATASET_SIZE_THRESHOLD}. Increase threshold to ingest. '
              f'\nCancelling...)')
        return

    new_track_ids = [track for track in track_ids if track not in processed_ids]
    track_counter = 0

    with (open(TRACK_ID_FILE_PATH, mode='w') as id_file,
          open(TRACK_FEATURES_FILE_PATH, mode='w', newline='', encoding='utf-8') as data_file):

        id_writer = csv.writer(id_file)
        data_writer = csv.DictWriter(data_file)
        data_writer.writeheader()

        for track_id in new_track_ids:
            track_features = collect_track_data(track_id, access_header)
            data_writer.writerow(track_features)
            id_writer.writerow(track_id)
            track_counter += 1


if __name__ == '__main__':
    main()
