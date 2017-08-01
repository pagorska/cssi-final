from google.appengine.ext import ndb
from main import SearchHandler

class Ingredient(ndb.Model):
    name = ndb.StringProperty()
    Ingredient = ndb.StringProperty()
    # expiration

class Fridge(ndb.Model):
    foodList = ndb.KeyProperty(Ingredient, repeated = True)
