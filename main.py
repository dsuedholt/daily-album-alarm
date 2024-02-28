import json
import base64
import argparse
import requests
import os

from spotipy import Spotify, MemoryCacheHandler, CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public"

def get_album_spotify_id(project_id):
    response = requests.get(
        "https://1001albumsgenerator.com/api/v1/projects/" + project_id
    )

    response.raise_for_status()

    album = response.json()["currentAlbum"]

    print("Today's Artist:", album["artist"])
    print("Today's Album:", album["name"])

    return album["spotifyId"]


def main():
    album_spotify_id = get_album_spotify_id(os.environ["ALBUM_PROJECT_ID"])

    cache_handler = MemoryCacheHandler(json.loads(base64.b64decode(os.environ["SPOTIPY_CACHE"]).decode("utf-8")))
    sp = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, cache_handler=cache_handler))

    album_tracks = sp.album_tracks(album_spotify_id)["items"]
    sp.playlist_replace_items(os.environ["SPOTIFY_PLAYLIST_ID"], [track["id"] for track in album_tracks])

    print("Album added to playlist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add today's album to a Spotify playlist"
    )
    parser.add_argument(
        "-a",
        "--authenticate",
        action="store_true",
        help="Authenticate the app with Spotify and print access token as a base64 string",
    )

    args = parser.parse_args()
    if args.authenticate:
        cache_handler = CacheFileHandler()
        auth_manager = SpotifyOAuth(scope=SCOPE, cache_handler=cache_handler)

        # Does nothing if .cache file already exists. Otherwise, opens a browser to authenticate
        auth_manager.get_access_token(as_dict=False)
        
        print(base64.b64encode(json.dumps(cache_handler.get_cached_token()).encode("utf-8")).decode("utf-8"))
        
    else:
        main()
