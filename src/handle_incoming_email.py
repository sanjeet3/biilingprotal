'''
Created on 16-Jul-2018

@author: Sanjay Saini
'''

import logging, datetime, StringIO

from src.db import MailData

from src.pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from src.pdfminer.pdfpage import PDFPage
from src.pdfminer.converter import TextConverter
from src.pdfminer.layout import LAParams

from cStringIO import StringIO

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
    domain = to.split('@')[0]
    namespace_manager.set_namespace(domain)    
    e = MailData()
    e.sender = sender
    e.subject = subject
    e.received_on = ' '.join(a[:4])
    e.email_date = email_date
    if attachment:
      filename, payload = attachment  
      self.read_attchmet(payload)
      e.atachment_name = filename 
        
    e.put()

  def read_attchmet(self, payload): 
    try:
      fp = StringIO.StringIO(payload)
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
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()
    logging.info(text)
    # Cleanup
    device.close()
    sio.close()
    
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)