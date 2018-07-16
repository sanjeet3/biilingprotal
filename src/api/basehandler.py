'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''

from src.app_configration import config
from src.db import User
import os, json 
import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.api import namespace_manager
import logging
 
SUCCESS='SUCCESS'
ERROR='ERROR'
WARNING='WARNING'
INFO='INFO'
ALL_PERMISSION_BIN = '1111111111111111111111111111111111111111111111111111111111111111'

def json_response(response, data_dict={}, status=SUCCESS, message=''):  
  ''' Response json string '''
    
  response.content_type = 'application/json'
  result = {'status' : status,
            'data': data_dict,
            'message': message}
    
  response.out.write(json.dumps(result))

class SABase(webapp2.RequestHandler):
  '''
     Action support for all requests in app
  '''
  
  def __init__(self, request, response):
    
    self.initialize(request, response)
    self.user = users.get_current_user()
    unauthorize=True
    if self.user and self.user.email() in config['super_admin']:
      unauthorize = False     
    if unauthorize:
      self.request_unauthorize(request)    
    #logging.info(get_integer_from_binary_string(ALL_PERMISSION_BIN))  
    namespace_manager.set_namespace(config.get('namespace'))  
      
  def dispatch(self):
    webapp2.RequestHandler.dispatch(self) 
    
  @webapp2.cached_property
  def get_jinja2_env(self):  
    environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), '..')), extensions=['jinja2.ext.do',],
        autoescape=True)
    return environment    

  @webapp2.cached_property
  def get_context(self):
    return {'logout_url': users.create_logout_url('/'),
            'email': self.user.email(),
            }
    
  def request_unauthorize(self, request):
    self.abort(401)  


class Basehandler(webapp2.RequestHandler):
  '''
     Action support for all requests in app
  '''
  
  def __init__(self, request, response):
    
    self.initialize(request, response)
    self.gmailuser = users.get_current_user()
    unauthorize=True
    if self.gmailuser:
      self.user = User.get_active_user_by_email(self.gmailuser.email())
      if self.user and self.user.system_owner:  
        unauthorize = False   
    if unauthorize:
      self.request_unauthorize(request)  
         
  def dispatch(self):
    webapp2.RequestHandler.dispatch(self) 
    
  @webapp2.cached_property
  def get_jinja2_env(self):  
    environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), '..')), extensions=['jinja2.ext.do',],
        autoescape=True)
    return environment    

  @webapp2.cached_property
  def get_context(self):
    return {'logout_url': users.create_logout_url('/'),
            'email': self.user.email,
            'user': self.user,
            }
    
  def request_unauthorize(self, request):
    self.abort(401)  
