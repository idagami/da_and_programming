import requests, os
from bs4 import BeautifulSoup

cur_file = os.path.dirname(__file__)
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
# print(response.status_code)
page = response.text
my_soup = BeautifulSoup(page, "html.parser")

movies_tags_list = my_soup.select("h3.title")

movies_opposite_list = []
for movie in movies_tags_list:
    movies_opposite_list.append(movie.getText())


movies_list = movies_opposite_list[::-1]
# Alternatively: movies_opposite_list.reverse() (do NOT assign to variable)
print(movies_list)
movies = "\n".join(str(movie) for movie in movies_list)

new_file_path = os.path.join(cur_file, "movies_to_watch.txt")
with open(new_file_path, "w", encoding="utf-8") as file:
    file.write(str(movies))
