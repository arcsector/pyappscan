.. PyAppscan documentation master file, created by
   sphinx-quickstart on Wed Jun 24 14:40:16 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyAppscan's documentation!
=========================================

This python module is used in conjunction with IBM Appscan Enterprise REST API, and allows anyone to do a multitude of things with simple python code. If you would like something added to the program, you may make a pull request, or request that it be added in `the issues section. <https://github.com/arcsector/pyappscan/issues>`_

Legal Disclaimer
----------------

Copyright 2022, by the California Institute of Technology. ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged. Any commercial use must be negotiated with the Office of Technology Transfer at the California Institute of Technology.

This software may be subject to U.S. export control laws. By accepting this software, the user agrees to comply with all applicable U.S. export laws and regulations. User has the responsibility to obtain export licenses, or other export authority as may be required before exporting such information to foreign countries or providing access to foreign persons.

Appscan Version Requirements
----------------------------

Your version of Appscan should be able to support the requisite API calls made by the library. This library is tested with Appscan v9.8.0+, however it is compatible with lower versions (though ymmv).

Dependencies
------------


* requests

Can be installed with:

.. code-block:: shell

   pip install --user pyappscan

How to Use
----------

Use this module by importing the class first, then calling the method you would like to use. It is initiazized with the url to the appscan api, followed by the username, password, featurekey, and ssl cert path (for more information on the feature key, please look at the appscan api docs, which give different options. The default is ``AppscanEnterpriseUser``\ ). Usage:

.. code-block:: python

   from pyappscan import create_engine
   myClass = create_engine(
    'https://route-to-appscan-api.com:443/ase/api',
    username='user',
    password='pass',
    key='AppscanEnterpriseUser',
    verify='/var/www/mycerts/appscancert.crt'
   )

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   best-practices
   special
   queries
   examples
   pyappscan



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
