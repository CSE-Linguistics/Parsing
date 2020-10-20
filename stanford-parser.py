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
print(sent1)
print("Constituency parsing")
for t in constituency_parser.raw_parse(sent1):
	print(t)

print("Dependency parsing")
result = dependency_parser.raw_parse(sent1)
dep = result.__next__()

print(list(dep.triples()))