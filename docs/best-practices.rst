Best Practices
==============

ID vs Name
----------

Obviously it's convenient to pass a name instead of an id, and most of the functions allow you to do such a thing. However, be warned that if you're executing a loop and you pass a name instead of an id, your program time will suffer:

It is much, much faster to pass the foldername, policyname, and templatename as their IDs (the function will receive them this way), instead of their names. This is because whichever ones you pass by name are run as queries in order to get them as IDs, thus, when using this function (or any function that asks for names or IDs), it would be much, much faster to simply run a templatequery or a policyquery first, save the ID, then use it in this function instead of the name, thereby executing the query only once instead of multiple times.

On Creating Jobs and Scans
--------------------------

If you are creating a job and scan, associate it with an application. If you are unsure which application you should be using, please consult your admin.

On Scanning Systems
-------------------

If you're planning on running a scan, be sure to only run one at a time, unless advised by an admin that you are able run more than one. This library has all the tools necessary to start your scan (startjob), monitor it to make sure it's done running (currentscans), and then run the next one.
