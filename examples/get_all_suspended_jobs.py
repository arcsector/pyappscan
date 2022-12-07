from pyappscan.pyappscan import PyAppscan
import logging
logging.basicConfig()

def suspended_test(appscan: PyAppscan, job_id: int) -> bool:
    """Test whether or not a job is in suspended state in Appscan
    Args:
        job_id (int): Job ID to test for suspension
    Returns:
        bool: Whether or not the scan is suspended
    """
    jobinfo = appscan.jobsquery(name=job_id)
    folder_id = jobinfo['folderId']
    jobid = jobinfo['id']
    app_id = jobinfo['applicationId']
    jobstats = appscan.folderitemquery(folderitemid=job_id)
    if 'content-scan-job' in jobstats:
        if 'state' in jobstats['content-scan-job']:
            if 'id' in jobstats['content-scan-job']['state']:
                if int(jobstats['content-scan-job']['state']['id']) == 9:
                    folder_name = appscan.folderquery(name=folder_id)['folder']['name']
                    application_name = appscan.applicationquery(name=app_id)['name']
                    logging.warning("short_message=\"Scan is suspended\", message=\"{}\", foldername=\"{}\", jobid=\"{}\", job=\"{}\",app=\"{}\"".format(
                        jobstats['content-scan-job']['state']['name'],
                        folder_name,
                        jobid,
                        jobinfo['name'],
                        application_name
                    ))
                    return True
            else:
                logging.warning("message=\"Value not found in folderitem dictionary\",parent=\"{}\",keys=\"{}\",value=\"{}\"".format(
                    'content-scan-job.state', 
                    jobstats['content-scan-job']['state'].keys(), 
                    'id'
                ))
        else:
            logging.warning("message=\"Value not found in folderitem dictionary\",parent=\"{}\",keys=\"{}\",value=\"{}\"".format(
                'content-scan-job', 
                jobstats['content-scan-job'].keys(), 
                'state'
            ))
    else:
        logging.warning("message=\"Value not found in folderitem dictionary\",parent=\"{}\",keys=\"{}\",value=\"{}\"".format(
            '', 
            jobstats.keys(), 
            'content-scan-job'
        ))
    return False

def suspended_folder_test(appscan: PyAppscan, folder_id: int):
    """Tests all jobs in a folder for suspension
    Args:
        folder_id (int): folder ID
    Returns:
        dict: Dictionary with the following format:
            
            >>> {"name": "str", "suspended": "bool"}
    """
    if type(folder_id) != int:
        folder_id = appscan.folderquery(name=folder_id, category="folderName")['folderId']
    joblist = appscan.folderjobsquery(folder_id)
    job_dict = {}
    for job in joblist:
        logging.info("message=\"Testing job for suspended state\",job=\"{}\",jobid=\"{}\"".format(
            job['name'],
            job['id']
        ))
        job_dict[job['id']] = { 'name': job['name'], 'suspended': suspended_test(appscan, job['id'])}
    return job_dict

if __name__ == "__main__":
    suspended_folder_test(PyAppscan("url", "user", "password", "featurekey"), 1)