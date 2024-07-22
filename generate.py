from jinja2 import Environment, FileSystemLoader
import os
import json

# ----------------------------------- helper funcs ----------------------------------- #
def convert_snakecase(value):
    return value.replace(' ', '_').lower()

def map_exists(trek):
	return "map" in trek.keys()

def get_images(trek):
	directory = "images/" + convert_snakecase(trek)
	images = [image for image in os.listdir(directory) if not image.startswith("thumbnail")]
	return sorted(images, key=lambda x: int(os.path.splitext(x)[0]))

# # ---------------------script to generate static site html -------------------------- #

treks_file = "treks.json"

with open(treks_file, 'r') as file:
    treks = json.load(file)

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
env.filters['convert_snakecase'] = convert_snakecase
template = env.get_template('index.html')

#render frontpage  
filename = 'index.html'
with open(filename, 'w+') as f:
    f.write(template.render(
        treks = [t["name"] for t in treks]
    ))

#render maps
for trek in treks:
    if map_exists(trek):
        template = env.get_template('map.html')
        filename = f"maps/{trek['name'].lower().replace(' ', '_')}.html"
        with open(filename, 'w+') as f:
            f.write(template.render(trek=trek))

#render albums
for trek in treks:
    template = env.get_template('album.html')
    filename = f"albums/{trek['name'].lower().replace(' ', '_')}.html"
    with open(filename, 'w+') as f:
        f.write(template.render(trek=trek, 
        						render_map=map_exists(trek),
        						images=get_images(trek['name'])))