from jinja2 import Environment, FileSystemLoader
import os
import json

def convert_snakecase(value):
    return value.replace(' ', '_').lower()

def map_exists(trek):
	filename = "maps/" + convert_snakecase(trek) + ".html"
	return os.path.exists(filename)

def get_images(trek):
	directory = "images/" + convert_snakecase(trek)
	images = [image for image in os.listdir(directory) if not image.startswith("thumbnail")]
	return sorted(images, key=lambda x: int(os.path.splitext(x)[0]))
 
treks_file = "treks.json"

with open(treks_file, 'r') as file:
    treks = json.load(file)


root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
env.filters['convert_snakecase'] = convert_snakecase
template = env.get_template('index.html')



# treks    = [
# 				{
# 			 		"name": "Extended Ciro Trail",
# 			 		"location": "Sarajevo, BiH -> Dubrovnik, HR",
# 			 		"stats": "196mi, 14,761ft+"
# 				},
# 				{
# 			 		"name": "Bariloche 4 Refugios",
# 			 		"location": "Bariloche, AR",
# 			 		"stats": "27.28mi, 11,982ft+"
# 				},
# 				{
# 			 		"name": "Eurovelo 1 PT South",
# 			 		"location": "Setubal -> Lagos, PT",
# 			 		"stats": "208.7mi, 14,443ft+"
# 				},
# 				{
# 			 		"name": "Bobotov Kuk",
# 			 		"location": "RT <-> Žabljak, MNE",
# 			 		"stats": "16.23mi, 5194ft+"
# 				},
# 				{
# 			 		"name": "Maja Jezerce",
# 			 		"location": "RT <-> Žabljak, MNE",
# 			 		"stats": "28.72mi, 6827ft+"
# 				},
# 				{
# 			 		"name": "GR20 Corsica",
# 			 		"location": "Corsica",
# 			 		"stats": "78mi, 30992ft+"
# 				},
# 				{
# 			 		"name": "Walkers Haute Route",
# 			 		"location": "Le Chable -> Zermatt, CH",
# 			 		"stats": "90mi, 31,167ft+"
# 				},
# 				{
# 			 		"name": "Camino de Santiago Portuguese Way",
# 			 		"location": "Porto, PT -> Santiago de Compostela, ES",
# 			 		"stats": "160.52mi, 13,957ft+"
# 				},
# 				{
# 			 		"name": "West Highland Way",
# 			 		"location": "Milngavie -> Fort William, SCT",
# 			 		"stats": "100.36mi, 13,359ft+"
# 				},
# 				{
# 			 		"name": "Fishermans Trail",
# 			 		"location": "Porto Covo -> Arrifana, PT",
# 			 		"stats": "62mi"
# 				},
# 				{
# 			 		"name": "Tour du Mont Blanc",
# 			 		"location": "RT <-> Chamonix, FR",
# 			 		"stats": "103mi, 32,700ft+"
# 				},
# 				{
# 			 		"name": "John Muir Trail",
# 			 		"location": "Horseshoe Meadow -> Tuolomne, CA, USA",
# 			 		"stats": "230mi, 47000ft+"
# 				},
# 				{
# 			 		"name": "Rubicon Peak",
# 			 		"location": "RT <-> Rubicon Bay, Lake Tahoe, CA, USA",
# 			 		"stats": ""
# 				},
# 				{
# 			 		"name": "Big Seki Loop",
# 			 		"location": "RT <-> Roads End, CA, USA",
# 			 		"stats": "classic high sierras bushwack detour"
# 				},
# 				{
# 			 		"name": "Grand Canyon of Tuolumne",
# 			 		"location": "White Wolf -> Tuolumne Meadows, CA, USA",
# 			 		"stats": ""
# 				},
# 				{
# 			 		"name": "Four Pass Loop",
# 			 		"location": "RT <-> Aspen, CO, USA",
# 			 		"stats": ""
# 				},
# 				{
# 			 		"name": "Crater Lake Loop",
# 			 		"location": "RT <-> Fort Klamath, OR, USA",
# 			 		"stats": ""
# 				},
# 				{
# 			 		"name": "Yosemite Loop",
# 			 		"location": "Yosemite Valley, CA, USA",
# 			 		"stats": ""
# 				},
# 			]

#render frontpage  
filename = 'index.html'
with open(filename, 'w+') as f:
    f.write(template.render(
        treks = [t["name"] for t in treks]
    ))

#render albums
for trek in treks:
    template = env.get_template('album.html')
    filename = f"albums/{trek['name'].lower().replace(' ', '_')}.html"
    with open(filename, 'w+') as f:
        f.write(template.render(trek=trek, 
        						render_map=map_exists(trek['name']),
        						images=get_images(trek['name'])))