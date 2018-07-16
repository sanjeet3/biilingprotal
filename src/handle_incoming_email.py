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
        
        
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)