from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from gaesessions import get_current_session
import logging
import model
import urllib
from google.appengine.ext import db
import random
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from os import environ
from google.appengine.api import memcache
from google.appengine.api import images
from google.appengine.api import oauth
import Cookie
import hashlib
from models import model
from controllers.datastore_results import datastore_results
from controllers.check_login import check_login
from controllers.show_error_html import show_error_html
from controllers.put_tag import put_tag
from controllers.get_date_time import get_date_time
from controllers.get_hash import get_hash
from controllers.datastore_results import datastore_results
import random

def put_post_flag(self):
    logging.debug("put_post_flag")
    if check_login(self):
        
        continue_boolean = False
        email = ""
        #try:
        session = get_current_session()
        email = session['email']
        continue_boolean = True
        #except:
            #logging.debug("gaesessions exception, do not continue")
            #continue_boolean = False
            #show_error_html(self, "session error")
            
            
        if continue_boolean:
            post_id = self.request.get("post_id")

            filters = {
                "post_id": post_id,
            }
            results, results_exist = datastore_results("Post", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
            key = None
            points = 0
            for result in results:
                key = result.key()
                post_id = result.post_id
                email = result.email
                title = result.title
                tags = result.tags
                entry = result.entry
                tags_list = result.tags_list
                timestamp = result.timestamp
                points = result.points
                user_email = session['email']
                
                p = model.FlagPost(post_id = post_id, email = email, title = title, tags = tags, entry = entry, tags_list = tags_list, timestamp = timestamp, points=points, added_by = user_email)
                p.put()
                db.delete(key)
            return post_id
            
    else:
        self.redirect("/")