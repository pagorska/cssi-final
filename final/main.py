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
        my_template = jinja_environment.get_template('templates/main.html')
        self.response.write(my_template.render())

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
        self.response.write(my_template.render())
        self.response.write("search works")
        ingredient = self.request.get("search")
        print 'milk'
        print ingredient
        self.response.write(ingredient)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/search', SearchHandler),
    ('/about-us', AboutHandler),
    ('/restaurants', RestaurantHandler)

], debug=True)

# query.fetch(in)
#
# ingredient = Ingredient(name="milk")
# ingredient = name.put()
