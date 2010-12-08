import types
from numpy import append

"""
name
name, parser
name, parser, defaulter

parser or defaulter can be None

-Att(name) > required string attribute
-Att(name,parser) > required attribute with a parser
-Att(name,parser, defaulter) > optional attribute with a parser
-Att(name, parser, None) > optional attribute with no default value
-Att(name, None, None) > optional attribute with no default value, no parser > string
-
-				Defaulter and parser sees its place in the document
-				
-Leaf has exactly the same syntax
"""

class StructParser:
  debug = True
  found = False
  okay = False  
  def __init__(self,name,*args):
    self.children = filter(lambda x: isinstance(x,StructParser), args)
    args = filter(lambda x: not(isinstance(x,StructParser)), args)
    self.args = args
    self.name = name
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
    if self.debug:
      print "====="
      print "Class: %s" % self.__class__.__name__
      print "We are in context\n ", context[0],"\n\n"
      print "Contextcounter:", contextcounter
      print "Name: %s" % self.name
    d=context[0]
    if not(isinstance(d,types.DictType)):
      raise Exception("StructParser instance %s is expecting a dict as primary context" %  self.__class__.__name__)
    subject = self.matches(context,contextcounter)
    if self.debug:
      print "subject: ", subject
    if not(subject is None):
      self.found=True
    if self.required and not(self.found):
        raise BaseException("Required dict entry '%s' not found in %s " %  (self.name,context))
    if not(self.required) and not(self.found) and hasattr(self,"defaulter") and not(self.defaulter is None):
      d[self.name]=self.defaulter(context,contextcounter)
      self.resolved = self.name
    if self.found:
      self.parseSubject(context,contextcounter,subject)

  def matches(self,context,contextcounter):
    d=context[0]
    if self.name in d:
      v=d[self.name]
      if not(self.typeokay(v)):
        raise Exception("StructParser instance %s found %s, but not of correct type" %  (self.__class__.__name__,self.name))
      self.found=True     
      return v
    else:
      self.found=False
      return None
    
  def parseChildren(self,context,contextcounter,subject):
    resolved=[]
    okay = True
    for i in range(len(self.children)):
      cp = self.children[i]
      cp.debug=self.debug
      cp.parseDict(append(subject,context),append(i,contextcounter))
      okay = okay and cp.okay
      resolved.append(cp.resolved)
    for k in subject.keys():
      okay = okay and k in resolved
      if not(k in resolved):
        raise Exception("Unknown thing %s - only these are allowed: %s" % (k,resolved))
    self.resolved = self.name
    self.okay = okay


class Top:
  def __init__(self,*args):
    self.args=args
  def parse(self,tree,debug=False):
    tree={'root':tree}
    l=Leaf('root',*self.args)
    l.debug = debug
    l.parseDict([tree],[0])

class List(StructParser):
  def typeokay(self,v):
    return isinstance(v,types.ListType)

  def parseSubject(self,context,contextcounter,subject):
    d=context[0]
    for j in range(len(subject)):
      self.parseChildren(append([subject[j],subject],context),append(j,contextcounter),subject[j])


class Leaf(StructParser):
  def typeokay(self,v):
    return isinstance(v,types.DictType)

  def parseSubject(self,context,contextcounter,subject):
    d=context[0]
    resolved=[]
    self.parseChildren(context,contextcounter,subject)


class Att(StructParser):
  resolved=None
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
    else:
      raise Exception("Required attribute %s not found in %d" % (self.name,subject))
