import requests
from bs4 import BeautifulSoup
import json

def clean_spaces(value):
    return ' '.join(value.split())

nos_url = 'https://cinemas.nos.pt'
response = requests.get(nos_url)
# Needs to return: <Response [200]>

soup = BeautifulSoup(response.content, 'html.parser')

# Get all movies
dropdown_movies = soup.find('article', class_='button is-hidden')
movies_a = dropdown_movies.find_all('a', class_='list-item')


movies = [{'Nome': item.text, 'Link Filme': nos_url + item['href']} for item in movies_a]

# Get movie details
for m in movies:
    mresponse = requests.get(m['Link Filme'])
    msoup = BeautifulSoup(mresponse.content, 'html.parser')

    # Get description
    description = msoup.find('section', class_='description').find_all('p')

    for item in description:
        name = item.b.text[:-1]
        
        if name == 'Data de estreia:':
            value = item.span.text
        else:
            item.b.extract()
            value = item.text

        m[name] = clean_spaces(value)
    
    # Get sinopse
    sinopse = msoup.find('section', class_='sinopse').find('div', id='ctl00_PlaceHolderMain_tfSinopse__ControlWrapper_RichHtmlField').text
    m['Sinopse'] = sinopse

    # Get Cinema, Room and Times
    tables = msoup.find_all('section', class_='table')
    datelist = msoup.find('select', class_='day--select').find_all('option')

    if len(tables) - 1 != len(datelist):
        print("Length mismatch in Times/Dates of Exhibitions")
        continue

    cinemas = {}
    for count, t in enumerate(tables):
        if count == len(tables) - 1:
            continue

        date = datelist[count].text

        lines = t.find_all('article', class_='line')
        for l in lines:
            cine = clean_spaces(l.find('div', class_='cinema').text)
            
            room = clean_spaces(l.find('div', class_='room').text)
            if cine not in cinemas:
                
                #cinemas[cine] = {
                #    'Sala': room,
                #    'Datas': []
                #}
                cinemas[cine] = {}
            cinemas[cine][room] = []

            times = l.find('div', class_='hours').find_all('a')
            hours = []
            for time in times:

                # There are 2 divs to remove
                time.div.extract()
                time.div.extract()

                tmp = clean_spaces(time.text)
                hours += [{tmp: time['href']}]
            
            cinemas[cine][room] += [{date: hours}]
                
    m['Cinemas'] = cinemas

data = {'Cinemas NOS': movies}
with open('movies_pt.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)