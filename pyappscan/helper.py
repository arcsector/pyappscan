import requests
from os.path import isfile
import logging
from .exceptions import LogoutError, LoginError, AttrError
from datetime import timedelta
import os
from typing import List, Dict, Union, Any, Tuple

try:
	from json import JSONDecodeError
except ImportError:
	JSONDecodeError = ValueError

class Helper(object):
	"""Helper class which is inherited by all other classes; do not use this class directly, use :func:`pyappscan.create_engine`"""
	def __init__(self, baseurl, username, password, key, apikey, secretkey, verify):
		i = baseurl.find(':')
		scanbaseurl1 = baseurl[:baseurl.find(':', i+1)]
		i = baseurl.find('/ase' or '/ASE')
		scanbaseurl2 = baseurl[i:i+4]+'/'
		self.scanbaseurl = scanbaseurl1+scanbaseurl2
		if baseurl[-1] == '/':
			self.baseurl = baseurl
		else:
			self.baseurl = baseurl+'/'
		if username:
			self.username = username
			self.password = password
			if key==None:
				self.key = 'AppscanEnterpriseUser'
			else:
				self.key = key
		self.apikey = apikey
		self.secretkey = secretkey
		self.verify = verify

		# Logger config
		logger = logging.getLogger(__name__)
		logging_level = logging.ERROR
		logging.captureWarnings(True)
		logger.setLevel(logging_level)
		handler = logging.StreamHandler()
		handler.setLevel(logging_level)
		if logger.handlers:
			logger.handlers = []
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		self.logger = logger

	def queryhelper(self, url_ext: str, name: str = None, category: str = None) -> Union[Dict[str, str], List[dict]]:
		"""Decides how to query endpoint data

		If name is given but category is not,
		returns query of ``url_ext`` with ``name`` appended for direct item query. If
		name is not given, it returns the query of ``url_ext``. If name and
		category are given, it returns the query of ``url_ext`` after searching for
		value ``name`` in key ``category``.

		Args:
			url_ext (str): Extension of :attr:`baseurl` to query
			name (str, optional): Value to search for; either appended to ``url_ext`` 
				or searched for in key ``category``. Defaults to None.
			category (str, optional): Key to search ``name`` in. Defaults to None.

		Returns:
			Union[Dict[str, str], List[str]]: either returns a dictionary or a list; will return dictionary 
				if ``name`` is given or if ``name`` and ``category`` are given.
		"""		
		r = self.login()
		if name != None and category == None:
			result = r.get(self.baseurl + url_ext + '/' + str(name), verify=self.verify)
			return self.returnobject(result)
		result = r.get(self.baseurl+url_ext, verify=self.verify)
		if name == None:
			return self.returnobject(result)
		else:
			return self.searchlist(result.json(), name, category)

	def searchlist(self, liss: List[dict], name: str, category: str) -> Union[Dict[str, Any], None]:
		"""Searches a python list of dictionaries for dict containing value ``name`` and key ``category``.

		Args:
			liss (List[dict]): List of dictionaries to be searched
			name (str): Value to be searched for
			category (str): Key to search ``name`` in

		Raises:
			TypeError: Raised when ``liss`` is not type :obj:`list`

		Returns:
			Union[Dict[str, Any], None]: returns dictionary if found, :obj:`None` if not found.
		"""
		if type(liss) != list:
			raise TypeError("Must be a list")
		for node in liss:
			if name == node[category]:
				return node
			elif str(name) == node[category]:
				return node
		return None
	
	def searchdict(self, dic: Dict[str, list], name: str, category: str) -> Union[Dict[str, Any], None]:
		"""Searches a dictionary of lists for a value

		Args:
			dic (Dict[str, list]): Dictionary of lists
			name (str): Value to be searched for
			category (str): Key to search ``name`` in

		Raises:
			TypeError: Raised when ``dic`` is not type :obj:`dict`

		Returns:
			Union[Dict[str, Any], None]: returns ``dict`` when found, :obj:`None` if not found
		"""
		if type(dic) != dict:
			raise TypeError("Must be a dictionary")
		for value in dic.values():
			res = self.searchlist(value, name, category)
			if res == None:
				continue
			else:
				return res
		return None

	def version(self) -> Dict[str, str]:
		"""Returns version of appscan

		Returns:
			Dict[str, str]: Version dictionary
		"""
		r = requests.session()
		result = r.get(self.baseurl+'version', verify=self.verify)
		return self.returnobject(result)

	def login(self) -> requests.Session:
		"""Logs into the server; you shouldn't have to call this yourself

		Raises:
			LoginError: Raised if Login was unsuccessful

		Returns:
			:class:`requests.Session`: Requests session with login cookies
		"""
		r = requests.session()
		if hasattr(self, 'username'):
			dic = {'userId':self.username,'password':self.password,'featureKey':self.key}
			result = r.post(self.baseurl+'login', json=dic, verify=self.verify)
		if self.apikey:
			dic = {'keyId':self.apikey,'keySecret':self.secretkey}
			result = r.post(self.baseurl+'keylogin/apikeylogin', json=dic, verify=self.verify)
		try:
			self.logger.debug("message=\"Login result json\", output=\"{}\"".format(result.json()))
			headers = {'asc_xsrf_token':result.json()['sessionId']}
		except JSONDecodeError:
			raise LoginError()
		r.headers.update(headers)
		return r
	
	def returnobject(self, obj: requests.Response) -> Union[dict, requests.Response]:
		"""Helper function to return json or log and return errors with the request

		Args:
			obj (:class:`requests.Response`): a requests response object from appscan

		Returns:
			Union[dict, :class:`requests.Response`]: if json can be coerced, return JSON, else return object back
		"""
		if obj.status_code == 200 or obj.status_code == 201 or obj.status_code == 204:
			try:
				return obj.json()
			except:
				return obj
		else:
			self.logger.error(obj.content)
			obj.raise_for_status()

	def returnhtml(self, obj: requests.Response) -> bytes:
		"""Helper function to return HTML content from a response object

		Args:
			obj (:class:`requests.Response`): a requests response object from appscan

		Returns:
			bytes: Returns binary unicode content that must be decoded
		"""
		if obj.status_code == 200 or obj.status_code == 201 or obj.status_code == 204:
			return obj.content
		else:
			self.logger.error(obj.content)
			obj.raise_for_status()
	
	def dicttolistofdicts(self, dic: Dict[str, Any]) -> List[Dict[str, Any]]:
		"""Converts a dictionary to a list of dictionaries

		Args:
			dic (Dict[str, Any]): dictionary to be converted

		Returns:
			List[Dict[str, Any]]: list of dictionaries
		"""
		liss = []
		if type(dic['URL']) != list:
			for k,v in dic.items():
				if type(v) != str:
					v = str(v)
				newdic={'name' : k, 'value' : [v]}
				liss.append(newdic)
		else:
			for k,v in dic.items():
				if type(v) != str:
					v = str(v)
				newdic={'name' : k , 'value' : v}
				liss.append(newdic)
		return liss

	def logout(self, session: requests.Session) -> requests.Response:
		"""Logs out of appscan

		Args:
			session (:class:`requests.Session`): a requests session object that has been logged into appscan with :meth:`login`

		Raises:
			LogoutError: Raised when logout failed

		Returns:
			:class:`requests.Response`: Requests response object after logging out
		"""
		if type(session) != requests.sessions.Session:
			raise LogoutError()
		result = session.get(self.baseurl+'logout', verify=self.verify)
		return result

	def dictprint(self, dic: Dict[Any, Any], string: str = '', tab: int = 0) -> str:
		for k,v in dic.items():
			for _ in range(tab):
				string+='|\t'
			string+='| '+k+'\n'
			if type(v) == dict:
				if not v:
					pass
				else:
					string = self.dictprint(v, string=string, tab=tab+1)
		return string

	def attributecheck(self, attributedict):
		"""Checks attributes for :meth:`pyappscan.pyappscan.PyAppscan.createapplication`

		Args:
			attributedict (dict): attribute dictionary

		Raises:
			AttrError: Raised if attribute not present
		
		References:
			* :meth:`pyappscan.pyappscan.PyAppscan.createapplication`
			* :meth:`pyappscan.pyappscan.PyAppscan.updateapplication`
		"""
		if len(attributedict.keys()) < 6:
			raise AttrError('len')
		if 'Name' not in attributedict.keys():
			raise AttrError('Name')
		if 'URL' not in attributedict.keys():
			raise AttrError('URL')
		if 'Hosts' not in attributedict.keys():
			raise AttrError('Hosts')
		if 'Development Contact' not in attributedict.keys():
			raise AttrError('Development Contact')
		if 'Business Unit' not in attributedict.keys():
			raise AttrError('Business Unit')
		if 'Description' not in attributedict.keys():
			raise AttrError('Description')

	def deltaToString(self, delta: timedelta) -> Tuple[str, str]:
		"""Converts a python :class:`datetime.timedelta` object to an appscan scheduling string

		Args:
			delta (:class:`datetime.timedelta`): python timedelta object

		Raises:
			ValueError: raised when delta is not timedelta

		Returns:
			Tuple[str, str]: tuple of the datestring, and the type of datestring respectively
		"""
		string = ''
		type_ = ''
		if type(delta) != timedelta:
			raise ValueError("delta must be type timedelta")
		schedule_months = delta.days / 30
		schedule_weeks = delta.days / 7
		schedule_month_days = delta.days % 30
		schedule_week_days = delta.days % 7
		if schedule_week_days == 0:
			schedule_week_days = 1
		if schedule_month_days == 0:
			schedule_month_days = 1
		if schedule_months == 0:
			if schedule_weeks == 0:
				string = "{};5:00PM".format(schedule_week_days)
				type_ = 'daily'
			else:
				string = "{};{};5:00PM".format(schedule_weeks, schedule_week_days)
				type_ = 'weekly'
		else:
			string = "{};{};5:00PM".format(schedule_months, schedule_month_days)
			type_ = 'monthly'
		return string, type_
