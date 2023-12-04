from flask import Flask, jsonify, render_template
import json
import requests
from bs4 import BeautifulSoup

def scrapHome():
    url = 'https://www.masakapahariini.com/resep/'
    html = requests.get(url)
    s = BeautifulSoup(html.content, 'html.parser')
    card_titles = s.find_all('a', class_='stretched-link')
    thumbnails = s.find_all('div', class_='thumbnail')

    img_src_list = [img['src'] for thumbnail in thumbnails for img in thumbnail.find_all('img') if 'src' in img.attrs and not img['src'].startswith('data:image/svg+xml')]

    href_values = [a['href'] for a in card_titles]
    title_food = [a.text for a in card_titles]
    
    result = [{'title': title,
                'href': href,
                'thumbnail': thumbnail,
                } for title, href, thumbnail in zip(title_food, href_values, img_src_list)]

    json_data = json.dumps(result, ensure_ascii=False)

    with open('deskripsi_makanan.json', 'a', encoding='utf-8') as json_file:
        json_file.write(json_data + '\n')



scrapHome()