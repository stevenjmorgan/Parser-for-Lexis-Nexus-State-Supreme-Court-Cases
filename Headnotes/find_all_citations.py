import os
import re
import csv
import string
import operator
import pickle
import sys
from sets import Set

mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"

def FindSubString(strText, strSubString, Offset=None):
    try:
        Start = strText.find(strSubString)
        if Start == -1:
            return -1 # Not Found
        else:
            if Offset == None:
                Result = strText[Start+len(strSubString):]
            elif Offset == 0:
                return Start
            else:
                AfterSubString = Start+len(strSubString)
                Result = strText[AfterSubString:AfterSubString + int(Offset)]
            return Result
    except:
        return -1


dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
#print dirlist
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

cleandirlist = cleandirlist[42312:42313]

for entry in cleandirlist: ## each entry is a txt file with an opinion

    infilepath = dirname + entry
    infilehandle = open(infilepath)
    txtlines = infilehandle.readlines()

    for txtline in txtlines:
        if re.search('HN2', txtline):
        #if re.search(' v. ', txtline):
            #print txtline

            if re.search("([\s]Fed\.\sAppx\.|[\s]F\.3d|[\s]F\.[\s]|[\s]F\.2d|[\d] U.S. [\d]|[\s]App\.)", txtline):
                print "FOUND IT"

            m = re.search('\\b(\\d{1,3})\\s([AFSNU]\\.\\s?[\\w\\.]+)\\s(\\d{1,4}|_{1,4})\\b', txtline)
            if m:
                found = m.group()
                print found

            #subText = "([\s]Fed\.\sAppx\.|[\s]F\.3d|[\s]F\.[\s]|[\s]F\.2d|[\d] U.S. [\d]|[\s]App\.)"
            #start = FindSubString(txtline, subText, 0)
            #print start

            #print txtline.split(subText)[0]

            #found = re.search('([\s]Fed\.\sAppx\.|[\s]F\.3d|[\s]F\.[\s]|[\s]F\.2d|[\d] U.S. [\d]|[\s]App\.)', txtline)#.group(1)
            #print found

            # For the first instance of a 'HNX', need to go back one line to
            # grab the text of the headnote (i.e. Constitutional Law > ... >
            # Case or Controversy > Standing > General Overview Civil Procedure > ... > Justiciability > Standing > General Overview)
            #sys.exit()
