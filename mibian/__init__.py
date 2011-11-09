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
	for i in range(1000000):
		mid = (high + low) / 2
		estimate = eval(className + '(args, volatility=mid).callPrice')

		if round(estimate, decimals) == target: 
			return mid
		elif estimate > target: 
			high = mid
		elif estimate < target: 
			low = mid

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
		if callPrice and not volatility:
			self.callPrice = float(callPrice)
			self.IV = impliedVolatility(self.__class__.__name__, args, \
				float(callPrice))
		if callPrice and putPrice:
			self.callPrice = float(callPrice)
			self.putPrice = float(putPrice)
			self.putCallParity = self._parity

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
	Used for pricing European options on stocks without dividends'''
	def price(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the option price: [Call price, Put price]
		price(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: price(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_a_ = volatility * daysToExpiration**0.5
		_d1_ = (log(underlyingPrice / strikePrice) + (interestRate + \
				(volatility**2) / 2) * daysToExpiration) / _a_
		_d2_ = (log(underlyingPrice / strikePrice) + (interestRate - \
				(volatility**2) / 2) * daysToExpiration) / _a_
		call = underlyingPrice * norm.cdf(_d1_) - strikePrice * \
				e**(-interestRate * daysToExpiration) * norm.cdf(_d2_)
		put = strikePrice * e**(-interestRate * daysToExpiration) * \
				norm.cdf(-_d2_) - underlyingPrice * norm.cdf(-_d1_)
		return [call, put]

	def delta(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the option delta: [Call delta, Put delta]
		delta(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: delta(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_d1_ = (log(underlyingPrice / strikePrice) + (interestRate + \
				(volatility**2) / 2) * daysToExpiration) / (volatility * \
				daysToExpiration**0.5)
		call = norm.cdf(_d1_)
		put = -norm.cdf(-_d1_)
		return [call, put]

	def delta2(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the dual delta: [Call dual delta, Put dual delta]
		delta2(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: delta2(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_d2_ = (log(underlyingPrice / strikePrice) + (interestRate - \
				(volatility**2) / 2) * daysToExpiration) / (volatility * \
				daysToExpiration**0.5)
		_b_ = e**-(interestRate * daysToExpiration)
		call = -norm.cdf(_d2_) * _b_
		put = norm.cdf(-_d2_) * _b_
		return [call, put]

	def vega(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the option vega
		vega(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: delta(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_d1_ = (log(underlyingPrice / strikePrice) + (interestRate + \
				(volatility**2) / 2) * daysToExpiration) / (volatility * \
				daysToExpiration**0.5)
		return underlyingPrice * norm.pdf(_d1_) * daysToExpiration**0.5 / 100

	def theta(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the option theta: [Call theta, Put theta]
		theta(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: theta(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_a_ = volatility * daysToExpiration**0.5
		_b_ = e**-(interestRate * daysToExpiration)
		_d1_ = (log(underlyingPrice / strikePrice) + (interestRate + \
				(volatility**2) / 2) * daysToExpiration) / _a_
		_d2_ = (log(underlyingPrice / strikePrice) + (interestRate - \
				(volatility**2) / 2) * daysToExpiration) / _a_
		call = -underlyingPrice * norm.pdf(_d1_) * volatility / \
				(2 * daysToExpiration**0.5) - interestRate * strikePrice * \
				_b_ * norm.cdf(_d2_)
		put = -underlyingPrice * norm.pdf(_d1_) * volatility / \
				(2 * daysToExpiration**0.5) + interestRate * strikePrice * \
				_b_ * norm.cdf(-_d2_)
		return [call / 365, put / 365]

	def rho(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the option rho: [Call rho, Put rho]
		rho(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: rho(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_b_ = e**-(interestRate * daysToExpiration)
		_d2_ = (log(underlyingPrice / strikePrice) + (interestRate - \
				(volatility**2) / 2) * daysToExpiration) / (volatility * \
				daysToExpiration**0.5)
		call = strikePrice * daysToExpiration * _b_ * norm.cdf(_d2_) / 100
		put = -strikePrice * daysToExpiration * _b_ * norm.cdf(-_d2_) / 100
		return [call, put]

	def gamma(self, underlyingPrice, strikePrice, interestRate, volatility, \
			daysToExpiration):
		'''Returns the option gamma
		gamma(underlyingPrice, strikePrice, interestRate, volatility, \
				daysToExpiration)
		eg: gamma(52, 60, 5, 20, 30)'''
		[underlyingPrice, interestRate, volatility, daysToExpiration] = \
				[float(underlyingPrice), float(interestRate) / 100, \
				float(volatility) / 100, float(daysToExpiration) / 365]
		_a_ = volatility * daysToExpiration**0.5
		_d1_ = (log(underlyingPrice / strikePrice) + (interestRate + \
				(volatility**2) / 2) * daysToExpiration) / _a_
		return norm.pdf(_d1_) / (underlyingPrice * _a_)

	def vol(self, underlyingPrice, strikePrice, interestRate, callPrice, \
			daysToExpiration):
		'''Returns the implied volatility for a given option price
		vol(underlyingPrice, strikePrice, interestRate, callPrice, \
				daysToExpiration)
		eg: vol(52, 50, 5, 2.5, 30)'''
		return solve(self.price, [underlyingPrice, strikePrice, interestRate, \
				0, daysToExpiration], -2, float(callPrice))

	def parity(self, callPrice, putPrice, underlyingPrice, strikePrice, \
			interestRate, daysToExpiration):
		'''Put-Call Parity
		parity(callPrice, putPrice, underlyingPrice, strikePrice, interestRate, \
				daysToExpiration)
		eg: parity(0.0085, 7.7591, 52, 60, 5, 30)'''
		[callPrice, putPrice, underlyingPrice, strikePrice, interestRate, \
				daysToExpiration] = [float(callPrice), float(putPrice), \
				float(underlyingPrice), float(strikePrice), \
				float(interestRate) / 100, float(daysToExpiration) / 365]
		return callPrice - putPrice - underlyingPrice + (strikePrice / \
				((1 + interestRate)**daysToExpiration))
