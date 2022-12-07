from json import loads
from pyappscan import create_engine, PyAppscan
import pytest
from os.path import isfile, join

@pytest.fixture(scope="session")
def import_creds():
    creds = {}  
    credspath = join('tests', '.creds.json')
    if isfile('.creds.json'):
        creds = loads(open(".creds.json", 'r').read())
    if isfile(credspath):
        creds = loads(open(credspath, 'r').read())
    return creds

@pytest.fixture(scope="session")
def app(import_creds) -> PyAppscan:
    creds = import_creds
    return create_engine(url=creds['url'], apikey=creds['id'], secretkey=creds['secret'])
