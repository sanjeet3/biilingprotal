'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''

from src import router
from src import app_configration
import webapp2 
from google.appengine.api import users 

 
def handle_401(request, response, exception): 
  response.write('<b>Access denied</b>')
  response.set_status(401)   
  
app = webapp2.WSGIApplication(router.get_routes(), debug=True,
                              config = app_configration.config)  

app.error_handlers[401] = handle_401