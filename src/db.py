'''
Created on 11-Jul-2018

@author: Sanjay Saini
'''
from src.app_configration import config
from src.endpoints_proto_datastore.ndb import EndpointsModel
from google.appengine.api import namespace_manager
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages

class Domain(EndpointsModel):
  ''' Data Store for Organization '''
  domain = ndb.StringProperty()
  company_title = ndb.StringProperty()
  address = ndb.TextProperty()
  country = ndb.StringProperty(default='KE')
  currency = ndb.StringProperty(default='KES')
  admin_email = ndb.StringProperty()
  admin_name = ndb.StringProperty() 
  subscription_date = ndb.DateProperty(auto_now_add=True)
  user_count = ndb.IntegerProperty(default=0)
  created_on = ndb.DateTimeProperty(auto_now_add=True)
  update_on = ndb.DateTimeProperty(auto_now=True) 

  @classmethod
  def verify_organization_account(cls, domain):
    #namespace_manager.set_namespace(config.get('namespace'))
    query_obj = cls.query(cls.domain == domain).get()
    return query_obj

  @classmethod
  def get_organization_list(cls):
    return cls.query().order(cls.domain)

class Role(EndpointsModel):
  ''' Data Store for User Role configration with access right '''
  creator_email = ndb.StringProperty(default='System')
  creator_name = ndb.StringProperty(default='System')  
  role = ndb.StringProperty(required=True)
  description = ndb.TextProperty(default='') 
    
  @classmethod
  def get_role_list(cls):
    return cls.query().order(cls.role)  
  
  @classmethod
  def get_role_by_name(cls, name):
    return cls.query(cls.role == name).get()


class User(EndpointsModel):
  ''' Data Store for User '''
  created_on = ndb.DateTimeProperty(auto_now_add=True)
  update_on = ndb.DateTimeProperty(auto_now=True) 
  system_owner = ndb.BooleanProperty(default=False)
  active_status = ndb.BooleanProperty(default=False)
  creator_email = ndb.StringProperty(default='System')
  creator_name = ndb.StringProperty(default='System')   
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  role = ndb.StringProperty(default='ADMIN')
  country = ndb.StringProperty()
  telephone = ndb.StringProperty()
  image_url = ndb.StringProperty()
  gs_key = ndb.StringProperty()
  
  @classmethod
  def get_all_user_list(cls):
    return cls.query().order(cls.name)
  
  @classmethod
  def get_active_user_by_email(cls, email):
    return cls.query(cls.email == email, cls.active_status == True).get()

  @classmethod
  def get_user_by_email(cls, email):
    return cls.query(cls.email == email).get()

  @classmethod
  def get_active_user_list(cls):
    return cls.query(cls.active_status == True).order(cls.name)

  @classmethod
  def get_suspend_user_list(cls):
    return cls.query(cls.active_status == False).order(cls.name)

  @classmethod
  def get_active_user_by_role(cls, role):
    return cls.query(cls.role == role, cls.active_status == True).get()
  @classmethod
  def get_user_email_dict(cls):
    user_dict={}  
    for u in cls.query():
      user_dict[u.email] = u
          
    return user_dict  

class MailData(EndpointsModel):
  ''' Data Store for User '''
  created_on = ndb.DateTimeProperty(auto_now_add=True)
  active_status = ndb.BooleanProperty(default=True)
  sender = ndb.StringProperty(default='')
  subject = ndb.StringProperty(default='')
  sender = ndb.StringProperty(default='')
  received_on = ndb.StringProperty(default='') 
  atachment_name = ndb.StringProperty(default='')
  email_date = ndb.DateProperty()
  
  @classmethod
  def get_today_list(cls, dt):
    return cls.query(cls.email_date==dt).order(-cls.created_on)
     