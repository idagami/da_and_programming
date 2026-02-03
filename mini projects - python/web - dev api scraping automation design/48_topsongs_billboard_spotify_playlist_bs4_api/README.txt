Scrape Billboard Hot 100 for a given date and create a private Spotify playlist with those songs.

Key Steps:
Ask user for a date (YYYY-MM-DD).
Fetch Billboard chart page for that date.
Parse the page with BeautifulSoup, extracting songs from li.o-chart-results-list__item.
Authenticate with Spotify using SpotifyAuth class.
Create a new private playlist in the user’s Spotify account.
Search each song on Spotify (track:{title} artist:{artist}) and add it to the playlist.

Notes:
Handles missing songs gracefully if Spotify search returns no results.
Can be extended for multiple weeks or automated scraping.