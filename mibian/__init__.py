'''
Mibian.py - Options Pricing Open Source Library - http://code.mibian.net/
Copyright (C) 2011 Yassine Maaroufi -  <yassinemaaroufi@mibian.net>
Distributed under GPLv3 - http://www.gnu.org/copyleft/gpl.html
'''
from math import log, e
try:
	from scipy.stats import norm
except:
	print 'Mibian requires scipy to be installed to work properly'

# WARNING: All numbers should be floats -> x = 1.0
'''
Arguments:
s: 	Underlying Price
k: 	Strike Price
rd: Domestic Interest Rate
rf: Foreign Interest Rate
o: 	Volatility
t: 	Nb of Days to Maturity
p: 	Option Price (Call)
'''

def N(x):
	''' Normal Cumulative Distribution Function'''
	return norm.cdf(x)

def P(x):
	'''Normal Probability Density Function'''
	return norm.pdf(x)

# Arguments: f: function, args: function arguments, p: position of the target in the argument array, target, high, low
def solve(f, args, p, target, high, low):
	r = len(str(target).split('.')[1])		# Count Digits
	while True:
		mid = (high + low) / 2
		args[p] = mid
		estimate = apply(f, args)[0]
		if round(estimate, r) == target: return mid
		elif estimate > target: high = mid
		elif estimate < target: low = mid

class GK:
	'''Garman-Kohlhagen
	Used for pricing European options on currencies'''

	def price(self, s, k, rd, rf, o, t):
		'''Returns the option price: [Call price, Put price]
		price(s, k, rd, rf, o, t)
		eg: price(1.4565, 1.45, 1, 2, 20, 30)'''
		#[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 360]
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s/k) + (rd - rf + (o**2)/2) * t) / a
		d2 = (log(s/k) + (rd - rf - (o**2)/2) * t) / a		#d2 = d1 - a
		c = e**(-rf * t) * s * N(d1) - e**(-rd * t) * k * N(d2)		# Call
		p = e**(-rd * t) * k * N(-d2) - e**(-rf * t) * s * N(-d1)	# Put
		return [c, p]

	def delta(self, s, k, rd, rf, o, t):
		'''Returns the option delta: [Call delta, Put delta]
		delta(s, k, rd, rf, o, t)
		eg: delta(1.4565, 1.45, 1, 2, 20, 30)'''
		#[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 360]
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (rd - rf + (o ** 2) / 2) * t) / a
		b = e ** -(rf * t)
		c = N(d1) * b
		p = -N(-d1) * b
		return [c, p]

	def delta2(self, s, k, rd, rf, o, t):
		'''Returns the dual delta: [Call dual delta, Put dual delta]
		delta2(s, k, rd, rf, o, t)
		eg: delta2(1.4565, 1.45, 1, 2, 20, 30)'''
		#[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 360]
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d2 = (log(s / k) + (rd - rf - (o ** 2) / 2) * t) / a
		b = e ** -(rd * t)
		c = -N(d2) * b
		p = N(-d2) * b
		return [c, p]

	def vega(self, s, k, rd, rf, o, t):
		'''Returns the option vega: [Call vega, Put vega]
		vega(s, k, rd, rf, o, t)
		eg: vega(1.4565, 1.45, 1, 2, 20, 30)'''
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (rd - rf + (o ** 2) / 2) * t) / a
		return s * e ** -(rf * t) * P(d1) * t ** 0.5

	def theta(self, s, k, rd, rf, o, t):
		'''Returns the option theta: [Call theta, Put theta]
		theta(s, k, rd, rf, o, t)
		eg: theta(1.4565, 1.45, 1, 2, 20, 30)'''
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		b = e ** -(rf * t)
		d1 = (log(s / k) + (rd - rf + (o ** 2) / 2) * t) / a
		d2 = (log(s / k) + (rd - rf - (o ** 2) / 2) * t) / a
		c = -s * b * P(d1) * o / (2 * t ** 0.5) + rf * s * b * N(d1) - rd * k * b * N(d2)
		p = -s * b * P(d1) * o / (2 * t ** 0.5) - rf * s * b * N(-d1) + rd * k * b * N(-d2)
		return [c / 365, p / 365]

	def rhod(self, s, k, rd, rf, o, t):
		'''Returns the option domestic rho: [Call rho, Put rho]
		rhod(s, k, rd, rf, o, t)
		eg: rhod(1.4565, 1.45, 1, 2, 20, 30)'''
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d2 = (log(s / k) + (rd - rf - (o ** 2) / 2) * t) / a
		c = k * t * e ** (-rd * t) * N(d2) / 100
		p = -k * t * e ** (-rd * t) * N(-d2) / 100
		return [c, p]

	def rhof(self, s, k, rd, rf, o, t):
		'''Returns the option foreign rho: [Call rho, Put rho]
		rhof(s, k, rd, rf, o, t)
		eg: rhof(1.4565, 1.45, 1, 2, 20, 30)'''
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (rd - rf + (o ** 2) / 2) * t) / a
		c = -s * t * e ** (-rf * t) * N(d1) / 100
		p = s * t * e ** (-rf * t) * N(-d1) / 100
		return [c, p]

	def gamma(self, s, k, rd, rf, o, t):
		'''Returns the option gamma: [Call rho, Put rho]
		gamma(s, k, rd, rf, o, t)
		eg: gamma(1.4565, 1.45, 1, 2, 20, 30)'''
		[s, rd, rf, o, t] = [float(s), float(rd) / 100, float(rf) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (rd - rf + (o ** 2) / 2) * t) / a
		return (P(d1) * e ** -(rf * t)) / (s * a)

	# Implied Volatility
	# s: underlying price, k: strike, rd: domestic interest rate, rf: Foreign interest rate, p: option price, t: nb of days to maturity
	def vol(self, s, k, rd, rf, c, t):
		'''Returns the implied volatility for a given option price
		vol(s, k, rd, rf, c, t)
		eg: vol(1.4565, 1.45, 1, 2, 0.021, 30)'''
		return solve(self.price, [s, k, rd, rf, 0, t], -2, float(c), high=500.0, low=0.0)

	def parity(self, c, p, s, k, rd, rf, t):
		'''Put-Call Parity
		parity(c, p, s, k, rd, rf, t)
		eg:  parity(0.036, 0.03, 1.4565, 1.45, 1, 2, 30)'''
		#[c, p, s, k, rd, rf, t] = [float(c), float(p), float(s), float(k), float(rd) / 100, float(rf) / 100, float(t) / 360]
		[c, p, s, k, rd, rf, t] = [float(c), float(p), float(s), float(k), float(rd) / 100, float(rf) / 100, float(t) / 365]
		return c - p - (s / ((1 + rf) ** t)) + (k / ((1 + rd) ** t))

