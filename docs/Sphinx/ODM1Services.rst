***************
ODM1 SQL Server
***************
A single service can be run from the command line.

    ``python runserver_odm11.py
    --config=lbr_config.cfg
    --connection=mssql+pyodbc://{user}:{password}@{host}/{db}?driver=SQL+Server+Native+Client+10.0``

Detailed Instructions
---------------------
This example is located in the **examples/odm_sqlserver** folder.

This example shows how to access CUAHSI Observations Data Model (ODM) databases
in Microsoft SQL Server.  The example uses the Little Bear River ODM 1.1
example database from the HIS website at
http://his.cuahsi.org/odmdatabases.html.

Follow the steps below to run this example.

#. Install Microsoft SQL Server.  You can download the free version, SQL
   Express.
#. Download the Little Bear River ODM 1.1 database from the HIS website.
#. Attach the database to SQL Server.
#. Grant a SQL Server account **select** privileges on the database.  WOFpy
   will use this account to connect to the database.
#. Determine the database connection string. **lbr_connection_string** set to a SQLAlchemy-compatible
   database connection string for the Little Bear River database, e.g.,
   'mssql+pyodbc://webservice:webservice@localhost/LittleBear11?driver=SQL+Server+Native+Client+10.0'``
#. In the **examples/odm_sqlserver** folder, edit the value of the **openPort**
   variable in **runserver_lbr.py** to match an open port on your computer,
   if necessary.  Then save and close the file.
#. Open a command window in the **examples/odm_sqlserver** folder and enter:
   ``python runserver_odm11.py
    --config=lbr_config.cfg
    --connection=mssql+pyodbc://{user}:{password}@{host}/{db}?driver=SQL+Server+Native+Client+10.0y``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.