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
BATCH_SIZE = 50


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


def call_spotify_endpoint(endpoint: str, spotify_id: str, calls: int = 0) -> Optional[dict]:
    """Calls a Spotify endpoint for a given track or playlist ID and handles various HTTP responses."""
    global ACCESS_HEADER
    if calls > 3:
        print(f"Maximum API call attempt limit reached")
        return None
    url = SPOTIFY_WEB_API + endpoint + spotify_id
    response = requests.get(url, headers=ACCESS_HEADER)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f'Rate limit exceeded. Retrying after {retry_after} seconds.')
        time.sleep(retry_after)
        return call_spotify_endpoint(endpoint, spotify_id, calls=calls + 1)
    elif response.status_code == 401:
        ACCESS_HEADER = request_access_token()
        return call_spotify_endpoint(endpoint, spotify_id, calls=calls + 1)
    elif response.status_code == 403:
        print(f'Access forbidden attempting to fetch {endpoint[:-5]} for track {spotify_id}. '
              f'Check permissions and scope of access token.')
        return None
    else:
        print(f'Failed to fetch {endpoint[:-5]} for: {spotify_id} due to unhandled response {response.status_code}')
        return None


def parse_track_responses(track_data: dict, audio_features: dict) -> []:
    batch_track_features = []

    for track, features in zip(track_data['tracks'], audio_features['audio_features']):
        track_features = {TRACK_DATA_FIELDS[field]: track[field] for field in TRACK_DATA_FIELDS}

        audio_data = {AUDIO_FEATURES_FIELDS[field]: features[field] for field in AUDIO_FEATURES_FIELDS}
        track_features.update(audio_data)

        artist_data = {}
        for artist in track['artists']:
            pass

        batch_track_features.append(track_features)

    return batch_track_features


def collect_track_data(batch: List[str]) -> Optional[dict]:
    """
    Placeholder
    """
    track_ids = ','.join(batch)
    batch_track_data = call_spotify_endpoint(TRACK_DATA_ENDPOINT, track_ids)
    batch_audio_features = call_spotify_endpoint(AUDIO_FEATURES_ENDPOINT, track_ids)
    if not batch_track_data or not batch_audio_features:
        print('Did not receive suitable API response for processing. Skipping batch...')
        return None
    batch_track_features = parse_track_responses(batch_track_data, batch_audio_features)

    return batch_track_features


def main():
    global ACCESS_HEADER
    ACCESS_HEADER = request_access_token()
    track_ids = get_track_ids()
    processed_ids, n_seen = get_existing_track_ids()
    new_track_ids = [track for track in track_ids if track not in processed_ids]
    n_new = len(new_track_ids)

    if n_new + n_seen >= DATASET_SIZE_THRESHOLD:
        print(f'Attempting to add {n_new} tracks, which will exceed threshold {DATASET_SIZE_THRESHOLD}. '
              f'Increase threshold to try again.\nCancelling ingest.)')
        return

    with (open(TRACK_ID_FILE_PATH, mode='a', newline='', encoding='utf-8') as id_file,
          open(TRACK_FEATURES_FILE_PATH, mode='a', newline='', encoding='utf-8') as data_file):

        id_writer = csv.writer(id_file)
        data_writer = csv.DictWriter(data_file)

        if n_seen == 0:
            data_writer.writeheader()

        n_batch_tracks = (n_new // BATCH_SIZE) * BATCH_SIZE
        track_counter, batch_counter, processed_tracks = 0, 0, 0
        batch = []
        for track_id in new_track_ids:
            track_counter += 1
            batch_counter += 1
            batch.append(track_id)
            if track_counter > n_batch_tracks or len(batch) == BATCH_SIZE:
                batch_track_features = collect_track_data(batch)
                if batch_track_features:
                    for track_features in batch_track_features:
                        data_writer.writerow(track_features)
                        id_writer.writerow([track_features['id']])
                    processed_tracks += len(batch_track_features)


if __name__ == '__main__':
    main()
