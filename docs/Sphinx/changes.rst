.. index::
   single: Changes


**********************************************
CHANGES
**********************************************

2.0.0001-alpha
============
* Added ODM2 examples
* Added WOF 1.1 and WaterML 1.1 services
* Simplified the implementation of services

    * Examples properties, like connections, are  configured on the command line.
    * Ability to run multiple services simplified.

* changed to use spyne.io framework

   * Ability to add other transports.
   * aka less dependent on Flask

* WSDL's now internal to the services

   * little more fragile since jinja2 template location may need to be specified