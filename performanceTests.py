'''
MibianLib - Options Pricing Open Source Library - http://code.mibian.net/
Copyright (C) 2011 Yassine Maaroufi -  <yassinemaaroufi@mibian.net>
Distributed under GPLv3 - http://www.gnu.org/copyleft/gpl.html

MibianLib Performance Tests
'''

#from time import time
from timeit import Timer
#import mibian

# Implied volatility performance
print 'Implied volatility: ',
#t = time()
#test = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.021)
#print time() - t

print Timer('mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.021)', 'import mibian').timeit(number=1)
#print t.timeit(number=1)
