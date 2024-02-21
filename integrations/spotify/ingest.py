import csv
import logging.handlers
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set, Tuple

import requests
from dotenv import load_dotenv

from integrations.spotify.auth import request_access_token
from integrations.spotify.endpoint_fields import *

load_dotenv()

log = logging.getLogger()
log.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)

file_handler = logging.FileHandler(f"spotify_ingest_{datetime.now().strftime('%Y-%m-%d_%H-%M_%S')}.log")
file_handler.setLevel(logging.DEBUG)
log.addHandler(file_handler)

ACCESS_HEADER = None
root = Path(os.getenv('PROJECT_ROOT', '.'))
TRACK_ID_FILE_PATH = root / 'data' / 'spotify_track_ids.csv'
ARTIST_ID_FILE_PATH = root / 'data' / 'spotify_artist_ids.csv'
TRACK_FEATURES_FILE_PATH = root / 'data' / 'spotify_track_features.csv'
ARTIST_FEATURES_FILE_PATH = root / 'data' / 'spotify_artist_features.csv'
DATASET_SIZE_THRESHOLD = 10
BATCH_SIZE = 50


def get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_track_ids():
    return ['3rUGC1vUpkDG9CZFHMur1t', '6Qb7YsAqH4wWFUMbGsCpap', '7gaA3wERFkFkgivjwbSvkG', '17phhZDn6oGtzMe56NuWvj',
            '4iZ4pt7kvcaH6Yo8UoZ4s2']


def get_existing_ids(file_path: Path) -> Tuple[Set, int]:
    """
    Reads existing track or artist ids from specified path and returns them in a tuple containing a set of known ids and
    the integer number of tracks or artists found

    Arguments:
    - file_path (Path): path of a csv file containing one Spotify track or artist id string per row

    Returns:
    - tuple: A tuple containing two elements, the set of track_id strings and the integer number of tracks in the file
    """
    seen_ids = set()
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as id_file:
            reader = csv.reader(id_file)
            seen_ids = {line[0] for line in reader}
    return seen_ids, len(seen_ids)


def call_spotify_endpoint(endpoint: str, spotify_id: str, calls: int = 0) -> Optional[dict]:
    """Calls a Spotify endpoint for a given track or playlist ID and handles various HTTP responses."""
    global ACCESS_HEADER
    if calls > 3:
        log.warning(f'[{get_time()}] Maximum API call attempt limit reached.')
        return None
    url = SPOTIFY_WEB_API + endpoint + spotify_id
    response = requests.get(url, headers=ACCESS_HEADER)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        log.info(f'[{get_time()}] Rate limit exceeded. Retrying after {retry_after} seconds.')
        time.sleep(retry_after)
        return call_spotify_endpoint(endpoint, spotify_id, calls=calls + 1)
    elif response.status_code == 401:
        ACCESS_HEADER = request_access_token()
        return call_spotify_endpoint(endpoint, spotify_id, calls=calls + 1)
    elif response.status_code == 403:
        log.warning(f'[{get_time()}] Access forbidden attempting to fetch {endpoint[:-5]} for track {spotify_id}. '
                    f'Check permissions and scope of access token.')
        return None
    else:
        log.warning(f'[{get_time()}] Failed to fetch {endpoint[:-5]} for: {spotify_id} due to unhandled response: '
                    f'{response.status_code}')
        return None


def parse_track_responses(track_data: dict, audio_features: dict) -> Tuple[List[dict], Set[str]]:
    batch_track_features = []
    batch_artist_ids = set()

    for track, features in zip(track_data['tracks'], audio_features['audio_features']):
        track_features = {TRACK_DATA_FIELDS[field]: track.get(field) for field in TRACK_DATA_FIELDS}
        audio_data = {AUDIO_FEATURES_FIELDS[field]: features.get(field) for field in AUDIO_FEATURES_FIELDS}
        track_features.update(audio_data)

        artist_ids = [artist.get('id') for artist in track['artists']]
        track_features['artist_ids'] = artist_ids
        batch_artist_ids.update(set(artist_ids))

        batch_track_features.append(track_features)

    return batch_track_features, batch_artist_ids


def collect_track_data(batch: List[str]) -> Tuple[Optional[List[dict]], Optional[Set[str]]]:
    """
    Placeholder
    """
    track_ids = ','.join(batch)
    batch_track_data = call_spotify_endpoint(TRACK_DATA_ENDPOINT, track_ids)
    batch_audio_features = call_spotify_endpoint(AUDIO_FEATURES_ENDPOINT, track_ids)
    if not batch_track_data or not batch_audio_features:
        log.warning(f'[{get_time()}] Did not receive suitable API response for processing tracks. Skipping batch...')
        return None, None
    batch_track_features, new_artist_ids = parse_track_responses(batch_track_data, batch_audio_features)

    return batch_track_features, new_artist_ids


