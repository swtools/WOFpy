======================
ODM SQL Server Example
======================

This example shows how to access CUAHSI Observations Data Model databases in Microsoft SQL Server.  The example uses the Little Bear River ODM 1.1 database from the HIS website at http://his.cuahsi.org/odmdatabases.html.  Follow the steps below to run this example.

#. Install Microsoft SQL Server.  You can download the free version, SQL Express.
#. Download the Little Bear River ODM 1.1 database from the HIS website.
#. Attach the database to SQL Server.
#. Create a file named **private_config.py** with a variable named **lbr_connection_string** set to a SQLAlchemy-compatible database connection string for the Little Bear River database, e.g., lbr_connection_string = 'mssql+pyodbc://username:password@(local)/LittleBear11'
#. Open a Command Window in the same folder as runserver_multiple.py and enter: python runserver_multiple.py
#. In your command window you should see a message indicating that the service is running along with instructions for accessing the service.  

To stop an example service, press CTRL+C in the command window.