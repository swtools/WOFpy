========
Examples
========

This folder contains examples demonstrating how to publish data with WOFpy.  Each example includes example data, a data access object (DAO), configuration files and a script to run the service.  To run a given example in Windows, open a command window in the example folder and enter this command: python runserver*.py. Be sure to read the readme file in each subfolder for additional setup instructions that may be required for a given example.

This folder contains a runserver_multiple.py script demonstrating how to run multiple services at once.  It uses the CBI and SWIS examples.  Follow the steps below to run this example.

#. Create a file named **private_config.py** with a variable named **swis_connection_string** set to a SQLAlchemy-compatible database connection string for the SWIS SQLite database, e.g., swis_connection_string = 'sqlite:///C:\\WOFpy\\WOFpy\\examples\\swis\\swis2.db'
#. Open a Command Window in the same folder as runserver_multiple.py and enter: python runserver_multiple.py
#. In your command window you should see a message indicating that the service is running along with  instructions for accessing the service.  

To stop an example service, press CTRL+C in the command window.