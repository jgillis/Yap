from structparser import *

context = {'foo':123,'bar':456}
s=Att('foo')
s.parseDict([context],[0])
print context
s2=Att('goo')
try:
  s2.parseDict([context],[0])
except:
  pass
s3=Att('bar',lambda x,c,cc: x+2)
s3.parseDict([context],[0])
s4=Att('gar',lambda x,c,cc: x+2,lambda c,cc: 'hoho')
s4.parseDict([context],[0])
s5=Att('gaf',None,'hoho')
s5.parseDict([context],[0])
s6=Att('foo',None,'hoho')
s6.parseDict([context],[0])
