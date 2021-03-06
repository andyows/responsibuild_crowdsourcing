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
from controllers.check_login import check_login
from controllers.datastore_results import datastore_results



def show_add_post_form(self, post_id = None):
    logging.debug("show_index_html")
    if check_login(self):
        #try:
        session = get_current_session()
        email = session['email']
        
        old_entry = None
        old_tags = None
        old_title = None
        old_hash = None
        
        if post_id:
            filters = {
                "email": email,
                "post_id": post_id,
            }
            results, results_exist = datastore_results("Post", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
            
            if not results_exist:
                return False
                
            for result in results:
                old_entry = result.entry
                old_tags = result.tags
                old_title = result.title
                old_hash = result.post_id
            
            
            
        path = os.path.join(os.path.dirname(__file__))
        path_length = path.__len__()
        final_path = path[0:path_length-11] + 'views/htmls/add_post.html'
        #print final_path
        
        
        logging.debug("path = " + path)
        logging.debug("final_path = " + final_path)

        logged_in = check_login(self)
        data = {
            "logged_in": logged_in,
            "title_kind": "What makes a good post",
            "old_entry": old_entry,
            "old_title": old_title,
            "old_tags": old_tags,
            "old_hash": old_hash,
        }
            
            
        self.response.out.write(template.render(final_path, data))         
        #except:
            #logging.debug("exception")
        #show_error_html(self, "template error")
    else:
        self.redirect("/")