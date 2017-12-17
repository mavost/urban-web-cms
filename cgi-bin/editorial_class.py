#!/Python36-32/python.exe #Windows shebang 
#!/usr/bin/python #Linux shebang plus chmod to make executable
#------------------------------------------------------------
# FILENAME: editorial_class.py
# VERSION: 1.0 - Python 3.6
# PURPOSE:
# AUTHOR: MVS
# LAST CHANGE: 11/12/2017
#------------------------------------------------------------
''' Python 3 main - Using the postgresdb, CGI, MD5 authentification
	to create an application to manage editorial staff and input.
	Managed editorial content by staff
	Note: this was a test and did not work as a CGI and also not standalone 
	because the missing form data threw exceptions


'''

from lib.database import Database
import hashlib, cgi, cgitb, time, logging

cgitb.enable()
logging.basicConfig(filename='logging.txt', format='%(funcName)s: %(message)s',
						level=logging.DEBUG, filemode='w')


#new content and password setting
HTMLTEMPLATE1="""Content-type: text/html; char-set=utf-8

<!DOCTYPE html>
<html>
  <head> 
        <title>Python Editorial Office</title>
        <meta http-equiv="content-type" content="charset=UTF-8" />
  </head>
  <body bgcolor=#C0C0C0>
    <h2>Python Editorial Office</h2>
        <form action="http://localhost:8100/cgi-bin/editorial_class.py" method="POST">
        <!-- Hidden variables -->
            <input type="Hidden" name="name" value="{}">
            <input type="Hidden" name="password" value="{}">
        <!-- Entries -->
            <b>Title: </b><input type="Text" name="title" size="50" maxlength="80"><br><br>
            <textarea name="text" cols="50" rows="8" >{}
            </textarea><br>
        <!-- Radio Buttons -->
        <h4>Persistence of new entry</h4>
            <input type="Radio" name="persist" value="14" checked="checked"> 2 weeks<br>
            <input type="Radio" name="persist" value="30" > 4 weeks<br>
            <input type="Radio" name="persist" value="90" > 3 months<br>
            <input type="Radio" name="persist" value="180" > 6 months<br>
        <!-- Password Entries -->
        <h4>Password Maintenance</h4>
            <input type="Checkbox" name="newpass" value="1" > Change password<br>
            <input type="Password" name="newpass1"> Enter new password<br>
            <input type="Password" name="newpass2"> Repeat new password<br>
        <!-- Submit button -->
            <input type="Submit" value="Send">
    </form>
    <!-- Status -->
    <i>{}<br><i><br></i>
    <br><br>
    <a href="../html/news.html">Go to news...</a>
    <br><br>
    <a href="../index.html">Go back...</a>
  </body>
</html>"""

#error due to wrong password
HTMLTEMPLATE2="""Content-type: text/html; char-set=utf-8

<!DOCTYPE html>
<html>
  <head> 
        <title>Python Editorial Office</title>
        <meta http-equiv="content-type" content="charset=UTF-8" />
  </head>
  <body bgcolor=#C0C0C0>
    <h2>Python Editorial Office</h2>
        <form action="http://localhost:8100/cgi-bin/editorial_class.py" method="POST">
            Name: <input type="Text" name="name" >&nbsp
            Password: <input type="Password" name="password" ><br><br>
            <input type="Submit" value="Login" >
    </form>
    <b> Login failed... Please verify user name and password.</b>
    <br><br>
    <a href="../html/news.html">Go to news...</a>
    <br><br>
    <a href="../index.html">Go back...</a>
  </body>
</html>"""

#Publication view - not for scripting


HTMLTEMPLATE3="""<!DOCTYPE html>
<html>
  <head> 
        <title>Python News</title>
        <meta http-equiv="content-type" content="charset=UTF-8" />
  </head>
  <body bgcolor=#C0C0C0>
    <h1>Python News</h1>
        Latest Changes on: {}
        {}
    <br><br>
    <a href="../index.html">Go back...</a>
  </body>
</html>"""

#Content block
HTMLVIEW="""<h3>{}</h3>
<h4>by {}</h4>
<p>{}</p>"""

#mapping to replace special chars
HTMLMAP = {ord('ä'): '&auml;', ord('ö'): '&ouml;', ord('ü'): '&uuml;',
		ord('Ä'): '&Auml;', ord('Ö'): '&Ouml;', ord('Ü'): '&Uuml;',
		ord('ß'): '&szlig;'}

HTML_CONTENT_PATH='html/news.html'

SQL_SELECT_1 = """SELECT fingerprint FROM persons WHERE name=%s"""
SQL_SELECT_2 = """SELECT user_id FROM persons WHERE name=%s"""
SQL_SELECT_3 = ('SELECT c.title, c.text, c.expiry_date, p.name, c.text_id FROM content c ' 
					'INNER JOIN persons p ON p.user_id=c.user_id')
SQL_UPDATE = """UPDATE persons SET fingerprint = %s WHERE name = %s"""
SQL_INSERT_1 = """INSERT INTO content VALUES (%s,%s,%s,%s,%s)""" 
SQL_DELETE = """DELETE FROM content WHERE text_id = %s""" 

