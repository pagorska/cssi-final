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
        remove_item = self.request.get("remove")
        user = users.get_current_user()
        if user is None:
            emptyList = ['Please sign in to save your food items to your fridge']
            render_dict = {
                'fridge_items' : emptyList,
                'logon' : 'Login'
            }
        else:
            food_query = Fridge.query(Fridge.user_id == user.user_id())
            user_fridge = food_query.get()
            removeItem = ''
            removeItem = self.request.get('remove')
            if removeItem != '':
                for item in user_fridge.foodList:
                    if item == removeItem:
                        user_fridge.foodList.remove(removeItem)
            if user_fridge == None:
                user_fridge = Fridge(user_id = user.user_id())
            if len(food_list) != 0:
                for item in food_list:
                    if item != '':
                        count=0
                        for itemF in user_fridge.foodList:
                            if item == itemF:
                                count +=1
                        if count == 0:
                            user_fridge.foodList.append(item)
                user_fridge.put()
            render_dict = {
                'fridge_items' : user_fridge.foodList,
                'logon' : 'Logout'
            }


        my_template = jinja_environment.get_template('templates/main.html')
        self.response.write(my_template.render(render_dict))

#for aboutUs.html
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            render_dict = {
                'logon' : 'Login'
            }
        else:
           render_dict = {
                 'logon' : 'Logout'
            }
        my_template = jinja_environment.get_template('templates/aboutUs.html')
        self.response.write(my_template.render(render_dict))


#for restaurants.html
class RestaurantHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            render_dict = {
                'logon' : 'Login'
            }
        else:
           render_dict = {
                 'logon' : 'Logout'
            }
        my_template = jinja_environment.get_template('templates/restaurants.html')
        self.response.write(my_template.render(render_dict))

#for searchResults.html
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            my_template = jinja_environment.get_template('templates/searchFailed.html')
            render_dict = {
                'loginOrFail' : "Please log in to continue",
                'logon' : 'Login'
            }
            self.response.write(my_template.render(render_dict))
        else:
            food_query = Fridge.query(Fridge.user_id == user.user_id())
            user_fridge = food_query.get()
            ingredients = ",".join(user_fridge.foodList)
            base_url = 'http://www.recipepuppy.com/api/?'
            url_params = {'i' : ingredients}
            request_url = base_url + urllib.urlencode(url_params)
            try:
                my_template = jinja_environment.get_template('templates/searchResults.html')
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
                    'num' : lenNum,
                    'logon' : 'Logout'
                }
                self.response.write(my_template.render(render_data))
            except urllib2.HTTPError, err:
                my_template = jinja_environment.get_template('templates/searchFailed.html')
                render_dict = {
                    'loginOrFail' : 'Unable to fetch results',
                    'logon' : 'Logout'
                }
                self.response.write(my_template.render(render_dict))


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
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/about-us', AboutHandler),
    ('/restaurants', RestaurantHandler),
    ('/login', LoginHandler)

], debug=True)
