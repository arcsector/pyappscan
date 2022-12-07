
Object Queries
==============

This page explains the Query subclass. In order to use any of the queries in this subclass, you must call it as ``pyappscan.[MYQUERY]``.

Default Calling Structure
-------------------------

The program has different queries to help you return different sets of data, such as a list of folders, or policies. You can sift through this data by adding the function arguments: name and category. The name is the value in the category you would like to search. If you do not choose to specify these arguments, the entire response dictionary will be returned (if any). Usage:

.. code-block:: python

   pprint(myClass.templatequery())
   pprint(myClass.templatequery(name='Default Template', category='name'))

Queries that follow this calling structure
------------------------------------------


* ``applicationquery``
* ``currentscans``
* ``folderquery``
* ``issuetypes``
* ``templatequery``
* ``scannerquery``
* ``testpolicyquery``
* ``userquery``
* ``usertypequery``

Queries that Deviate from Default Structure
-------------------------------------------


* `aboutissue`_
* `appissuequery`_
* `applicationattributequery`_
* `buildfoldertree`_
* dashboardquery
* dastquery
* `folderjobsquery`_
* `issuequery`_
* permissionquery
* `reportquery (DEPRECATED)`_
* `reportjsonquery`_
* `issuetypequery`_
* `folderitemsquery`_
* `folderitemquery`_

aboutissue
----------

This function gets an html document showing the issue type, description, generation method, and payload, as well as the response received and the fix information. Usage:

.. code-block:: python

   pprint(myClass.aboutissue(appid=93, issueid=31986138))
   pprint(myClass.aboutissue(appid="App Name", issueid=31986138))

appissuequery
-------------

Issue query is a bit different from all the rest of the queries. It takes five optional arguments:


* The name of the application you would like to search issues for. Defaults to quering all available applications and their issues.
* The severity level of the issues you would like to see. Inheritance applies (accepted values: 'High', 'Medium', 'Low'), meaning if you only want to see medium and low issues, you should specify medium, because low issues inherit medium value. Default value is High.
* The column you would like to sort by. Accepted values: 'Severity', 'Location', 'Issue Type', 'Element'. Defaults to Severity.
* Whether you want to include issues with a severity of 'information' (True/False). Defaults to False.
* How many issues you want to pull, with the default being the first 100

Usage:

.. code-block:: python

   pprint(myClass.appissuequery())
   pprint(myClass.appissuequery(
     appname='Main',
     severity='Medium',
     sortBy='Issue Type',
     includeinfoseverity=True,
     itemcount=1000
    )
   )

applicationattributequery
-------------------------

This function returns json data on application attributes. You can use this as a reference to create new applications. It takes one mandatory argument, the appid:

.. code-block:: python

   pprint(myClass.applicationattributequery(appid=10))
   pprint(myClass.applicationattributequery(appid=10))

buildfoldertree
---------------

This function displays a directory tree of folders that we have. If you need a visual representation of it, or just need to look up a file name, this is a good function to use. Usage:

.. code-block:: python

   pprint(myClass.buildfoldertree())

currentscans
------------

If you need a list of currently running scans, you can use the currentscans method to do so. This method is called similarly to the queries, where you can just print the function to see all current scans, or you can print a current scan that's running by adding an identifier of the scan along with the category. Usage:

.. code-block:: python

   pprint(myClass.currentscans())
   pprint(myClass.currentscans(name=1,category='id'))

folderjobsquery
---------------

This function gets all DAST-type jobs in a folder, with only the folder name or id provided. You may also provide a jobname or ID in order to just return the job dictionary. Usage:

.. code-block:: python

   pprint(myClass.folderjobsquery('Main Folder', 'Job Name'))
   pprint(myClass.folderjobsquery(335, 13))

issuequery
----------

This function takes one mandatory argument with three optional arguments: the mandatory argument is either the report id or the appid, and the optional ones are the issueid and zipfile. You can enter a reportid or appid to get all the issues in a specified report or app, and you can also get a specific issue with the use of the issueid. In addition, if you're using an app, you can specify the zipfile argument as ``True`` in order to return a zip bit stream. You can also specify an number of issues you'd like to get, with the default being the first 100. Usage:

