from yap.structparser import *
import yaml


parser = Top(
	Leaf('foo',
		Att('bar',lambda x,c,cc: x+1),
		Att('baz'),
		List('ike',
			Att('i',None,lambda c,cc: cc),
			Att('j',None,lambda c,cc: cc),
			Att('k',None,lambda c,cc: cc)
		)
	),
	List('bar',
		Att('name'),
		Att('description',None,lambda c,cc: c[0]['name'])
	)
)


tree = yaml.load(file('sample.yaml','r'))
print tree
parser.parse(tree)

print tree
