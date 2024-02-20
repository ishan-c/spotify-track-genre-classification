SPOTIFY_WEB_API = 'https://api.spotify.com/v1/'

TRACK_DATA_ENDPOINT = 'tracks?ids='
TRACK_DATA_FIELDS = {
    'id': 'track_id',
    'duration_ms': 'duration_ms',
    'name': 'track_name',
    'popularity': 'track_popularity'
}
ARTIST_FIELDS = {
    'genres': 'artist_genres',
    'id': 'artist_id',
    'name': 'artist_name',
    'popularity': 'artist_popularity'
}

FOLLOWERS_FIELDS = {
    'total': 'artist_followers'
}

AUDIO_FEATURES_ENDPOINT = 'audio-features?ids='
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
