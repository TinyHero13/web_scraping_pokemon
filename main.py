from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

pokemon_name = []
all_pokemon = 'https://serebii.net/pokedex-sv/'
result = requests.get(all_pokemon)
soup = bs(result.content, 'lxml')

tables=soup.find_all('table')
second_table = tables[1]

options = second_table.find_all('option')
pokemon_names = [option.get_text(strip=True) for option in options]

pokemon_list = []
for option in options:
    text = option.get_text(strip=True)
    if(option['value'] != '#'):
        number, name = text.split(' ', 1) 
        pokemon_list.append((number, name))

for number, name in pokemon_list:
    pokemon_website = f'https://serebii.net/pokedex-sv/{name.lstrip().lower()}/'
    result = requests.get(pokemon_website)
    content = result.text
    soup = bs(content, 'lxml')
        
    content = soup.find_all('table', class_='dextable')
    content = content[1].find_all('td', class_='fooinfo')

    name_pokemon = []
    name_pokemon.append(content[0].get_text())
    
    print(name_pokemon)
    
    gender = []
    gender.append(content[3].get_text())
    
    content_type = soup.find_all('table', class_='dextable')
    content_type = content_type[1].find_all('td', class_='cen')
    img_tag = content_type[0]
    img_tag = img_tag.find_all('img')

    pokemon_type = []

    for i in img_tag:
        pokemon_type.append(i['alt'].split('-')[0])  
        
    classification = []
    classification.append(content[4].get_text())
    print(classification)
    
    height = content[5].get_text()
    height = height.split('\t')[-1]
        
        
    index_list = range(len(name_pokemon))
    if len(pokemon_type) == 1:
        pokemon_type.append("null")
    dataset_pokemon = pd.DataFrame({
        'Nome': name_pokemon,
        'Genero': gender,
        'Tipo 1': pokemon_type[0],
        'Tipo 2': pokemon_type[1],
        'Altura': height
    }, index=index_list)
    dataset_pokemon
    
