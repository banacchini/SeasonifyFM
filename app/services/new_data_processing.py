import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import datetime

def get_season(date):
    if date.month in [12, 1, 2]:
        return 'Winter'
    elif date.month in [3, 4, 5]:
        return 'Spring'
    elif date.month in [6, 7, 8]:
        return 'Summer'
    elif date.month in [9, 10, 11]:
        return 'Fall'
    return None

def load_and_preprocess(tracks):
    track_data = pd.DataFrame(tracks)

    track_data['artist'] = track_data['artist'].apply(lambda x: x['#text'] if isinstance(x, dict) else x)
    track_data['date'] = track_data['date'].apply(lambda x: int(x['uts']) if isinstance(x, dict) else None)
    track_data['date'] = pd.to_datetime(track_data['date'], unit='s', errors='coerce')
    track_data['month'] = track_data['date'].dt.month
    track_data['season'] = track_data['date'].apply(get_season)
    return track_data

def get_seasonal_artists(tracks):
    track_data = load_and_preprocess(tracks)

    artist_seasonal_streams = track_data.groupby(['artist', 'season']).size().reset_index(name='stream_count')
    total_streams_per_artist = track_data.groupby('artist').size().reset_index(name='total_stream_count')
    total_streams_per_artist = total_streams_per_artist[total_streams_per_artist['total_stream_count'] > 100]
    artist_seasonal_streams = artist_seasonal_streams.merge(total_streams_per_artist, on='artist')
    artist_seasonal_streams['stream_percentage'] = (artist_seasonal_streams['stream_count'] / artist_seasonal_streams['total_stream_count']) * 100
    seasonal_artists = artist_seasonal_streams[artist_seasonal_streams['stream_percentage'] > 50]
    seasonal_artists = seasonal_artists.sort_values(by='stream_percentage', ascending=False)

    season_palette = {
        'Winter': '#1f77b4',
        'Spring': '#2ca02c',
        'Summer': '#ff7f0e',
        'Fall': '#d62728'
    }

    plt.figure(figsize=(14, 10))
    sns.barplot(x='stream_percentage', y='artist', hue='season', data=seasonal_artists, palette=season_palette)
    plt.title('Seasonal Stream Percentage for Artists')
    plt.xlabel('Percentage of streams')
    plt.ylabel('Artist')
    plt.legend(title='Season')
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return img

def get_artist_streams(tracks, artist):
    track_data = load_and_preprocess(tracks)

    artist_data = track_data[track_data['artist'] == artist]
    artist_monthly_streams = artist_data.groupby('month').size().reset_index(name='stream_count')
    total_monthly_streams = track_data.groupby('month').size().reset_index(name='total_stream_count')
    artist_monthly_streams = artist_monthly_streams.merge(total_monthly_streams, on='month')
    artist_monthly_streams['stream_percentage'] = (artist_monthly_streams['stream_count'] / artist_monthly_streams['total_stream_count']) * 100

    plt.figure(figsize=(12, 8))
    sns.barplot(x='month', y='stream_percentage', data=artist_monthly_streams, palette='viridis')
    plt.title(f'Monthly Stream Percentage for {artist}')
    plt.xlabel('Month')
    plt.ylabel('Percentage of streams')
    plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return img

def create_seasonal_spotify_playlists(tracks):
    # Placeholder for Spotify playlist creation logic
    # This function will be implemented later
    pass