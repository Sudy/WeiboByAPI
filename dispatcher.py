#!/usr/bin/env python
#-*- coding:utf-8 -*-
from SimpleXMLRPCServer import SimpleXMLRPCServer
from Queue import Queue
import json
from itertools import islice

class Dispatcher(object):

	"""docstring for Dispatcher"""
	def __init__(self):
		self.json_data = open("result","r")
		self.count = 0
	def getSeed(self):
		print self.count
		self.count += 30
		return list(islice(self.json_data,30))

server = SimpleXMLRPCServer(("192.168.3.48",8000),allow_none = True)
server.register_instance(Dispatcher())
server.serve_forever()