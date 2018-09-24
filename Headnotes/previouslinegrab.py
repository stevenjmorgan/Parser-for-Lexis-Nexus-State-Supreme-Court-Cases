from itertools import izip
import os
import re
import sys

mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"

dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
#print dirlist
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

cleandirlist = cleandirlist[42312:42313]

infilepath = dirname + cleandirlist[0]
print infilepath
#infilehandle = open(infilepath)
#txtlines = infilehandle.readlines()

'''with open(infilepath) as lines:
    for input_line, output_line in izip(lines):
        if output_line.startswith('HN1'):
            print input_line
            print output_line'''


index_list = []
line_list = []

with open(infilepath) as f:
    for index, line in enumerate(f):
        line_list.append(line)
        if line.startswith('HN1'):
            index_list.append(index)
            break


for index in index_list:
    print line_list[index-1].strip()#, line_list[index]
