'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''
from src.action import user
from src.action import superadmin


from webapp2_extras.routes import RedirectRoute

__route_list = [
    RedirectRoute(r'/', user.Home, name='Home page', strict_slash=True),
    RedirectRoute(r'/Role', user.RoleHandler, name='RoleHandler', strict_slash=True),
    
    #superadmin
    RedirectRoute(r'/superadmin', superadmin.Home, name='superadmin page', strict_slash=True),
    RedirectRoute(r'/superadmin/AddDomain',  superadmin.AddDomain, name='superadmin AddDomain page', strict_slash=True),
    RedirectRoute(r'/superadmin/AddUserAccount',  superadmin.AddUserAccount, name='superadmin user account page', strict_slash=True),
    RedirectRoute(r'/superadmin/GetDaomainData',  superadmin.GetDaomainData, name='superadmin GetDaomainData', strict_slash=True),
   
    ]

def get_routes():
  return __route_list

def add_routes(app):
  if app.debug:
    secure_scheme = 'http'
  for __route in __route_list:
    app.router.add(__route)