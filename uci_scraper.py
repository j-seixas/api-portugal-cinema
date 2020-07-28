import requests
from bs4 import BeautifulSoup
import json

def clean_spaces(value):
    return ' '.join(value.split())

uci_url = 'https://ucicinemas.pt'
response = requests.get(uci_url + '/Filmes/Cartaz')
# Needs to return: <Response [200]>

soup = BeautifulSoup(response.content, 'html.parser')

# Get all movies
movies_posters = soup.find('article', id='cartelera')
movies_h3 = movies_posters.find_all('h3')

movies = [{'Nome': clean_spaces(item.a.text), 'Link Filme': uci_url + item.a['href']} for item in movies_h3]

# Get movie details
for m in movies:
    # Get details + times in UCI Arrabida
    mresponse = requests.get(m['Link Filme'] + '/arrabida-20')
    msoup = BeautifulSoup(mresponse.content, 'html.parser')

    details_p = msoup.find('article', class_='descripcion d2 cuadros_ficha').find('div', class_='datos').div.find_all('p')
    
    for i in range(len(details_p)):
        if details_p[i].span.text == 'Data de estreia:':
            details_name = details_p[i].span.text[:-1]
            details_p[i].span.extract()
            value_tmp = clean_spaces(details_p[i].text).split('-')
            value = value_tmp[2] + '-' + value_tmp[1] + '-' + value_tmp[0]
        
        elif details_p[i].span.text == 'Duração:':
            details_name = details_p[i].span.text[:-1]
            details_p[i].span.extract()
            value = clean_spaces(details_p[i].text)
            # remove 'min'
            value = clean_spaces(value[:-3])
        else:
            if details_p[i].span.text == 'Título original:':
                details_name = 'Título Original'
            elif details_p[i].span.text == 'Realização:':
                details_name = 'Realizador'
            elif details_p[i].span.text == 'Elenco:':
                details_name = 'Actores'
            elif details_p[i].span.text == 'Classificação':
                details_name = details_p[i].span.text
            else:
                details_name = details_p[i].span.text[:-1]
            
            if details_name == 'Género' or details_name == 'País':
                details_p[i].span.extract()
                value = ', '.join(clean_spaces(details_p[i].text).split(' - '))
            else:
                details_p[i].span.extract()
                value = clean_spaces(details_p[i].text)
        
        m[details_name] = value
    
    


print(json.dumps(movies, indent=4, ensure_ascii=False))


"""
dropdown_movies = soup.find('article', class_='button is-hidden')
movies_a = dropdown_movies.find_all('a', class_='list-item')


movies = [{'Nome': item.text, 'Link Filme': uci_url + item['href']} for item in movies_a]

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
                cinemas[cine] = {}
            if room not in cinemas[cine]:
                cinemas[cine][room] = {}
            if date not in cinemas[cine][room]:
                cinemas[cine][room][date] = {}

            times = l.find('div', class_='hours').find_all('a')
            for time in times:

                # There are 2 divs to remove
                time.div.extract()
                time.div.extract()

                tmp = clean_spaces(time.text)
                cinemas[cine][room][date][tmp] = time['href']
                
    m['Cinemas'] = cinemas

with open('movies_pt.json') as json_file:
    data = json.load(json_file)    
    data['UCICinemas'] = movies
with open('movies_pt.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

"""