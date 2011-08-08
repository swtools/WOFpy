=====
WOFpy
=====

WOFpy is a Python package that implements CUAHSI's (http://his.cuahsi.org) WaterOneFlow Web service.  WaterOneFlow is a Web service with methods for querying time series of water data at point locations, and which returns data in WaterML format, providing standardized access to water data.   

WOFpy reads data from a Data Access Object (DAO) and translates the data into WaterML.  DAOs can represent a variety of data sources, including databases, text files, and Web sites or services.  You can view example DAOs in the examples folder, or write your own based on the BaseDao class in wof/dao.py.

WOFpy uses Python version 2.6.

Installation
------------

Follow the steps below for Basic installation on a Windows computer.

#. Install **Python 2.6**.  The 32-bit installer is recommended.
#. Add the **Python** folder to your **Path** environment variable.
#. Install **setuptools**. This allows the setup script to be run.
#. Add the **Python/scripts** folder to your **Path** environment variable.
#. Open a command window (run cmd), navigate to the WOFpy folder (with setup.py
   in it), and enter this command: ``python setup.py install``

The wof package (in the subfolder named wof) is now accessible from any directory.

.. note::
    If you edit code in the **wof** folder, you may need to run setup.py again to apply the changes to your system.

Running the Examples
--------------------

Example services are included with WOFpy.  Each example consists of data, Data
Access Objects (DAOs), models, and the service definition.  The examples are
located in the **examples** folder.  See the documentation for more information.  

Publishing Your Data
--------------------

Follow the general steps below to publish your data with WOFpy.

#. Write a new DAO class based on wof.dao.BaseDao; the methods should return objects as defined in wof.models.  This class helps WOFpy read your data. 
#. Write a new config file like those found in the examples, e.g. examples/swis/swis_config.cfg. This file contains static descriptors of your Web service such as the name of your water observations network.
#. Write a new runserver script to use the new DAO you implemented.  See files named runserver_*.py in the examples folder for examples.
#. To test, open a command window, navigate where your runserver file is located, and use Python to run the script, e.g., python runserver.py.

Unit Tests
----------

After everything is installed, open a command window and navigate to your WOFpy/test/ folder.  Type "nosetests -v" to run the included tests.  If they all pass, then congratulations!
