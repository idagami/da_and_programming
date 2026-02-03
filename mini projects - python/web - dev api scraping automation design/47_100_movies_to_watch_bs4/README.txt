scraping a list of top movies from Empire Online and save them locally as a text file.

Core Features:
Web Scraping:
Uses requests to fetch the HTML of a specific archived page:
https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/
Parses the page with BeautifulSoup using the "html.parser".

Data Extraction:
Selects all movie titles using the CSS selector: h3.title.
Stores them in a list in original order from #1 to #100 (or reverse if needed).

Data Processing:
Reverses the scraped list so that the top-ranked movie comes first.
Converts the list to a newline-separated string suitable for text files.

Output:
Saves the list to a local file: movies_to_watch.txt
File contains one movie title per line.

Workflow:
Fetch HTML from the archived Empire page.
Parse HTML with BeautifulSoup.
Extract all <h3 class="title"> tags.
Reverse list order to have rank #1 first.
Save the list to a .txt file in the current directory.

Notes / Tips:
The script uses a web archive link, so it’s stable and won’t break if the live site changes.