The services will be run. At start, a set of HTML pages with examples is generated.

* http://127.0.0.1:8080/{network}/
* http://127.0.0.1:8080/{network}/rest_1_0/
* http://127.0.0.1:8080/{network}/rest_1_1/
* http://127.0.0.1:8080/{network}/rest_2/
* http://127.0.0.1:8080/{network}/soap/wateroneflow/.wsdl
* http://127.0.0.1:8080/{network}/soap/wateroneflow_1_1/.wsdl

The services can  be found:
* http://127.0.0.1:8080/{network}/rest/1_0
* http://127.0.0.1:8080/{network}/rest/1_1
* http://127.0.0.1:8080/{network}/rest/2
* http://127.0.0.1:8080/{network}/soap/wateroneflow
* http://127.0.0.1:8080/{network}/soap/wateroneflow_1_1

Accessing WOFpy REST Web Services for WaterML 1 and WaterML2
=================================

Running the examples is a great way to learn the REST syntax for accessing data
with WOFpy.  The examples create a web page with sample URIs illustrating
the required syntax.  You can click the URIs in your browser to see the
results.  The syntax is also described below.

* http://127.0.0.1:8080/{network}/rest_1_0/
* http://127.0.0.1:8080/{network}/rest_1_1/

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

WaterML 2
=========
* http://127.0.0.1:8080/{entwork}/rest/2/

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

WSDL Endpoints:
* http://127.0.0.1:8080/{network}/soap/wateroneflow/.wsdl
* http://127.0.0.1:8080/{network}/soap/wateroneflow_1_1/.wsdl
These correspond to SOAP endpoints:
* http://127.0.0.1:8080/{network}/soap/wateroneflow
* http://127.0.0.1:8080/{network}/soap/wateroneflow_1_1

One of the easiest ways to test the SOAP endpoint is to use the free soapUI
program.  To test with soapUI:

#. Install soapUI.
#. Run WOFpy, perhaps using one of the :ref:`examples <examples>`.
#. Start soapUI.
#. In soapUI, click **File**, and then click **Import Project**.
#. Go to test\wofpy-1-1-soapui-project.xml
#. Expand the example request for **GetSites** and double-click
   **GetAllSites** to open that request.
#. At the top of the window, there is a menu with url  like **http://127.0.0.1:8080/TxRivers/soap/wateroneflow/**
   click, select the url for the example, or if you have a new service, **[add new endpoint]**
#. Expand **WOF11 Soap TestSuite**, Double Click **Run Test Case**
#. In window, select URL icon. Run
#. Click the play button to issue the request.  A new window should open with
   the SOAP response showing information about the site.



