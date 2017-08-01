from google.appengine.ext import ndb

class Fridge(ndb.Model):
    user_id = ndb.StringProperty()
    foodList = ndb.StringProperty(repeated = True)
