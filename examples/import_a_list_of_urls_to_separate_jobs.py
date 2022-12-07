from pyappscan import create_engine
import traceback

app=create_engine('https://appscan.url.com/ase/api/', username='appscan_user', password='pass')
with open('/home/user/import.txt', 'r') as urllist:
	for url in urllist:
		url=url.rstrip()
		print('importing '+url)
		desc='A scan of '+url
		name='Scan of '+url
		try:
			#returns a job dictionary with values of the parameters of the job as the variable 'job'
			job = app.jobcreate(jobname=name,foldername='Test_Folder',policyname='My Policy',templatename='My Template', jobdesc=desc,jobcontact='appscan_user')
		except:
			print(traceback.print_exc())
		app.updatescan(jobid=job['id'], data=url, datacode='url', encrypt=False)
