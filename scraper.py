import requests
#import urllib.request
#import time
from bs4 import BeautifulSoup
import json

nos_url = 'https://cinemas.nos.pt'
response = requests.get(nos_url)

#print(response)
# Returns: <Response [200]>

soup = BeautifulSoup(response.content, 'html.parser')

dropdown_movies = soup.find('article', class_='button is-hidden')
movies_a = dropdown_movies.find_all('a', class_='list-item')

movies = []
for item in movies_a:
    movie = {
        'title': item.text,
        'url': nos_url + item['href']
    }
    movies += [movie]

print(movies)

for m in movies:
    mresponse = requests.get(m['url'])
    msoup = BeautifulSoup(mresponse.content, 'html.parser')

    description = msoup.find('section', class_='description').find_all('p')

    for item in description:
        name = item.b.text[:-1]
        
        if name == 'Data de estreia:':
            value = ' '.join(item.span.text.split())
        else:
            item.b.extract()
            value = ' '.join(item.text.split())

        m[name] = ' '.join(value.split())
    
    sinopse = msoup.find('section', class_='sinopse').find('div', id='ctl00_PlaceHolderMain_tfSinopse__ControlWrapper_RichHtmlField').text
    m['Sinopse'] = sinopse

print(movies)

data = {'NOS Cinemas': movies}
with open('movies.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)