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


    for i in range(1,11):

        hnCounter = 'HN' + str(i)
        print '\n'
        print repr(hnCounter)

        for txtline in txtlines:

            if re.search(hnCounter, txtline):

                '''
                m = re.search('(?:review: )?(\\b(\\d{1,3})\\s([AFSNU]\\.\\s?[\\w\\.]+)\\s(\\d{1,4}|_{1,4})\\b)', txtline)
                if m:
                    reporter_hn = m.group()
                    #print reporter_hn

                m2 = re.search('\\b(\\d{1,3})\\s[S]\\.\\s[C][t]\\.\\s(\\d{1,4}|_{1,4})\\b', txtline)
                if m2:
                    sct_cite_hn = m2.group()

                    #print repr(sct_cite_hn)

                m3 = re.search('\\b(\\d{1,3})\\s([A-Z]\\.)\\s([A-Z][a-z]\\.)\\s(\\d[a-z])\\s(\\d{1,3}|_{1,3})\\b', txtline)
                if m3:
                    lexis_cite_hn = m3.group()
                    #print repr(lexis_cite_hn)
                '''

                txtline = txtline.split(hnCounter)[1]


                report_pattern = re.compile('(\\b\\d{1,3}\\s[AFSNU]\\.\\s?[\\w\\.]+\\s\\d{1,4}|_{1,4}\\b)')
                report_match = report_pattern.findall(txtline)
                #print report_match

                sct_pattern = re.compile('(\\b\\d{1,3}\\s[S]\\.\\s[C][t]\\.\\s\\d{1,4}|_{1,4}\\b)')
                sct_match = sct_pattern.findall(txtline)
                #print sct_match

                lexis_pattern = re.compile('(\\b\\d{1,3}\\s[A-Z]\\.\\s[A-Z][a-z]\\.\\s\\d[a-z]\\s\\d{1,3}|_{1,3}\\b)')
                lexis_match = lexis_pattern.findall(txtline)
                #print lexis_match

                # For the first instance of a 'HNX', need to go back one line to
                # grab the text of the headnote (i.e. Constitutional Law > ... >
                # Case or Controversy > Standing > General Overview Civil Procedure > ... > Justiciability > Standing > General Overview)
                #sys.exit()

        try:
            print report_match
            print repr('\n')
        except:
            pass
        try:
            print sct_match
            print repr('\n')
        except:
            pass
        try:
            print lexis_match
        except:
            pass
