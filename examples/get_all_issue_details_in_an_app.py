from pyappscan import create_engine
from pprint import pprint

app=create_engine('https://appscan.url.com/ase/api/', username='appscan_user', password='pass')
liss=app.issuequery(appid='Test App')
newliss = []
for i in liss:
	newliss.append(app.issuequery(appid='Test App', issueid=i['id']))
pprint(newliss)
