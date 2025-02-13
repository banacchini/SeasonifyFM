import requests
import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import API_KEY

FETCH_STATUS_FILE = os.path.join('data', 'fetch_status.json')

def set_fetch_status(status):
    with open(FETCH_STATUS_FILE, 'w') as f:
        json.dump({'fetch_in_progress': status}, f)

def get_fetch_status():
    if not os.path.exists(FETCH_STATUS_FILE):
        return False
    with open(FETCH_STATUS_FILE, 'r') as f:
        status = json.load(f)
        return status.get('fetch_in_progress', False)

def fetch_page(user, from_timestamp, to_timestamp, limit, page):
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={API_KEY}&limit={limit}&page={page}&from={from_timestamp}&until={to_timestamp}&format=json"
    response = requests.get(url)
    data = response.json()
    if 'recenttracks' not in data or 'track' not in data['recenttracks']:
        print(f"Error fetching data for page {page}: {data}")
        return [], 1
    return data['recenttracks']['track'], int(data['recenttracks']['@attr'].get('totalPages', 1))

def get_last_n_years(user, limit=200, n=1):
    now = datetime.datetime.utcnow()
    n_years_ago = now - datetime.timedelta(days=n*365)
    from_timestamp = int(n_years_ago.timestamp())
    to_timestamp = int(now.timestamp())

    # Fetch the first page to get the total number of pages
    initial_data, total_pages = fetch_page(user, from_timestamp, to_timestamp, limit, 1)
    all_tracks = initial_data

    # Use ThreadPoolExecutor to fetch pages in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_page, user, from_timestamp, to_timestamp, limit, page) for page in range(2, total_pages + 1)]
        for future in as_completed(futures):
            tracks, _ = future.result()
            all_tracks.extend(tracks)

    return all_tracks

def save_tracks_to_file(tracks, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(tracks, f, indent=4)
    print(f"Saved {len(tracks)} tracks to {file_path}")