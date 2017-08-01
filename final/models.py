from google.appengine.ext import ndb
from main import SearchHandler
class Fridge(ndb.Model):
    foodList = ndb.KeyProperty(Food, repeated = True)

class Food(ndb.Model):
    name = ndb.StringProperty()
    # expiration
