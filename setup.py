from distutils.core import setup
from os import walk

def getPackages():
	return [a.replace('/','.') for a, b, c in walk('mibian')]

setup(
	name='mibian',	
	version='0.1.2',
	description='Options Pricing Library',
	long_description='MibianLib is an options pricing library implementing '
			+ 'the Garman-Kohlhagen, Black-Scholes and Merton pricing models '
			+ 'for European options on currencies and stocks.',
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