def parse_artist_responses(artist_data: dict) -> List[dict]:
    batch_artist_features = []
    for artist in artist_data['artists']:
        artist_features = {ARTIST_FIELDS[field]: artist.get(field) for field in ARTIST_FIELDS}
        artist_features['artist_followers'] = artist.get('followers', {}).get('total', 0)

        batch_artist_features.append(artist_features)

    return batch_artist_features


def collect_artist_data(batch: list[str]) -> Optional[List[dict]]:
    artist_ids = ','.join(batch)
    batch_artist_data = call_spotify_endpoint(ARTIST_DATA_ENDPOINT, artist_ids)
    if not batch_artist_data:
        log.warning(f'[{get_time()}] Did not receive suitable API response for processing artists. Skipping batch...')
        return None
    batch_artist_features = parse_artist_responses(batch_artist_data)

    return batch_artist_features


def main():
    """
    Orchestrates the data ingestion process from the Spotify API, focusing on collecting new track and artist data.

    This function performs several key operations:
    - Requests a new access token for Spotify API authentication.
    - Retrieves a list of track IDs to be processed.
    - Filters out track IDs already present in the dataset to avoid duplicates.
    - Checks against a dataset size threshold to prevent excessive data collection.
    - Collects and stores new track data along with associated artist IDs.
    - Identifies new artist IDs and collects detailed artist information in a second pass.
    - Logs the progress and completion of data ingestion steps, including the number of tracks and artists added.

    The process involves reading and writing to CSV files for track IDs, artist IDs, track features, and artist
    features. It ensures that only new data is added, leveraging existing datasets to maintain a comprehensive and
    up-to-date collection.
    """
    log.info(f'[{get_time()}] Starting Spotify API data ingest')
    global ACCESS_HEADER
    ACCESS_HEADER = request_access_token()
    track_ids = get_track_ids()
    known_artist_ids, n_artists = get_existing_ids(ARTIST_ID_FILE_PATH)
    known_track_ids, n_tracks = get_existing_ids(TRACK_ID_FILE_PATH)
    new_track_ids = [track for track in track_ids if track not in known_track_ids]
    n_new_tracks = len(new_track_ids)

    if n_new_tracks + n_tracks >= DATASET_SIZE_THRESHOLD:
        log.error(f'[{get_time()}] Attempting to add {n_new_tracks} tracks, which will exceed threshold of '
                  f'{DATASET_SIZE_THRESHOLD}. Increase threshold to try again. Cancelling ingest.')
        return

    log.info(f"[{get_time()}] Attempting to get {n_new_tracks} new tracks. There are {n_tracks} in the existing "
             f"data files.")
    with (open(TRACK_ID_FILE_PATH, mode='a', newline='', encoding='utf-8') as id_file,
          open(ARTIST_ID_FILE_PATH, mode='a', newline='', encoding='utf-8') as artist_id_file,
          open(TRACK_FEATURES_FILE_PATH, mode='a', newline='', encoding='utf-8') as data_file):

        track_id_writer = csv.writer(id_file)
        artist_id_writer = csv.writer(artist_id_file)
        track_data_writer = csv.DictWriter(data_file, fieldnames=CSV_FIELDNAMES)

        if n_tracks == 0:
            track_data_writer.writeheader()

        processed_tracks = 0
        new_artist_ids = set()

        for i in range(0, n_new_tracks, BATCH_SIZE):
            batch = new_track_ids[i:i + BATCH_SIZE]
            batch_track_features, batch_artist_ids = collect_track_data(batch)
            if batch_track_features:
                for track_features in batch_track_features:
                    track_data_writer.writerow(track_features)
                    track_id_writer.writerow([track_features['track_id']])
                processed_tracks += len(batch_track_features)
                batch_new_artist_ids = batch_artist_ids - known_artist_ids
                if batch_new_artist_ids:
                    for artist_id in batch_new_artist_ids:
                        artist_id_writer.writerow([artist_id])
                    new_artist_ids.update(batch_new_artist_ids)
                    known_artist_ids.update(batch_new_artist_ids)

    n_new_artists = len(new_artist_ids)
    log.info(f"[{get_time()}] Successfully added {processed_tracks} new tracks to dataset. Found {n_new_artists} new "
             f"artists.\nPopulating artist data...")

    with open(ARTIST_FEATURES_FILE_PATH, mode='a', newline='', encoding='utf-8') as artist_data_file:
        artist_data_writer = csv.DictWriter(artist_data_file, fieldnames=ARTIST_CSV_FIELDNAMES)

        if n_artists == 0:
            artist_data_writer.writeheader()

        new_artist_ids = list(new_artist_ids)
        for j in range(0, n_new_artists, BATCH_SIZE):
            batch = new_artist_ids[j:j + BATCH_SIZE]
            batch_artist_features = collect_artist_data(batch)
            if batch_artist_features:
                for artist_features in batch_artist_features:
                    artist_data_writer.writerow(artist_features)

    log.info(f"[{get_time()}] Data ingest complete.")


if __name__ == '__main__':
    main()
