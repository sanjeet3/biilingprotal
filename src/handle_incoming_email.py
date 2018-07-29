'''
Created on 16-Jul-2018

@author: Sanjay Saini
'''

import logging, datetime
import base64

from src.db import MailData

from src.pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from src.pdfminer.pdfpage import PDFPage
from src.pdfminer.converter import TextConverter
from src.pdfminer.layout import LAParams

import StringIO as pySIO
from StringIO import StringIO
#from cStringIO import StringIO
from google.appengine.api import namespace_manager
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

import webapp2
from google.appengine.ext import ndb


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
        
    for atch in attachments: 
      attachment = atch
      break 
      #logging.info('atch: %s, type: %s' %(atch, type(atch)))
          
    a = date.split(' ')  
    email_date = datetime.datetime.strptime('%s%s%s'%(a[1],a[2],a[3]),'%d%b%Y')
    domain = to.split('@')[0]
    namespace_manager.set_namespace(domain)    
    e = MailData()
    e.sender = sender
    e.subject = subject
    e.received_on = ' '.join(a[:4])
    e.email_date = email_date
    if attachment:
      filename, payload = attachment  
      content = payload.decode()
      e.atachment_name = filename 
      e.attachment_content = content
      try:
        self.read_attchmet(content)
      except Exception, msg:
        logging.error(msg)  
        pass    
    e.put()

  def read_attchmet(self, content): 
    try:
      fp = pySIO.StringIO(content)
      logging.info(fp)
    except Exception, msg:
      logging.error(msg)    
      return
    
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    try:
      for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    except Exception, msg: 
      logging.error(msg)       
    fp.close()

    # Get text from StringIO
    logging.info(sio.len)
    text = sio.getvalue()
    logging.info(text)
    # Cleanup
    device.close()
    sio.close()
    

class TestPDF(webapp2.RequestHandler):
  def get(self):    
    kay = 'ahRqfmJpbGxpbmctcGRmLXBvcnRhbHIVCxIITWFpbERhdGEYgICAoKSVggoMogEEY3NwbA'
    e = MailData()
    e = ndb.Key(urlsafe=kay).get()
    self.read_attchmet(e.attachment_content)
    
    
    self.response.out.write('<h1>Testing')    

  def read_attchmet(self, content): 
    try:
      fp = pySIO.StringIO(base64.b64decode(content).decode('UTF-8'))
      logging.info(fp)
    except Exception, msg:
      logging.error(msg)    
      return
    
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'ascii'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    try:
      for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    except Exception, msg: 
      logging.error(msg)       
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()
    logging.info(text)
    # Cleanup
    device.close()
    sio.close()
    
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)