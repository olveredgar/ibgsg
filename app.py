
import os
import sys

import random
import Cookie
from enrutadorhttp import EnrutadorHTTP

from dominios import dominios

from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer





class ManejadorPersonalizado(BaseHTTPRequestHandler, EnrutadorHTTP):
	"""docstring for ClassName"""
	session={}
	galleta=''

	def do_GET(self):
		self.procesar_peticion_get()

	def do_POST(self):

		self.procesar_peticion_post()


	def iniciar_session(self):
		self.cookie=Cookie.SimpleCookie()

		if "Cookie" in self.headers:
			self.cookie.load(self.headers.get('cookie'))
			sesion,galleta=self.server.get_session(self.cookie)
			if 'IDSS' not in self.cookie:
				self.cookie['IDSS']=galleta
			if 'LANG' not in self.cookie:
				self.cookie['LANG']='es'

		else:
			sesion,galleta=self.server.get_session()
			self.cookie['IDSS']=galleta
			self.cookie['LANG']="es"

			
		self.session=sesion['Sesion']
		self.galleta=galleta

	def setSession(self,g,k,value):
		self.server.set_session(g,k,value)




class Server(ThreadingMixIn, HTTPServer):
	abc={}
	num=0
	def get_session(self,val=None):

#		obj=val['IDSS'].value

		c=Cookie.SimpleCookie(val)
		if len(c)==0:
			obj=None
		elif 'IDSS' not in c:
			obj=None
		else:
			obj=c['IDSS'].value

		t=''
		for x in xrange(1,10):
			r=random.randint(1, 61)
			if r<10:
				t+=chr(r+48)
			elif r<36:
				t+=chr(r+55)
			else:
				t+=chr(r+61)



#        if obj:

		if obj in self.abc:
			return self.abc[obj],obj
		elif obj==None:
			self.abc[t]={'Sesion':{}}
			return (self.abc[t], t)
		else:
			self.abc[obj]={'Sesion':{}}
			return (self.abc[obj],obj)
	def set_session(self,obj,k,value):

		self.abc[obj]['Sesion'][k]=value

		return
dominios.instanciar()
http=Server(('',1542),ManejadorPersonalizado)
http.serve_forever()
