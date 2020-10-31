import nltk
import os
from nltk.parse import stanford
from collections import defaultdict
from itertools import chain

os.environ['STANFORD_PARSER'] = '/home/rishi/Downloads/stanford-nlp-jars'
os.environ['STANFORD_MODELS'] = '/home/rishi/Downloads/stanford-nlp-jars'
constituency_parser = stanford.StanfordParser(model_path="/home/rishi/Downloads/stanford-nlp-jars/stanford-parser-4.0.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dependency_parser = stanford.StanfordDependencyParser()

sent1 = "The quick brown fox jumped over the lazy dog"
sent1 = "The boy who jumped into the river saved another boy"
sent1 = "Senior boys who had exams played football on the ground"
parsed_sent1 = dependency_parser.raw_parse(sent1)
# for t in parsed_sent1:
# 	print(list(t.nodes[9]['deps'].values()))

def dependency_to_phrase(tree):
	index = 0
	children = list(tree.nodes[index]["deps"].values())
	phrase_tree = []
	for c in children:
		for idx in c:
			phrase_tree.append(convert_to_phrase_without_root(tree, idx))
	phrase_tree = ['ROOT'] + phrase_tree
	return phrase_tree


def convert_to_phrase_without_root(tree, index):
	noun_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']
	verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	children = list(tree.nodes[index]["deps"].values())
	if len(children) == 0:
		if tree.nodes[index]["tag"] not in noun_tags:
			return [tree.nodes[index]["tag"], tree.nodes[index]["word"]]
		else:
			return [[tree.nodes[index]["tag"], tree.nodes[index]["word"]]]

	right_children = []
	left_children = []
	for l in children:
		for idx in l:
			if idx > index:
				right_children.append(idx)
			elif idx < index:
				left_children.append(idx)

	left_children.reverse()
	phrase_tree = [[tree.nodes[index]["tag"], tree.nodes[index]["word"]]]
	left_ext_projections = []
	right_ext_projections = []
	# print(right_children, left_children)
	for lc in left_children:
		phrase_subtree = convert_to_phrase_without_root(tree, lc)
		if  (tree.nodes[lc]["tag"] in noun_tags and tree.nodes[index]["tag"] in verb_tags):
			left_ext_projections = [phrase_subtree] + left_ext_projections
		else:
			phrase_tree = [phrase_subtree] + phrase_tree
	for rc in right_children:
		phrase_subtree = convert_to_phrase_without_root(tree, rc)
		if  (tree.nodes[rc]["tag"] in verb_tags and tree.nodes[index]["tag"] in noun_tags):
			right_ext_projections.append(phrase_subtree)
		else:
			phrase_tree.append(phrase_subtree)
	if tree.nodes[index]["tag"] in noun_tags:
		phrase_tree = ['NP'] + phrase_tree
	elif tree.nodes[index]["tag"] in verb_tags:
		phrase_tree = ['VP'] + phrase_tree
	else:
		phrase_tree = ['X'] + phrase_tree
	if len(left_ext_projections) + len(right_ext_projections) > 0:
		phrase_tree = left_ext_projections + [phrase_tree] + right_ext_projections
		if len(left_ext_projections) > 0:
			phrase_tree = ['S'] + phrase_tree
		else:
			phrase_tree = ['NP'] + phrase_tree
	return phrase_tree



for t in parsed_sent1:
	print(dependency_to_phrase(t))