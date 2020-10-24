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

sent1 = "The quick brown fox jumped over the lazy dog"
sent1 = "Senior boys who had exams played football on the ground"
sent1 = "The boy who jumped into the river saved another boy"
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
			h = subtree.leaves()[0]#[subtree.label(), subtree.leaves()[0]]
			children_heads.append(h)
	#print(children_heads)
	h = find_head(tree)
	#print(h)
	for m in children_heads:
		if m != h:
			dep_tree.append((h, m))
	#print(dep_tree)
	return h, dep_tree

def add_root_node(dep_tree, h):
	dep_tree.append(("Root", h))
	return dep_tree

def find_head_old(possible_heads):
	h = possible_heads[0]
	for p in possible_heads:
		if more_imp(p[0],h[0]):
			h = p
	#print(h)
	return h

def find_head(tree):
	if tree.label() == 'NP':
		return find_head_of_np(tree)
	elif tree.label() == 'VP':
		return find_head_of_vp(tree)
	# elif tree.label() == 'PP':
	# 	find_head_of_pp(tree)
	elif tree.label() == 'ROOT':
		subtrees = [t for t in tree if type(t)==nltk.tree.Tree]
		return find_head_of_s(subtrees[0])
	elif tree.label() == 'S':
		return find_head_of_s(tree)
	else:
		return find_head_in_general(tree)

def find_head_of_np(np):
	noun_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']
	top_level_trees = [np[i] for i in range(len(np)) if type(np[i]) is nltk.tree.Tree]
	## search for a top-level noun
	top_level_nouns = [t.leaves()[0] for t in top_level_trees if t.label() in noun_tags]
	if len(top_level_nouns) > 0:
		return top_level_nouns[-1]
	else:
		top_level_nps = [t for t in top_level_trees if t.label()=='NP']
		if len(top_level_nps) > 0:
			return find_head_of_np(top_level_nps[-1])
		else:
			nouns = [p[0] for p in np.pos() if p[1] in noun_tags]
			if len(nouns) > 0:
				return nouns[-1]
			else:
				return np.leaves()[-1]

def find_head_of_vp(vp):
	verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	top_level_trees = [vp[i] for i in range(len(vp)) if type(vp[i]) is nltk.tree.Tree]
	top_level_verbs = [t.leaves()[0] for t in top_level_trees if t.label() in verb_tags]
	if len(top_level_verbs) > 0:
		return top_level_verbs[0]
	else:
		top_level_vps = [t for t in top_level_trees if t.label()=='VP']
		if len(top_level_vps) > 0:
			return find_head_of_vp(top_level_vps[0])
		else:
			verbs = [p[0] for p in vp.pos() if p[1] in verb_tags]
			if len(verbs) > 0:
				return verbs[0]
			else:
				return vp.leaves()[0]

def find_head_of_s(s):
	top_level_trees = [s[i] for i in range(len(s)) if type(s[i]) is nltk.tree.Tree]
	top_level_vps = [t for t in top_level_trees if t.label()=='VP']
	top_level_nps = [t for t in top_level_trees if t.label()=='NP']
	if len(top_level_vps) > 0:
		return find_head_of_vp(top_level_vps[0])
	elif len(top_level_nps) > 0:
		return find_head_of_np(top_level_nps[-1])
	else:
		return s.leaves()[0]

def find_head_in_general(s):
	top_level_trees = [s[i] for i in range(len(s)) if type(s[i]) is nltk.tree.Tree]
	top_level_vps = [t for t in top_level_trees if t.label()=='VP']
	top_level_nps = [t for t in top_level_trees if t.label()=='NP']
	top_level_s = [t for t in top_level_trees if t.label()=='S']
	if len(top_level_vps) > 0:
		return find_head_of_vp(top_level_vps[0])
	elif len(top_level_nps) > 0:
		return find_head_of_np(top_level_nps[-1])
	elif len(top_level_s) > 0:
		return find_head_of_s(top_level_s[0])	
	else:
		return s.leaves()[0]

## Not required
# def find_head_of_pp(pp):
# 	prep_tags = ['TO', 'IN']
# 	top_level_trees = [pp[i] for i in range(len(pp)) if type(pp[i]) is nltk.tree.Tree]
# 	top_level_preps = [t.leaves()[0] for t in top_level_trees if t.label() in prep_tags]
# 	if len(top_level_preps) > 0:
# 		return top_level_preps[0]
# 	else:
# 		top_level_pps = [t for t in top_level_trees if t.label()=='PP']
# 		if len(top_level_pps) > 0:
# 			return find_head_of_pp(top_level_pps[0])
# 		else:
# 			preps = [p[0] for p in pp.pos() if p[1] in prep_tags]
# 			if len(preps) > 0:
# 				return preps[0]
# 			else:
# 				return pp.leaves()[0]	

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