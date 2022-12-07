from .pyappscan import PyAppscan

def create_engine(url, username=None, password=None, key='AppscanEnterpriseUser', apikey=None, secretkey=None, verify=True):
	"""Convenience function for importing all modules.

	This function is in the base of the module and will return a properly initialized object namespace with which you can access all appscan methods. This abstracts the state management and login management of appscan. Usage:
	
	Example:
			>>> from pyappscan import create_engine
			# imported
			>>> appscan = create_engine(
			...		url="https://appscan.domain.com/ase/api/", 
			...		apikey="AEF8137319C8", 
			...		secretkey="XXXXXXXX"
			... )
			
	Args:
		url (str): Base URL for appscan API
		username (str, optional): Username to log in with; used in conjunction with ``password``. Defaults to None.
		password (str, optional): Password to log in with; used in conjunction with ``username``. Defaults to None.
		key (str, optional): Feature Key to log in as. Defaults to "AppscanEnterpriseUser".
		apikey (str, optional): API Key to log in with; used in conjunction with ``secretkey``. Defaults to None.
		secretkey (str, optional): API Secret to log in with; used in conjunction with ``apikey``. Defaults to None.
		verify (bool, optional): Certificate path for requests. Defaults to False.
	
	Returns:
		:class:`pyappscan.pyappscan.PyAppscan`
	"""
	return PyAppscan(url, username, password, key, apikey, secretkey, verify)
