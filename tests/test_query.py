from json import dumps
from pyappscan import PyAppscan
import pytest
from os.path import isfile, join
from .attributeInfo import AttributeInfo

def attribute_tester(jsonData, compareData):
    compareType = type(compareData)
    type_ = type(jsonData)

    # if compareType is list, that means no recursion
    if compareType == list:
        if type_ == dict:
            return compareType.sort() == list(jsonData.keys()).sort()
        elif type_ == list:
            return compareType.sort() == list(jsonData.keys()).sort()

    if type_ == dict:
        for key, value in jsonData.items():
            raise NotImplementedError


def test_folderitem_job(app: PyAppscan):
    ### Test IDs ###
    # get folder item name since it can change
    jobs = app.folderjobsquery(1088)
    testJob = jobs[0]
    testJobId = testJob['id']
    testJobName = testJob['name']

    # test default
    data = app.folderitemquery(testJobId)
    assert data != {} and data != []
    
    # test statistics
    data = app.folderitemquery(testJobId, statistics=True)
    assert data != {} and data != []

    # test options
    data = app.folderitemquery(testJobId, options=True)
    assert data != {} and data != []

    # test scanlog
    data = app.folderitemquery(testJobId, scanlog=True)
    assert data != {} and data != []

    # test report
    data = app.folderitemquery(testJobId, reports=True)
    assert data != {} and data != []

def test_folderitems_report(app: PyAppscan):
    jobs = app.folderjobsquery(1088)
    testJob = jobs[0]
    testJobId = testJob['id']
    testJobName = testJob['name']

    # test default
    data = app.folderitemquery(testJobId)
    assert data != {} and data != []
    
    # test statistics
    data = app.folderitemquery(testJobId, statistics=True)
    assert data != {} and data != []

    # test options
    data = app.folderitemquery(testJobId, options=True)
    assert data != {} and data != []

    # test scanlog
    data = app.folderitemquery(testJobId, scanlog=True)
    assert data != {} and data != []

    # test report
    data = app.folderitemquery(testJobId, reports=True)
    assert data != {} and data != []

def test_templatequery(app: PyAppscan):
    r = app.templatequery()
    assert r != None

def test_folderquery(app: PyAppscan):
    r = app.folderquery(name=1088, category="folderId")
    assert r != None

def test_testpolicyquery(app: PyAppscan):
    r = app.testpolicyquery()
    assert r != None

def test_applicationquery(app: PyAppscan):
    r = app.applicationquery()
    assert r != None

def test_scannerquery(app: PyAppscan):
    r = app.scannerquery()
    assert r != None

def test_userquery(app: PyAppscan):
    r = app.userquery()
    assert r != None

def test_usertypequery(app: PyAppscan):
    r = app.usertypequery()
    assert r != None

def test_jobsquery(app: PyAppscan):
    r = app.jobsquery()
    assert r != None

def test_folderjobsquery(app: PyAppscan):
    r = app.folderjobsquery()
    assert r != None

def test_appissuequery(app: PyAppscan):
    r = app.appissuequery()
    assert r != None

def test_dastquery(app: PyAppscan):
    r = app.dastquery()
    assert r != None

def test_permissionsquery(app: PyAppscan):
    r = app.permissionsquery()
    assert r != None

def test_schedulequery(app: PyAppscan):
    r = app.schedulequery()
    assert r != None

def test_reportquery(app: PyAppscan):
    r = app.reportquery()
    assert r != None

def test_reportjsonquery(app: PyAppscan):
    r = app.reportjsonquery()
    assert r != None

def test_issuequery(app: PyAppscan):
    r = app.issuequery()
    assert r != None

def test_issuetypequery(app: PyAppscan):
    r = app.issuetypequery()
    assert r != None

def test_applicationattributequery(app: PyAppscan):
    r = app.applicationattributequery()
    assert r != None

def test_issueattributequery(app: PyAppscan):
    r = app.issueattributequery()
    r = r['attributeDefColl']
    new_dict = []
    for i in r:
        options = []
        if 'attrOptionColl' in i:
            for j in i['attrOptionColl']['attrOptionList']:
                options.append({"lookup": j['lookup'], "name": j['name'], "foreignKey": j['attributeDefinitionId']})
        item = {"lookup": i['lookup'], "name": i['name'], "type": i['type'], "options": options}
        new_dict.append(item)
    print(dumps(new_dict, indent=4))
    assert r != None

def test_folderitemsquery(app: PyAppscan):
    r = app.folderitemsquery()
    assert r != None

def test_folderitemquery(app: PyAppscan):
    r = app.folderitemquery()
    assert r != None

def test_dashboardquery(app: PyAppscan):
    r = app.dashboardquery()
    assert r != None

def test_servergroupquery(app: Appscan_Query):
    r = app.servergroupquery()
    assert r != None