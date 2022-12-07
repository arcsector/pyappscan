from .exceptions import UserTypeError, DataCodeError
from time import time
from datetime import datetime
from .query import Query
from typing import Dict, Union, Any

class PyAppscan(Query):
	"""Main class that is returned when called from :func:`pyappscan.create_engine`

	Note:
		You may be wondering why there is no ``deletejob`` method. This is because you
		cannot directly delete jobs via the API, you have to delete the folder item.
		This can be done using the :meth:`deletefolderitem` method, during which you
		should also delete the associated report, as not deleting it causes issues with
		Appscan internals.

	Args:
		baseurl (str): Base URL for appscan
		username (str, optional): Username to log in with; used in conjunction with ``password``. Defaults to None.
		password (str, optional): Password to log in with; used in conjunction with ``username``. Defaults to None.
		key (str, optional): Feature Key to log in as. Defaults to "AppscanEnterpriseUser".
		apikey (str, optional): API Key to log in with; used in conjunction with ``secretkey``. Defaults to None.
		secretkey (str, optional): API Secret to log in with; used in conjunction with ``apikey``. Defaults to None.
		verify (bool, optional): Certificate path for requests. Defaults to False.
	
	Attributes:
		baseurl (str): Base URL for appscan
		username (str): Username to log in with; used in conjunction with ``password``. Defaults to None.
		password (str): Password to log in with; used in conjunction with ``username``. Defaults to None.
		key (str): Feature Key to log in as. Defaults to "AppscanEnterpriseUser".
		apikey (str): API Key to log in with; used in conjunction with ``secretkey``. Defaults to None.
		secretkey (str): API Secret to log in with; used in conjunction with ``apikey``. Defaults to None.
		verify (bool): Certificate path for requests. Defaults to False.
		logger (:class:`logging.Logger`): logger for pyappscan; this can be overwritten by running the following
			on an instantiated object:

				>>> app.logger.handlers = []
	"""
	def __init__(self, baseurl: str, username: str = None, password: str = None, key: str ='AppscanEnterpriseUser', apikey: str = None, secretkey: str = None, verify: bool = True):
		super(PyAppscan, self).__init__(baseurl=baseurl, username=username, password=password, key=key, apikey=apikey, secretkey=secretkey, verify=verify)

	def adduser(self, realname: str, username: str, email: str, usertype: Union[str, int]) -> Dict[str, str]:
		"""Add a user to appscan with a given usertype

		Args:
			realname (str): Real name of the user
			username (str): Desired user name of the user
			email (str): Email of the user
			usertype (Union[str, int]): Usertype ID; if string, usertype ID will be grabbed

		Raises:
			UserTypeError: Not a valid user type; valid user types can be found using
				the :meth:`usertypequery` method

		Returns:
			Dict[str, str]: Result of user submission

		References:
			:meth:`pyappscan.query.Query.usertypequery`
		"""
		try:
			if bool(int(usertype)) != True:
				usertype = self.usertypequery(usertype,'name')
				if usertype == None:
					raise UserTypeError()
				else:
					usertype=int(usertype['id'])
		except ValueError:
			usertype = int(usertype)
		r = self.login()
		dic = {
			'fullName':realname,
			'userName':username,
			'email':email,
			'userTypeId':usertype
		}
		result = r.post(self.baseurl+'consoleusers', json=dic, verify=self.verify)
		return self.returnobject(result)

	def createuser(self, realname: str, username: str, email: str, usertype: Union[str, int]) -> Dict[str, str]:
		"""Alias for :meth:`adduser` for convenience

		References:
			:meth:`adduser`
		"""
		return self.adduser(realname, username, email, usertype)

	def jobcreate(self, jobname: str, policyname: Union[str, int], foldername: Union[str, int], 
		templatename: Union[str, int], jobdesc: str = None, jobcontact: str = None, appname: Union[str, int] = None) -> Dict[str, str]:
		"""Create a folder job

		Note:
			In order to initialize a job you have to run :meth:`updatescan` to 
			specify a starting URL.

		Args:
			jobname (str): Job name
			policyname (Union[str, int]): Policy ID or Name
			foldername (Union[str, int]): Folder ID or Name
			templatename (Union[str, int]): Template ID or Name
			jobdesc (str, optional): Job Description. Defaults to None.
			jobcontact (str, optional): Job contact. Defaults to None.
			appname (Union[str, int], optional): Application ID or Name to associate 
			with the job. Defaults to None.

		Returns:
			Dict[str, str]: Results of job creation including assigned Job ID

		References:
			:meth:`updatescan`
		"""
		r = self.login()
		dic = {'name':jobname}
		try:
			if bool(int(policyname)) != True:
				dic['testPolicyId'] = self.testpolicyquery(policyname,'name')['id']
			else:
				dic['testPolicyId'] = int(policyname)
		except ValueError:
			dic['testPolicyId'] = self.testpolicyquery(policyname,'name')['id']
		try:
			if bool(int(foldername)) != True:
				dic['folderId'] = self.folderquery(foldername,'folderName')['folderId']
			else:
				dic['folderId'] = int(foldername)
		except ValueError:
			dic['folderId'] = self.folderquery(foldername,'folderName')['folderId']
		if appname != None:
			try:
				if bool(int(appname)) != True:	
					dic['applicationId'] = self.applicationquery(appname,'name')['id']
				else:
					dic['applicationId'] = int(appname)
			except ValueError:
				dic['applicationId'] = self.applicationquery(appname,'name')['id']
		if jobdesc != None:
			dic['description'] = jobdesc
		if jobcontact == None:
			dic['contact'] = self.username
		else:
			dic['contact'] = jobcontact
		try:
			if bool(int(templatename)) != True:
				templateid = str(self.templatequery(templatename,'name')['id'])
			else:
				templateid = str(templatename)
		except ValueError:
			templateid = str(self.templatequery(templatename,'name')['id'])
		result = r.post(self.baseurl+'jobs/'+templateid+'/dastconfig/createjob', json=dic, verify=self.verify)
		return self.returnobject(result)
	
	def createjob(self, jobname: str, policyname: Union[str, int], foldername: Union[str, int], 
		templatename: Union[str, int], jobdesc: str = None, jobcontact: str = None, appname: Union[str, int] = None) -> Dict[str, str]:
		"""Alias for :meth:`jobcreate`

		References:
			:meth:`jobcreate`
		"""
		return self.jobcreate(jobname, policyname, foldername, templatename, jobdesc, jobcontact, appname)

	def updatescan(self, jobid: int, data: str, datacode: str = 'url', encrypt: bool = False) -> Dict[str, Any]:
		"""Updates variables in a given job

		Args:
			jobid (int): Job ID
			data (str): Data value to send to datacode
			datacode (str, optional): Data code to apply value to on given job. Defaults to 'url'. Acceptable entries:
				* ``url``
				* ``username``
				* ``password``
				* ``method``
				* ``header``
				* ``lockout``
				* ``additionaldomains``
				* ``exclusions``
			encrypt (bool, optional): Whether or not to encrypt data; should be 
			done when datacode is ``username`` or ``password`` or when other 
			sensitive info is being uploaded, like ``header`` auth tokens. Defaults to False.

		Raises:
			DataCodeError: When ``datacode`` is not valid.

		Returns:
			Dict[str, Any]: Result of scan update
		"""
		r = self.login()
		dic={
			'scantNodeNewValue':data,
			'encryptNodeValue':encrypt
		}
		if datacode == 'url' or datacode == 'URL':
  			dic['scantNodeXpath'] = 'StartingUrl'
		elif datacode == 'username' or datacode == 'Username':
			dic['scantNodeXpath'] = 'LoginUsername'
		elif datacode == 'password' or datacode == 'Password':
			dic['scantNodeXpath'] = 'LoginPassword'
		elif datacode == 'method' or datacode == 'Method':
			dic['scantNodeXpath'] = 'LoginMethod'
		elif datacode == 'header' or datacode == 'Header' or datacode == 'headers' or datacode == 'Headers':
			dic['scantNodeXpath'] = 'CustomHeaders'
		elif datacode == 'lockout' or datacode == 'Lockout':
			dic['scantNodeXpath'] = 'AccountLockout'
		elif datacode == 'additionaldomains' or datacode == 'AdditionalDomains':
			dic['scantNodeXpath'] = 'AdditionalDomains'
		elif datacode == 'exclusions' or datacode == 'Exclusions':
			dic['scantNodeXpath'] = 'Exclusions'
		else:
			raise DataCodeError()
		result = r.post(self.baseurl+'jobs/'+str(jobid)+'/dastconfig/updatescant', json=dic, verify=self.verify)
		return self.returnobject(result)

	def schedulescan(self, jobid: int, scheduleDelta: timedelta, schedule_start: datetime = None, schedule_end: datetime = None,
		exclusionDelta: timedelta = None, exclusion_start: datetime = None, exclusion_end: datetime = None) -> Dict[str, str]:
		"""Schedule scan for recurring scanning

		Note:
			This feature is still in beta.

		Args:
			jobid (int): Job ID
			scheduleDelta (:class:`datetime.timedelta`): interval to schedule at
			schedule_start (:class:`datetime.datetime`, optional): time to start scan schedule. Defaults to None.
			schedule_end (:class:`datetime.datetime`, optional): time to end scan schedule. Defaults to None.
			exclusionDelta (:class:`datetime.timedelta`, optional): interval to exlude during. Defaults to None.
			exclusion_start (:class:`datetime.datetime`, optional): time to start exclusion schedule. Defaults to None.
			exclusion_end (:class:`datetime.datetime`, optional): time to end exclusion schedule. Defaults to None.

		Returns:
			Dict[str, str]: Schedule result
		"""
		r = self.login()

		strftime_format = "%Y/%m/%d %H:%M %p"
		schedule_string, schedule_cat = self.deltaToString(scheduleDelta)
		dic = {
			"enableSchedule": True,
			"scheduleStartDate": datetime.now().strftime(strftime_format),
			"scheduleFrequency": {},
			"enableExclusion": False,
			"exclusionStartDate": datetime.now().strftime(strftime_format),
			"exclusionFrequency": {}
		}

		dic['scheduleFrequency'][schedule_cat] = schedule_string
		if schedule_start != None:
			dic['scheduleStartDate'] = schedule_start.strftime(strftime_format)
		if schedule_end != None:
			dic['scheduleEndDate'] = schedule_end.strftime(strftime_format)

		if exclusionDelta != None:
			exclusion_string, exclusion_cat = self.deltaToString(exclusionDelta)
			dic['exclusionFrequency'] = {exclusion_cat: exclusion_string}
			dic['enableExclusion'] = True

		if exclusion_start != None:
			dic['exclusionStartDate'] = exclusion_start.strftime(strftime_format)
		if exclusion_end != None:
			dic['exclusionEndDate'] = exclusion_end.strftime(strftime_format)
		
		result = r.post(self.baseurl + 'jobs/schedulescan/' + str(jobid), json=dic, verify=self.verify)
		return self.returnobject(result)

	def updatejob(self, jobid: int, jobname: str, policyname: Union[int, str], foldername: Union[int, str], 
		templatename: Union[int, str], jobdesc: str = None, jobcontact: str = None, appname: Union[int, str]=None) -> Dict[str, str]:
		"""Update job information

		Args:
			jobid (int): Job ID
			jobname (str): Job name
			policyname (int OR str): Policy ID or Name
			foldername (int OR str): Folder ID or Name
			templatename (int OR str): Template ID or Name
			jobdesc (str, optional): Job Description. Defaults to None.
			jobcontact (str, optional): Job contact. Defaults to None.
			appname (int OR str, optional): Application ID or Name to associate 
			with the job. Defaults to None.

		Returns:
			dict: Results of job update
		"""
		r = self.login()
		dic = {'name':jobname}
		try:
			if bool(int(policyname)) != True:
				dic['testPolicyId'] = self.testpolicyquery(policyname,'name')['id']
			else:
				dic['testPolicyId'] = int(policyname)
		except ValueError:
			dic['testPolicyId'] = int(policyname)
		try:
			if bool(int(foldername)) != True:
				dic['folderId'] = self.folderquery(foldername,'folderName')['folderId']
			else:
				dic['folderId'] = int(foldername)
		except ValueError:
			dic['folderId'] = int(foldername)
		if appname != None:
			try:
				if bool(int(appname)) != True:	
					dic['applicationId'] = self.applicationquery(appname,'name')['id']
				else:
					dic['applicationId'] = int(appname)
			except ValueError:
				dic['applicationId'] = int(appname)
		if jobdesc != None:
			dic['description'] = jobdesc
		if jobcontact == None:
			dic['contact'] = self.username
		else:
			dic['contact'] = jobcontact
		Etag = r.get(self.baseurl+'jobs/'+str(jobid), verify=self.verify)
		header={'If-Match':Etag.headers['ETag']}
		result = r.put(self.baseurl+'jobs/'+str(jobid), json=dic, headers=header, verify=self.verify)
		return self.returnobject(result)
	
	def startjob(self, jobid: int, action: str = 'run') -> Dict[str, str]:
		"""Start a scan on a job

		Args:
			jobid (int): Job ID
			action (str, optional): Action to take; only exists for extensibility, as 
				the only supported action as of writing is ``run``. Defaults to 'run'.

		Returns:
			Dict[str, str]: Result of job start
		"""
		r = self.login()
		if action == 'run' or action == 'Run' or action == 'RUN':
			dic={'type':'run'}
		Etag = r.get(self.baseurl+'jobs/'+str(jobid), verify=self.verify)
		header={'If-Match':Etag.headers['ETag']}
		result = r.post(self.baseurl+'jobs/'+str(jobid)+'/actions', json=dic, headers=header, verify=self.verify)
		return self.returnobject(result)
	
	def startscan(self, jobid: int, action: str = 'run') -> Dict[str, str]:
		"""Alias for :meth:`startjob`

		References:
			:meth:`startjob`
		"""
		return self.startjob(jobid, action)
	
	def createapplication(self, appname: str, attributedict: Dict[str, str] = None, 
		appdesc: str = None, appoutdated: bool = False, copyappname: str = None) -> Dict[str, Any]:
		"""Create application from attribute dictionary

		Note that the dictionary structure is:
		dict
		----dict
		--------list
		------------dict

		Note:
			When giving a ``copyappname`` and an ``attributedict``, you will overwrite only the entries in the
			``copyappname`` app's attriute dictionary which exist in the ``attributedict``.

		Args:
			appname (str): Application name
			attributedict (dict, optional): Attribute dictionary for application; you can find this by querying :meth:`applicationattributequery`. Defaults to None.
			appdesc (str, optional): App description. Defaults to None.
			appoutdated (bool, optional): Is the app outdated. Defaults to False.
			copyappname (str, optional): Application to copy and merge attributes. Defaults to None.

		Raises:
			ValueError: Raised when neither ``attributedict`` or ``copyappname`` are given,
				although they can both be given to merge attributes

		Returns:
			Dict[str, Any]: Result of app creation, including app ID

		References:
			:meth:`pyappscan.query.Query.applicationattributequery`
		"""
		r = self.login()
		attrlist = []
		currenttime = int(time()*1000)
		if attributedict == None and copyappname == None:
			raise ValueError("You must have either an attribute dictionary or a copyappname")
		if copyappname != None:
			oldliss = self.applicationattributequery(copyappname)['attributeCollection']['attributeArray']
			attributedictcopy = {}
			if attributedict != None:
				self.attributecheck(attributedict)
				oldlisscopy = {}
				for i in oldliss:
					oldlisscopy[i['name']] = i['value']
				if type(attributedict) != list:
					for k,v in attributedict:
						oldlisscopy[k] = v
					attrlist = oldlisscopy
				else:
					for i in attributedict:
						attributedictcopy[i['name']] = i['value']
					for k,v in attributedictcopy:
						oldlisscopy[k] = v
					attrlist = oldlisscopy
				attrlist = self.dicttolistofdicts(attrlist)
			else:
				attrlist = oldliss
		else:
			self.attributecheck(attributedict)
			if type(attributedict) != list:
				attrlist = self.dicttolistofdicts(attributedict)
			else:
				attrlist = attributedict
		#dictionary struct is:
		#dict
		#    dict
		#        list
		#            dict
		secondarydic = {"attributeArray" : attrlist}
		primarydic = {
			"attributeCollection" : secondarydic,
			"name" : appname,
			"dateCreated" : currenttime,
			"lastUpdated" : currenttime
		}
		if appdesc != None:
			primarydic['description'] = appdesc
		if appoutdated == True:
			primarydic['isOutOfDate'] = 1
		elif appoutdated == False:
			primarydic['isOutOfDate'] = 0
		else:
			primarydic['isOutOfDate'] = 2
		result = r.post(self.baseurl+'applications', json=primarydic, verify=self.verify)
		return self.returnobject(result)

	def updateapplication(self, appid: int, appname: str, attributedict: Dict[str, Any] = None, 
		appdesc: str = None, appoutdated: bool = False, copyappname: str = None) -> Dict[str, Any]:
		"""Update application

		Args:
			appid (int): App ID
			appname (str): Application name
			attributedict (dict, optional): Attribute dictionary for application; you can find this by querying :meth:`applicationattributequery`. Defaults to None.
			appdesc (str, optional): App description. Defaults to None.
			appoutdated (bool, optional): Is the app outdated. Defaults to False.
			copyappname (str, optional): Application to copy and merge attributes. Defaults to None.

		Raises:
			ValueError: Raised when neither ``attributedict`` or ``copyappname`` are given,
				although they can both be given to merge attributes

		Returns:
			Dict[str, Any]: Result of app creation, including app ID
		"""
		r = self.login()
		attrlist = []
		currenttime = int(time()*1000)
		if attributedict == None and copyappname == None:
			raise ValueError("You must have either an attribute dictionary or a copyappname") 
		if copyappname != None:
			oldliss = self.applicationattributequery(copyappname)['attributeCollection']['attributeArray']
			attributedictcopy = {}
			if attributedict != None:
				self.attributecheck(attributedict)
				oldlisscopy = {}
				for i in oldliss:
					oldlisscopy[i['name']] = i['value']
				if type(attributedict) != list:
					for k,v in attributedict:
						oldlisscopy[k] = v
					attrlist = oldlisscopy
				else:
					for i in attributedict:
						attributedictcopy[i['name']] = i['value']
					for k,v in attributedictcopy:
						oldlisscopy[k] = v
					attrlist = oldlisscopy
				attrlist = self.dicttolistofdicts(attrlist)
			else:
				attrlist = oldliss
		else:
			self.attributecheck(attributedict)
			if type(attributedict) != list:
				attrlist = self.dicttolistofdicts(attributedict)
			else:
				attrlist = attributedict
		#dictionary struct is:
		#dict
		#    dict
		#        list
		#            dict
		secondarydic = {"attributeArray" : attrlist}
		primarydic = {
			"attributeCollection" : secondarydic,
			"name" : appname,
			"dateCreated" : currenttime,
			"lastUpdated" : currenttime
		}
		if appdesc != None:
			primarydic['description'] = appdesc
		if appoutdated == True:
			primarydic['isOutOfDate'] = 1
		elif appoutdated == False:
			primarydic['isOutOfDate'] = 0
		else:
			primarydic['isOutOfDate'] = 2
		if type(appid) != int:
			appid = str(self.applicationquery(appid, 'name')['id'])
		else:
			appid = str(appid)
		result = r.put(self.baseurl+'applications'+appid, json=primarydic, verify=self.verify)
		return self.returnobject(result)

	def deleteapplication(self, appid: int) -> Dict[str, str]:
		"""Delete application

		Args:
			appid (int): Application ID

		Raises:
			ValueError: raised if App ID is :class:`None`

		Returns:
			Dict[str, str]: Result of deletion
		"""
		try:
			if bool(int(appid)) != True:
				appid == self.applicationquery(appid, 'name')['id']
		except ValueError:
			if appid == None:
				raise ValueError("appid can't be NoneType")
			else:
				appid == int(appid)
		r = self.login()
		result = r.delete(self.baseurl+'applications/'+str(appid), verify=self.verify)
		return self.returnobject(result)

	def createfolder(self, name: str, parent: Union[int, str], description: str = None, contact: str = None) -> Dict[str, str]:
		"""Create a folder

		Args:
			name (str): Folder name
			parent (int OR str): Folder parent ID; if string, folder ID will be grabbed
			description (str, optional): Folder description. Defaults to None.
			contact (str, optional): Folder contact info. Defaults to None.

		Raises:
			ValueError: Parent cannot be :class:`None`

		Returns:
			dict: Result of folder creation including folder ID
		"""
		try:
			if bool(int(parent)) != True:
				parent = self.folderquery(parent, 'name')['folderId']
		except ValueError:
			if parent == None:
				raise ValueError("Parent cannot be Nonetype")
			else:
				parent == int(parent)
		r = self.login()
		dic = {
			'folderName':name,
			'parentId':parent
		}
		if description:
			dic['description'] = description
		if contact:
			dic['contact'] = contact
		else:
			dic['contact'] = self.username
		result = r.post(self.baseurl+'folders/create', json=dic, verify=self.verify)
		return self.returnobject(result)
	
	def updatefolder(self, folderid: int, name: str = None, description: str = None, contact: str = None) -> Dict[str, str]:
		"""Update folder

		Args:
			folderid (int): Folder ID
			name (str, optional): Folder name. Defaults to None.
			description (str, optional): Folder description. Defaults to None.
			contact (str, optional): Folder contact info. Defaults to None.

		Returns:
			Dict[str, str]: Result of folder update
		"""
		try:
			if bool(int(folderid)) != True:
				folderid = self.folderquery(folderid, 'name')['folderId']
		except ValueError:
			folderid = int(folderid)
		r = self.login()
		dic = {}
		if name:
			dic['folderName'] = name
		if description:
			dic['description'] = description
		if contact:
			dic['contact'] = contact
		result = r.post(self.baseurl+'folders/edit/'+str(folderid), json=dic, verify=self.verify)
		return self.returnobject(result)
	
	def deletefolder(self, folderid: int) -> Dict[str, str]:
		"""Delete folder

		Args:
			folderid (int): Folder ID

		Returns:
			dict: Result of folder deletion
		"""
		try:
			if bool(int(folderid)) != True:
				folderid = self.folderquery(folderid, 'name')['folderId']
		except ValueError:
			folderid == int(folderid)
		r = self.login()
		result = r.delete(self.baseurl+'folders/delete/'+str(folderid), verify=self.verify)
		return self.returnobject(result)
	
	def createapikey(self) -> Dict[str, str]:
		"""Create API key

		Creates an API key and Secret Key for current user to utilize instead 
		of username/password combo, also no ``key`` is needed, and can be safely
		stored in environment variables or encrypted files (still do not commit 
		these to Github)!

		Note:
			Can be run as many times as you want, but invalidates old API/Secret key combo

		Returns:
			Dict[str, str]: Dictionary containing api key and secret key
		"""
		r = self.login()
		result = r.post(self.baseurl+'account/apikey', verify=self.verify)
		return self.returnobject(result)
	
	def deleteapikey(self) -> Dict[str, str]:
		"""Deletes API key for current user

		Returns:
			Dict[str, str]: Result of api key deletion
		"""
		r = self.login()
		result = r.post(self.baseurl+'account/deleteapikey', verify=self.verify)
		return self.returnobject(result)

	def createfolderitem(self, templateid, appid, size=None, empty=False, keySet=None, values=None):
		"""Create a folder item

		Args:
			templateid (int): Template ID
			appid (App ID): Application ID
			size (int, optional): size of folder item. Defaults to None.
			empty (bool, optional): Is item empty. Defaults to False.
			keySet (str, optional): Keyset for folder item. Defaults to None.
			values (dict, optional): Value dictionary for folder item. Defaults to None.

		Raises:
			NotImplementedError: Not implemented yet
		"""
		raise NotImplementedError

	def deletefolderitem(self, folderitemid: int) -> Dict[str, str]:
		"""Delete folder item

		Args:
			folderitemid (int): Folder item ID

		Returns:
			dict: Result of folder item deletion
		"""
		r = self.login()
		result = r.delete(self.baseurl + 'folderitems/{}'.format(folderitemid), verify=self.verify)
		return self.returnobject(result)