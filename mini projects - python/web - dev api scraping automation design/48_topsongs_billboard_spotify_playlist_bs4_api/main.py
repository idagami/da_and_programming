import os, requests, spotipy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotify_auth_class import SpotifyAuth

date_searched = input(
    "Which week in the history would you like to travel to? Type the date in this format YYYY-MM-DD: "
)  # 2005-09-10

cur_file = os.path.dirname(__file__)
URL = f"https://www.billboard.com/charts/hot-100/{date_searched}/"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

auth = SpotifyAuth()
sp, user_id = auth.get_token_user_id()

response = requests.get(URL, headers=header)
# print(response.status_code)
page = response.text
my_soup = BeautifulSoup(page, "html.parser")

# a_list = my_soup.select(
#     "h3#title-of-a-story.c-title.a-font-basic.u-letter-spacing-0010.u-max-width-397.lrv-u-font-size-16.lrv-u-font-size-14@mobile-max.u-line-height-22px.u-word-spacing-0063.u-line-height-normal@mobile-max.a-truncate-elipsis-2line.lrv-u-margin-b-025.lrv-u-margin-b-00@mobile-max"
# )
# I was trying to copy the entire long CSS class string from the HTML. That doesn’t work reliably. No need to match all the classes – just picked one stable attribute
# (like the id or a simple class).

songs_list = my_soup.select(
    "li.o-chart-results-list__item"
)  # Avoids scraping random h3 elements in the sidebar. So we limited search to specific page elements containing the chart itself

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"Top songs of {date_searched}",
    public=False,
    collaborative=False,
    description=f"Top songs / week of {date_searched}",
)
playlist_id = playlist["id"]

# # alternative for below first part:
# song_names_spans = my_soup.select("li ul li h3")
# song_names = [song.getText().strip() for song in song_names_spans]
# print(song_names)
for song in songs_list:
    title_tag = song.find("h3", id="title-of-a-story")
    artist_tag = song.find("span", class_="c-label")
    if title_tag and artist_tag:
        title = title_tag.get_text(strip=True)
        artist = artist_tag.get_text(strip=True)
        search_query = f"track:{title} artist:{artist}"
        results = sp.search(q=search_query, type="track", limit=1)
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            sp.playlist_add_items(playlist_id, [track_uri])
        # else:
        #     print(f"No result for: {title} — {artist}")
        print(f"{artist} - {title}")
