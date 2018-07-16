'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''
from src.api.basehandler import Basehandler, SUCCESS, WARNING, json_response
from src.db import Role, User, Form, FormType, FormLayout, FormSlider


class Home(Basehandler):
  def get(self):
    context = self.get_context
    context['user_list']=User.get_active_user_list()
    
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
  
  
class Forms(Basehandler):
  def get(self):
    form_list = Form.get_all_form()
    role_list = Role.get_role_list().fetch()  
    context = {'role_list': role_list,
               'form_list': form_list,
               'FormType': FormType,
               'FormLayout': FormLayout,
               'FormSlider': FormSlider}
    
    template = self.get_jinja2_env.get_template('html/form')    
    self.response.out.write(template.render(context))   