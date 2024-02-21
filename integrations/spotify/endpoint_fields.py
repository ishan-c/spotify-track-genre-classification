SPOTIFY_WEB_API = 'https://api.spotify.com/v1/'

PLAYLIST_ENDPOINT = 'playlists/'

TRACK_DATA_ENDPOINT = 'tracks?ids='

AUDIO_FEATURES_ENDPOINT = 'audio-features?ids='

TRACK_DATA_FIELDS = {
    'id': 'track_id',
    'duration_ms': 'duration_ms',
    'name': 'track_name',
    'popularity': 'track_popularity'
}
AUDIO_FEATURES_FIELDS = {
    'acousticness': 'acousticness',
    'danceability': 'danceability',
    'energy': 'energy',
    'instrumentalness': 'instrumentalness',
    'key': 'key',
    'liveness': 'liveness',
    'loudness': 'loudness',
    'mode': 'mode',
    'speechiness': 'speechiness',
    'tempo': 'tempo',
    'time_signature': 'time_signature',
    'valence': 'valence'
}
CSV_FIELDNAMES = list(TRACK_DATA_FIELDS.values()) + ['artist_ids'] + list(AUDIO_FEATURES_FIELDS.values())

ARTIST_DATA_ENDPOINT = 'artists?ids='

ARTIST_FIELDS = {
    'genres': 'artist_genres',
    'id': 'artist_id',
    'name': 'artist_name',
    'popularity': 'artist_popularity'
}

ARTIST_CSV_FIELDNAMES = list(ARTIST_FIELDS.values()) + ['artist_followers']
