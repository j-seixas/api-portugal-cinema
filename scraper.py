import requests
#import urllib.request
#import time
from bs4 import BeautifulSoup

nos_url = 'https://cinemas.nos.pt'
response = requests.get(nos_url)

print(response)

soup = BeautifulSoup(response.content, 'html.parser')

dropdowns = soup.find_all('section', class_='search-bar')
print(dropdowns)