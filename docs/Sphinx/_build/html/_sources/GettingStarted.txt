.. _Getting Started:

***************
Getting Started
***************

Here is a quick guide to getting WOFpy up and running

The folder contains Python modules that can read data from a Data Access Object (DAO) and return the data to the client in WaterML format, using the same access methods defined by the CUAHSI-HIS WaterOneFlow web service.  DAOs can represent a variety of data sources, including an Observations Data Model (ODM)-format database, the Surface Water Information System (SWIS) database, or even a pass-through web-service, such as that by the Conrad-Blucher Institute (CBI).  The three aforementioned data sources have their associated DAO implementations included with this package.  Others may be written by following the BaseDao (see base_dao.py) class description.

The code was written using Python version 2.6


Requirements
============
WOFpy require a number of python libraries in order to run.  
Please follow the following to install them.

Installation on a Windows computer
==================================

#. Install Python 2.6.  Use the 32-bit installer, not the 64-bit version. (Setuptools, which you'll install later, can't detect Python when the 64-bit version is installed).
#. Add the Python folder to your Path environment variable.
#. Install setuptools. This includes the easy_install program, which you'll use to install Flask.
#. Add the Python\scripts folder to your Path environment variable.
#. Open a command Window (run cmd) and enter this command: easy_install flask
#. Enter: easy_install lxml
#. Enter: easy_install pyodbc
#. Enter: easy_install soaplib==2.0.0-beta1 (unless the 2.0 release has been finalized -- then use that one instead of beta)
#. Enter: easy_install sqlalchemy
#. Enter: easy_install nose
#. Enter: easy_install suds
#. If you want the package that was used to generate the code for serializing/deserializing WaterML, enter: easy_install generateds
#. Create a "private_config.py" file in your WOFpy/WOFpy/ folder.  This file should contain the following variables:

* lbr_connection_string = ''
* swis_connection_string = ''
* swis_test_connection_string = ''

Each should be set to a SQLAlchemy-compatible database connection string.
#. (OPTIONAL) Download and install pywin32 http://sourceforge.net/projects/pywin32/files/pywin32/Build%20215/  This package can be used to create a Windows service for your WOFpy application.

After everything is installed, open a command window and navigate to your WOFpy/WOFpy/ folder.  Type "nosetests -v" to run the included tests.  If they all pass, the congratulations!

Getting a web service up and running
====================================
Example for running the code on your local Windows machine:

#. Populate an ODM database on an instance of SQL Server.  You can download one from the ODM page at http://his.cuahsi.org.

#. Make a private_config.py file in your local folder and add a line that says database_connection_string = '[YOUR_DB_CONNECTION_STRING]'.

#. Open a Command Window in the same folder as the runserver module and enter: python runserver_[dbname].py

   *Tip: In the folder tree view in Windows Explorer, hold down the shift key and right-click on a folder to see the option for opening a command window in that folder.*

#. In your command window you should see a message that says "* Running on http://127.0.0.1:5000/".  Congratulations, your development server is operational!

#. You may now visit http://127.0.0.1:8080 with your web browser.  Other URLS to visit include:

* /GetSite?siteCode=XXX,YYY

* /GetSiteInfo?siteCode=XXX

* /GetVariableInfo?varCode=ABC

* /GetValues?siteCode=XXX&varCode=ABC&startDateTime=2010-01-01:12:00&endDateTime=2010-02-01-01:12:00

Accessing WOFpy REST web services
=================================

Accessing WOFpy SOAP web services
=================================