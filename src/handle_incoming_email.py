'''
Created on 16-Jul-2018

@author: Sanjay Saini
'''

import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import webapp2


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        sender = mail_message.sender
        subject = mail_message.subject
        date = mail_message.date
        attachments = mail_message.attachments
        logging.info('subject: %s' %(subject))
        logging.info('date: %s, type: %s' %(date, type(date)))
        logging.info(attachments)  
        for atch in attachments: 
          logging.info('atch: %s, type: %s' %(atch, type(atch)))
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)