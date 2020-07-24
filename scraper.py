import requests
#import urllib.request
#import time
from bs4 import BeautifulSoup

nos_url = 'https://cinemas.nos.pt'
response = requests.get(nos_url)

print(response)

soup = BeautifulSoup(response.content, 'html.parser')

dropdown_movies = soup.find('article', class_='button is-hidden')

movies_a = dropdown_movies.find_all('a', class_='list-item')


movies = []
mid = 0
for item in movies_a:
    movie = {
        'id': mid,
        'title': item.text,
        'url': nos_url + item['href']
    }
    movies += [movie]
    mid += 1

print(movies)

