from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from .services.new_data_processing import get_seasonal_artists, get_artist_streams, create_seasonal_spotify_playlists
from .services.new_data_fetching import get_last_n_years

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/fetch_data', methods=['GET', 'POST'])
def fetch_data():
    if request.method == 'POST':
        try:
            user = request.form['username']
            n = int(request.form['years'])
            tracks = get_last_n_years(user, 200, n)
            return redirect(url_for('main.analysis', user=user, years=n))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.home'))
    return render_template('fetch_data.html')

@main.route('/analysis')
def analysis():
    user = request.args.get('user')
    years = request.args.get('years')
    return render_template('analysis.html', user=user, years=years)

@main.route('/seasonal_artists', methods=['POST'])
def seasonal_artists():
    data = request.json
    user = data['user']
    years = int(data['years'])
    tracks = get_last_n_years(user, 200, years)
    img = get_seasonal_artists(tracks)
    return send_file(img, mimetype='image/png')

@main.route('/top_10_artists_monthly_streams', methods=['POST'])
def top_10_artists_monthly_streams():
    data = request.json
    user = data['user']
    years = int(data['years'])
    tracks = get_last_n_years(user, 200, years)
    img = get_artist_streams(tracks, user)
    return send_file(img, mimetype='image/png')

@main.route('/create_seasonal_playlists', methods=['POST'])
def create_seasonal_playlists():
    data = request.json
    user = data['user']
    years = int(data['years'])
    tracks = get_last_n_years(user, 200, years)
    result = create_seasonal_spotify_playlists(tracks)
    return jsonify(result)