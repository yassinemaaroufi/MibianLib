'''
Mibian.py - Options Pricing Open Source Library - http://code.mibian.net/
Copyright (C) 2011 Yassine Maaroufi -  <yassinemaaroufi@mibian.net>
Distributed under GPLv3 - http://www.gnu.org/copyleft/gpl.html
'''
from math import log, e
try:
	from scipy.stats import norm
except ImportError:
	print 'Mibian requires scipy to be installed to work properly'

# WARNING: All numbers should be floats -> x = 1.0

def impliedVolatility(className, args, target, high=500.0, low=0.0):
	'''Returns the estimated implied volatility'''
	decimals = len(str(target).split('.')[1])		# Count decimals
	for i in range(10000):
	#while True:
		mid = (high + low) / 2
		estimate = eval(className + '(args, volatility=mid).callPrice')
		if round(estimate, decimals) == target: 
			break
		elif estimate > target: 
			high = mid
		elif estimate < target: 
			low = mid
	return mid

class GK:
	'''Garman-Kohlhagen
	Used for pricing European options on currencies
	
	GK([underlyingPrice, strikePrice, domesticRate, foreignRate, \
			daysToExpiration], volatility=x, callPrice=y, putPrice=z)

	eg: 
		c = mibian.GK([1.4565, 1.45, 1, 2, 30], volatility=20)
		c.callPrice			# Returns the call price
		c.putPrice			# Returns the put price
		c.callDelta			# Returns the call delta
		c.putDelta			# Returns the put delta
		c.callDelta2		# Returns the call dual delta
		c.putDelta2			# Returns the put dual delta
		c.callRhoD			# Returns the call domestic rho
		c.putRhoD			# Returns the put domestic rho
		c.callRhoF			# Returns the call foreign rho
		c.putRhoF			# Returns the call foreign rho
		c.vega				# Returns the option vega
		c.gamma				# Returns the option gamma

		c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.0359)
		c.IV				# Returns the implied volatility
		
		c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.0359, putPrice=0.0306)
		c.putCallParity		# Returns the put-call parity
	'''

	def __init__(self, args, volatility=None, callPrice=None, putPrice=None):
		self.underlyingPrice = float(args[0])
		self.strikePrice = float(args[1])
		self.domesticRate = float(args[2]) / 100
		self.foreignRate = float(args[3]) / 100
		self.daysToExpiration = float(args[4]) / 365

		for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', \
				'callDelta2', 'putDelta2', 'callTheta', 'putTheta', \
				'callRhoD', 'putRhoD', 'callRhoF', 'callRhoF', 'vega', \
				'gamma', 'IV', 'putCallParity']:
			self.__dict__[i] = None
		
		if volatility:
			self.volatility = float(volatility) / 100
			self._a_ = self.volatility * self.daysToExpiration**0.5
			self._d1_ = (log(self.underlyingPrice / self.strikePrice) + \
				(self.domesticRate - self.foreignRate + \
				(self.volatility**2)/2) * self.daysToExpiration) / self._a_
