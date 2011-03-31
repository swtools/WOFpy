The folder contains Python modules that can read data from a CUAHSI-HIS Observations Data Model (ODM) database and return the data to the client in WaterML format, using the same access methods defined by the CUAHSI-HIS WaterOneFlow web service.  The code uses Flask, a package for handling web stuff.  It also uses sqlalchemy, a package for handling object relational models.  It also uses pyodbc, which helps you connect to databases.

The code was written using Python version 2.7 and should be compatible with version 2.6.

Requirements when installing on a Windows computer:
1. Install Python 2.7.  Use the 32-bit installer, not the 64-bit version.  Setuptools, which you'll install later, can't detect Python when the 64-bit version is installed.
2. Add the Python folder to your Path environment variable.
3. Install setuptools. This includes the easy_install program, which you'll use to install Flask.
4. Add the Python\scripts folder to your Path environment variable.
5. Open a command Window (run cmd) and enter this command: easy_install flask
6. Enter: easy_install flask-sqlalchemy
7. Enter: easy_install lxml==2.2.8
8. Enter: easy_install pyodbc
9. Enter: easy_install soaplib==2.0.0-beta1
10. Enter: easy_install cherrypy
11. If you want the package that was used to generate the code for serializing/deserializing WaterML, enter: easy_install generateds
12. Download and install pywin32 http://sourceforge.net/projects/pywin32/files/pywin32/Build%20215/

To run the code on your local machine:
0. Populate an ODM database on an instance of SQL Server.  You can download one from the ODM page at http://his.cuahsi.org.
1. Edit one of the runserver_[dbname].py files to use a connection for your ODM database.  
2. Open a Command Window in the same folder as the runserver module and enter: python runserver_[dbname].py
Tip: In the folder tree view in Windows Explorer, hold down the shift key and right-click on a folder to see the option for opening a command window in that folder.
3. In your command window you should see a message that says "* Running on http://127.0.0.1:5000/".  Congratulations, your development server is operational!
4. You may now visit http://127.0.0.1:5000 with your web browser.  Other URLS to visit include:
	- /GetSite?siteCode=XXX,YYY
	- /GetSiteInfo?siteCode=XXX
	- /GetVariableInfo?varCode=ABC
	- /GetValues?siteCode=XXX&varCode=ABC&startDateTime=2010-01-01:12:00&endDateTime=2010-02-01-01:12:00

