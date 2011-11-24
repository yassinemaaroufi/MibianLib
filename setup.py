from distutils.core import setup
from os import walk

def getPackages():
	return [a.replace('/','.') for a, b, c in walk('mibian')]
	#l = []
	#for a, b, c in walk('mibian'):
	#	l.append(a.replace('/','.'))
	#return l	

setup(
	name='mibian',	
	version='0.1.1',
	description='Options Pricing Library',
	long_description='MibianLib is an options pricing library implementing '
			+ 'the Garman-Kohlhagen and Black-Scholes pricing models for '
			+ 'European options on currencies and stocks.',
	author='Yassine Maaroufi',
	author_email='yassinemaaroufi@mibian.net',
	url='http://code.mibian.net/',
	license='GPL',
	packages=getPackages(),
	requires=['scipy'],
	classifiers = [
		'Intended Audience :: Education',
		'Intended Audience :: Financial and Insurance Industry',
		'License :: OSI Approved :: GNU General Public License (GPL)'
	]
	)
