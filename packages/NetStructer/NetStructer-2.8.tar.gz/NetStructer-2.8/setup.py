import setuptools

setuptools.setup(
	name = 'NetStructer',
	version = '2.8',
	author='Haytam-Zakaria',
	description="This NetStructer provides classes for implementing secure communication between client and server applications over TCP/IP using encryption. It includes the Bridge class, which represents the communication bridge between client and server, as well as utility classes for encryption, error handling, and session management.",
	packages=['NetStructer'],
	long_description=open(r'F:\Secrit\description.txt','r').read(),
	long_description_content_type='text/markdown',
	classifiers=[
	'Programming Language :: Python :: 3',
	'Operating System :: OS Independent',
	'License :: OSI Approved :: MIT License'],
	install_requires=['cryptography','requests','psutil']
)