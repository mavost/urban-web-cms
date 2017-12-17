# urban_web_cms by 2017-12-17 by Markus von Steht
using python, cgi-scripting and a postgreSQL connection to generate a small multi-user content management system 
(CMS) 
I provides functionality to an editorial board of various users to generate content to an updating news site:
  - cms system relies on CGI scripting
  - login screen requires password authentification by server-side MD5 hash keys
  - content (in form of Title/Text Block with an expiry date) is submitted to the system and stored in a postgres DB
      - user login hash/authors is maintained by the same DB in a different table and JOINED during publication
      - the user's password can be optionally updated on the content submission page
  - on submission of new content it is immediately published to the corresponding news.html site
      - this is a re-reading of the unexpired DB entries and printing to the webpage in order of submission


How to Install:
  1) download source
  2) two options for deployment:
    A) start cgi_scripting_server.py  as localhost and connect using a web browser via localhost:8100
    B) put everything on a web server (untested)
  3) edit config.ini to be able to access a postgresql server running either remotely or locally
  4) edit editorial_office_admin.py to set the initial editorial board members in variable PERSONS 
  5) run the script editorial_office_admin.py at least once to create the database and tables 
    - optionally to add users to the editorial board
    - the entry 'alias' does not serve any purpose currently
    - uncomment the DROP table statements to reset
  6) access the index.html and log in using a default password i.e. the board member name (case sensitive)
