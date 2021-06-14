
MibianLib - Options Pricing Open Source Library - http://code.mibian.net/
Copyright (C) 2011 Yassine Maaroufi - <yassinemaaroufi@mibian.net>
Distributed under GPLv3 - http://www.gnu.org/copyleft/gpl.html



Documentation
-------------
BS - Black-Scholes        Used for pricing European options on stocks without dividends
BS([underlyingPrice, strikePrice, interestRate, daysToExpiration], volatility=x, callPrice=y, putPrice=z)

eg: 
c = mibian.BS([1.4565, 1.45, 1, 30], volatility=20)
c.callPrice               Returns the call price
c.putPrice                Returns the put price
c.callDelta               Returns the call delta
c.putDelta                Returns the put delta
c.callDelta2              Returns the call dual delta
c.putDelta2               Returns the put dual delta
c.callTheta               Returns the call theta
c.putTheta                Returns the put theta
c.callRho                 Returns the call rho
c.putRho                  Returns the put rho
c.vega                    Returns the option vega
c.gamma                   Returns the option gamma

c = mibian.BS([1.4565, 1.45, 1, 30], callPrice=0.0359)
c.impliedVolatility       Returns the implied volatility from the call price

c = mibian.BS([1.4565, 1.45, 1, 30], putPrice=0.0306)
c.impliedVolatility       Returns the implied volatility from the put price

c = mibian.BS([1.4565, 1.45, 1, 30], callPrice=0.0359, putPrice=0.0306)
c.putCallParity           Returns the put-call parity


GK - Garman-Kohlhagen     Used for pricing European options on currencies
GK([underlyingPrice, strikePrice, domesticRate, foreignRate, daysToExpiration], volatility=x, callPrice=y, putPrice=z)

eg: 
c = mibian.GK([1.4565, 1.45, 1, 2, 30], volatility=20)
c.callPrice               Returns the call price
c.putPrice                Returns the put price
c.callDelta               Returns the call delta
c.putDelta                Returns the put delta
c.callDelta2              Returns the call dual delta
c.putDelta2               Returns the put dual delta
c.callTheta               Returns the call theta
c.putTheta                Returns the put theta
c.callRhoD                Returns the call domestic rho
c.putRhoD                 Returns the put domestic rho
c.callRhoF                Returns the call foreign rho
c.putRhoF                 Returns the call foreign rho
c.vega                    Returns the option vega
c.gamma                   Returns the option gamma

c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.0359)
c.impliedVolatility       Returns the implied volatility from the call price

c = mibian.GK([1.4565, 1.45, 1, 2, 30], putPrice=0.03)
c.impliedVolatility       Returns the implied volatility from the put price

c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.0359, putPrice=0.03)
c.putCallParity           Returns the put-call parity

Me - Merton               Used for pricing European options on stocks with dividends
Me([underlyingPrice, strikePrice, interestRate, annualDividends, daysToExpiration], volatility=x, callPrice=y, putPrice=z)

eg: 
c = mibian.Me([52, 50, 1, 1, 30], volatility=20)
c.callPrice               Returns the call price
c.putPrice                Returns the put price
c.callDelta               Returns the call delta
c.putDelta                Returns the put delta
c.callDelta2              Returns the call dual delta
c.putDelta2               Returns the put dual delta
c.callTheta               Returns the call theta
c.putTheta                Returns the put theta
c.callRho                 Returns the call rho
c.putRho                  Returns the put rho
c.vega                    Returns the option vega
c.gamma                   Returns the option gamma

c = mibian.Me([52, 50, 1, 1, 30], callPrice=0.0359)
c.impliedVolatility       Returns the implied volatility from the call price

c = mibian.Me([52, 50, 1, 1, 30], putPrice=0.0306)
c.impliedVolatility       Returns the implied volatility from the put price

c = mibian.Me([52, 50, 1, 1, 30], callPrice=0.0359, putPrice=0.0306)
c.putCallParity           Returns the put-call parity



Contributions:
--------------
Contributions to MibianLib are welcome.  Please send suggestions, critics,
patches to yassinemaaroufi@mibian.net.  Otherwise you can create a fork on
github at https://github.com/yassinemaaroufi/MibianLib.



Contributors List:								
------------------
Yassine Maaroufi <yassinemaaroufi@mibian.net>	
Jack Grahl <jack.grahl@yahoo.co.uk>				
Dmitry Vatolin <vatolin@gmail.com>
https://github.com/smickles
