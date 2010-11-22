import types

"""

Att(name) > required string attribute
Att(name,parser) > required attribute with a parser
Att(name,parser, defaulter) > optional attribute with a parser
Att(name, parser, None) > optional attribute with no default value
Att(name, None, None) > optional attribute with no default value, no parser > string

				Defaulter and parser sees its place in the document
				
Leaf has exactly the same syntax

"""

class StructParser:
  found = False
  okay = False  
  def __init__(self,name,*args):
    children = filter(lambda x: isinstance(x,StructParser), args)
    args = filter(lambda x: not(isinstance(x,StructParser)), args)
    self.name=name
    if len(args)==0:
      self.required=True
      self.parser = lambda x,c,cc : x 
    if len(args)==1:
      self.parser=args[0]
      if self.parser is None:
        self.parser= lambda x,c,cc :x
      self.required = False
    if len(args)==2:
      self.parser=args[0]
      if self.parser is None:
        self.parser= lambda x,c,cc: x
      self.required = False 
      if isinstance(args[1],types.FunctionType):
        self.defaulter = args[1]
      elif args[1] is None:
        self.defaulter = None
      elif not(args[1] is None):
        self.defaulter = lambda c,cc : args[1]

  def parseDict(self,context,contextcounter):
    print "====="
    print "We are in context\n ", context,"\n\n"
    print "Contextcounter:", contextcounter
    d=context[0]
    if not(isinstance(d,types.DictType)):
      raise "StructParser instance %s is expecting a dict as primary context" %  self.__class__.__name__
    subject = self.matches(context,contextcounter)
    print "subject: ", subject
    if not(subject is None):
      self.found=True
    if self.required and not(self.found):
        raise BaseException("Required dict entry not found: expecting %s " %  self.name)
    if not(self.required) and not(self.found) and not(self.defaulter is None):
      d[self.name]=self.defaulter(context,contextcounter)
    if self.found:
      self.parseSubject(context,contextcounter,subject)

  def matches(self,context,contextcounter):
    d=context[0]
    if self.name in d:
      v=d[self.name]
      if not(self.typeokay(v)):
        raise "StructParser instance %s found %s, but not of correct type" %  (self.__class__.__name__,self.name)
      self.found=True     
      return v
    else:
      self.found=False
      return None
    
  def parseChildren(self,context,contextcounter):
    resolved=[]
    for i in length(self.children):
      cp = self.children[i]
      cp.parse(append(subject,context),append(i,contextcounter))
      okay = okay and cp.okay
      resolved.append(cp.resolved)
    for k in keys(subject):
      okay = okay and k in resolved
      if not(k in resolved):
        raise "Unknown thing " , subject[k]
    self.resolved = name
    self.okay = self.okay

class List(StructParser):
  def typeokay(self,v):
    return isinstance(v,types.ListType)

  def parse(self,context,contextcounter,subject):
    d=context[0]
    for j in length(subject):
      parseChildren(append(subject,context),append(j,contextcounter))

class Leaf(StructParser):
  def typeokay(self,v):
    return isinstance(v,types.DistType)

  def parseSubject(self,context,contextcounter,subject):
    d=context[0]
    resolved=[]
    self.parseChildren(context,contextcounter)

class Att(StructParser):
  def typeokay(self,v):
    return not(isinstance(v,types.DictType))

  def parseSubject(self,context,contextcounter,subject):
    d=context[0]
    #print subject
    #print self.parser(subject,context,contextcounter)
    d[self.name] = self.parser(subject,context,contextcounter)
    if self.found or not(self.required):
      self.okay = True
      self.resolved = self.name