#			self._d2_ = (log(self.underlyingPrice / self.strikePrice) + \
#					(self.domesticRate - self.foreignRate - \
#					(self.volatility**2)/2) * self.daysToExpiration) / self._a_
			self._d2_ = self._d1_ - self._a_
			self.exerciceProbability = norm.cdf(self._d2_)
			[self.callPrice, self.putPrice] = self._price()
			[self.callDelta, self.putDelta] = self._delta()
			[self.callDelta2, self.putDelta2] = self._delta2()
			[self.callTheta, self.putTheta] = self._theta()
			[self.callRhoD, self.putRhoD] = self._rhod()
			[self.callRhoF, self.putRhoF] = self._rhof()
			self.vega = self._vega()
			self.gamma = self._gamma()
		if callPrice:
			self.callPrice = round(float(callPrice), 6)
			self.IV = impliedVolatility(self.__class__.__name__, args, \
				self.callPrice)
		if callPrice and putPrice:
			self.callPrice = float(callPrice)
			self.putPrice = float(putPrice)
			self.putCallParity = self._parity()

	def _price(self):
		'''Returns the option price: [Call price, Put price]'''
		call = e**(-self.foreignRate * self.daysToExpiration) * \
				self.underlyingPrice * norm.cdf(self._d1_) - \
				e**(-self.domesticRate * self.daysToExpiration) * \
				self.strikePrice * norm.cdf(self._d2_)
		put = e**(-self.domesticRate * self.daysToExpiration) * \
				self.strikePrice * norm.cdf(-self._d2_) - \
				e**(-self.foreignRate * self.daysToExpiration) * \
				self.underlyingPrice * norm.cdf(-self._d1_)
		return [call, put]

	def _delta(self):
		'''Returns the option delta: [Call delta, Put delta]'''
		_b_ = e**-(self.foreignRate * self.daysToExpiration)
		call = norm.cdf(self._d1_) * _b_
		put = -norm.cdf(-self._d1_) * _b_
		return [call, put]

	def _delta2(self):
		'''Returns the dual delta: [Call dual delta, Put dual delta]'''
		_b_ = e**-(self.domesticRate * self.daysToExpiration)
		call = -norm.cdf(self._d2_) * _b_
		put = norm.cdf(-self._d2_) * _b_
		return [call, put]

	def _vega(self):
		'''Returns the option vega'''
		return self.underlyingPrice * e**-(self.foreignRate * \
				self.daysToExpiration) * norm.pdf(self._d1_) * \
				self.daysToExpiration**0.5

	def _theta(self):
		'''Returns the option theta: [Call theta, Put theta]'''
		_b_ = e**-(self.foreignRate * self.daysToExpiration)
		call = -self.underlyingPrice * _b_ * norm.pdf(self._d1_) * \
				self.volatility / (2 * self.daysToExpiration**0.5) + \
				self.foreignRate * self.underlyingPrice * _b_ * \
				norm.cdf(self._d1_) - self.domesticRate * self.strikePrice * \
				_b_ * norm.cdf(self._d2_)
		put = -self.underlyingPrice * _b_ * norm.pdf(self._d1_) * \
				self.volatility / (2 * self.daysToExpiration**0.5) - \
				self.foreignRate * self.underlyingPrice * _b_ * \
				norm.cdf(-self._d1_) + self.domesticRate * self.strikePrice * \
				_b_ * norm.cdf(-self._d2_)
		return [call / 365, put / 365]

	def _rhod(self):
		'''Returns the option domestic rho: [Call rho, Put rho]'''
		call = self.strikePrice * self.daysToExpiration * \
				e**(-self.domesticRate * self.daysToExpiration) * \
				norm.cdf(self._d2_) / 100
		put = -self.strikePrice * self.daysToExpiration * \
				e**(-self.domesticRate * self.daysToExpiration) * \
				norm.cdf(-self._d2_) / 100
		return [call, put]

	def _rhof(self):
		'''Returns the option foreign rho: [Call rho, Put rho]'''
		call = -self.underlyingPrice * self.daysToExpiration * \
				e**(-self.foreignRate * self.daysToExpiration) * \
				norm.cdf(self._d1_) / 100
		put = self.underlyingPrice * self.daysToExpiration * \
				e**(-self.foreignRate * self.daysToExpiration) * \
				norm.cdf(-self._d1_) / 100
		return [call, put]

	def _gamma(self):
		'''Returns the option gamma'''
		return (norm.pdf(self._d1_) * e**-(self.foreignRate * \
				self.daysToExpiration)) / (self.underlyingPrice * self._a_)

	def _parity(self):
		'''Returns the put-call parity'''
		return self.callPrice - self.putPrice - (self.underlyingPrice / \
				((1 + self.foreignRate)**self.daysToExpiration)) + \
				(self.strikePrice / \
				((1 + self.domesticRate)**self.daysToExpiration))

class BS:
	'''Black-Scholes
	Used for pricing European options on stocks without dividends

	GK([underlyingPrice, strikePrice, domesticRate, foreignRate, \
			daysToExpiration], volatility=x, callPrice=y, putPrice=z)

	eg: 
		c = mibian.BS([1.4565, 1.45, 1, 30], volatility=20)
		c.callPrice			# Returns the call price
		c.putPrice			# Returns the put price
		c.callDelta			# Returns the call delta
		c.putDelta			# Returns the put delta
		c.callDelta2		# Returns the call dual delta
		c.putDelta2			# Returns the put dual delta
		c.callRho			# Returns the call rho
		c.putRho			# Returns the put rho
		c.vega				# Returns the option vega
		c.gamma				# Returns the option gamma

		c = mibian.BS([1.4565, 1.45, 1, 30], callPrice=0.0359)
		c.IV				# Returns the implied volatility
		
		c = mibian.BS([1.4565, 1.45, 1, 30], callPrice=0.0359, putPrice=0.0306)
		c.putCallParity		# Returns the put-call parity
		'''

	def __init__(self, args, volatility=None, callPrice=None, putPrice=None):
		self.underlyingPrice = float(args[0])
		self.strikePrice = float(args[1])
		self.interestRate = float(args[2]) / 100
		self.daysToExpiration = float(args[3]) / 365

		for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', \
				'callDelta2', 'putDelta2', 'callTheta', 'putTheta', \
				'callRho', 'putRho', 'vega', 'gamma', 'IV', 'putCallParity']:
			self.__dict__[i] = None
		
		if volatility:
			self.volatility = float(volatility) / 100
			self._a_ = self.volatility * self.daysToExpiration**0.5
			self._d1_ = (log(self.underlyingPrice / self.strikePrice) + \
					(self.interestRate + (self.volatility**2) / 2) * \
					self.daysToExpiration) / self._a_
