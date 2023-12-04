from flask import Flask, jsonify, render_template
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

with open('deskripsi_makanan.json', 'r') as file:
    data = json.load(file)

def scrapHome():
    url = 'https://www.masakapahariini.com/resep/'
    html = requests.get(url)
    s = BeautifulSoup(html.content, 'html.parser')
    card_titles = s.find_all('a', class_='stretched-link')
    thumbnails = s.find_all('div', class_='thumbnail')

    img_src_list = [img['src'] for thumbnail in thumbnails for img in thumbnail.find_all('img') if 'src' in img.attrs and not img['src'].startswith('data:image/svg+xml')]
    href_values = [a['href'] for a in card_titles]
    title_food = [a.text for a in card_titles]
    
    resultHome = [{'title': title,
                'href': href,
                'thumbnail': thumbnail,
                } for title, href, thumbnail in zip(title_food, href_values, img_src_list)]

    return resultHome

@app.route("/index")
def home():
    scraped_data = scrapHome()
    return render_template("index.html", data=scraped_data)

if __name__== "__main__":
    app.run(debug=True)