from json import loads
from pyappscan import create_engine, PyAppscan
import pytest

def test_username(import_creds):
    creds = import_creds
    test_app = create_engine(url=creds['url'], username=creds['username'], password=creds['password'], key=creds['featureKey'])
    assert type(test_app) == PyAppscan
    perms = test_app.permissionsquery()
    assert perms['userName'] == creds['username']

def test_apikey(import_creds):
    creds = import_creds
    test_app = create_engine(url=creds['url'], apikey=creds['id'], secretkey=creds['secret'])
    assert type(test_app) == PyAppscan
    apikey_get = test_app.getapikey()
    assert apikey_get['keyId'] == creds['id']    

def test_version(app):
    version = app.version()
    # test string but for python 2 have to test not types
    assert type(version['version']) != (int or bool or dict or list)

def test_queryhelper(app):
    # make sure that category works
    data = app.queryhelper(url_ext='applications', name='Dev_Application', category="name")
    assert type(data) == dict
    assert data != {}
    
    # make sure just id works
    data1 = app.queryhelper(url_ext='applications', name=26)
    assert type(data1) == dict
    assert data1 != {}

    # make sure we got the same app from both queries
    assert int(data['id']) == int(data1['id'])

    data2 = app.queryhelper(url_ext='applications')
    assert type(data2) == list
    assert data2 != []