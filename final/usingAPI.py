import urllib
import urllib2
import json

listFood = raw_input("list your food: ")

base_url = 'http://www.recipepuppy.com/api/?'
url_params = { 'i': listFood}
request_url = base_url + urllib.urlencode(url_params)
print request_url
recipe_response = urllib2.urlopen(request_url)
recipe_json = recipe_response.read()
print recipe_json
recipe_data = json.loads(recipe_json)
recipe_title = recipe_data['results'][0]['title']
print recipe_title
title_list = []
ingr_list = []
link_list = []
for i in recipe_data['results']:
    title_list.append(i['title'])
    ingr_list.append(i['ingredients'])
    link_list.append(i['href'])

print title_list
print ingr_list
print link_list