.. code-block:: python

   pprint(myclass.issuequery(reportid=1344))
   pprint(myclass.issuequery(appid=1382, issueid=7894175831, zipfile=True))
   pprint(myclass.issuequery(appid="App Name", issuecount=1000))

reportquery (DEPRECATED)
------------------------

This function is used to get a report summary (contains no issueid's but does have a count of the number of issues sorted by severity), or a report of the issues and their issue id's. Usage:

.. code-block:: python

   pprint(myClass.reportquery(reportid=31986, issues=True))

reportjsonquery
---------------

This function is a json version of ``reportquery``. Eventually ``reportquery`` will be aliased to this function, but for now I will leave it. This function allows you to get a detailed breakdown of the report packs generated by a scan job. It takes one mandatory argument, the ``reportid`` (which is either the report ID or the report name), and two optional arguments, ``issues`` and ``summary``. The ``issues`` parameter is used to get a report along with detailed information about each individual issue in the report (such as traffic summary, and other information), whereas the ``summary`` parameter is used to generate a base-level summary about issues found in the report, such as severity level and count. Usage:

.. code-block:: python

   pprint(myClass.reportjsonquery(12345))
   pprint(myClass.reportjsonquery(12345, issues=True))
   pprint(myClass.reportjsonquery(12345, summary=True))

How do reportquery(reportid) and issuequery(reportid) differ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``reportquery(reportid)`` returns a report xml document of issues and issueids. ``issuequery(reportid)`` returns a list of issue xml documents, detailing issues further than the reportquery does.

issuetypequery
--------------

This function gets information about a specific issue type. Multiple issues can have the same issue type. For information about fixes and advisory on the issue type, see this query. It takes one mandatory argument, and two optional arguments: issuetypeid is the mandatory one, and lookuptype and lookupname are the optional arguments. Accepted values for lookuptype are "advisory" or "fix". Usage:

.. code-block:: python

   pprint(myClass.issuetypequery(issuetypeid=525))
   pprint(myClass.issuetypequery(issuetypeid="Issue Name", lookuptype='advisory'))
   pprint(myClass.issuetypequery(issuetypeid="Issue Name", lookuptype='fix', lookupname='wf-security-check-attcrosssitescripting'))

folderitemsquery
----------------

This function returns items in a folder, not just DAST-configured jobs like `\ ``folderjobsquery`` <#folderjobsquery>`_. This will return any item in a folder, be it report pack, content scan job, dashboard, template, and all other types. It has one mandatory argument and three optional arguments. The mandatory argument is ``folderid`` which is the name/id of the folder you'd like to use. The optional arguments are ``keyword``\ , ``name``\ , and ``category``. Name and category function the same as the default call structure. Keyword is simply an easy way to ensure you get a certain type of folder item. Accepted values are below, along with the item descriptions, with more possibly available:


* ``report-pack``\ : a report pack of scan issues
* ``content-scan-job``\ : a job-type, whether DAST or otherwise
* ``dashboard``\ : a display configuration
* ``import-job``\ : config for importing issues from other appscan versions

Usage:

.. code-block:: python

   pprint(myClass.folderitemsquery(folderid=20))
   pprint(myClass.folderitemsquery(folderid="Folder Name", keyword="report-pack"))
   pprint(myClass.folderitemsquery(folderid="Folder Name", keyword="report-pack", name="My Report pack name", category="name"))

folderitemquery
---------------

This function gets information about a specific folderitem. This gets much more granular than ``folderitemsquery``. It accepts one mandatory argument, ``folderitemid`` which can be id or name, and one of four optional arguments: ``options``\ , ``reports``\ , ``scanlog``\ , and ``statistics``. Usage:

.. code-block:: python

   pprint(myClass.folderitemquery(folderitemid=1110))
   pprint(myClass.folderitemquery(folderitemid="my folder item name", options=True))
   pprint(myClass.folderitemquery(folderitemid=1110, statistics=True))
