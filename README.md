# urban_web_cms
*coded and tested on Python 3.6 and a postgres 10.0 server by Markus von Steht on 2017-12-17*

using python, cgi-scripting and a postgreSQL connection via the `psycopg2` driver to generate a small multi-user content management system (CMS). I coded this example in order to combine different concepts (server-side scripting, user access, database communication) into one small application which can be reshaped and extended quickly for different purposes.

I provides functionality to an editorial board of various users to generate content for an updating "news"-HTML site:
  - CMS system relies on CGI scripting and is coded object-oriented
  - SQL connection is handled in modules external to the CGI scripts to make them less bloated
      - only an SQL string and a optionally a list of arguments ´data´ needs to be transmitted
  - login screen requires password authentification by comparing server-side MD5 hash keys
  - content (in form of Title/Text Block with an expiry date) is submitted to the system and stored in a postgres DB
      - user login hash/authors is maintained by the same DB in a different table and JOINED during publication
      - the user's password can be optionally updated on the content submission page
  - on submission of new content it is immediately published to the corresponding news.html site
      - this is a re-reading of the unexpired DB entries and printing to the webpage in order of submission

How to Install:
  1. download source and  
  2. two options for deployment:
     1. start `cgi_scripting_server.py` as a local instance and connecting by using a web browser via `localhost:8100`
     2. put everything on a web server (untested for now)
  3. edit `config.ini` to be able to access a postgresql server running either remotely or locally
  4. edit `editorial_office_admin.py` to set the initial editorial board members in `PERSONS` global var
  5. run the script `editorial_office_admin.py` at least once to create the database and tables
     - optionally to add users to the editorial board
     - the entry `alias` does not serve any purpose currently
     - I advise to uncomment the calling of the `DROP table` statements to keep the DB side flexible until log in can 
        be achieved under initial circumstances
  6. access the `index.html` and log in using any existing user with its default password 
      i.e. the user `name` (case sensitive)
  7. CGI debug is turned on by default and written to file `logging.txt`

Assuming that the following python modules are available to the server:
  - in `editorial_office_admin.py` and `editorial_class.py`
    - `hashlib`, `cgi`, `cgitb`, `time`, `logging`
  - in `cgi_scripting_server.py`
    - `http`
  - in `database.py`
    - `psycopg2`
  - in `configuration.py`
    - `os`, `configparser`
