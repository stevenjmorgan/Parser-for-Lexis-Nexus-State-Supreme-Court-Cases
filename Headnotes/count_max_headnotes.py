import os
import re
import csv
import string
import operator
import pickle
import sys
from sets import Set

mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"

dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
#print dirlist
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

cleandirlist = cleandirlist

entryCount = 0

for entry in cleandirlist[34854:34855]: ## each entry is a txt file with an opinion #[34854:34855]
    #print(entry)
    infilepath = dirname + entry
    print entry
    entryCount += 1

    hn1index_list = []
    hn2index_list = []
    hn3index_list = []
    hn4index_list = []
    hn5index_list = []
    hn6index_list = []
    hn7index_list = []
    hn8index_list = []
    hn9index_list = []
    hn10index_list = []
    hn11index_list = []
    hn12index_list = []

    line_list = []

    headnoteCounter = 0
    betterCounter = 0
    strIncr = 1

    with open(infilepath) as f:
        for index, line in enumerate(f):

            if re.search('HN' + str(strIncr) + ' ', line):  # Assumes HN's are in order - that's fine
                betterCounter += 1
                strIncr += 1


            line_list.append(line)
            if re.search('HN1 ',line):
                hn1index_list.append(index)
                #print(hn1index_list)
                headnoteCounter += 1
                pass
            if re.search('HN2 ',line):
                hn2index_list.append(index)
                #print(hn2index_list)
                headnoteCounter += 1
                pass
            if re.search('HN3',line):
                hn3index_list.append(index)
                #print(hn3index_list)
                headnoteCounter += 1
                pass
            if re.search('HN4',line):
                hn4index_list.append(index)
                #print(hn4index_list)
                headnoteCounter += 1
                pass
            if re.search('HN5',line):
                hn5index_list.append(index)
                #print(hn5index_list)
                headnoteCounter += 1
                pass
            if re.search('HN6',line):
                hn6index_list.append(index)
                #print(hn6index_list)
                headnoteCounter += 1
                pass
            if re.search('HN7',line):
                hn7index_list.append(index)
                #print(hn7index_list)
                headnoteCounter += 1
                pass
            if re.search('HN8',line):
                hn8index_list.append(index)
                #print(hn8index_list)
                headnoteCounter += 1
                pass
            if re.search('HN9',line):
                hn9index_list.append(index)
                #print(hn9index_list)
                headnoteCounter += 1
                pass
            if re.search('HN10',line):
                hn10index_list.append(index)
                #print(hn10index_list)
                headnoteCounter += 1
                pass
            if re.search('HN11',line):
                hn11index_list.append(index)
                #print(hn11index_list)
                headnoteCounter += 1
                pass
            if re.search('HN12',line):
                hn12index_list.append(index)
                #print(hn12index_list)
                headnoteCounter += 1
                #break
                pass

        print('This file contains: ' + str(betterCounter) + ' headnotes.') # Should say 21 headnoteCounter
