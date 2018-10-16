#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code runs the headnote citation parser from an OOB-based approach.
# Last updated 10-16-18

mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"
dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

cleandirlist = cleandirlist
infilepath = dirname + cleandirlist[0]

def find_hn_top(hn_list_str, hnindex_list, index, line):

    for i in hn_list_str:
        if re.search(i, line):
            hnindex_list.append(index)
            pass

            if i == 'HN12':
                break
