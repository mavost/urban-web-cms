#!/Python36-32/python.exe #Windows shebang 
#!/usr/bin/python #Linux shebang plus chmod to make executable
#------------------------------------------------------------
# FILENAME: editorial_office_admin.py
# VERSION: 1.0 - Python 3.6
# PURPOSE:
# AUTHOR: MVS
# LAST CHANGE: 11/12/2017
#------------------------------------------------------------
''' Python 3 main - Using the postgresdb, CGI, MD5 authentification
	to create an application to manage editorial staff and input.
	Administration of staff


'''

from lib.database import Database
import hashlib


SQL_CREATE_DB = """CREATE DATABASE editorialdb ENCODING 'UTF8'"""

SQL_SELECT_1 = """SELECT * FROM persons"""
SQL_SELECT_2 = """SELECT * FROM content"""
SQL_DROP_1 = """DROP TABLE IF EXISTS persons"""
SQL_DROP_2 = """DROP TABLE IF EXISTS content"""
SQL_CREATE_1 = """CREATE TABLE persons(user_id INTEGER PRIMARY KEY, name VARCHAR(100), alias VARCHAR(100), fingerprint BYTEA)"""
SQL_CREATE_2 = """CREATE TABLE content(text_id INTEGER PRIMARY KEY, title VARCHAR(100), text VARCHAR(1000), expiry_date FLOAT, user_id INTEGER)"""
SQL_SELECT_NAME = """SELECT name FROM persons WHERE name=%s"""
SQL_SELECT_ALIAS = """SELECT name FROM persons WHERE alias=%s"""

SQL_INSERT_1 = """INSERT INTO persons VALUES (%s, %s, %s, %s)"""
SQL_INSERT_2 = """INSERT INTO content VALUES (%s, %s, %s, %s, %s)"""

LINEWIDTH = 79

PERSONS = {1: ['Admin', 'admin'],
			2: ['Tom', 'tomtom'],
			3: ['Mike', 'rico123'],
			4: ['Silke', 'admin1']}


class Admin(object):
	def __init__(self):
		try:
			self.db = Database(None)			#reading all connection data from config.ini
			print('Database connected...')
		except:
			self.db = Database('postgres')		#entering on master level using config.ini
			self.db.execute(SQL_CREATE_DB)
			self.db.closeDb()
			self.db = Database(None)			#now enter at db level using autocommit
			print('Database created and connected...')
		print('#'*LINEWIDTH)
		
		#self.db.execute(SQL_DROP_1)				#drop tables to start over
		#self.db.execute(SQL_DROP_2)
		#print('Tables dropped...')
		#print('#'*LINEWIDTH)
		
		try:										#do both table exist?
			self.db.fetchAll(SQL_SELECT_1)
			print('Table persons exists...')
		except:
			self.db.execute(SQL_CREATE_1)
			print('Table persons created...')
			counter = self.getMaxUserId()				#get highest user_id
															#add new users based on highest id
			for key,value in PERSONS.items():			#add default rows to persons table
				md5key = hashlib.md5(value[0].encode('utf-8'))
				data = [key+counter, *value, md5key.digest()]	#increment id, list unpacking, hashing
				self.db.insert(SQL_INSERT_1, data)
				print(data, 'inserted')

		try:										
			self.db.fetchAll(SQL_SELECT_2)
			print('Table content exists...')
		except:										#otherwise re-create them
			self.db.execute(SQL_CREATE_2)
			print('Table content created...')
			data = [1, "Start of Journal", "Hello World", 1.0e20, 1]
			self.db.insert(SQL_INSERT_2, data)			#add default entry to content table

		#self.db.commit()
		print('Table write successful...')
		print('#'*LINEWIDTH)

		result = self.db.fetchAll(SQL_SELECT_1)
		print('List of users in DB:')
		for id, name, alias, hash in list(result):
			print(name, alias)
		print('Output successful')
		print('#'*LINEWIDTH)

		newname = input('New User (exit with enter):')
		counter = self.getMaxUserId()
		while newname:
			if list(self.db.fetchAll(SQL_SELECT_NAME,data=[newname])):
				print('Name exists already...')
			else:
				newalias = input('Please enter also a new alias:')
				if list(self.db.fetchAll(SQL_SELECT_ALIAS,data=[newalias])):
					print('Alias exists already...')
				else:
					md5key = hashlib.md5(newname.encode('utf-8'))
					counter += 1
					#print(counter)
					data = [counter, newname, newalias, md5key.digest()]
					self.db.insert(SQL_INSERT_1, data)
					print('New user {} created successfully'.format(newname))
			newname = input('New User (exit with enter):')
					
		
		print('Manual input completed')
		print('#'*LINEWIDTH)

		self.db.closeDb()
		print('Connection closed')
		print('#'*LINEWIDTH)

	def getMaxUserId(self):								#a non-existing table throws error
		result = self.db.fetchOne("""SELECT MAX(user_id) FROM persons""")
		#print(result[0])
		if result[0] is None or len(result) == 0: 		#an empty table returns [None], empty list check is extra
			return 0
		else:
			return result[0]
	

myadmin = Admin()