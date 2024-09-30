from jinja2 import Environment, FileSystemLoader
import os
import json
import requests
from lxml import objectify, etree
import re

# ----------------------------------- Helper funcs ----------------------------------- #

# images are served via cloudfront 
CLOUD_FRONT_BASE_URL = "https://d2j97febc1ug11.cloudfront.net"

def convert_snakecase(value):
    return value.replace(' ', '_').lower()

# check if the trek has a map (some don't)
def map_exists(trek):
	return "map" in trek.keys()

# images are named with an integer sequence, returns this number
def get_image_num(path):
    return int(path.split('/')[-1].split('.')[0])

# return list of all s3 image urls for a trek
def get_image_urls(trek):
    res = requests.get(f"{CLOUD_FRONT_BASE_URL}?prefix=images/{trek['name'].lower().replace(' ', '_')}")
    root = objectify.fromstring(res.text.encode())
    image_urls = []
    for elem in root.Contents:
        if "thumbnail" not in str(elem.Key) and not str(elem.Key).endswith("/"):
            image_urls.append(CLOUD_FRONT_BASE_URL + "/" + elem.Key)
    return sorted(image_urls, key=get_image_num)

# # ---------------------Script to generate static site html -------------------------- #

treks_file = "treks.json"

with open(treks_file, 'r') as file:
    treks = json.load(file)

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
env.filters['convert_snakecase'] = convert_snakecase
template = env.get_template('index.html')

# Step #1: Render front page
filename = 'index.html'
with open(filename, 'w+') as f:
    f.write(template.render(
        treks = [t["name"] for t in treks]
    ))

# Step #2: Render map pages
for trek in treks:
    if map_exists(trek):
        template = env.get_template('map.html')
        filename = f"maps/{trek['name'].lower().replace(' ', '_')}.html"
        with open(filename, 'w+') as f:
            f.write(template.render(trek=trek))

# Step #3: Render album pages
for trek in treks:
    template = env.get_template('album.html')
    filename = f"albums/{trek['name'].lower().replace(' ', '_')}.html"
    with open(filename, 'w+') as f:
        f.write(template.render(trek=trek, 
        						render_map=map_exists(trek),
        						image_urls=get_image_urls(trek)
        ))

# Done! 