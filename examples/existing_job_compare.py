from pyappscan import create_engine as cea
import traceback

urllist = open('importlist.txt', 'r').read().split()
appclass = cea('https://example.com/ase/api/', username='user', password='pass', verify=False)
joblist = appclass.folderjobsquery('folder')
for job in joblist:
	hostname = job['name']
	hostname = job['name'][hostname.find('http'):].rstrip()
	if hostname in urllist:
		del urllist[urllist.index(hostname)]
if urllist:
	tid = int(appclass.templatequery('tempscan', 'name')['id'])
	pid = int(appclass.testpolicyquery('policy', 'name')['id'])
	fid = int(appclass.folderquery('folder', 'folderName')['folderId'])
	aid = int(appclass.applicationquery('app', 'name')['id'])
	for j in urllist:
		try:
			print('importing '+j)
			job = appclass.jobcreate(jobname='QS of '+j.rstrip(),foldername=fid,policyname=pid,templatename=tid, jobdesc="A scan of site "+j,jobcontact='user', appname=aid)
			app.updatescan(job['id'], data=j, datacode='url', encrypt=False)
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			print(traceback.print_exc())
