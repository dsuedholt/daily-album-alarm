Quick and simple Python script that will get the next album from a project on  [One Album A Day](https://1001albumsgenerator.com/) and populate a Spotify playlist with it. Github Actions are set up to run it once a day.

Useful to me because I have my alarm set to that playlist, and this automates populating it with the next album.

Should you want to do the same or find this useful for any other reason, here's some quick documentation.

### Setup

The script expects the following environment variables to be set:
- `ALBUM_PROJECT_ID`: The name of your project on  [One Album A Day](https://1001albumsgenerator.com/)
- `SPOTIFY_PLAYLIST_ID`: The Spotify ID (not URI) of the playlist that's being updated

The script uses [spotipy](https://github.com/spotipy-dev/spotipy) to call the Spotify API. Spotipy requires the following environment variables:
- `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`: App credentials for the [Spotify Developer API](https://developer.spotify.com/documentation/web-api)
- `SPOTIPY_REDIRECT_URI`: http://localhost:8888/, used for obtaining an authenticated access token. Should be the same as in the Spotify API App.

Set up these variables and run 

```python
pip install -r requirements.txt
python main.py --authenticate
```

When running this for the first time, this will open up a webpage asking you to log into Spotify and approve access for the application. Once successful, it will output a b64-encoded string containing an authenticated access token and a refresh token. Save this string in an environment variable called `SPOTIPY_CACHE`.

Now simply running `python main.py` will pull the current album and update your playlist. To run this daily using Github Actions, save the variables as repository secrets.