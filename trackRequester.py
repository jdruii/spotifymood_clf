import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import time
from hidden import secrets

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = secrets['client_id'],
                                                 client_secret = secrets['client_secret'],
                                                 redirect_uri = 'http://localhost:8080',
                                                 scope = 'playlist-read-private'))

happy = ['https://open.spotify.com/playlist/37i9dQZF1DWYBO1MoTDhZI', 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC',
         'https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4', 'https://open.spotify.com/playlist/37i9dQZF1DX2sUQwD7tbmL',
         'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0', 'https://open.spotify.com/playlist/37i9dQZF1DWZKuerrwoAGz',
         'https://open.spotify.com/playlist/37i9dQZF1EIcqv6dNT3Dgk', 'https://open.spotify.com/playlist/4iltRRtJm366KuNWbVuseK']

melancholic = ['https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1', 'https://open.spotify.com/playlist/37i9dQZF1DWSqBruwoIXkA',
               'https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR', 'https://open.spotify.com/playlist/37i9dQZF1DWVgPyzcfsKdn',
               'https://open.spotify.com/playlist/37i9dQZF1DX3YSRoSdA634','https://open.spotify.com/playlist/37i9dQZF1DWXeI0OwDbgC4',
               'https://open.spotify.com/playlist/37i9dQZF1DWWlf1FfxbDir', 'https://open.spotify.com/playlist/37i9dQZF1DWWlf1FfxbDir',
               'https://open.spotify.com/playlist/37i9dQZF1DXbrUpGvoi3TS', 'https://open.spotify.com/playlist/37i9dQZF1DXavVu4MrOFo3',
               'https://open.spotify.com/playlist/37i9dQZF1DWW2hj3ZtMbuO', 'https://open.spotify.com/playlist/5XB0tMu0xrkVDVmyLgPVte?si=b03c7544af2342b2',
               'https://open.spotify.com/playlist/3BZCnH82CgdJQoaLxDr95Q']

energetic = ['https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif', 'https://open.spotify.com/playlist/37i9dQZF1DWSf2RDTDayIx',
             'https://open.spotify.com/playlist/37i9dQZF1DWW668oFRU96k', 'https://open.spotify.com/playlist/37i9dQZF1DXaCACvgOVs5K',
             'https://open.spotify.com/playlist/37i9dQZF1DWZK99LPvBBfP', 'https://open.spotify.com/playlist/37i9dQZF1DX7D8GQsPKGvy',
             'https://open.spotify.com/playlist/37i9dQZF1DX8AliSIsGeKd', 'https://open.spotify.com/playlist/37i9dQZF1DWYfVJ5emu90I',
             'https://open.spotify.com/playlist/37i9dQZF1DXcZDD7cfEKhW', 'https://open.spotify.com/playlist/37i9dQZF1DWWY64wDtewQt']

relaxing = ['https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7', 'https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6',
            'https://open.spotify.com/playlist/37i9dQZF1DX3qCx5yEZkcJ', 'https://open.spotify.com/playlist/37i9dQZF1DWYoYGBbGKurt',
            'https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn']

anger = ['https://open.spotify.com/playlist/37i9dQZF1DWY1j3jZdCWOQ', 'https://open.spotify.com/playlist/37i9dQZF1DXasneILDRM7B',
         'https://open.spotify.com/playlist/37i9dQZF1DX3LDIBRoaCDQ', 'https://open.spotify.com/playlist/37i9dQZF1DXd6tJtr4qeot',
         'https://open.spotify.com/playlist/37i9dQZF1DX3ND264N08pv', 'https://open.spotify.com/playlist/07JztNEdtMFhc6hoLzQLsH',
         'https://open.spotify.com/playlist/5Nd0SHhQ8bQUXgYQ08jaar', 'https://open.spotify.com/playlist/11oabvR4QDkNzfenjxmN77']

romantic = ['https://open.spotify.com/playlist/37i9dQZF1DX6ZiG5Dz8cUM', 'https://open.spotify.com/playlist/37i9dQZF1DWTbzY5gOVvKd',
            'https://open.spotify.com/playlist/37i9dQZF1DX4s3V2rTswzO', 'https://open.spotify.com/playlist/37i9dQZF1DX6DLB6M8zkNk',
            'https://open.spotify.com/playlist/37i9dQZF1DX7rOY2tZUw1k', 'https://open.spotify.com/playlist/37i9dQZF1DX4cizS4wQeF2',
            'https://open.spotify.com/playlist/37i9dQZF1DWXqpDKK4ed9O', 'https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn',
            'https://open.spotify.com/playlist/5XrtkWpFklOxv0kIMxpDuZ']

