import unittest

import mibian

class UnitTesting(unittest.TestCase):
	def testGK(self):
		#c = mibian.GK()	# Garman-Kohlhagen
		c = mibian.GK([1.4565, 1.45, 1, 2, 30], volatility=20)
		self.assertEqual([c.callPrice, c.putPrice], [0.03591379198404554, 0.030614780580200285])
		self.assertEqual([c.callDelta, c.putDelta], [0.53590471276326945, -0.46245280197803584])
		self.assertEqual([c.callDelta2, c.putDelta2], [-0.51353891183148714, 0.48563950804221351])
#		self.assertEqual([c.callTheta, c.putTheta], [-0.51353891183148714, 0.48563950804221351])
		self.assertEqual([c.callRhoD, c.putRhoD], [0.00061202582642930648, -0.00057877585205030923])
		self.assertEqual([c.callRhoF, c.putRhoF], [-0.00064154401162167267, 0.00055361301869671985])
		self.assertEqual(c.vega, 0.16560340559332973)
		self.assertEqual(c.gamma, 4.7488658326126272)

		c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.021)
		self.assertEqual(c.IV, 10.7421875)

		c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.036133685584059827, putPrice=0.030851333789832069)
		self.assertEqual(c.putCallParity, -3.433431599675352e-05)

		# 360 days in a year
		#self.assertEqual(c.price(1.4565, 1.45, 1, 2, 20, 30), [0.036133685584059827, 0.030851333789832069])
		#self.assertEqual(c.vol(1.4565,1.45, 1, 2, 0.36, 30), 218.75)
		#self.assertEqual(c.delta(1.4565, 1.45, 1, 2, 20, 30), [0.53571919501679555, -0.46261552643414316])
		#self.assertEqual(c.delta2(1.4565, 1.45, 1, 2, 20, 30), [-0.51320091169510551, 0.48596610209735286])
		#self.assertEqual(c.parity(0.036133685584059827, 0.030851333789832069, 1.4565, 1.45, 1, 2, 30), -1.7919713349190403e-05)

		# 365 days in a year
#		self.assertEqual(c.price(1.4565, 1.45, 1, 2, 20, 30), [0.03591379198404554, 0.030614780580200285])
#		self.assertEqual(c.vol(1.4565,1.45, 1, 2, 0.021, 30), 10.7421875)
#		self.assertEqual(c.delta(1.4565, 1.45, 1, 2, 20, 30), [0.53590471276326945, -0.46245280197803584])
#		self.assertEqual(c.delta2(1.4565, 1.45, 1, 2, 20, 30), [-0.51353891183148714, 0.48563950804221351])
#		self.assertEqual(c.vega(1.4030, 1.4050, 2, 0.186, 16.22, 4), 0.058473816915058006)
#		self.assertEqual(c.parity(0.036133685584059827, 0.030851333789832069, 1.4565, 1.45, 1, 2, 30), -3.433431599675352e-05)

	def testBS(self):
		#c = mibian.BS() # Black-Scholes
		c = mibian.BS([81, 80, 6, 60], volatility=30) 
		self.assertEqual([c.callPrice, c.putPrice], [4.8422936422068901, 3.0571309465072147])
		self.assertEqual([c.callDelta, c.putDelta], [0.5963986247019829, -0.4036013752980171])
		self.assertEqual([c.callDelta2, c.putDelta2], [-0.54332493698317152, 0.4468605293205825])
#		self.assertEqual([c.callTheta, c.putTheta], [-0.51353891183148714, 0.48563950804221351])
		self.assertEqual([c.callRho, c.putRho], [0.07145095061696502, -0.05876522029421359])
		self.assertEqual(c.vega, 0.12717225103657845)
		self.assertEqual(c.gamma, 0.039304536595328565)

		c = mibian.BS([52, 60, 5, 30], callPrice=3)
		#self.assertEqual(c.vol(52, 60, 5, 0.0085, 30), 20.111083984375)
		self.assertEqual(c.IV, 95.703125)
		
		#c = mibian.BS([52, 60, 5, 30], callPrice=0.0085843159589928941, putPrice=7.7591044266655942)
		c = mibian.BS([81, 80, 6, 60], callPrice=4.8422936422068901, putPrice=3.0571309465072147)
		#self.assertEqual(c.parity, 0.009352655480121541)
		self.assertEqual(c.putCallParity, 0.02254482311879258)

		# 360 days in a year
		#self.assertEqual(c.price(52, 60, 5, 20, 30), [0.0085843159589928941, 7.7591044266655942])
		#self.assertEqual(c.vol(52, 60, 5, 0.0085, 30), 19.989013671875)
		#self.assertEqual(c.delta(100, 100, 5, 25, 30), [0.53737369710190119, -0.46262630289809875])
		#self.assertEqual(c.delta2(100, 100, 5, 25, 30), [-0.50652176861821263, 0.48932023322689738])
		#self.assertEqual(c.vega(81, 80, 6, 30, 60), 0.12804358832569662)
		#self.assertEqual(c.rho(81, 80, 6, 30, 60), [0.072404043465647425, -0.059602601034241635])
		#self.assertEqual(c.parity(0.0085843159589928941, 7.7591044266655942, 52, 60, 5, 30), 0.006024330357419672)
		
		# 365 days in a year
#		self.assertEqual(c.price(81, 80, 6, 30, 60), [4.842293642206883, 3.0571309465072147])
#		self.assertEqual(c.vol(52, 60, 5, 0.0085, 30), 20.111083984375)
#		self.assertEqual(c.vol(52, 50, 5, 3, 30), 29.296875)
#		self.assertEqual(c.delta(81, 80, 6, 30, 60), [0.5963986247019829, -0.4036013752980171])
#		self.assertEqual(c.delta2(81, 80, 6, 30, 60), [-0.54332493698317164, 0.44686052932058251])
#		self.assertEqual(c.vega(81, 80, 6, 30, 60), 0.12717225103657845)
#		self.assertEqual(c.rho(81, 80, 6, 30, 60), [0.071450950616965048, -0.058765220294213591])
#		self.assertEqual(c.gamma(81, 80, 6, 30, 60), 0.039304536595328565)
#		self.assertEqual(c.parity(0.0085843159589928941, 7.7591044266655942, 52, 60, 5, 30), 0.009352655480121541)

if __name__ == '__main__':
	unittest.main()

