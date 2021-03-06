from models import model
from google.appengine.ext import db


BATCH_SIZE = 200

def update_org(self): 
    query = model.Organization.all()
    to_put = []
    for p in query.fetch(limit=BATCH_SIZE):
        to_put.append(p)

    if to_put:
        db.put(to_put)  
