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


def show_add_post_form(self):
    logging.debug("show_index_html")
    #try:
    path = os.path.join(os.path.dirname(__file__))
    path_length = path.__len__()
    final_path = path[0:path_length-11] + 'views/htmls/add_post.html'
    
    logging.debug("path = " + path)
    logging.debug("final_path = " + final_path)

    logged_in = check_login(self)
    
    
    data = {
        "logged_in": logged_in,
        "title_kind": "What makes a good post"
    }
        
        
    self.response.out.write(template.render(final_path, data))         
    #except:
        #logging.debug("exception")
        #show_error_html(self, "template error")