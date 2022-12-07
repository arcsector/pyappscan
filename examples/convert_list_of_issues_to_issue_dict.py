from typing import List

def issuelisttodict(self, issuelist: List[dict], appid: int, hostfilter: str) -> List[dict]:
		"""Converts an appscan issue list of values to a dictionary
		This issue list of values is returned by the application issues endpoint
		in appscan, /applications/{appid}/issues. The list adds another depth of
		complexity to the algorithm, so to keep this under `O(n^2)`, we're converting
		the list first and then utilizing the dictionary instead. the list is
		located at ``attributeCollection.attributeArray`` in the appscan json response.
		Args:
			issuelist (List[dict]): list of issue dictionaries (deprecated, only here for 
				backwards compatibility)
			appid (int): Application ID to get issues from
			hostfilter (str): host to filter issues from
		Returns:
			List[dict]: list of issue dictionaries
		"""
		issuelist = [self.appscan.issuequery(appid=appid, issueid=issue['id']) for issue in issuelist]
		for issue in issuelist:
			newdict = {}
			for attribute in issue['attributeCollection']['attributeArray']:
				self.logger.debug("message=\"Parsing issue attribute\", name=\"{}\", value=\"{}\"".format(
					attribute['lookup'], 
					attribute['value']
				))
				newdict[attribute['lookup']] = ''.join(attribute['value'])
			issue['attributeCollection'] = newdict
		if hostfilter != None:
			self.logger.debug("message=\"Using host filter\", hostname=\"{}\"".format(hostfilter))
			issuelist = [issue for issue in issuelist if issue['attributeCollection']['domain'] == hostfilter]
		return issuelist