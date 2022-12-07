from setuptools import setup, find_packages
import os

def here(*path):
    return os.path.join(os.path.dirname(__file__), *path)

def get_file_contents(filename):
    with open(here(filename)) as fp:
        return fp.read()

long_description = get_file_contents("README.md")

# This is a quick and dirty way to include everything from
# requirements.txt as package dependencies.
install_requires = get_file_contents('requirements.txt').split()

packageinfo = {}
exec(open('pyappscan/__packageinfo__.py').read(), packageinfo)

setup(
	name='pyappscan',
	description='Python REST API Wrapper for IBM/HCL Appscan, a tool which helps scan and report on website and mobile app vulnerabilities.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url=packageinfo['giturl'],
	author=packageinfo['author'],
	author_email=packageinfo['author_email'],
	version=packageinfo['version'],
	packages=find_packages(exclude=['tests']),
	include_package_data=True,
	install_requires=install_requires,
	python_requires=">=3.5.0",
	zip_safe=False
)
