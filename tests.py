'''
MibianLib - Options Pricing Open Source Library - http://code.mibian.net/
Copyright (C) 2011 Yassine Maaroufi -  <yassinemaaroufi@mibian.net>
Distributed under GPLv3 - http://www.gnu.org/copyleft/gpl.html

MibianLib Unit Tests
'''

import unittest

import mibian

class UnitTesting(unittest.TestCase):
	'''Unit tests for MibianLib'''
	def testGK(self):
		'''Garman-Kohlhagen model tests'''
		#test = mibian.GK()	# Garman-Kohlhagen
		test = mibian.GK([1.4565, 1.45, 1, 2, 30], volatility=20)
		self.assertEqual([test.callPrice, test.putPrice], [0.03591379198404554, 
			0.030614780580200285])
		self.assertEqual([test.callDelta, test.putDelta], [0.53590471276326945,
			-0.46245280197803584])
		self.assertEqual([test.callDelta2, test.putDelta2],
				[-0.51353891183148714, 0.48563950804221351])
		#self.assertEqual([test.callTheta, test.putTheta], [-0.51353891183148714,
		#					0.48563950804221351])
		self.assertEqual([test.callRhoD, test.putRhoD], [0.00061202582642930648,
			-0.00057877585205030923])
		self.assertEqual([test.callRhoF, test.putRhoF],
				[-0.00064154401162167267, 0.00055361301869671985])
		self.assertEqual(test.vega, 0.16560340559332973)
		self.assertEqual(test.gamma, 4.7488658326126272)

		test = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.021)
		self.assertEqual(test.impliedVolatility, 10.7421875)

		test = mibian.GK([1.4565, 1.45, 1, 2, 30],
				callPrice=0.036133685584059827, putPrice=0.030851333789832069)
		self.assertEqual(test.putCallParity, -3.433431599675352e-05)

	def testBS(self):
		'''Black-Scholes model tests'''
		#test = mibian.BS() # Black-Scholes
		test = mibian.BS([81, 80, 6, 60], volatility=30) 
		self.assertEqual([test.callPrice, test.putPrice], [4.8422936422068901,
							3.0571309465072147])
		self.assertEqual([test.callDelta, test.putDelta], [0.5963986247019829,
							-0.4036013752980171])
		self.assertEqual([test.callDelta2, test.putDelta2],
							[-0.54332493698317152, 0.4468605293205825])
		#self.assertEqual([test.callTheta, test.putTheta], [-0.51353891183148714,
		#					0.48563950804221351])
		self.assertEqual([test.callRho, test.putRho], [0.07145095061696502,
							-0.05876522029421359])
		self.assertEqual(test.vega, 0.12717225103657845)
		self.assertEqual(test.gamma, 0.039304536595328565)

		test = mibian.BS([52, 60, 5, 30], callPrice=3)
		#self.assertEqual(test.vol(52, 60, 5, 0.0085, 30), 20.111083984375)
		self.assertEqual(test.impliedVolatility, 95.703125)
		
		test = mibian.BS([81, 80, 6, 60], callPrice=4.8422936422068901,
							putPrice=3.0571309465072147)
		self.assertEqual(test.putCallParity, 0.02254482311879258)

if __name__ == '__main__':
	unittest.main()

