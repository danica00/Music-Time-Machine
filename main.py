import os

import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

#####################################################MY SPOTIPY DATA##############################################
CLIENT_ID= f"{os.environ['CLIENT_ID']}"
CLIENT_SECRET =f"{os.environ['CLIENT_SECRET']}"




###################################################BILBOARD SCRAPING##############################################
URL = "https://www.billboard.com/charts/hot-100/"
date =input("Which year do you want to travel to? type the date in this format:YYYY-MM-DD:")
response = requests.get(URL + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names = soup.select(selector="li ul li h3")
songs_list = [song.getText().strip("\t\n") for song in song_names]
print(songs_list)
####################################################SPOTIPY APP SETUP#############################################
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
################################################connection#######################################################

song_uris = []
year = date.split("-")[0]

for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}",type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