class EditorialUser(object):
	def __init__(self, form, db):
		self.name = form.getvalue("name")
		self.pw = form.getvalue("password")
		self.db = db

	def verifyId(self):
		logging.debug('Name: {}, Password: {}'.format(self.name, self.pw))
		try:
			logging.debug(self.db)
			result = self.db.fetchOne(SQL_SELECT_1, [self.name])
			logging.debug('Database connected')
			fingerprint_db = bytearray(result[0])
			logging.debug('fingerprint_db: {}'.format(fingerprint_db))
			pw_bytes = self.pw.encode('utf-8')			#check whether password matches on client side
			fingerprint_pw = hashlib.md5(pw_bytes).digest()
			logging.debug('fingerprint_pw: {}'.format(fingerprint_pw))
			return fingerprint_db == fingerprint_pw
		except:
			return False	#user not in DB or wrong password
			
	def updatePass(self, form):
		newpw1 = form.getvalue("newpass1","")
		newpw2 = form.getvalue("newpass2","")
		if newpw1==newpw2:				#allows for empty password?
			self.pw = newpw1
			data = [hashlib.md5(self.pw.encode('utf-8')).digest(), self.name]
			self.db.insert(SQL_UPDATE, data)
			return "Password change successful"
		else:
			return "New passwords do not match"

class EditorialContent(object):
	def __init__(self, form, author, db):
		self.title = ''
		self.text = ''
		self.db = db
		self.author = author
		if "title" in form.keys():
			self.title = form.getvalue("title")
			self.text = form.getvalue("text")
			lifetime_sec = float(form.getvalue("persist"))*24*3600			#in seconds
			self.expirytime = lifetime_sec + time.time()
			logging.debug('Expiry time for content: {:.2f}'.format(self.expirytime))
	
	def ecSubmit(self):			#add content to db
		if self.title :
			logging.debug('Title: {}'.format(self.title))
			logging.debug('Text: {:.30}...'.format(self.text))
			result = self.db.fetchOne(SQL_SELECT_2, [self.author.name])			#get user_id from persons-table
			counter = self.getMaxContentId()								#get highest index from content-table
			counter += 1
			data = [counter, self.title, self.text, self.expirytime, result[0]]
			self.db.insert(SQL_INSERT_1, data)
			logging.debug('Saved: {}...'.format(self.title))
			self.title = ''
			self.text = ''
			message = 'Content has been submitted.'
		else:
			message = 'Content needs a title'
		return message
	
	def updateNewsfile(self, newspath):
		results = self.db.fetchAll(SQL_SELECT_3)			#get content/author list from persons-content-JOIN
		pubtext = ''
		counter=0
		for (title, text, expiry, author, textid) in results:
			if float(expiry) > time.time():
				counter += 1
				pubtext += HTMLVIEW.format(title, author, text).translate(HTMLMAP)
			else:
				#self.db.insert(SQL_DELETE, [text_id])
				logging.debug('Title: {} has expired'.format(title))
		logging.debug('Published text contains {} entry/entries'.format(counter))
		f = open(HTML_CONTENT_PATH, 'w')
		f.write(HTMLTEMPLATE3.format(time.asctime(),pubtext))
		f.close()

	def getMaxContentId(self):								#a non-existing table throws error
		result = self.db.fetchOne("""SELECT MAX(text_id) FROM content""")
		#print(result[0])
		if result[0] is None or len(result) == 0: 		#an empty table returns [None], empty list check is extra
			return 0
		else:
			return result[0]


class Editorial(object):
	def __init__(self):
		try:
			self.db = Database(None)			#reading all connection data from config.ini
			logging.debug('Database connected...')
		except:
									#if DB server is not accessible should wrap up an close connection here
			logging.debug('Connection to DB failed, try running admin first...')
		self.form = cgi.FieldStorage()
		self.user = EditorialUser(self.form, self.db)
		self.content = EditorialContent(self.form, self.user, self.db)
	
	
	def getPage(self):
		contenterror = ''
		pwerror = ''
		if self.user.verifyId():							#check of username succeeded: prepare content page
			if 'title' in self.form.keys():					#if we are calling the cgi from the content page
				contenterror = self.content.ecSubmit()			#add to content table in DB 
																#	and get message for pageupdate
				self.content.updateNewsfile(HTML_CONTENT_PATH)	#update news.html
			if 'newpass' in self.form.keys():				#if we are calling the cgi from the content page AND have checked the changePW box
				pwerror = self.user.updatePass(self.form)		#update PW in persons table in DB

			self.db.closeDb()									#DB server close
			logging.debug('Branch1: Database connection closed...')
			logging.debug('pwerror: {}'.format(pwerror))
			logging.debug('contenterror: {}'.format(contenterror))
			print(HTMLTEMPLATE1.format(self.user.name, self.user.pw, #hidden form data
										self.content.text, 			 #text will be carried over
										contenterror, pwerror))
		else: 												#bad username: prepare another login prompt
			self.db.closeDb()
			logging.debug('Branch2: Database connection closed...')
			print(HTMLTEMPLATE2)

			

myedit = Editorial()
myedit.getPage()