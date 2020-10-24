import nltk
import os
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = '/home/rishi/Downloads/stanford-nlp-jars'
os.environ['STANFORD_MODELS'] = '/home/rishi/Downloads/stanford-nlp-jars'
constituency_parser = stanford.StanfordParser(model_path="/home/rishi/Downloads/stanford-nlp-jars/stanford-parser-4.0.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dependency_parser = stanford.StanfordDependencyParser()

# def traverse_tree(tree):
# 	print("tree:", tree, tree.label())
# 	for subtree in tree:
# 		if type(subtree) == nltk.tree.Tree:
# 			traverse_tree(subtree)

sent1 = "Senior boys who had exams played football on the ground"#"The quick brown fox jumped over the lazy dog"
print(sent1)
# print("Constituency parsing")
parsed_sent1 = constituency_parser.raw_parse(sent1)
# for t in parsed_sent1:
# 	print(t)


def phrase_to_dependency(tree):
	h,dep_tree = convert_to_dependency_without_root(tree)
	return add_root_node(dep_tree, h)

def convert_to_dependency_without_root(tree):
	children_heads = []
	dep_tree = []
	#print(tree)
	for subtree in tree:
		if type(subtree) == nltk.tree.Tree and subtree.height() > 2:
			h, dep_subtree = convert_to_dependency_without_root(subtree)
			children_heads.append(h)
			dep_tree += dep_subtree
		elif type(subtree) == nltk.tree.Tree and subtree.height() == 2:
			h = [str(subtree.label()), subtree.leaves()[0]]
			children_heads.append(h)
	#print(children_heads)
	h = findHead(children_heads)
	#print(h)
	for m in children_heads:
		if m != h:
			dep_tree.append((h[1], m[1]))
	#print(dep_tree)
	return h, dep_tree

def add_root_node(dep_tree, h):
	dep_tree.append(("Root", h[1]))
	return dep_tree

def findHead(possible_heads):
	h = possible_heads[0]
	for p in possible_heads:
		if more_imp(p[0],h[0]):
			h = p
	#print(h)
	return h

def more_imp(t1, t2):
	if t1.startswith("V") and not t2.startswith("V"):
		return True
	if t1.startswith("N") and not (t2.startswith("V") or t2.startswith("N")):
		return True

	return False

for t in parsed_sent1:
	print("Dependency parser")
	dep_tree = phrase_to_dependency(t)
	print(dep_tree)