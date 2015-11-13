**********************
ODM2 PostgreSQL Server
**********************
A single service can be run from the command line.

#. ODM2 Measurement data use case

    ``python runserver_odm2_measurement.py
    --config=odm2_config_measurement.cfg
    --connection=postgresql+psycopg2://username:password/db_name``
#. ODM2 Timeseries data use case

    ``python runserver_odm2_timeseries.py
    --config=odm2_config_timeseries.cfg
    --connection=postgresql+psycopg2://username:password/db_name``

Multiple services can be run from the command line

    ``python runserver_multiple.py``

Detailed Instructions
---------------------
These examples are located in the **examples/odm2** folder.

These examples show how to access Observations Data Model (ODM2) databases in PostgreSQL Server.
The example for ODM2 measurement data uses the Marchantaria Time Series ODM2 database from the ODM2 github at https://github.com/ODM2/ODM2/tree/master/usecases/marchantariats.
And the example for ODM2 timeseries uses YODA file (needs YODA loader to store it into ODM2 database) from ODM2 github at https://github.com/ODM2/YODA-Tools/blob/master/examples/Timeseries_Template_Working_my_version.yaml.

Follow the steps below to run this example.

#. Install PostgreSQL Server.
#. Download ODM2 database from the ODM2 github at above URLs.
#. Determine the database connection string. **odm2_connection_string** set to a SQLAlchemy-compatible
   database connection string for the ODM2 database, e.g.,
   'postgresql+psycopg2://username:passowkr@hostname:port/db_name'
#. In the **examples/odm2/{measurement|timeseries}** folder, edit the value of the **openPort**
   variable in **runserver_multiple.py|runserver_odm2_measurement.py|runserver_odm2_timeseries.py** to match an open port on your computer,
   if necessary.  Then save and close the file.
#. In case of ODM2 measurement data use case, open a command window in the **examples/odm2/measurement** folder and enter:

    ``python runserver_odm2_measurement.py
    --config=odm2_config_measurement.cfg
    --connection=postgresql+psycopg2://username:password/db_name``
#. In case of ODM2 timeseries data use case, open a command window in the **examples/odm2/timeseries** folder and enter:

    ``python runserver_odm2_timeseries.py
    --config=odm2_config_timeseries.cfg
    --connection=postgresql+psycopg2://username:password/db_name``
#. In case of multiple services, open a command window in the **examples/odm2/** folder and enter:

    ``python runserver_multiple.py``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.