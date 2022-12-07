from .helper import Helper
import re
from typing import List, Dict, Union, Tuple, Any

class Query(Helper):
	"""Do not call this directly; use :func:`pyappscan.create_engine`"""
	def __init__(self, baseurl: str, username: str, password: str, key: str, apikey: str, secretkey: str, verify: bool):
		super(Query, self).__init__(baseurl=baseurl, username=username, password=password, key=key, apikey=apikey, secretkey=secretkey, verify=verify)

	def getapikey(self):
		'''Gets API key and API secret from appscan; requires :attr:`username` and :attr:`password` to work'''
		r = self.login()
		result = r.get(self.baseurl+'account/getapikey', verify=self.verify)
		return self.returnobject(result)

	def templatequery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries template endpoint.
		
		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('templates', name, category)
	
	def folderquery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries folder endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('folders', name, category)

	def testpolicyquery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries test policy endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('testpolicies', name, category)
	
	def applicationquery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries application endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('applications', name, category)

	def scannerquery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries scanner endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		r = self.login()
		result = r.get(self.baseurl+'scanners?includeUnregisteredScanners=true', verify=self.verify)
		if name == None:
			return self.returnobject(result)
		else:
			i = self.searchdict(result.json(), name, category)
			return i
	
	def userquery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries user endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('consoleusers', name, category)

	def usertypequery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries usertype endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('usertypes', name, category)

	def issuetypes(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries issue type endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('issuetypes', name, category)

	def currentscans(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries scan queue/management endpoint

		Omit category if using element ID as name argument to query element directly.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		'''
		return self.queryhelper('scansmanagement', name, category)
	
	def jobsquery(self, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		'''Queries jobs endpoint for a given folder or job

		Returns all DAST-configured jobs in a folder. Given a ``name`` as a job 
		ID and no ``category``, this will return the entry for the given 
		job ID. If given no ``name``, this will return all jobs in the 
		console. If given a ``name`` and a ``category``, this will return the job 
		that matches the category in a manner similar to queryhelper.

		Args:
			name (str, optional): Key to search for. Defaults to ``None``.
			category (str, optional): Value to search for. Defaults to ``None``.
		
		Returns:
			dict OR list: If you have both or neither, a :class:`dict` is returned, 
			otherwise :class:`list` is returned
		
		References:
			:meth:`folderjobsquery`
		'''
		r = self.login()
		jobslist = []
		if name and not category:
			result = r.get(self.baseurl + '/jobs/' + str(name))
			return self.returnobject(result)
		folderlist = self.folderquery()
		for folder in folderlist:
			if name == None:
				jobquery = self.folderjobsquery(foldername=folder['folderName'])
				jobslist.append(jobquery)
			else:
				jobquery = self.folderjobsquery(foldername=folder['folderName'], jobname=name)
				if jobquery:
					return jobquery
				else:
					continue
		return jobslist

	def folderjobsquery(self, foldername: Union[str, int], jobname: Union[str, int] = None) -> Union[List[dict], Dict[str, str]]:
		"""Queries jobs endpoint of folder path

		Args:
			foldername (Union[str, int]): ID or name of folder to query; if :class:`str` 
			grabs ID for you
			jobname (Union[str, int], optional): Job ID or name; if :class:`str` grabs ID 
			for you. Defaults to ``None``.

		Returns:
			Union[List[dict], Dict[str, str]]: Returns :class:`list` if only ``foldername`` is given, 
			returns :class:`dict` otherwise
		"""
		r = self.login()
		try:
			if bool(int(foldername)) == True: 
				folderid = int(foldername)
		except ValueError:
			folderid = self.folderquery(foldername, 'folderName')['folderId']
		result = r.get(self.baseurl+'folders/'+str(folderid)+'/jobs', verify=self.verify)
		if jobname == None:
			return self.returnobject(result)
		else:
			try:
				if bool(int(jobname)) == True:
					return self.searchlist(result.json(), jobname, 'id')
			except ValueError:
				return self.searchlist(result.json(), jobname, 'name')

	def appissuequery(self, appname: Union[str, int] = None, severity: str = 'High', sortBy: str = 'Severity', itemcount: int = 100, includeinfoseverity: bool = False) -> List[dict]:
		"""Queries issues endpoint using application path

		Args:
			appname (str OR int, optional): Application ID or name. If :class:`str` 
			grabs app ID for you. Defaults to ``None``.
			severity (str, optional): Severity of issues to include. Defaults to 'High'.
			sortBy (str, optional): Sorting category. Defaults to 'Severity'.
			itemcount (int, optional): Amount of issues to return. Defaults to 100.
			includeinfoseverity (bool, optional): Include issues with informational 
			severity. Defaults to ``False``.

		Returns:
			list: list of issue dictionaries
		"""
		r = self.login()
		if appname == None:
			jsonlist = []
			appjson = self.applicationquery()
			applist = []
			for node in appjson:
				applist.append(node['name'])
			for node in applist:
				url = self.baseurl+'issues?columns=Severity,Location,Issue Type,Element&query=Application Name='+node
				if severity == 'Medium' or severity == 'medium': sev=['Medium', 'Low']
				elif severity == 'Low' or severity == 'low': sev=['Low']
				else: sev=['High', 'Medium', 'Low']
				if includeinfoseverity == True:
					sev.append('Information')
				for entry in sev:
					url+=',Severity='+entry
				url+='&sortBy=-'+sortBy+'&compactResponse=false'
				result = r.get(url, verify=self.verify)
				jsonlist.append(result.json())
			return jsonlist
		else:
			try:
				if bool(int(appname)) == True:
					appname = self.applicationquery(appname, 'id')['name']
			except ValueError:
				pass
			url = self.baseurl+'issues?columns=Severity,Location,Issue Type,Element&query=Application Name='+appname
			if severity == 'Medium' or severity == 'medium': sev=['Medium', 'Low']
			elif severity == 'Low' or severity == 'low': sev=['Low']
			else: sev=['High', 'Medium', 'Low']
			if includeinfoseverity == True:
				sev.append('Information')
			for entry in sev:
				url+=',Severity='+entry
			url+='&sortBy=-'+sortBy+'&compactResponse=false'
			header = {'Range':'items=0-{}'.format(itemcount)}
			r.headers.update(header)
			result = r.get(url, verify=self.verify)
			return self.returnobject(result)
	
	def dastquery(self, jobid: int) -> Dict[str, str]:
		"""Gets the DAST configuration of the job

		Args:
			jobid (int): ID of job

		Returns:
			dict: DAST configuration
		"""
		r = self.login()
		result = r.get(self.baseurl+'jobs/'+str(jobid)+'/dastconfig', verify=self.verify)
		return self.returnobject(result)

	def permissionsquery(self) -> Dict[str, str]:
		"""Get permissions of the current user

		Returns:
			dict: permissions dictionary
		"""
		r = self.login()
		result = r.get(self.baseurl+'currentuser_v2', verify=self.verify)
		return self.returnobject(result)
	
	def schedulequery(self, jobid: int) -> Dict[str, str]:
		"""Get the current schedule of the job

		Args:
			jobid (int): ID of the job

		Returns:
			dict: Dictionary of the schedule of the scan
		"""
		r = self.login()
		result = r.get(self.baseurl+'jobs/schedulescan/'+str(jobid)+'?responseFormat=json', verify=self.verify)
		return self.returnobject(result)

	def reportquery(self, reportid: int, issues: bool = False) -> bytes:
		"""Report information from XML reports endpoint; please use :meth:`reportjsonquery` instead

		Note:
			This only exists for backwards compatibility; please use :meth:`reportjsonquery` instead

		Args:
			reportid (int): Report ID
			issues (bool, optional): Whether to get issue report (default is summary report). Defaults to False.

		Returns:
			bytes: HTML/XML of the endpoint

		References:
			:meth:`reportjsonquery`
		"""
		r = self.login()
		if issues == False:
			result = r.get(self.scanbaseurl+'services/reports/'+str(reportid), verify=self.verify)
		else:
			result = r.get(self.scanbaseurl+'services/reports/'+str(reportid)+'/issues', verify=self.verify)
		return self.returnhtml(result)

	def reportjsonquery(self, reportid: int, issues: bool = False, summary: bool = False) -> Union[List[dict], Dict[str, Any]]:
		"""Get report data in JSON format

		By default you hit the `reports/{reportid}/data` endpoint, from which you will 
		get a detailed data dictionary in which the issues list usually at ``wf-security-issues.issue``. 
		If you set ``issues`` to :class:`True`, you get a detailed issue dictionary
		which has the issue list at ``issues.security-issue``. If you set ``summary`` 
		to :class:`True` you will get an issue summary by severity and status.

		Args:
			reportid (int): Report ID
			issues (bool, optional): Get detailed issues list. Defaults to False.
			summary (bool, optional): Get summary of issues. Defaults to False.

		Returns:
			Union[List[dict], Dict[str, Any]]: This method tries to filter out the nonsense and leave 
			only the issue lists, but for some reason sometimes the base dictionary
			structure changes, so sometimes we just return the dictionary.
		"""
		r = self.login()
		result = ''
		try:
			if bool(int(reportid)) == True:
				reportid = int(reportid)
		except:
			reportlist = self.folderitemquery(folderitemid=reportid, reports=True)['id']
			reportid = int(reportlist)
		if issues == False and summary == True:
			result = r.get(self.baseurl+'reports/' + str(reportid), verify=self.verify)
		elif issues == True and summary == False:
			url = self.baseurl+'reports/' + str(reportid) + '/issues'
			result = r.get(url, verify=self.verify)
			json_result = self.returnobject(result)
			if json_result['issues']['TotalPages'] != 1:
				for page in range(2, json_result['issues']['TotalPages']):
					paged_result = r.get(url+'/pages/'+str(page), verify=self.verify)
					json_paged_result = self.returnobject(paged_result)
					json_result['issues']['security-issue'] = json_result['issues']['security-issue'] + json_paged_result['issues']['security-issue']
			return json_result
		else:
			url = self.baseurl+'reports/' + str(reportid) + '/data'
			result = r.get(url, verify=self.verify)
			json_result = self.returnobject(result)
			if json_result['wf-security-issues']['TotalPages'] != 1:
				for page in range(2, json_result['wf-security-issues']['TotalPages']):
					paged_result = r.get(url+'/pages/'+page, verify=self.verify)
					json_paged_result = self.returnobject(paged_result)
					json_result['wf-security-issues']['security-issue'] = json_result['wf-security-issues']['security-issue'] + json_paged_result['wf-security-issues']['security-issue']
			return json_result
		return self.returnobject(result)

	def issuequery(self, reportid: int = None, appid: Union[str, int] = None, issueid: int = None, zipfile: bool = False, issuecount: int = 100) -> Union[List[dict], Dict[str, Any]]:
		"""Grabs issues from either a report or an app, or grabs issue details

		Provided a ``reportid``, this will use :meth:`reportquery` to grab issues, or if 
		provided an ``appid``, this will use :meth:`appissuequery` to grab issues, or if 
		provided an ``issueid`` in concurrence with either one will return that 
		specific isssue from the requested app or report.

		Note:
			This method is deprecated due to being discouraged when the ability 
			to call :meth:`reportjsonquery` or :meth:`appissuequery` is feasible, 
			and for using :meth:`reportquery` instead of :meth:`reportjsonquery`.

		Args:
			reportid (int, optional): Report ID. Defaults to None.
			appid (Union[str, int], optional): App ID; if string, app ID will be grabbed. Defaults to None.
			issueid (int, optional): Issue ID. Defaults to None.
			zipfile (bool, optional): Should the app issues be returned in ZIP format. 
				Note that this cannot be :class:`True` while ``reportid`` is given. Defaults to False.
			issuecount (int, optional): Issue count to be returned. Defaults to 100.

		Raises:
			TypeError: Raised if ``zipfile`` is :class:`True` while ``reportid`` is given.

		Returns:
			Union[List[dict], Dict[str, Any]]: Returns issue :class:`list` if ``issueid`` is not provided, and
			:class:`dict` if it is provided.

		References:
			* :meth:`appissuequery`
			* :meth:`reportjsonquery`
			* :meth:`reportquery`
		"""		
		r = self.login()
		if reportid != None:
			if zipfile != False:
				raise TypeError("You can't return a report issue in zip format")
			#if reportid is given but issue id isnt
			if issueid == None:
				liss = []
				for entry in re.finditer('\\<id\\>[\\d]+\\<\\/id\\>', self.reportquery(reportid, issues=True).decode('utf-8')):
					ent = entry.group()
					ent = int(ent[ent.find('>')+1:ent.find('<', 2)])
					if ent != reportid:
						if ent > 1000:
							liss.append(self.issuequery(reportid, issueid=ent).decode('utf-8'))
				return liss
			#if reportid is given and issue id is as well
			else:
				result = r.get(self.scanbaseurl+'services/reports/'+str(reportid)+'/issues/'+str(issueid), verify=self.verify)
				return self.returnhtml(result)
		elif appid != None:
			try:
				if bool(int(appid)) == True:
					appid = int(appid)
			except ValueError:
				appid = self.applicationquery(appid, 'name')['id']
			#if appid is given but issueid isnt
			if issueid == None:
				return self.appissuequery(appname=appid, itemcount=issuecount)
			#if appid is given and so is issue id
			else:
				if zipfile == False:
					result = r.get(self.baseurl+'issues/'+str(issueid)+'/application/'+str(appid), verify=self.verify)
				else:
					result = r.get(self.baseurl+'issues/details_v2?appId='+str(appid)+'&ids=["'+str(issueid)+'"]', verify=self.verify)
			return self.returnobject(result)
		else: return ValueError("Please have either the reportid or the appid in your arguments")

	def aboutissue(self, appid: Union[int, str], issueid: int) -> bytes:
		"""Gets HTML document about given issue ID

		Args:
			appid (Union[int, str]): Application ID; if string, app ID will be grabbed.
			issueid (int): Issue ID

		Returns:
			bytes: HTML encoded in UTF-8 format
		"""
		r = self.login()
		try:
			if bool(int(appid)) == True:
				appid = int(appid)
		except ValueError:
			appid = self.applicationquery(appid, 'name')['id']
		result = r.get(self.baseurl+'issues/'+str(issueid)+'/application/'+str(appid)+'/aboutthisissue', verify=self.verify)
		return self.returnhtml(result)

	def issuetypequery(self, issuetypeid: int = None, lookuptype: str = None, lookupname: str = None) -> Union[bytes, Dict[str, Any]]:
		"""Gets data about issue type depending on information given

		Args:
			issuetypeid (int, optional): Issuetype ID. If :class:`None`, ``lookupname`` is required. Defaults to None.
			lookuptype (str, optional): Type of information to look up; defaults to None. Accepted values are:
				
				* ``advisory``
				* ``fix``

			lookupname (str, optional): Lookup string identifier; usually ``wf-*``. If 
				:class:`None`, lookup name associated with issue type is looked up and searched. 
				Defaults to None.

		Returns:
			Union[bytes, Dict[str, Any]]: Returns :class:`bytes` type HTML information for a lookupname or :class:`dict` when no ``lookuptype`` and ``lookupname`` is given.
		"""
		r = self.login()
		if issuetypeid != None:
			try:
				if bool(int(issuetypeid)) == True:
					issuetypeid = int(issuetypeid)
			except ValueError:
				issuetypeid = self.issuetypes(issuetypeid, category="name")['id']
		if lookuptype == None:
			result = r.get(self.baseurl+'issuetypes/'+str(issuetypeid), verify=self.verify)
			return self.returnobject(result)
		elif lookuptype == 'advisory' or lookuptype == 'Advisory':
			if lookupname != None:
				result = r.get(self.baseurl+'issuetypes/'+str(lookupname)+'/advisory', verify=self.verify)
			else:
				if issuetypeid == 0:
					lookupname = lookupname
				else:
					lookupname = self.issuetypequery(issuetypeid)['issueTypeLookup']
				result = r.get(self.baseurl+'issuetypes/'+str(lookupname)+'/advisory', verify=self.verify)
			return self.returnhtml(result)
		elif lookuptype == 'fix' or lookuptype == 'Fix':
			if lookupname != None:
				result = r.get(self.baseurl+'issuetypes/'+str(lookupname)+'/fixrecommendation', verify=self.verify)
			else:
				if issuetypeid == 0:
					lookupname = lookupname
				else:
					lookupname = self.issuetypequery(issuetypeid)['issueTypeLookup']
				result = r.get(self.baseurl+'issuetypes/'+str(lookupname)+'/advisory', verify=self.verify)
			return self.returnhtml(result)

	def applicationattributequery(self, appid: Union[int, str] = None) -> Dict[str, List[dict]]:
		"""Gets attributes of application

		Args:
			appid (int OR str, optional): App ID; if string, the app ID is grabbed. Defaults to None.

		Returns:
			Dict[str, List[dict]]: dictionary of attributes with attribute list inside.
		"""
		r = self.login()
		try:
			if bool(int(appid)) == True:
				result = r.get(self.baseurl+'applications/'+str(appid), verify=self.verify)
				return self.returnobject(result)
		except TypeError:
			if type(appid) == str:
				appid = self.applicationquery(appid, 'name')['id']
				result = r.get(self.baseurl+'applications/'+str(appid), verify=self.verify)
				return self.returnobject(result)
			else:
				result = r.get(self.baseurl+'appattributedefinitions', verify=self.verify)
				return self.returnobject(result)

	def issueattributequery(self) -> Dict[str, List[dict]]:
		"""Gets issue attributes JSON schema

		Returns:
			Dict[str, List[dict]]: dictionary of attirbutes
		"""
		r = self.login()
		result = r.get(self.baseurl + 'issueattributedefinitions', verify=self.verify)
		return self.returnobject(result)

	def folderitemsquery(self, folderid: Union[int, str], keyword: str = None, name: str = None, category: str = None) -> Dict[str, Any]:
		"""Get all items in a folder, DAST-compliant or not.

		Args:
			folderid (int OR str): Folder ID; if string, folder ID will be grabbed.
			keyword (str, optional): Keyword if you know the type of folder items you're 
			looking for. Defaults to None. Accepted values:
				``report-pack``
				``content-scan-job``
			name (str, optional): Value to search for in ``category``. Defaults to None.
			category (str, optional): Key to search for ``name``. Defaults to None.

		Returns:
			dict: Report pack, scan jobs, or both, depending on the keyword or lack thereof

		References:
			:meth:`pyappscan.helper.Helper.queryhelper`
		"""
		r = self.login()
		try:
			if bool(int(folderid)) == True:
				folderid = int(folderid)
		except ValueError:
			if type(folderid) == str:
				folderid = int(self.folderquery(name=folderid, category='folderName')['folderId'])
		result = r.get(self.baseurl +'folders/'+str(folderid)+'/folderitems', verify=self.verify)
		try:
			jsondict = result.json()['folder-items']
			if keyword != None:
				jsondict = jsondict[keyword]
			if name != None and category != None:
				if keyword == None:
					return self.searchdict(jsondict, name, category)
				else:
					return self.searchlist(jsondict, name, category)
			else:
				return jsondict
		except:
			return self.returnobject(result)

	def folderitemquery(self, folderitemid: int, options: bool = False, reports: bool = False, scanlog: bool = False, statistics: bool = False):
		"""Gets a given folder item's requested information

		``options`` returns the options associated with the folder item
		``reports`` returns report IDs and info associated with the folder item
		``scanlog`` returns the scan log of the folder item
		``statistics`` returns the statistics of the folder item

		Args:
			folderitemid (int): Folder item ID
			options (bool, optional): returns the options associated with the folder item. Defaults to False.
			reports (bool, optional): returns report IDs and info associated with the folder item. Defaults to False.
			scanlog (bool, optional): returns the scan log of the folder item. Defaults to False.
			statistics (bool, optional): returns the statistics of the folder item. Defaults to False.

		Raises:
			ValueError: Raised if you provide a string for ``folderitemid``

		Returns:
			dict: Returns information requested
		"""
		r = self.login()
		# decide if folderitemid is an id or the name of the folderitem
		try:
			# if it is, all good
			if bool(int(folderitemid)) == True:
				folderitemid = int(folderitemid)
		except ValueError:
			if type(folderitemid) == str:
				# if it's not, get all folders and iterate through them for folderitems until we find the name we're looking for
				folderjson = self.folderquery()
				for item in folderjson:
					potential_item_json = self.folderitemsquery(folderid=item['folderId'], name=folderitemid, category='name')
					if potential_item_json == None:
						continue
					else:
						folderitemid = int(potential_item_json['id'])
				else:
					raise ValueError("Not a valid folderitem name")
		result = ''
		if options and not (reports or scanlog or statistics):
			result = r.get(self.baseurl+'folderitems/'+str(folderitemid)+'/options', verify=self.verify)
		elif reports and not (options or scanlog or statistics):
			result = r.get(self.baseurl+'folderitems/'+str(folderitemid)+'/reports', verify=self.verify).json()['reports']['report']
			result = [rep for rep in result if rep['name'] == 'Security Issues'][0]
		elif scanlog and not (options or reports or statistics):
			result = r.get(self.baseurl+'folderitems/'+str(folderitemid)+'/scanlog', verify=self.verify)
		elif statistics and not (options or reports or scanlog):
			result = r.get(self.baseurl+'folderitems/'+str(folderitemid)+'/statistics', verify=self.verify)
		else:
			result = r.get(self.baseurl+'folderitems/'+str(folderitemid), verify=self.verify)
		if type(result) == dict:
			return result
		return self.returnobject(result)

	def servergroupquery(self) -> Dict[str, dict]:
		r = self.login()
		result = r.get(self.baseurl + 'servergroups?responseFormat=json', verify=self.verify)
		return self.returnobject(result)

	def dashboardquery(self, businessunit: str) -> bytes:
		"""Queries dashboard

		Note:
			This is method is still in beta

		Args:
			businessunit (str): Business unit associated with the dashboard

		Returns:
			bytes: HTML of dashboard
		"""
		r = self.login()
		result = r.get(self.baseurl+'dashboard?query=Business Unit='+businessunit, verify=self.verify)
		return self.returnhtml(result)

	def buildfoldertree(self) -> str:
		"""Used to print out the entire tree of the folder structure of appscan

		Returns:
			str: formatted tree string
		"""
		folderjson = self.folderquery()
		folders = {}
		folderdict = {}
		for i in folderjson:
			folderid = i['folderId']
			foldername = i['folderName']
			if folderid == 1:
				folderdict[folders[1]] = {}
			dirlist = i['folderPath'].split('/')
			dirlist = dirlist[:-1]
			for path in dirlist[:-1]:
				pointer = pointer[path]
			pointer[foldername] = {}	
		return self.dictprint(folderdict)	
