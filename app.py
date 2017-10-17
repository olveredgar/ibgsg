#!/usr/bin/python
import os
import sys
import wsgi
from cherrypy import wsgiserver

#hack to make sure we can load wsgi.py as a module in this class
sys.path.insert(0, os.path.dirname(__file__))

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
  #execfile(virtualenv, dict(__file__=virtualenv)) # for Python v2.7
  #exec(compile(open(virtualenv, 'rb').read(), virtualenv, 'exec'), dict(__file__=virtualenv)) # for Python v3.3
  # Multi-Line for Python v3.3:
  exec_namespace = dict(__file__=virtualenv)
  with open(virtualenv, 'rb') as exec_file:
    file_contents = exec_file.read()
  compiled_code = compile(file_contents, virtualenv, 'exec')
  exec(compiled_code, exec_namespace)
except IOError:
  pass


# Get the environment information we need to start the server
ip = os.environ['OPENSHIFT_PYTHON_IP']
port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
host_name = os.environ['OPENSHIFT_GEAR_DNS']


server = wsgiserver.CherryPyWSGIServer((ip, port), wsgi.application, server_name=host_name)
server.start()
