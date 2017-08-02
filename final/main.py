#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.api import users
from models import Fridge
import webapp2
import jinja2
import os
import urllib
import urllib2
import json


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# for main.html
class MainHandler(webapp2.RequestHandler):
    def get(self):
        food_list = self.request.get('ingredient').split(', ')
        user = users.get_current_user()
        food_query = Fridge.query(Fridge.user_id == user.user_id())
        user_fridge = food_query.get()
        if user_fridge == None:
            user_fridge = Fridge(user_id = user.user_id())
        if len(food_list) != 0:
            for item in food_list:
                user_fridge.foodList.append(item)
            user_fridge.put()
        render_dict = {}

        render_dict['fridge_items'] = user_fridge.foodList
        my_template = jinja_environment.get_template('templates/main.html')
        self.response.write(my_template.render(render_dict))

#for aboutUs.html
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        my_template = jinja_environment.get_template('templates/aboutUs.html')
        self.response.write(my_template.render())


#for restaurants.html
class RestaurantHandler(webapp2.RequestHandler):
    def get(self):
        my_template = jinja_environment.get_template('templates/restaurants.html')
        self.response.write(my_template.render())

#for searchResults.html
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        my_template = jinja_environment.get_template('templates/searchResults.html')
        ingredient = self.request.get("search")
        base_url = 'http://www.recipepuppy.com/api/?'
        url_params = {'i' : ingredient}
        request_url = base_url + urllib.urlencode(url_params)
        recipe_response = urllib2.urlopen(request_url)
        recipe_json = recipe_response.read()
        recipe_data = json.loads(recipe_json)
        title_list = []
        ingr_list = []
        link_list = []
        for i in recipe_data['results']:
            title_list.append(i['title'])
            ingr_list.append(i['ingredients'])
            link_list.append(i['href'])
        lenNum = len(title_list)
        render_data = { 'title': title_list,
            'ingredients' : ingr_list,
            'link' : link_list,
            'num' : lenNum
        }
        self.response.write(my_template.render(render_data))
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))
        self.response.write('<html><body>%s</body></html>' % greeting)

class FridgeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('fridge works!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/about-us', AboutHandler),
    ('/restaurants', RestaurantHandler),
    ('/login', LoginHandler),
    ('/fridge', FridgeHandler)

], debug=True)
