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

    hn1_list = []
    hn2_list = []
    hn3_list = []
    hn4_list = []
    hn5_list = []
    hn6_list = []
    hn7_list = []
    hn8_list = []
    hn9_list = []
    hn10_list = []

    for i in range(1,11):

        hnCounter = 'HN' + str(i)

        ### Parse full citation
        for txtline in txtlines:

            if re.search(hnCounter, txtline): # and hnote = True

                txtline = txtline.split(hnCounter)[1]

                report_pattern = re.compile('(\\b\\d{1,3}\\sU\.S\.\\s\\d{1,4}|_{1,4}\\b)') #(\\b\\d{1,3}\\s[AFUSN]\\.\\s?[\\w\\.]+\\s\\d{1,4}|_{1,4}\\b)
                report_match = report_pattern.findall(txtline)

                sct_pattern = re.compile('(\\b\\d{1,3}\\s[S]\\.\\s[C][t]\\.\\s\\d{1,4}|_{1,4}\\b)|(\\b\\d{1,3}\\s[US]\\.\\s?[\\w\\.]+\\sApp\.\\sD\.C\.\\s\\d{1,3}\\b)')
                sct_match = sct_pattern.findall(txtline)
                #print sct_match

                #appeals_pattern = re.compile('(\\b\\d{1,3}\\s[US]\\.\\s?[\\w\\.]+\\sApp\.\\sD\.C\.\\s\\d{1,3}\\s)') #305 U.S. App. D.C. 125
                #appeals_match = appeals_pattern.findall(txtline)

                lexis_pattern = re.compile('(\\b\\d{1,3}\\s[A-Z]\\.\\s[A-Z][a-z]\\.\\s\\d[a-z]\\s\\d{1,3}|_{1,3}\\b)') #167 L. Ed. 2d 248
                lexis_match = lexis_pattern.findall(txtline)
                #print lexis_match

                # For the first instance of a 'HNX', need to go back one line to
                # grab the text of the headnote (i.e. Constitutional Law > ... >
                # Case or Controversy > Standing > General Overview Civil Procedure > ... > Justiciability > Standing > General Overview)

                #try:
                    #print repr(re.split('(\\b[v]\.\\s[\w]+\,\\b)', txtline)[1])

                full_pattern = re.compile('\\s[v]\.\\s[\D]+\,\\s')
                full_match = full_pattern.findall(txtline)
                #print full_match

                for elem in full_match:
                    cite = re.split('\(',re.split(elem, txtline)[1])[0].strip()
                    #print cite

                    if i == 1:
                        hn1_list.append(cite)
                    if i == 2:
                        hn2_list.append(cite)
                    if i == 3:
                        hn3_list.append(cite)
                    if i == 4:
                        hn4_list.append(cite)
                    if i == 5:
                        hn5_list.append(cite)
                    if i == 6:
                        hn6_list.append(cite)
                    if i == 7:
                        hn7_list.append(cite)
                    if i == 8:
                        hn8_list.append(cite)
                    if i == 9:
                        hn9_list.append(cite)
                    if i == 10:
                        hn10_list.append(cite)


    print hn1_list
    print hn2_list
    print hn3_list
    print hn4_list
    print hn5_list
    print hn6_list
    print hn7_list
    print hn8_list
    print hn9_list
    print hn10_list

        #sys.exit()
'''
        try:

            #print report_match
            #print repr(appeals_match)
            print repr('\n')
        except:
            pass
        try:
            #print sct_match
            print repr('\n')
        except:
            pass
        try:
            #print lexis_match
            print repr('\n')
        except:
            pass
'''
