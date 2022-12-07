class LogoutError(Exception):
	"""Logout failed"""
	def __init__(self):
		Exception.__init__(self, "LOGOUT FAILED: Object passed is not a session object.")

class LoginError(Exception):
	"""Login failed"""
	def __init__(self):
		Exception.__init__(self, "LOGIN FAILED: Credentials invalid. Please check your username, password, and featureKey to make sure they are all correct.")

class UserTypeError(Exception):
	"""Bad Usertype"""
	def __init__(self):
		Exception.__init__(self, "USER TYPE INVALID: please specify a user type with an integer of a known user type, or with the name of a known user type. If you aren't sure which usertypeID does what, call\nfor i in PyAppscan.usertypequery():\n\tfor k,v in i.items():\n\t\tprint(k,v)")

class DataCodeError(Exception):
	"""Bad Data Code"""
	def __init__(self):
		Exception.__init__(self, 'Please enter a valid data code. Valid data codes are:\n\turl\n\tusername\n\tpassword\n\tmethod\n\theader\n\tlockout\n\tadditionaldomains\n\texclusions')

class AttrError(Exception):
	"""Bad attribute in app attribute dictionary"""
	def __init__(self, *args):
		if args[0] == 'len':
			Exception.__init__(self, 'You must have the required amount of dictionary entries in your attributedict (6), and they must be the same as the ones in the documentation.')
		else:
			Exception.__init__(self, 'You must have %s in your attributedict; it seems to be missing, or it is not spelled correctly. Please check the documentation for spelling, as it is case sensetive' % args[0])
