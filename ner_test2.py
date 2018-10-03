# -*- coding: utf-8 -*-
"""
Created on Mon. Oct  1 09:54:04 2018

@author: sum410
"""

import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
import string
import re

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

'''
my_sent = "Maddox Hornsby and Jones Almon Shores Houston Steagall and Kennedy concur."

parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(my_sent.split()), binary=True)
print(parse_tree)

named_entities = []

for t in parse_tree.subtrees():
    if t.label() == 'NE':
        named_entities.append(t)
        # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree

print(named_entities)
'''

exclude = set(string.punctuation)
#sentence = 'Judges: Maddox, J., Hornsby, C.J., and Jones, Almon, Shores, Houston, Steagall, and Kennedy, JJ., concur.'
sentence = 'Judges: Frederick J. Martone, Justice. CONCURRING: Thomas A. Zlaket, Chief Justice, Charles E. Jones, Vice Chief Justice, Stanley G. Feldman, Justice, Ruth V. McGregor, Justice.'
print(sentence)
sentence = re.sub(' J\.| JJ\.| C\.J\.|Chief Justice|Justice', '', sentence)
sentence = re.sub(' A\.| E\.| G\.| V\.|', '', sentence)
sentence = re.sub(' Vice', '', sentence)
sentence = re.sub('CONCURRING', '', sentence)
sentence = re.sub('Judges', '', sentence)
print(sentence)
sentence = ''.join(ch for ch in sentence if ch not in exclude)
print(sentence)
just_tag = nltk.tag.pos_tag(sentence.split())
print(just_tag)

is_name = lambda pos: pos == 'NNP'
tokenized = nltk.word_tokenize(sentence)
names = [word for (word, pos) in nltk.pos_tag(tokenized) if is_name(pos)]
names = names[1:][::2]
print(names)



sentence = 'Judges: Frederick J. Martone, Justice. CONCURRING: Thomas A. Zlaket, Chief Justice, Charles E. Jones, Vice Chief Justice, Stanley G. Feldman, Justice, Ruth V. McGregor, Justice.'
sentence = ''.join(ch for ch in sentence if ch not in exclude)
print(sentence)
parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(sentence.split()), binary=True)  # POS tagging before chunking!
print(parse_tree)

for t in parse_tree.subtrees():
    print(t.label())
    if t.label() == 'NE':
        print(t)