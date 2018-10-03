# -*- coding: utf-8 -*-
"""
Created on Mon. Oct  1 09:54:04 2018

@author: sum410
"""

import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

'''
sentence = "Larry Page is an American business magnate and computer scientist who is the co-founder of Google, alongside Sergey Brin"

chunked = ne_chunk(pos_tag(word_tokenize(sentence)))
print(type(chunked))
print(type(chunked[0]))
print(type(chunked[0][0][0]))
print(chunked[0][0][0])

ne_in_sent = []
for subtree in chunked:
    if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
        ne_label = subtree.label()
        ne_string = " ".join([token for token, pos in subtree.leaves()])
        ne_in_sent.append((ne_string, ne_label))
print(ne_in_sent)
print(type(ne_in_sent[0]))
'''

my_sent = "Maddox Hornsby and Jones Almon Shores Houston Steagall and Kennedy concur."

parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(my_sent.split()), binary=True)  # POS tagging before chunking!
print(parse_tree)

named_entities = []

for t in parse_tree.subtrees():
    if t.label() == 'NE':
        named_entities.append(t)
        # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree

print(named_entities)
