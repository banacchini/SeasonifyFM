from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
import os
from .services.data_processing import get_seasonal_artists, get_artist_streams
from .services.data_fetching import get_last_n_years, save_tracks_to_file, set_fetch_status, get_fetch_status

main = Blueprint('main', __name__)

DATA_FILE_PATH = os.path.join('data', 'streams_history.json')


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/fetch_data', methods=['GET', 'POST'])
def fetch_data():
    if request.method == 'POST':
        if get_fetch_status():
            flash('Data fetching is already in progress. Please wait until it completes.', 'warning')
            return redirect(url_for('main.home'))

        set_fetch_status(True)
        try:
            user = request.form['username']
            n = int(request.form['years'])
            tracks = get_last_n_years(user, 200, n)
            save_tracks_to_file(tracks, DATA_FILE_PATH)
            flash('Data fetched successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            set_fetch_status(False)
        return redirect(url_for('main.home'))
    return render_template('fetch_data.html')


@main.route('/seasonal_artists')
def seasonal_artists():
    if not os.path.exists(DATA_FILE_PATH):
        flash('Data file not found. Please fetch the data first.', 'error')
        return redirect(url_for('main.fetch_data'))

    img = get_seasonal_artists(DATA_FILE_PATH)
    return send_file(img, mimetype='image/png')


@main.route('/artist_streams', methods=['GET', 'POST'])
def artist_streams():
    if request.method == 'POST':
        artist = request.form['artist']
        if not os.path.exists(DATA_FILE_PATH):
            flash('Data file not found. Please fetch the data first.', 'error')
            return redirect(url_for('main.fetch_data'))
        img = get_artist_streams(DATA_FILE_PATH, artist)
        return send_file(img, mimetype='image/png')

    return render_template('artist_streams.html')