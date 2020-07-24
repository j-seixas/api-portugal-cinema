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
        'Title': item.text,
        'url': nos_url + item['href']
    }
    movies += [movie]

#print(movies)

for m in movies:
    mresponse = requests.get(m['url'])
    msoup = BeautifulSoup(mresponse.content, 'html.parser')

    # Get description
    description = msoup.find('section', class_='description').find_all('p')

    for item in description:
        name = item.b.text[:-1]
        
        if name == 'Data de estreia:':
            value = ' '.join(item.span.text.split())
        else:
            item.b.extract()
            value = ' '.join(item.text.split())

        m[name] = ' '.join(value.split())
    
    # Get sinopse
    sinopse = msoup.find('section', class_='sinopse').find('div', id='ctl00_PlaceHolderMain_tfSinopse__ControlWrapper_RichHtmlField').text
    m['Sinopse'] = sinopse

    # Get Cinema, Room and Times
    tables = msoup.find_all('section', class_='table')

    #size = len(tables[0].find_all('article', class_='line'))
    cinemas = {}
    #for i in range(size):
    for count, t in enumerate(tables):
        if count == len(tables) - 1:
            continue
        #entry = t.select('article.line:nth-child({})'.format(i))
        #print(dir(t))
        #print(msoup)
        datelist = msoup.find('select', class_='day--select')
        #print(datelist)
        datelist = datelist.find_all('option')

        date = datelist[count].text
        lines = t.find_all('article', class_='line')
        for l in lines:
            cine = l.find('div', class_='cinema').text
            
            if cine not in cinemas:
                room = l.find('div', class_='room').text
                
                cinemas[cine] = {
                    'Room': room,
                    'Dates': []
                }


            times = l.find('div', class_='hours').find_all('a')
            hours = []
            for time in times:
                hours += [{time.text: time['href']}]
            
            #if date not in cinemas[cine]['Dates']:
            cinemas[cine]['Dates'] += [{date: hours}]
                
            #cinemas[cine]['Dates'][date] = hours
            #times = l.find('div', class_:'cinema')
       # name = 
    m['Cinemas'] = cinemas

print(movies)

data = {'NOS Cinemas': movies}
with open('movies.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)