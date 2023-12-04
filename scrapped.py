import requests
from bs4 import BeautifulSoup
import json

url = f'https://www.masakapahariini.com/resep/'

html = requests.get(url)

s = BeautifulSoup(html.content, 'html.parser')

card_titles = s.find_all('a', class_='stretched-link')

href_values = [a['href'] for a in card_titles]


urlEachRecipe = 'https://www.masakapahariini.com/resep/{}'

urlEachRecipe = urlEachRecipe.format(','.join(href_values))

urlEachRecipeList = urlEachRecipe.split(',')

# Deskripsi Resep
for recipeDetails in urlEachRecipeList:
    html = requests.get(recipeDetails)

    newS = BeautifulSoup(html.content, 'html.parser')
    if newS:
        excerpt_element = newS.find(class_='excerpt')
        image = newS.find('img', class_='image')
        steps = newS.find(class_='_recipe-steps')
        if excerpt_element and image and steps:
            food_desc = excerpt_element.text.strip()
            image_food = image['src']
            step = steps.find_all('p')
        else:
            food_desc = ""
            image_food = ""
            step = ""
    else:
        food_desc = ""
        image_food = ""
        step = ""

    steps = []
    for stepRecipe in step:
        steps.append(stepRecipe.text)
    
    ingredients = []

    results = newS.find(class_='_section-title')

    if results:
        h1_element = results.find('h1')
        if h1_element:
            food_title = h1_element.text.strip()
        else:
            food_title = ""
    else:
        food_title = ""
    

    food_desc = {
                    "status": 200,
                    "url": recipeDetails,
                    "data": [
                        {
                            "title": food_title,
                            "author": "Nama Auth",
                            "author_avatar": "auth avatar",
                            "author_profile": "auth profile",
                            "description": food_desc,
                            "image": image_food,
                            "likes": 4,
                            "duration": "15 menit",
                            "portion": "2 porsi",
                            "step":  steps,
                            "ingredients" : "Bahan"
                        }
                    ]
                }          
   
    
    json_data = json.dumps(food_desc, ensure_ascii=False)

    with open('deskripsi_makanan.json', 'a', encoding='utf-8') as json_file:
        json_file.write(json_data + '\n')

with open('deskripsi_makanan.json', 'r', encoding='utf-8') as json_file:
    print(json_file.read())