playlist_lists = [happy, melancholic, energetic, relaxing, anger, romantic]

titles = []
artists = []
years = []
albums = []
duration = []
genres = []
popularity = []
audio_features_data = []

artist_cache = {}

def chosen_playlist():
    mood_labels = ['Happy', 'Melancholic', 'Energetic', 'Relaxing', 'Anger', 'Romantic']
    for mood, playlist_group in zip(mood_labels, playlist_lists):
        for url in playlist_group:
            yield url, mood

# retrieves all tracks in a playlist with pagination
def get_all_playlist_tracks(sp, playlist_id, playlist_items_requests, audio_features_requests, artist_requests):
    offset = 330
    limit = 100

    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        playlist_items_requests += 1
        print(f"Playlist Items Request #{playlist_items_requests}: Fetching tracks from offset {offset}")

        track_ids_batch = []

        for track in results['items']:
            track_info = track['track']
            title = track_info['name']
            album = track_info['album']['name']
            year = track_info['album']['release_date'][:4]
            track_duration = track_info['duration_ms']
            track_popularity = track_info['popularity']
            track_ids_batch.append(track_info['id'])

            artist_info = track_info['artists']
            artist_names = [artist['name'] for artist in artist_info]
            artist_genres = set()

            for artist in artist_info:
                artist_id = artist['id']
                if artist_id in artist_cache:
                    artist_data = artist_cache[artist_id]
                else:
                    artist_data = sp.artist(artist_id)
                    artist_cache[artist_id] = artist_data
                    artist_requests += 1
                    print(f"Artist Genre Request #{artist_requests}: Fetching data for artist ID {artist_id}")
                    if artist_requests % 100 == 0:
                        print("Pausing due to API rate limits")
                        time.sleep(10)

                artist_genres.update(artist_data['genres'])

            titles.append(title)
            artists.append(', '.join(artist_names))
            years.append(year)
            albums.append(album)
            duration.append(track_duration)
            genres.append(', '.join(list(artist_genres)))
            popularity.append(track_popularity)

        audio_features_batch = sp.audio_features(tracks=track_ids_batch)
        audio_features_requests += 1
        print(f"Audio Features Request #{audio_features_requests}: Fetching audio features for {len(track_ids_batch)} tracks")

        for audio_features in audio_features_batch:
            audio_features_data.append(audio_features)

        offset += limit
        if offset >= results['total']:
            break

    return playlist_items_requests, audio_features_requests, artist_requests

def main():
    playlist_items_requests = 0
    audio_features_requests = 0
    artist_requests = 0
    combined_csv_filename = 'all_playlists_mood_combined.csv'

    for playlist_id, mood in chosen_playlist():
        playlist_items_requests, audio_features_requests, artist_requests = get_all_playlist_tracks(
            sp, playlist_id, playlist_items_requests, audio_features_requests, artist_requests)

        moods = [mood] * len(titles)
        data = {
            'Title': titles,
            'Artist': artists,
            'Genres': genres,
            'Year': years,
            'Album': albums,
            'Popularity': popularity,
            'Mood': moods
        }

        for feature in audio_features_data[0]:
            if feature is not None:
                data[feature] = [audio_feature[feature] if audio_feature is not None else None for audio_feature in audio_features_data]

        df = pd.DataFrame(data)
        csv_filename = f'{mood.lower()}_playlist_data.csv'

        # Append to the mood-specific CSV file
        if os.path.exists(csv_filename):
            df.to_csv(csv_filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(csv_filename, mode='w', header=True, index=False, encoding='utf-8-sig')

        # Append to the combined CSV file
        if os.path.exists(combined_csv_filename):
            df.to_csv(combined_csv_filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(combined_csv_filename, mode='w', header=True, index=False, encoding='utf-8-sig')

        # Clear lists for the next playlist
        titles.clear()
        artists.clear()
        years.clear()
        albums.clear()
        duration.clear()
        genres.clear()
        popularity.clear()
        audio_features_data.clear()

    print(f'Total Playlist Items Requests: {playlist_items_requests}')
    print(f'Total Audio Features Requests: {audio_features_requests}')
    print(f'Total Artist-Genre Requests: {artist_requests}')

if __name__ == '__main__':
    main()
