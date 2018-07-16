'''
Created on 05-Apr-2017

@author: Sanjay Saini
'''

import os
import sys

def namespace_manager_default_namespace_for_request():
  """ Binding namespace to be used for a request 
  """
  url_extension_list = str(os.environ['SERVER_NAME']).split(".")
  namespace = url_extension_list[1] if url_extension_list[0].lower() in ['www'] else url_extension_list[0]
  return namespace
  #return 'superadmin'
  
ENDPOINTS_PROJECT_DIR = os.path.join(os.path.dirname(__file__),
                                    'src.endpoints-proto-datastore')
sys.path.append(ENDPOINTS_PROJECT_DIR)
