.. _Publishing your data with WOFpy:

*******************************
Publishing your data with WOFpy
*******************************

Concepts
========
Models
------

Data Access Objects (DAO)
-------------------------
(to be continued)
* DAOs define object-relational mapping (ORM) from native schema to Model.
* They contain methods for translating user arguments into queries to native db.
* The python module, SQLalchemy, supports ORMs and can accommodate different db environments (e.g. MSSQL, SQLite, etc)

DAO Tutorial
============
To Make a New DAO:

#. Create a new folder in /daos to put all your dao code.

#. Write a new DAO class based on BaseDao in base_dao.py.  The methods should return objects as defined in base_models.py

#. Write a new config file as those found in /config

#. Write a new runserver script (see runserver_flask.py as an example) to use the new DAO you implemented.

Example: Writing a DAO for a simple three-table database
--------------------------------------------------------
(In progress)
This example shows how to write a new dao for a simple three-table database.  The dao can be found under the folder,
'examples\barebones\' in 'swtools\WOFpy'.  The database contains data from the Lake Champlain Monitoring 
Program (LCM) from the Vermont Department of Environmental Conservation.  The original data were in a 
collection of ASCII and MS Excel files.  These were imported into a sqlite database for publishing 
through WOFpy.  Please note that data is for demonstration purposes and has been modified slightly to make 
the tutorial clearer.

The three tables are sampling_sites, variables and LCM_data.  Information on the source are contained 
in a .cfg file.  Despite its simplicity, the database supports all four WaterOneFlow methods.




