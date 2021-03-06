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
from controllers.get_hash import get_hash
from controllers.get_date_time import get_date_time


import random

def put_comment(self):
    logging.debug("put_post")
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
        comment = self.request.get("comment")
        post_id = self.request.get("post_id")
        
        if not comment:
            logging.debug("No comment entered")
            return False, post_id
        if continue_boolean:
            ### check db, if not in db put tag
            new_hash = get_hash()
            timestamp = get_date_time()
        
            c = model.Comment(comment = comment, email = email, comment_id = new_hash, post_id = post_id, timestamp = timestamp)
            c.put()
            filters = {
                "email": email,
            }
            results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
            if results_exist:
                for result in results:
                    key = result.key()
                    points = result.rep_points
                    
                    member = model.Member.get(key)
                    member.rep_points = points + 5
                    member.put()
            return True, post_id
                
    else:
        self.redirect("/")