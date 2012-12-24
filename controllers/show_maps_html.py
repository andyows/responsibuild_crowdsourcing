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
from controllers.show_error_html import show_error_html
from controllers.datastore_results import datastore_results



def show_maps_html(self):
    logging.debug("show_maps_html")
    login_check = check_login(self)
    if login_check:
        #try:
        path = os.path.join(os.path.dirname(__file__))
        path_length = path.__len__()
        final_path = path[0:path_length-11] + 'views/htmls/main_maps_html.html'
        
        logging.debug("path = " + path)
        logging.debug("final_path = " + final_path)
        logged_in = check_login(self)
            
        results, results_exist = datastore_results("Organization", filters = None, inequality_filters = None, order = None, fetch_total = 1000, offset = 0, mem_key = None)
        
        data = {
            "logged_in": logged_in,
            "title_kind": "Maps",
            "organization_results": results,
        }
        
        self.response.out.write(template.render(final_path, data))         
        #except:
            #logging.debug("exception")
            #show_error_html(self, "template error")
    else:
        self.redirect('/?' + urllib.urlencode({'member_login': True}))
        
        