#			self._d2_ = (log(self.underlyingPrice / self.strikePrice) + \
#					(self.interestRate - (self.volatility**2) / 2) * \
#					self.daysToExpiration) / self._a_
			self._d2_ = self._d1_ - self._a_
			self.exerciceProbability = norm.cdf(self._d2_)
			[self.callPrice, self.putPrice] = self._price()
			[self.callDelta, self.putDelta] = self._delta()
			[self.callDelta2, self.putDelta2] = self._delta2()
			[self.callTheta, self.putTheta] = self._theta()
			[self.callRho, self.putRho] = self._rho()
			self.vega = self._vega()
			self.gamma = self._gamma()
		if callPrice:
			self.callPrice = round(float(callPrice), 6)
			self.IV = impliedVolatility(self.__class__.__name__, args, \
				self.callPrice)
		if callPrice and putPrice:
			self.callPrice = float(callPrice)
			self.putPrice = float(putPrice)
			self.putCallParity = self._parity()

	def _price(self):
		'''Returns the option price: [Call price, Put price]'''
		call = self.underlyingPrice * norm.cdf(self._d1_) - self.strikePrice * \
				e**(-self.interestRate * self.daysToExpiration) * \
				norm.cdf(self._d2_)
		put = self.strikePrice * e**(-self.interestRate * \
				self.daysToExpiration) * norm.cdf(-self._d2_) - \
				self.underlyingPrice * norm.cdf(-self._d1_)
		return [call, put]

	def _delta(self):
		'''Returns the option delta: [Call delta, Put delta]'''
		call = norm.cdf(self._d1_)
		put = -norm.cdf(-self._d1_)
		return [call, put]

	def _delta2(self):
		'''Returns the dual delta: [Call dual delta, Put dual delta]'''
		_b_ = e**-(self.interestRate * self.daysToExpiration)
		call = -norm.cdf(self._d2_) * _b_
		put = norm.cdf(-self._d2_) * _b_
		return [call, put]

	def _vega(self):
		'''Returns the option vega'''
		return self.underlyingPrice * norm.pdf(self._d1_) * \
				self.daysToExpiration**0.5 / 100

	def _theta(self):
		'''Returns the option theta: [Call theta, Put theta]'''
		_b_ = e**-(self.interestRate * self.daysToExpiration)
		call = -self.underlyingPrice * norm.pdf(self._d1_) * self.volatility / \
				(2 * self.daysToExpiration**0.5) - self.interestRate * \
				self.strikePrice * _b_ * norm.cdf(self._d2_)
		put = -self.underlyingPrice * norm.pdf(self._d1_) * self.volatility / \
				(2 * self.daysToExpiration**0.5) + self.interestRate * \
				self.strikePrice * _b_ * norm.cdf(-self._d2_)
		return [call / 365, put / 365]

	def _rho(self):
		'''Returns the option rho: [Call rho, Put rho]'''
		_b_ = e**-(self.interestRate * self.daysToExpiration)
		call = self.strikePrice * self.daysToExpiration * _b_ * \
				norm.cdf(self._d2_) / 100
		put = -self.strikePrice * self.daysToExpiration * _b_ * \
				norm.cdf(-self._d2_) / 100
		return [call, put]

	def _gamma(self):
		'''Returns the option gamma'''
		return norm.pdf(self._d1_) / (self.underlyingPrice * self._a_)

	def _parity(self):
		'''Put-Call Parity'''
		return self.callPrice - self.putPrice - self.underlyingPrice + \
				(self.strikePrice / \
				((1 + self.interestRate)**self.daysToExpiration))
