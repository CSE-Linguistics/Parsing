import os
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = '/home/rishi/Downloads/stanford-nlp-jars'
os.environ['STANFORD_MODELS'] = '/home/rishi/Downloads/stanford-nlp-jars'
constituency_parser = stanford.StanfordParser(model_path="/home/rishi/Downloads/stanford-nlp-jars/stanford-parser-4.0.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dependency_parser = stanford.StanfordDependencyParser()
sentences = constituency_parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))

# for line in sentences:
#     for sentence in line:
#         sentence.draw()

sent1 = "The quick brown fox jumped over the lazy dog"
sent1 = "The boy who jumped into the river saved another boy"
sent1 = "Senior boys who had exams played football on the ground"
print(sent1)
print("Constituency parsing")
for t in constituency_parser.raw_parse(sent1):
	print(t)

print("Dependency parsing")
result = dependency_parser.raw_parse(sent1)
dep = result.__next__()

l = list(dep.triples())
dep_parse = []
for el in l:
	dep_parse.append((el[0][0],el[2][0]))
print(dep_parse)