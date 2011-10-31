.. WOFpy documentation master file, created by
   sphinx-quickstart on Thu Jun 09 13:37:45 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to WOFpy!
=================
.. image:: /graphics/WOFpy_logo.png

What is WOFpy?
--------------

**WOFpy** stands for **Water One Flow in Python**.  It is designed to produce WaterML 
web services from a variety of back-end database formats, e.g. SQLite, 
Microsoft SQL server, PostgreSQL, etc.  It is a key part of the Python services stack developed by
the **Texas Water Development Board** for **'Water Data for Texas'** - a unified hydrological 
information system that shares environmental data for the state of Texas.  

How do I get started?
---------------------

The latest version of WOFpy is available for download via Github (https://github.com/swtools/WOFpy).  
Once downloaded, you can follow the following steps to get **WOFpy and its dependencies installed** 
and to start and access the **example web services** that come pre-packaged with WOFpy.
 
.. toctree::
   :maxdepth: 3
   
   GettingStarted   

What goes on inside WOFpy?
--------------------------

From a conceptual point of view, WOFpy can be compared to a **restaurant** that serves data.  **Data consumers** 
are the restaurant customers.  The **data providers** create the agricultural produce (i.e. **raw data**) and stock 
the pantry (i.e. **provider's database**).  However before the produce can be consumed they need to be first prepared 
into a palatable form (i.e. **WaterML**).  This requires a restaurant (i.e. **WOFpy**) with a smart catering staff 
(i.e. **WOFpy components**) to select, cook and serve (i.e. **extract, transform and load**) the dishes.
   
.. image:: /graphics/ARestaurantAnalogyForWOFpy_55.png

The components within WOFpy are further explained in the following links:

.. toctree::
   :maxdepth: 3

   WOFpyArchitecture   
   
How do I use WOFpy to publish my data?
--------------------------------------
.. toctree::
   :maxdepth: 3
   
   PublishingWithWOFpy
   CsvDaoTutorial

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

Developers
==========
.. image:: /graphics/companylogos.png
