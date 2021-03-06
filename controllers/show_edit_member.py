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



def show_edit_member(self):
    logging.debug("show_index_html")
    if check_login(self):
        #try:
        session = get_current_session()
        email = session['email']
        
        old_email = None
        old_first_name = None
        old_last_name = None
        old_twitter = None
        old_orgs = None
        old_orgs_list = None
        old_anything_else = None
        old_location = None
        old_rep_points = None
        old_city = None
        old_state = None
        old_country = None
        
        
        filters = {
            "email": email,
        }
        results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
        
        if not results_exist:
            return False
            
        for result in results:
            old_email = result.email
            old_first_name = result.first_name
            old_last_name = result.last_name
            old_twitter = result.twitter
            old_orgs = result.orgs
            old_orgs_list = result.orgs_list
            old_anything_else = result.anything_else
            old_location = result.location
            old_rep_points = result.rep_points
            try:
                old_city = result.city
                old_state = result.state
                old_country = result.country
            except:
                pass
            
        
            
            
        path = os.path.join(os.path.dirname(__file__))
        path_length = path.__len__()
        final_path = path[0:path_length-11] + 'views/htmls/member_info_form.html'
        #print final_path
        
        
        logging.debug("path = " + path)
        logging.debug("final_path = " + final_path)

        logged_in = check_login(self)
        data = {
            "logged_in": logged_in,
            "title_kind": "Edit Member Info",
            "old_email": old_email,
            "old_first_name": old_first_name,
            "old_last_name": old_last_name,
            "old_twitter": old_twitter,
            "old_orgs": old_orgs,
            "old_orgs_list": old_orgs_list,
            "old_anything_else": old_anything_else,
            "old_location": old_location,
            "old_rep_points": old_rep_points,
            "old_city": old_city,
            "old_state": old_state,
            "old_country": old_country,
        }
            
            
        self.response.out.write(template.render(final_path, data))         
        #except:
            #logging.debug("exception")
        #show_error_html(self, "template error")
    else:
        self.redirect("/")