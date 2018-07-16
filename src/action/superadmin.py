'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''
from src.db import Domain
from src.db import User, Role
from src.api.basehandler import SABase, json_response, WARNING, SUCCESS

from google.appengine.api import namespace_manager

class Home(SABase):
  def get(self):
    domain_list = Domain.get_organization_list().fetch()  
    context = self.get_context
    context['domain_list']=domain_list
    template = self.get_jinja2_env.get_template('html/superadmin.html')    
    self.response.out.write(template.render(context)) 
    
class AddDomain(SABase):
  def get(self):
    context={}  
    template = self.get_jinja2_env.get_template('super/addDomain.html')    
    self.response.out.write(template.render(context))    

  def post(self):    
    data_dict={}  
    address=self.request.get('address')
    domain=self.request.get('domain').lower().strip() 
    company_title=self.request.get('company_title')
    country=self.request.get('country')
    admin_email=self.request.get('admin_email')
    admin_name=self.request.get('admin_name')
    user_count=int(self.request.get('user_count'))  
    domain = domain.replace(' ', '')
    if domain.__len__()<3:
      return json_response(self.response, data_dict, WARNING, 'Domain must minimum 3 char long') 
    
    if Domain.verify_organization_account(domain):
      return json_response(self.response, data_dict, WARNING, 'Domain exist')
  
    e=Domain()
    e.address=address
    e.admin_email=admin_email
    e.admin_name=admin_name
    e.company_title=company_title
    e.currency = 'KES'
    e.domain = domain
    e.user_count=user_count
    if country:
      e.country = country
    e.put()
    
    namespace_manager.set_namespace(domain) 
    r=Role()
    r.description='Domain admin full access' 
    r.role='ADMIN'
    r.put()
    
    return json_response(self.response, data_dict, SUCCESS, 'Domain Created')    

class AddUserAccount(SABase):
  def get(self):
    
    domain_list = Domain.get_organization_list().fetch()    
    context={'domain_list': domain_list}  
    template = self.get_jinja2_env.get_template('super/addUser.html')    
    self.response.out.write(template.render(context))  
    
  def post(self):
    role_list=[]
    domain=self.request.get('domain')
    role=self.request.get('role')
    email=self.request.get('email')
    name=self.request.get('name') 
    d=Domain.verify_organization_account(domain)
    if not d.user_count:
      return json_response(self.response, {}, WARNING, 'Domain inactive kindly increase user count.')     
    namespace_manager.set_namespace(domain) 
    active_user=User.get_active_user_list().count()  
    if active_user >= d.user_count:
      return json_response(self.response, {}, WARNING, 'Domain max user count %s.' %(d.user_count))
    
    if User.get_user_by_email(email):
      return json_response(self.response, {}, WARNING, 'Domain has user account: %s' %(email))
    e = User()
    e.active_status=True
    e.country=d.country
    e.email=email
    e.name=name
    e.role=role
    if email==d.admin_email:
      e.system_owner=True
    e.put()
    data_dict={}
    return json_response(self.response, data_dict, SUCCESS, 'User account ready: %s' %(email))

class GetDaomainData(SABase):
  def get(self):
    role_list=[]
    domain=self.request.get('domain')
    d=Domain.verify_organization_account(domain) 
    namespace_manager.set_namespace(domain) 
    active_user=User.get_active_user_list().count()
    for r in Role.get_role_list().fetch():
      role_list.append(r.role)    
    
    data_dict={'user_count': d.user_count,
               'active_user': active_user,
               'role_list': role_list}
    return json_response(self.response, data_dict, SUCCESS)

                       

    