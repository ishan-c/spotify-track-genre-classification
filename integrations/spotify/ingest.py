"""
Spotify Data Ingestion Script

This script automates the process of collecting and processing data from the Spotify API, focusing on tracks and their
associated artists. It is designed to fetch track metadata, audio features, and artist details in batches, optimizing
API call efficiency and handling common issues like rate limiting and authentication token expiration.

Features include:
- Batch fetching of track data and audio features using a list of track IDs.
- Collection of unique artist IDs from tracks and subsequent batch fetching of detailed artist information.
- Robust error handling to gracefully manage rate limiting (429 errors), access token expiration (401 errors),
  and other potential API response issues.
- Logging of key events and warnings to facilitate monitoring and troubleshooting of the data ingestion process.
- Structured storage of fetched data into CSV files, including a separate file for track features, artist IDs, and
  artist features.

The script organizes data collection into three main phases:
1. Playlist Iteration: Retrieves track ids from a list of playlist ids provided in a flat file
2. Track Data Collection: Retrieves track metadata and audio features, logging and skipping over tracks with no response
3. Artist Data Enrichment: Uses collected artist IDs to fetch and store additional artist information

Usage:
The script is executed with a `main` function call, which initiates the data ingestion process. It requires a valid
Spotify API client ID and client secret, which should be provided via environment variables or a configuration file.

Components:
- `main`: Orchestrates the data ingestion workflow, managing file operations and the overall sequence of API calls.
- `get_track_ids`: Reads a list of playlist ids and creates a list of track ids to attempt importing
- `collect_track_data`: Fetches data for a batch of tracks and parses the response.
- `collect_artist_data`: Fetches detailed information for a batch of artists and parses the response.
- `parse_track_responses`: Processes API responses for track data, combining metadata with audio features.
- `parse_artist_responses`: Processes API responses for artist data, structuring the information for further analysis.
- Various helper functions to support the main data collection tasks.

This script is a practical application of interacting with the Spotify API to build a dataset for music analysis,
demonstrating batch processing, error handling, and data structuring techniques.
"""
import csv
import logging.handlers
import os
import time
from datetime import datetime, timedelta
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
PLAYLIST_IDS_FILE_PATH = root / 'data' / 'spotify_ingest_playlist_ids.csv'
TRACK_ID_FILE_PATH = root / 'data' / 'spotify_track_ids.csv'
ARTIST_ID_FILE_PATH = root / 'data' / 'spotify_artist_ids.csv'
TRACK_FEATURES_FILE_PATH = root / 'data' / 'spotify_track_features.csv'
ARTIST_FEATURES_FILE_PATH = root / 'data' / 'spotify_artist_features.csv'
LAST_API_CALL = datetime.now()
DATASET_SIZE_THRESHOLD = 50000
BATCH_SIZE = 50


