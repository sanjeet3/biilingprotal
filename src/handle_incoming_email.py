'''
Created on 16-Jul-2018

@author: Sanjay Saini
'''

import logging, datetime

from src.db import MailData

from google.appengine.api import namespace_manager
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

import webapp2


class LogSenderHandler(InboundMailHandler):
  def receive(self, mail_message):
    attachment, filename, payload=None, '', None
    logging.info("Received a message from: " + mail_message.sender)
    sender = mail_message.sender
    to = mail_message.to
    subject = mail_message.subject
    date = mail_message.date
    attachments = mail_message.attachments
    
    logging.info('To: %s' %(to)) 
    logging.info('subject: %s' %(subject)) 
    logging.info(attachments)  
        
    for atch in attachments: 
      attachment = atch
      break 
      #logging.info('atch: %s, type: %s' %(atch, type(atch)))
          
    a = date.split(' ')  
    email_date = datetime.datetime.strptime('%s%s%s'%(a[1],a[2],a[3]),'%d%b%Y')
    #namespace_manager.set_namespace()    
    e = MailData()
    e.sender = sender
    e.subject = subject
    e.received_on = ' '.join(a[:4])
    e.email_date = email_date
    if attachment:
      filename, payload = attachment  
      self.read_attchmet(payload)
      e.atachment_name = filename 
        
    #e.put()

  def read_attchmet(self, payload):
    logging.info(type(payload)) 
    logging.info(payload)  
          
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)