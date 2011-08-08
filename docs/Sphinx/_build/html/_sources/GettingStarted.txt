.. _Getting Started:

***************
Getting Started
***************

Here is a quick guide to getting WOFpy up and running.

Installation
============

Follow the steps below to install WOFpy and its prerequisites on a Windows
computer.

#. Install **Python 2.6**.  The 32-bit installer is recommended.
#. Add the **Python** folder to your **Path** environment variable.
#. Install **setuptools**. This allows the setup script to be run.
#. Add the **Python/scripts** folder to your **Path** environment variable.
#. Open a command window (run cmd), navigate to the WOFpy folder (with setup.py
   in it), and enter this command: ``python setup.py install``

The wof package (in the subfolder named **wof**) is now accessible from any
directory.

.. note::
    If you edit code in the **wof** folder, you may need to run setup.py again
    to apply the changes to your system.

.. _examples:

Running the Examples
====================

Example services are included with WOFpy.  Each example consists of data, Data
Access Objects (DAOs), models, and the service definition.  The examples are
located in the **examples** folder.

The general procedure for each example is to set up any required data
connections, use Python to run the runserver.py script, and test the service
using a Web browser or other client application.  The script should print
service endpoint URIs in the window used to execute the script.

When testing is complete, you should stop the service.  For example, if you
started the service using a command window in Windows, you can stop the service
by pressing ``CTRL+C`` in the command window.

.. note::
    These examples are run in debug mode for demonstration purposes.  In a
    production environment, you would use something like IIS or Apache to
    manage the service.

The examples are described in more detail below.

.. _barebones-example:

Barebones SQLite Example
------------------------

This example is located in the **examples/barebones** folder.

This example shows how to access a very simple SQLite database located in the
**LCM_Data** subfolder.  The database only has three tables in it: one for
sites, one for variables, and one for data values.  The remaining information
required for WaterML is read from a config file.

Follow the steps below to run this example.

#. Open a command window in the **examples/barebones** folder and enter:
   ``python runserver_LCM.py``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.  

.. _swis-example:

SWIS SQLite Example
-------------------

This example is located in the **examples/swis** folder.

This example shows how to access a more complicated SQLite database based on
early designs of the Texas Water Development Board's Surface Water Information
System (SWIS) database.

Follow the steps below to run this example.

#. Open a command window in the **examples/swis** folder and enter:
   ``python runserver_swis.py``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.  

ODM SQL Server Example
----------------------

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
#. In the odm_sqlserver folder, create a file named **private_config.py** with
   a variable named **lbr_connection_string** set to a SQLAlchemy-compatible
   database connection string for the Little Bear River database, e.g.,
   ``lbr_connection_string =
   'mssql+pyodbc://username:password@(local)/LittleBear11'``
#. Open a command window in the **examples/odm_sqlserver** folder and enter:
   ``python runserver_lbr.py``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.  

CBI External Service Example
----------------------------

This example is located in the **examples/cbi** folder.

This example shows how to access a Web service provided by the Conrad Blucher
Institute (CBI) for the Texas Coastal Ocean Observation Network (TCOON).
TCOON is a live network with new values continuously pouring in from sensors
along the Texas coast.  Data access is provided by a variant of the OGC's
Sensor Observation Service (SOS).  We will provide access to the data with
a WaterOneFlow service by wrapping the TCOON SOS service with our data access
object (DAO) and supporting modules.  Because site and variable descriptions
do not change frequently in TCOON, we store that information in a local SQLite
database.  The result is a Web service that uses both a SQLite database and
another Web service to provide data to the client.  Of course, the client has
no idea that this is happening.  All the client cares about is that we provide
access using a standard WaterOneFlow service and send responses back in WaterML
format!

This example requires an internet connection to access the TCOON Web service.
To prepare your service, you will make a cache of sites and variables available
from TCOON.  Then you will run the service.

Follow the steps below to run this example.

#. Open a command window in the **examples/cbi** folder and enter:
   ``python build_cbi_cache.py``
#. In the command window, enter:
   ``python runserver_cbi.py``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.  

Multiple Services Example
-------------------------

This example is located in the **examples** folder.

This folder contains a **runserver_multiple.py** script demonstrating how to
run multiple services at once.  It uses the
:ref:`barebones <barebones-example>` and :ref:`SWIS <swis-example>` examples.
Follow the steps below to run this example.

#. Open a command window in the **examples** folder and enter:
   ``python runserver_multiple.py``
#. In your command window you should see a message indicating that the service
   is running along with instructions for accessing the service.  

Accessing WOFpy REST Web Services
=================================

Running the examples is a great way to learn the REST syntax for accessing data
with WOFpy.  The examples create a web page with sample URIs illustrating
the required syntax.  You can click the URIs in your browser to see the
results.  The syntax is also described below.

All query results are provided in WaterML 1.0 unless specified otherwise.

Getting Site Locations
----------------------

* **GetSites** - Returns locations of all sites
* **GetSites?site=network:site_code** - Returns location of site with given
  site code in given network

Discovering What Is Measured at a Site
--------------------------------------

* **GetSites?site=network:site_code** - Returns location of given site and 
  summary of all time series available at the site

Getting Information about Variables
-----------------------------------

* **GetVariableInfo** - Returns descriptions of all variables
* **GetVariableInfo?variable=vocabulary:variable_code** - Returns description
  of variable with given variable code within the given vocabulary

Downloading Time Series Values
------------------------------

* **GetValues?location=network:site_code&variable=vocabulary:variable_code** -
  Returns all data at the given site for the given variable
* **GetValues?location=network:site_code&variable=vocabulary:variable_code&startDate=YYYY-MM-DDThh:mm&endDate=YYYY-MM-DDThh:mm** -
  Returns data at the given site for the given variable intersecting the given
  time period

.. note::
    The time format is `ISO time
    <http://www.iso.org/iso/date_and_time_format>`_.  You can leave out the
    time component and just write YYYY-MM-DD.  You can specify time zone by
    appending the offset from Universal Time Coordinates (UTC) in hours to the
    end of the date string, or by appending Z to indicate UTC.  For example,
    to specify April 5, 2011, 5:00 PM in US Central Standard Time:
    ``2011-04-05T05:00-06``
    
    See `Wikipedia <http://en.wikipedia.org/wiki/ISO_8601>`_ for more examples.

* **GetValues?format=wml2&location=network:site_code&variable=vocabulary:variable_code&startDate=YYYY-MM-DDThh:mm&endDate=YYYY-MM-DDThh:mm** -
  Returns data at the given site for the given variable intersecting the given
  time period in WaterML 2.0 format.

.. note::
    WaterML 2.0 format is only available for GetValues requests.    

Accessing WOFpy SOAP Web Services
=================================

The SOAP endpoint follows the WaterOneFlow standard, whose method signatures
and WaterML responses are described on the HIS website at
http://his.cuahsi.org/wofws.html.

One of the easiest ways to test the SOAP endpoint is to use the free soapUI
program.  To test with soapUI:

#. Install soapUI.
#. Run WOFpy, perhaps using one of the :ref:`examples <examples>`.
#. Start soapUI.
#. In soapUI, click **File**, and then click **New soapUI Project**.
#. Give your project any name, input the URI to your SOAP endpoint, and click
   **OK**.
#. Expand the example request for **GetSiteInfoObject** and double-click
   **Request1** to open that request.
#. Input a valid network:site_code in the **site** parameter.  You can use the
   default parameter provided on the Web page for the REST endpoint of your
   service.
#. Click the play button to issue the request.  A new window should open with
   the SOAP response showing information about the site.