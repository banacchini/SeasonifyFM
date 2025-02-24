# Seasonal Artists Analysis

Have you ever wondered how do your seasons sound like? Discover the patterns behind your listening habits and see who do you listen to in each of the seasons! Fetch your (or anyones!) streaming history from Last.fm and look at the cool charts!

## Features

- Fetch and analyze Last.fm streaming data based on user input.
- Display seasonal artists chart.
- Display top 10 streamed artists monthly streams chart (to be implemented).
- Create seasonal Spotify playlists (to be implemented).

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/seasonal-artists-analysis.git
    cd seasonal-artists-analysis
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Last.fm API key:
    Create a file named `config.py` in the root directory and add your Last.fm API key:
    ```python
    API_KEY = 'your_last_fm_api_key'
    ```

## Usage

1. Run the Flask application:
    ```bash
    python run.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Enter your Last.fm username and the number of years to analyze, then click "Fetch Data".

4. Explore the data analysis page to view seasonal artists charts, top 10 streamed artists monthly streams, and create seasonal Spotify playlists.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Last.fm API](https://www.last.fm/api)
- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, feel free to reach out to [banacchini](mailto:dominik.czech03@gmail.com).