class BS:
	'''Black-Scholes
	Used for pricing European options on stocks without dividends'''
	# s: underlying price, k: strike, r: interest rate, o: volatility, t: nb of days to maturity
	def price(self, s, k, r, o, t):
		'''Returns the option price: [Call price, Put price]
		price(s, k, r, o, t)
		eg: price(52, 60, 5, 20, 30)'''
		#[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 360]
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (r + (o ** 2) / 2) * t) / a
		d2 = (log(s / k) + (r - (o ** 2) / 2) * t) / a 	#d2 = d1 - a
		c = s * N(d1) - k * e ** (-r * t) * N(d2)
		p = k * e ** (-r * t) * N(-d2) - s * N(-d1)
		return [c, p]

	def delta(self, s, k, r, o, t):
		'''Returns the option delta: [Call delta, Put delta]
		delta(s, k, r, o, t)
		eg: delta(52, 60, 5, 20, 30)'''
		#[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 360]
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (r + (o ** 2) / 2) * t) / a
		c = N(d1)
		p = -N(-d1)
		return [c, p]

	def delta2(self, s, k, r, o, t):
		'''Returns the dual delta: [Call dual delta, Put dual delta]
		delta2(s, k, r, o, t)
		eg: delta2(52, 60, 5, 20, 30)'''
		#[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 360]
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d2 = (log(s / k) + (r - (o ** 2) / 2) * t) / a
		b = e ** -(r * t)
		c = -N(d2) * b
		p = N(-d2) * b
		return [c, p]

	def vega(self, s, k, r, o, t):
		'''Returns the option vega: 
		vega(s, k, r, o, t)
		eg: delta(52, 60, 5, 20, 30)'''
		#[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 360]
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (r + (o ** 2) / 2) * t) / a
		return s * P(d1) * t ** 0.5 / 100

	def theta(self, s, k, r, o, t):
		'''Returns the option theta: [Call theta, Put theta]
		theta(s, k, r, o, t)
		eg: theta(52, 60, 5, 20, 30)'''
		#[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 360]
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		b = e ** -(r * t)
		d1 = (log(s / k) + (r + (o ** 2) / 2) * t) / a
		d2 = (log(s / k) + (r - (o ** 2) / 2) * t) / a
		c = -s * P(d1) * o / (2 * t ** 0.5) - r * k * b * N(d2)
		p = -s * P(d1) * o / (2 * t ** 0.5) + r * k * b * N(-d2)
		return [c / 365, p / 365]

	def rho(self, s, k, r, o, t):
		'''Returns the option rho: [Call rho, Put rho]
		rho(s, k, r, o, t)
		eg: rho(52, 60, 5, 20, 30)'''
		#[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 360]
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		b = e ** -(r * t)
		d2 = (log(s / k) + (r - (o ** 2) / 2) * t) / a
		c = k * t * b * N(d2) / 100
		p = -k * t * b * N(-d2) / 100
		return [c, p]

	def gamma(self, s, k, r, o, t):
		'''Returns the option gamma: [Call gamma, Put gamma]
		gamma(s, k, r, o, t)
		eg: gamma(52, 60, 5, 20, 30)'''
		[s, r, o, t] = [float(s), float(r) / 100, float(o) / 100, float(t) / 365]
		a = o * t ** 0.5
		d1 = (log(s / k) + (r + (o ** 2) / 2) * t) / a
		return P(d1) / (s * a)

	def vol(self, s, k, r, c, t):
		'''Returns the implied volatility for a given option price
		vol(s, k, r, c, t)
		eg: vol(52, 50, 5, 2.5, 30)'''
		return solve(self.price, [s, k, r, 0, t], -2, float(c), high=500.0, low=0.0)

	def parity(self, c, p, s, k, r, t):
		'''Put-Call Parity
		parity(c, p, s, k, r, t)
		eg: parity(0.0085, 7.7591, 52, 60, 5, 30)'''
		#[c, p, s, k, r, t] = [float(c), float(p), float(s), float(k), float(r) / 100, float(t) / 360]
		[c, p, s, k, r, t] = [float(c), float(p), float(s), float(k), float(r) / 100, float(t) / 365]
		return c - p - s + (k / ((1 + r) ** t))
