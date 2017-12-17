#!/usr/bin/python #Linux shebang plus chmod to make executable
#------------------------------------------------------------
# FILENAME: configurations.py
# VERSION: 1.0 - Python 3.6
# PURPOSE:
# AUTHOR: MVS
# LAST CHANGE: 08/11/2017
#------------------------------------------------------------
''' Intro to using encapsulated access to PostgreSQL databases
	-converted to python 3
	-ini file located in parent folder to lib contains database params
	http://www.andreafiori.net/posts/connecting-to-a-postgresql-database-with-python
	Modules
	pip install ConfigParser
'''
import os
import configparser

class Configurations:
	def __init__(self):
		path=os.path.join(os.path.dirname(__file__),'../config.ini')
		print("Accessing: {}".format(path))
		self.config = configparser.ConfigParser()
		self.config.read( path )

	def getConfigParser(self):
		return self.config
