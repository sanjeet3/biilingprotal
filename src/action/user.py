'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''
from src.api.basehandler import Basehandler, SUCCESS, WARNING, json_response
from src.db import Role, User, MailData

import datetime

class Home(Basehandler):
  def get(self):
    dt = datetime.datetime.now().date()  
    mail_list = MailData.get_today_list(dt)  
      
    context = self.get_context
    context['user_list']=User.get_active_user_list()
    context['mail_list']=mail_list
    template = self.get_jinja2_env.get_template('html/base.html')    
    self.response.out.write(template.render(context))      

class RoleHandler(Basehandler):
  def get(self):
    role_list = Role.get_role_list().fetch()  
    context = {'role_list': role_list}
    template = self.get_jinja2_env.get_template('html/role.html')    
    self.response.out.write(template.render(context)) 
    
  def post(self):  
    name = self.request.get('name').upper()
    description = self.request.get('description')         
    if name.__len__()>3:
      if Role.get_role_by_name(name):
        return json_response(self.response, {}, WARNING, 'Role duplicate')
      else:
        r = Role()
        r.creator_email=self.user.email
        r.creator_name=self.user.name
        r.description=description
        r.role=name
        r.put()  
        return json_response(self.response,
                             {'name': name,
                              'description': description},
                             SUCCESS, 'Role created')     
    else:
      return json_response(self.response, {}, WARNING, 'Role minimum 3 character')      