def get_time() -> str:
    """
    Utility for docstrings

    Returns:
    - str: current time as a formatted string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def call_spotify_endpoint(endpoint: str, spotify_id: str, calls: int = 0, url: str = None) -> Optional[dict]:
    """
    Makes a request to a Spotify API endpoint for a given Spotify ID payload, handling retries and common HTTP errors.

    This function is designed to handle each potential response outlined in the Spotify Web API reference, including
    rate limiting (HTTP 429), access token expiration (HTTP 401), and forbidden access (HTTP 403). It implements
    automatic retries for rate limiting and token expiration, with a maximum limit on retry attempts.

    Parameters:
    - endpoint (str): The Spotify API endpoint to be called.
    - spotify_id (str): The unique identifier for the track, artist, or other Spotify entity.
    - calls (int): A counter tracking the number of API call attempts made for this request, used to limit retries.
    - url (str): Optional string to override default behavior if full API call is available (used for playlists)
    Returns:
    - dict: The dictionary JSON response from the Spotify API if the request is successful; otherwise, None.

    The function logs warnings for rate limiting and errors, and retries the request after a delay specified by the
    Spotify API when rate limited. For access token issues, it refreshes the token and retries the request. If the
    maximum number of retries is exceeded or an unhandled HTTP status code is received, the function returns None.
    """
    global ACCESS_HEADER, LAST_API_CALL
    if calls > 3:
        log.warning(f'[{get_time()}] Maximum API call attempt limit reached.')
        return None
    if not url:
        url = SPOTIFY_WEB_API + endpoint + spotify_id
    if datetime.now() < LAST_API_CALL + timedelta(seconds=1):
        time.sleep(1)
    LAST_API_CALL = datetime.now()
    response = requests.get(url, headers=ACCESS_HEADER)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        log.info(f'[{get_time()}] Rate limit exceeded. Retrying after {retry_after} seconds.')
        time.sleep(retry_after)
        return call_spotify_endpoint(endpoint, spotify_id, calls=calls + 1, url=url)
    elif response.status_code == 401:
        ACCESS_HEADER = request_access_token()
        return call_spotify_endpoint(endpoint, spotify_id, calls=calls + 1, url=url)
    elif response.status_code == 403:
        log.warning(f'[{get_time()}] Access forbidden attempting to fetch from endpoint {endpoint} for id {spotify_id}.'
                    f'Check permissions and scope of access token.')
        return None
    elif response.status_code == 404:
        log.warning(f'[{get_time()}] Entity not found accessing {endpoint} for id {spotify_id}. Recheck URL and ID.')
        return None
    else:
        log.warning(f'[{get_time()}] Failed to access {endpoint} for id {spotify_id} due to unhandled response: '
                    f'{response.status_code}')
        return None


def get_track_ids() -> Optional[List[str]]:
    """
    Accesses a fixed playlist ids file and calls the Spotify API in order to yield the track ids of every track in each
    playlist, automatically handling pagination using the API response to ensure all tracks are retrieved.

    Returns:
         track_ids (list) - list of strings representing Spotify track ids found each of the playlists
    """

    if not os.path.exists(PLAYLIST_IDS_FILE_PATH):
        log.error(f'[{get_time()}] No playlists IDS found at path: {PLAYLIST_IDS_FILE_PATH}')
        return None

    with open(PLAYLIST_IDS_FILE_PATH, mode='r', newline='', encoding='utf-8-sig') as playlist_file:
        reader = csv.reader(playlist_file)
        playlist_ids = {line[0] for line in reader}

    track_ids = []
    for playlist_id in playlist_ids:
        log.debug(f"[{get_time()}] Collecting track ids for playlist id: {playlist_id}")
        next_url = SPOTIFY_WEB_API + PLAYLIST_ENDPOINT + playlist_id + '/tracks?limit=50'
        while next_url:
            playlist_data = call_spotify_endpoint(PLAYLIST_ENDPOINT, playlist_id, calls=0, url=next_url)
            if not playlist_data:
                log.warning(f'[{get_time()}] Did not receive suitable API response for playlist {playlist_id}. '
                            f'Skipping...')
                break
            track_ids.extend([item['track']['id'] for item in playlist_data['items']])
            next_url = playlist_data['next']

    return track_ids


def get_existing_ids(file_path: Path) -> Tuple[Set, int]:
    """
    Reads existing track or artist ids from specified path and returns them in a tuple containing a set of known ids and
    the integer number of tracks or artists found

    Arguments:
    - file_path (Path): path of a csv file containing one Spotify track or artist id string per row

    Returns:
    - tuple: A tuple containing two elements, the set of track or artist id strings and the integer number of
             tracks/artists in the file
    """
    seen_ids = set()
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as id_file:
            reader = csv.reader(id_file)
            seen_ids = {line[0] for line in reader}
    return seen_ids, len(seen_ids)


def parse_track_responses(track_data: dict, audio_features: dict) -> Tuple[List[dict], Set[str]]:
    """
    Parses track data and audio features from Spotify's API responses into a structured format.

    This function combines information from two separate API responses: track metadata and audio features,
    merging them into a list of dictionaries, each representing a track with its associated features.
    Additionally, it collects and returns a set of unique artist IDs found across all tracks processed in the batch.

    Parameters:
    - track_data (dict): The JSON response from the Spotify API containing track metadata.
    - audio_features (dict): The JSON response from the Spotify API containing audio features for the tracks.

    Returns:
    - tuple: A two-element tuple containing:
        - A list of dictionaries, where each dictionary contains merged metadata and audio features for a single track.
        - A set of unique artist IDs associated with the tracks processed in this batch.

    Each track dictionary includes fields specified in `TRACK_DATA_FIELDS` and `AUDIO_FEATURES_FIELDS`, along
    with a list of artist IDs under the key 'artist_ids'. This function ensures that data from both responses
    are aligned and combined based on the track IDs.
    """
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
    Fetches and processes a batch of track IDs to collect track data and audio features from the Spotify API.

    This function makes calls to the Spotify API to fetch data for a list of track IDs, including track metadata
    and audio features. It then parses the responses to structure the data into a list of dictionaries per track
    and collects a set of artist IDs associated with those tracks.

    Parameters:
    - batch (list): A list of Spotify track IDs to be processed.

    Returns:
    - tuple: a two-element tuple containing the following:
        - A list of dictionaries with combined track data and audio features, or None if the API response is inadequate.
        - A set of unique artist IDs found within the batch of tracks, or None if the API response is inadequate.

    The function logs a warning and returns None for both elements of the tuple if it fails to receive valid responses
    from the Spotify API for either track data or audio features.
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
    """
    Parses artist data from Spotify's API response into a structured format.

    This function transforms the JSON response containing artist details into a list of dictionaries,
    each representing an artist with selected fields specified in `ARTIST_FIELDS`. It includes the artist's
    follower count, extracted from a nested structure within the response data.

    Parameters:
    - artist_data (dict): The JSON response from the Spotify API containing details for multiple artists.

    Returns:
    - list: A list of dictionaries, each containing fields for an artist as specified by `ARTIST_FIELDS`,
      along with the artist's follower count under the key 'artist_followers'.

    The function focuses on extracting relevant information to facilitate the analysis of artist popularity
    and other attributes by providing a clean, flat structure for each artist's data.
    """
    batch_artist_features = []
    for artist in artist_data['artists']:
        artist_features = {ARTIST_FIELDS[field]: artist.get(field) for field in ARTIST_FIELDS}
        artist_features['artist_followers'] = artist.get('followers', {}).get('total', 0)

        batch_artist_features.append(artist_features)

    return batch_artist_features


def collect_artist_data(batch: list[str]) -> Optional[List[dict]]:
    """
    Fetches and processes a batch of artist IDs to collect detailed artist information from the Spotify API.

    This function makes a call to the Spotify API to fetch detailed information for a list of artist IDs. It
    parses the response to structure the data into a list of dictionaries, each representing an artist with
    selected fields of interest.

    Parameters:
    - batch (list): A list of Spotify artist IDs to be processed.

    Returns:
    - list: A list of dictionaries with artist data, or None if the API response is inadequate.

    The function logs a warning and returns None if it fails to receive a valid response from the Spotify API.
    This ensures that the data collection process can gracefully handle and log API-related issues without interrupting
    the broader data ingest workflow.
    """
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
    if not track_ids:
        log.error(f'[{get_time()}] No tracks or playlists found. Please provide a file at path: '
                  f'{PLAYLIST_IDS_FILE_PATH}')
        return
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
