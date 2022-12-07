Core Object Methods
===================

createapplication
-----------------

.. note::
    This function is very complicated. Use the GUI to create an application if you are unfamiliar with the application attributes


Here is the meatiest function in the API. In order to create an application, you must provide one mandatory arguement, the application name, as well as these optional arguments:


* attributedict: A dictionary of attributes that can be found by calling the applicationattributesquery method
* appdesc: The description of the application
* appoutdated: Boolean as to whether or not the application needs a recalculation of formula results
* copyappname: If you don't know the application attributes that you specifically want, but you want to make one similar to a current application, pass an existing application's name to this variable and it will return an array of attributes which mirror the existing application's.

You can pass both a copyappname and an attributedict in order to copy an application and then override the existing application's attributes with your own, while keeping the ones you don't override static. Usage:

The arguments for the attributedict are as follows. A quick note; every dictionary entry, even the integers and dates, must be a string data type:


* Necessary:

  * 'Name': the name of the application
  * 'URL': the URL to the application that you're scanning
  * 'Hosts': the IP address or server name where the application is hosted. If necessary, enter multiple values, and separate them by commas
  * 'Development Contact': the name of the development lead
  * 'Business Unit': the name of your ORG (i.e. 9100)
  * 'Description': a description of your scan and scanning reason

* Optional:

  * 'Max Severity': the name of the maximum severity of the application. Accepted values are 'Critical', 'High', 'Medium', and 'Low'
  * 'RR_MaxSeverity': the maximum Risk Rating. Accepted values are integers up to 10
  * 'Tester': the user who is testing. Defaults to the appscan_api
  * 'Type': the type of application to be scanned. Accepted values are 'web', 'mobile', or 'desktop'
  * 'Business Owner': Owner of the application. Usually the section manager.

.. code-block:: python

   mydictionary={
    'Name':'New App',
    'URL':'https://www.example.com/webapp/url',
    'Hosts':'https://www.example.com',
    'Deveopment Contact':'username or my name',
    'Business Unit':'3342',
    'Description':'new javascript application scan from org 3342 to get clearance for external access'
   }
   myClass.createapplication(
    appname='New App',
    attributedict=mydictionary,
    appdesc='a new application from scratch'
   )
   myClass.createapplication(
    appname='New App2',
    attributedict=mydictionary,
    appdesc='a new application copied from an existing one',
    copyappname="Existing App"
   )


jobcreate
---------

.. note::
    It is much, much faster to pass the foldername, policyname, and templatename as their IDs (the function will receive them this way), instead of their names. This is because whichever ones you pass by name are run as queries in order to get them as IDs, thus, when using this function (or any function that asks for names or IDs), it would be much, much faster to simply run a templatequery or a policyquery first, save the ID, then use it in this function instead of the name, thereby executing the query only once instead of multiple times.

.. warning::
    You must use `updatescan`_ in order to actually start this job; it has not been initialized yet.

In addition to the Queries, the program will create jobs. The required attributes are templatename, jobname, foldername, and policyname. To get this information, you may run queries (such as templatequery) to get a list of names to pass. Optional attributes are appname, jobdesc, and jobcontact (jobcontact default is the username used in the initial class, which you cannot create a job without). Usage:

.. code-block:: python

   json_result = myClass.jobcreate(
    jobname='job1',
    foldername='folder1',
    policyname='policy',
    templatename='template',
    jobdesc='description of job',
    jobcontact='user',
    appname='Main'
   )
   json_result = myClass.jobcreate(
    jobname='job1',
    foldername='32',
    policyname='44',
    templatename='16',
    jobdesc='description of job',
    jobcontact='user',
    appname='Main'
   )
   pprint(json_result)

startjob
--------

This function starts any job you would like to run. It takes one mandatory argument, the jobid, and one optional argument, the action you would like to take. Currently Appscan only supports the 'run' argument, so it is defaulted for you to 'run'. Usage:

.. code-block:: python

   pprint(myClass.startjob(jobid=312))

updatescan
----------

.. note::
    In order to make your jobs scan a url, you must also use this method

This method adds information to your job, such as starting url, login username, password, and other information, such as exceptions. This takes three mandatory arguments and one optional argument: jobid, data, and datacode are mandatory, while encrypt is not. Encrypt is a boolean which specifies whether or not you want your data encrypted in the database. Datacode defaults to 'url'. Here is a list of passable arguments for datacode (for a list of descriptions of the following attributes, please visit the apidocs in appscan enterprise):


* url
* username
* password
* method
* header
* lockout
* additionaldomains
* exclusions

Usage:

.. code-block:: python

   pprint(myClass.updatescan(jobid=332, data='https://mysite.to.scan', datacode='url', encrypt=False)
   pprint(myClass.updatescan(jobid=332, data='myname', datacode='username', encrypt=False))
   pprint(myClass.updatescan(jobid=332, data='mypass', datacode='password', encrypt=True)

schedulescan
------------

This method schedules a scan to run at a defined interval. The required arguments are the ``jobid`` which is an integer and the ``scheduleDelta`` which is a timedelta object. The optional arguments are schedule_start (datetime), schedule_end (datetime), exclusionDelta (timedelta), exclusion_start (datetime), and exclusion_end (datetime). Usage:

.. code-block:: python

   from datetime import timedelta, datetime

   # run every week
   delta = timedelta(days=7)
   pprint(myClass.schedulescan(jobid=332, scheduleDelta=delta)

   # run every month except on mondays (monday being the 2nd day of the week) for this November
   delta = timedelta(days=30)
   ex_delta = timedelta(days=2)
   nov_first = datetime(2019, 11, 1, 0, 0, 0)
   nov_last = datetime(2019, 11, 30, 0, 0, 0)
   pprint(myClass.schedulescan(
    jobid=332,
    scheduleDelta=delta,
    exclusionDelta=delta,
    exclusion_start=nov_first,
    exclusion_end=nov_last
   )

deletefolderitem
----------------

This method deletes any folder item. Best practice is to delete a job and it's report in the same query, but the only support for this right now is using the folder item ID. Usage:

.. code-block:: python

   pprint(myClass.deletefolderitem(folderitemid=1001))

adduser
-------

This function allows any user with the right permissions to create other users. The required attributes are the new user's Full Name, desired username, email, and userTypeId. Usage:

.. code-block:: python

   json_result = myClass.adduser(
    realname='Full Name',
    username='username',
    email='user@gmail.com',
    usertype='No Access'
   )
   pprint(json_result)
