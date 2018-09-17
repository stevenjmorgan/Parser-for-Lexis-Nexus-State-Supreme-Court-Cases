# This code saves citations to headnotes as they appear in LN files.

import sys
import os
import re
import csv
import string

reload(sys)
sys.setdefaultencoding('utf8')

os.chdir('C:/Users/sum410/Documents/GitHub/Parser-for-Lexis-Nexus-State-Supreme-Court-Cases/Headnotes')

# Store directory, store file names in list
dirname = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/AdminTxt/"
dirlist = os.listdir(dirname)
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

# Iterate through case files
for entry in cleandirlist[49:50]:
    infilepath = dirname + entry
    infilehandle = open(infilepath)
    txtlines = infilehandle.readlines()
    print entry

    for txtline in txtlines:

        if re.search('hn1|HN1', txtline):
            print txtline
