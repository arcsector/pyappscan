from pyappscan import create_engine
import traceback

app=create_engine('https://appscan.url.com/ase/api/', username='appscan_user', password='pass')
joblist = app.folderjobsquery('Test_Folder')
for job in joblist:
	try:
		app.startjob(jobid=job['id'])
	except:
		print(traceback.print_exc())
