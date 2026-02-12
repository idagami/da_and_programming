import os, spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
cur_file = os.path.dirname(__file__)
token_path = os.path.join(cur_file, "token.txt")


class SpotifyAuth:
    def __init__(self):
        self.my_client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.my_client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.my_redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
        self.my_scope = "playlist-modify-private"
        self.sp = None
        self.user_id = None

    def get_token_user_id(self):
        my_auth_manager = SpotifyOAuth(
            client_id=self.my_client_id,
            client_secret=self.my_client_secret,
            redirect_uri=self.my_redirect_uri,
            scope=self.my_scope,
            show_dialog=True,
            cache_path=token_path,
        )
        self.sp = spotipy.Spotify(auth_manager=my_auth_manager)
        self.user_id = self.sp.current_user()["id"]
        return self.sp, self.user_id
