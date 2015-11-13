"""
WOFpy
-------

WOFpy is a python library for serving CUAHSI's WaterOneflow 1.0 web services

CUAHSI is the Consortium of Universities for the
Advancement of Hydrologic Science, Inc.

"""

from setuptools import Command, setup, find_packages

setup(
    name='WOFpy',
    version='2.0.0001-alpha',
    license='BSD',
    author='James Seppi',
    author_email='james.seppi@gmail.com',
    # note: maintainer gets listed as author in PKG-INFO, so leaving
    # this commented out for now
    maintainer='David Valentine',
    maintainer_email='david.valentine@gmail.com',
    description='a python library for serving WaterOneFlow web services',
    long_description=__doc__,
    keywords='cuahsi his wofpy water waterml cuahsi wateroneflow odm2 czodata',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'flask>=0.6.1',
        'lxml>=2.3',
        'spyne>=2.12.8',
        'nose',
        'python-dateutil==1.5.0',
        'jinja2',
        'pytz'
    ],
    extras_require = {
        'odm1':  ["sqlalchemy", 'pyodbc'],
        'odm2':  ["sqlalchemy",'ODM2API'],
        'sqlite': ["sqlalchemy",'sqlite3'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

)
