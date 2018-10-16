#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code takes .txt case files as input, parses case level data,
# w/ emphasis on headnotes and headnote citations. Outputs to .csv.
# Last updated 10-16-18

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

def CleanCells(emptyHN):
    if emptyHN == []:
        return ''
    return str(emptyHN)

def circuit2number(ctstring):
    cirnumber = -999
    if (re.search("FIRST|First", ctstring)):
        cirnumber = "1"
    if (re.search("SECOND|Second", ctstring)):
        cirnumber = "2"
    if (re.search("THIRD|Third", ctstring)):
        cirnumber = "3"
    if (re.search("FOURTH|Fourth", ctstring)):
        cirnumber = "4"
    if (re.search("FIFTH|Fifth", ctstring)):
        cirnumber = "5"
    if (re.search("SIXTH|Sixth", ctstring)):
        cirnumber = "6"
    if (re.search("SEVENTH|Seventh", ctstring)):
        cirnumber = "7"
    if (re.search("EIGHTH|Eighth", ctstring)):
        cirnumber = "8"
    if (re.search("NINTH|Ninth", ctstring)):
        cirnumber = "9"
    if (re.search("TENTH|Tenth", ctstring)):
        cirnumber = "10"
    if (re.search("ELEVENTH|Eleventh", ctstring)):
        cirnumber = "11"
    if (re.search("COLUMBIA|Columbia", ctstring)):
        cirnumber = "12"
    if (re.search("FEDERAL|Federal", ctstring)):
        cirnumber = "13"
    if (re.search("SUPREME|Supreme", ctstring)):
        cirnumber = "0"
    return cirnumber

def expandmonth(mstring):
    mstring2 = re.sub("Jan\.", "January", mstring)
    mstring2 = re.sub("Feb\.", "February", mstring2)
    mstring2 = re.sub("Mar\.", "March", mstring2)
    mstring2 = re.sub("Apr\.", "April", mstring2)
    mstring2 = re.sub("Aug\.", "August", mstring2)
    mstring2 = re.sub("Sept\.", "September", mstring2)
    mstring2 = re.sub("Oct\.", "October", mstring2)
    mstring2 = re.sub("Nov\.", "November", mstring2)
    mstring2 = re.sub("Dec\.", "December", mstring2)
    return mstring2

fout = open(mydir + "headnote_cases.csv", "wb")
outfilehandle = csv.writer(fout,
                           delimiter=",",
                           quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)
localrow = []
#localrow.append("caseID")
localrow.append("filename")
localrow.append("year")
localrow.append('parties')
localrow.append('court')
localrow.append('circuit')
localrow.append('Lexis_Cite')
#localrow.append('Reporter')
localrow.append("hdnote1")
localrow.append("hdnote1_2")
localrow.append("hdnote1_3")
localrow.append("hdnote1_cites")
localrow.append("hdnote2")
localrow.append("hdnote2_2")
localrow.append("hdnote2_3")
localrow.append("hdnote2_cites")
localrow.append("hdnote3")
localrow.append("hdnote3_2")
localrow.append("hdnote3_3")
localrow.append("hdnote3_cites")
localrow.append("hdnote4")
localrow.append("hdnote4_2")
localrow.append("hdnote4_3")
localrow.append("hdnote4_cites")
localrow.append("hdnote5")
localrow.append("hdnote5_2")
localrow.append("hdnote5_3")
localrow.append("hdnote5_cites")
localrow.append("hdnote6")
localrow.append("hdnote6_2")
localrow.append("hdnote6_3")
localrow.append("hdnote6_cites")
localrow.append("hdnote7")
localrow.append("hdnote7_2")
localrow.append("hdnote7_3")
localrow.append("hdnote7_cites")
localrow.append("hdnote8")
localrow.append("hdnote8_2")
localrow.append("hdnote8_3")
localrow.append("hdnote8_cites")
localrow.append("hdnote9")
localrow.append("hdnote9_2")
localrow.append("hdnote9_3")
localrow.append("hdnote9_cites")
localrow.append("hdnote10")
localrow.append("hdnote10_2")
localrow.append("hdnote10_3")
localrow.append("hdnote10_cites")
localrow.append("hdnote11")
localrow.append("hdnote11_2")
localrow.append("hdnote11_3")
localrow.append("hdnote11_cites")
localrow.append("hdnote12")
localrow.append("hdnote12_2")
localrow.append("hdnote12_3")
localrow.append("hdnote12_cites")
outfilehandle.writerow(localrow)

dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
#print dirlist
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

cleandirlist = cleandirlist #[42300:42313] 42000:

entryCount = 0

for entry in cleandirlist: ## each entry is a txt file with an opinion #[34854:34855]
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

    hn1_text = ''
    hn2_text = ''
    hn3_text = ''
    hn4_text = ''
    hn5_text = ''
    hn6_text = ''
    hn7_text = ''
    hn8_text = ''
    hn9_text = ''
    hn10_text = ''
    hn11_text = ''
    hn12_text = ''
    hn1_text2 = ''
    hn2_text2 = ''
    hn3_text2 = ''
    hn4_text2 = ''
    hn5_text2 = ''
    hn6_text2 = ''
    hn7_text2 = ''
    hn8_text2 = ''
    hn9_text2 = ''
    hn10_text2 = ''
    hn11_text2 = ''
    hn12_text2 = ''
    hn1_text3 = ''
    hn2_text3 = ''
    hn3_text3 = ''
    hn4_text3 = ''
    hn5_text3 = ''
    hn6_text3 = ''
    hn7_text3 = ''
    hn8_text3 = ''
    hn9_text3 = ''
    hn10_text3 = ''
    hn11_text3 = ''
    hn12_text3 = ''
    line_list = []

    ### Pull line before HN1 -> open separately but text after hn section not
    ### stored in memory for parsimonious parsing
    with open(infilepath) as f:
        for index, line in enumerate(f):
            line_list.append(line)
            if re.search('HN1',line):
                hn1index_list.append(index)
                pass
            if re.search('HN2',line):
                hn2index_list.append(index)
                pass
            if re.search('HN3',line):
                hn3index_list.append(index)
                pass
            if re.search('HN4',line):
                hn4index_list.append(index)
                pass
            if re.search('HN5',line):
                hn5index_list.append(index)
                pass
            if re.search('HN6',line):
                hn6index_list.append(index)
                pass
            if re.search('HN7',line):
                hn7index_list.append(index)
                pass
            if re.search('HN8',line):
                hn8index_list.append(index)
                pass
            if re.search('HN9',line):
                hn9index_list.append(index)
                pass
            if re.search('HN10',line):
                hn10index_list.append(index)
                pass
            if re.search('HN11',line):
                hn11index_list.append(index)
                pass
            if re.search('HN12',line):
                hn12index_list.append(index)
                break

    # Enumerate based on line before HN1, store headnote text
    for index in hn1index_list[0:1]:
        hn1_text = line_list[index-1].strip()
        #print hn1_text
        if re.search('>', line_list[index-2].strip()):
            hn1_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn1_text3 = line_list[index-3].strip()

    for index in hn2index_list[0:1]:
        hn2_text = line_list[index-1].strip()
        #print hn2_text
        if re.search('>', line_list[index-2].strip()):
            hn2_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn2_text3 = line_list[index-3].strip()

    for index in hn3index_list[0:1]:
        hn3_text = line_list[index-1].strip()
        #print hn2_text
        if re.search('>', line_list[index-2].strip()):
            hn3_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn3_text3 = line_list[index-3].strip()

    for index in hn4index_list[0:1]:
        hn4_text = line_list[index-1].strip()
        #print hn4_text
        if re.search('>', line_list[index-2].strip()):
            hn4_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn4_text3 = line_list[index-3].strip()

    for index in hn5index_list[0:1]:
        hn5_text = line_list[index-1].strip()
        #print hn5_text
        if re.search('>', line_list[index-2].strip()):
            hn5_text2 = line_list[index-2].strip()
            #print hn2_text2
            if re.search('>', line_list[index-3].strip()):
                hn5_text3 = line_list[index-3].strip()
            #print hn5_text3
        #else:


    for index in hn6index_list[0:1]:
        hn6_text = line_list[index-1].strip()
        #print hn6_text
        if re.search('>', line_list[index-2].strip()):
            hn6_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn6_text3 = line_list[index-3].strip()

    for index in hn7index_list[0:1]:
        hn7_text = line_list[index-1].strip()
        #print hn7_text
        if re.search('>', line_list[index-2].strip()):
            hn7_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn7_text3 = line_list[index-3].strip()

    for index in hn8index_list[0:1]:
        hn8_text = line_list[index-1].strip()
        #print hn8_text
        if re.search('>', line_list[index-2].strip()):
            hn8_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn8_text3 = line_list[index-3].strip()

    for index in hn9index_list[0:1]:
        hn9_text = line_list[index-1].strip()
        #print hn9_text
        if re.search('>', line_list[index-2].strip()):
            hn9_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn9_text3 = line_list[index-3].strip()

    for index in hn10index_list[0:1]:
        hn10_text = line_list[index-1].strip()
        #print hn10_text
        if re.search('>', line_list[index-2].strip()):
            hn10_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn10_text3 = line_list[index-3].strip()

    for index in hn11index_list[0:1]:
        hn11_text = line_list[index-1].strip()
        #print hn11_text
        if re.search('>', line_list[index-2].strip()):
            hn11_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn11_text3 = line_list[index-3].strip()

    for index in hn12index_list[0:1]:
        hn12_text = line_list[index-1].strip()
        #print hn12_text
        if re.search('>', line_list[index-2].strip()):
            hn12_text2 = line_list[index-2].strip()
        #print hn2_text
            if re.search('>', line_list[index-3].strip()):
                hn12_text3 = line_list[index-3].strip()

    f.close()

    # Open file and store text in memory
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
    hn11_list = []
    hn12_list = []
    localrow = []
    case = ''

    # Store case file name
    finished_reporter = False
    finished_cite = False
    full_case_name = ''
    cite_string = ''
    cite_line = False
    blank_after_cite = False
    year = 0
    finished_date = False
    finished_court = False
    action_line = False
    finished_parties = False
    finished_header = False
    header = ''
    header_line = False
    parties_line = False
    parties_string = ''
    court_string = ''
    action_string = ''
    docketnum = ''
    date = ''

    for txtline in txtlines:

        if(finished_cite):
           finished_cite = False
           full_case_name = line
           full_case_name = str(txtline)
           full_case_name = string.strip(full_case_name)

        #if reporter == True and re.search("[\w]+", line):
        #    case = case + str(line).strip()
        #    print line
        #    reporter = False

        if(finished_reporter and re.search("[\w]+", txtline)):
            ## the citation block
            finished_reporter = False
            cite_line = True
            cite_string = cite_string + txtline
            cite_string = re.sub("[\s]+", " ", cite_string)
            finished_cite = True

        if(cite_line):
            ##removed from above on 5/11/17:  and re.match("^[\s]+$", txtline)
            ## done with citation block
            blank_after_court = False
            cite_line = False
            blank_after_cite = True
            all_cites = re.split(";", cite_string)
            #print all_cites
            Lexis_cite = [cite for cite in all_cites if re.search("LEXIS", cite)]
            Fed_cite = [cite for cite in all_cites if re.search("([\s]Fed\.\sAppx\.|[\s]F\.3d|[\s]F\.[\s]|[\s]F\.2d|[\d] U.S. [\d]|[\s]App\.)", cite)]


            try:
                Lexis_cite = string.strip(Lexis_cite[0])
                Fed_cite = string.strip(Fed_cite[0])

            except:
                print "Problem with citation"

            if len(Fed_cite) == 0:
                Fed_cite = ""
            else:
                Fed_cite = str(Fed_cite)

            Lexis_cite = str(Lexis_cite)
            year = Lexis_cite[0:4]

        if (re.search("^Reporter", txtline) and not re.search("Reporters",txtline)):
            ## Reporter line
            finished_docket = False
            finished_reporter = True

        if (finished_date and re.search("[\w]+", txtline)):
            ## the parties
            finished_date = False
            docket_line = True
            docketnum = docketnum + txtline
            finished_docket = True
            docket_line = False
            #print docketnum

        if(finished_court and re.search("[\w]+", txtline)):
            ## these lines give the date of some action
            #action_number += 1
            finished_court = False
            action_line = True
            action_string = action_string + txtline
            finished_date = True

        if(action_line and re.match("^[\s]+$", txtline)):
            blank_after_cite = False
            blank_after_action = True
            action_line = False
            action_string = expandmonth(action_string)
            action_string = re.sub(":", ",", action_string)
            action_string = re.sub(";", ",", action_string)
            action_string = re.sub("\*", "", action_string)
            action_string = re.sub("Argued and Submitted ", "Argued and Submitted, ", action_string)
            action_string = re.sub("Argued ", "Argued, ", action_string)
            action_string = re.sub("Decided ", "Decided, ", action_string)
            action_string = re.sub("Supplemental Briefing Submitted ", "Supplemental Briefing Submitted, ", action_string)
            action_string = re.sub("Submitted Under Third Circuit Rule 12\(6\) ", "Submitted Under Third Circuit Rule 12(6), ", action_string)
            action_string = re.sub("Cause argued ", "Cause argued, ", action_string)

            split_action = re.split("\n", action_string)
            action1 = string.strip(split_action[0])
            action2 = string.strip(split_action[1])
            action1 = re.split(", ", action1)
            #action1_month = re.split(" ", action1[0])[0]
            #action1_day = re.split(" ", action1[0])[1]
            #action1_year = action1[1]
            #action1_date = str(month2number(action1_month)) + "-" + action1_day + "-" + action1_year
            #if(len(split_action) > 2):
            action2 = re.split(", ", action2)

            if(len(split_action) < 3):
                action1[1] = re.sub("\.", "", action1[1])
                action1[1] = re.sub(",", "", action1[1])
                action1[0] = re.sub("Argued ", "", action1[0])
                action1[0] = re.sub("Submitted ", "", action1[0])
                date = date + action1[0] + ", " + action1[1]
            if(len(action1) > 2 and len(date) == 0 and re.search("Decided|DECIDED", action1[2])):
                date = date + action1[0] + ", " + action1[1]
            if(len(action1) > 2 and len(date) == 0 and re.search("Filed|FILED", action1[2])):
                date = date + action1[0] + ", " + action1[1]
            if(len(action2) > 2 and len(date) == 0 and re.search("Decided|DECIDED", action2[2])):
                date = date + action2[0] + ", " + action2[1]
            if(len(action2) > 2 and len(date) == 0 and re.search("Filed|FILED", action2[2])):
                date = date + action2[0] + ", " + action2[1]
            if(len(action2) > 1 and len(date)==0):
                date = date + action2[0] + ", " + action2[1]
                date = re.sub(",$", "", date)
                date = re.sub("\*", "", date)
                date = re.sub("\.", "", date)
            if(len(action2) > 1 and len(date)==0):
                date = date + action2[0] + ", " + action2[1]
                date = re.sub(",$", "", date)
                date = re.sub("\.", "", date)


            action_string = string.strip(action_string)
            action_string = re.sub("[\s]+", " ", action_string)

        if(finished_parties and re.search("Court", txtline)):
            ## the court
            finished_parties = False
            court_line = True
            court_string = court_string + txtline
            #court_string = re.sub("[\s]*UNITED STATES COURT OF APPEALS[\s]*[,]?[\s]?", "", court_string)
            #court_string = re.sub("[\s]*CIRCUIT[\s]*\n", " ", court_string)
            circuit = circuit2number(court_string)
            #print "Circuit: " + str(circuit)
            #print court_string + "\n"
            finished_court = True
            court_string = re.sub("[\s]+", " ", court_string)
            court_string = re.sub(" of of ", " of ", court_string)
            court_string = re.sub(" for the ", " ", court_string)
            court_string = re.sub("In the ", " ", court_string)
            court_string = re.sub("Unit A", "", court_string)
            court_string = re.sub("Unit B", "", court_string)
            court_string = re.sub(",", " ", court_string)
            court_string = re.sub("\*", "", court_string)
            court_string = re.sub("United States Circuit Court", "", court_string)
            court_string = re.sub("Circuit Court of Appeals", "United States Court of Appeals", court_string)
            court_string = re.sub("United States Court of Appeals ","",court_string)
            court_string = re.sub(" of the United States","",court_string)
            court_string = re.sub("United States ","",court_string)
            court_string = re.sub("Court of Appeals of ","",court_string)
            court_string = re.sub("District of Columbia Circuit","District of Columbia",court_string)
            court_string = re.sub("District Columbia Circuit","District of Columbia",court_string)
            court_string = re.sub("District of Columbia","District of Columbia Circuit",court_string)
            court_string = re.sub("Second Circuit New York","Second Circuit",court_string)
            court_string = re.sub("US Court of Appeals  8th Circuit","Eighth Circuit",court_string)


            court_string = re.sub("\.","",court_string)
            court_string = string.strip(court_string)

        if (finished_header and re.search("[\w]+", txtline)):
            ## the parties
            finished_header = False
            parties_line = True
            parties_string = parties_string + txtline
            #print txtline.replace("\n", "")
            #print parties_string
            finished_parties = True

        if re.search("^ INCLUDEPICTURE", txtline) and re.search("space\.gif",txtline):
            header_line = True

        if header_line:
            header += txtline
            header_line = False
            finished_header = True

        if (parties_line and re.match("^[\s]+$", txtline)):
            ## done with parties block
            blank_after_searchterms = False
            case_with_preamble = True
            blank_after_parties = True
            parties_line = False
            parties_string = re.sub("[\s]+", " ", parties_string)



    for i in range(1,13):

        hnCounter = 'HN' + str(i) + ' '

        ### Parse full citation
        for txtline in txtlines:

            if re.search(hnCounter, txtline): # and hnote = True

                txtline = txtline.split(hnCounter)[1]

                report_pattern = re.compile('(\\b\\d{1,3}\\sU\.S\.\\s\\d{1,4}|_{1,4}\\b)') #(\\b\\d{1,3}\\s[AFUSN]\\.\\s?[\\w\\.]+\\s\\d{1,4}|_{1,4}\\b)
                report_match = report_pattern.findall(txtline)
                report_match = list(report_match)
                #report_match = filter(None, report_match)

                sct_pattern = re.compile('(\\b\\d{1,3}\\s[S]\\.\\s[C][t]\\.\\s\\d{1,4}|_{1,4}\\b)|(\\b\\d{1,3}\\s[US]\\.\\s?[\\w\\.]+\\sApp\.\\sD\.C\.\\s\\d{1,3}\\b)')
                sct_match = sct_pattern.findall(txtline)
                #sct_match = filter(None, sct_match)

                #appeals_pattern = re.compile('(\\b\\d{1,3}\\s[US]\\.\\s?[\\w\\.]+\\sApp\.\\sD\.C\.\\s\\d{1,3}\\s)') #305 U.S. App. D.C. 125
                #appeals_match = appeals_pattern.findall(txtline)

                lexis_pattern = re.compile('(\\b\\d{1,3}\\s[A-Z]\\.\\s[A-Z][a-z]\\.\\s\\d[a-z]\\s\\d{1,3}|_{1,3}\\b)|(\\b\d{1,3}\s[F].\d{1,2}d\s[a][t]\s\d{1,4}\\b)|(\\b\d{1,3}\s[P].\d{1,2}d\s\d{1,3}\\b)') #167 L. Ed. 2d 248
                lexis_match = lexis_pattern.findall(txtline)
                lexis_match = [(tuple(int(x) if x.isdigit() else x for x in _ if x)) for _ in lexis_match]
                #lexis_match = filter(None, lexis_match)
                #print lexis_match

                # For the first instance of a 'HNX', need to go back one line to
                # grab the text of the headnote (i.e. Constitutional Law > ... >
                # Case or Controversy > Standing > General Overview Civil Procedure > ... > Justiciability > Standing > General Overview)

                full_pattern = re.compile('\\s[v]\.\\s[\D]+\,\\s')
                full_match = full_pattern.findall(txtline)
                #print full_match

                #if entryCount > 5000:
                if int(year) >= 1950:
                    for elem in full_match:
                        try:
                            cite = re.split('\(',re.split(elem, txtline)[1])[0].strip()
                        except:
                            pass
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

                        if i == 11:
                            hn11_list.append(cite)
                        if i == 12:
                            hn12_list.append(cite)

                ### First 5000 cases are wonky; this should probably be done by year
                #if entryCount <= 5000:
                if int(year) < 1950 or int(year) >1949:

                    if i == 1:
                        hn1_list.extend(report_match)
                        hn1_list.extend(sct_match)
                        hn1_list.extend(lexis_match)
                    if i == 2:
                        hn2_list.extend(report_match)
                        hn2_list.extend(sct_match)
                        hn2_list.extend(lexis_match)
                    if i == 3:
                        hn3_list.extend(report_match)
                        hn3_list.extend(sct_match)
                        hn3_list.extend(lexis_match)
                    if i == 4:
                        hn4_list.extend(report_match)
                        hn4_list.extend(sct_match)
                        hn4_list.extend(lexis_match)
                    if i == 5:
                        hn5_list.extend(report_match)
                        hn5_list.extend(sct_match)
                        hn5_list.extend(lexis_match)
                    if i == 6:
                        hn6_list.extend(report_match)
                        hn6_list.extend(sct_match)
                        hn6_list.extend(lexis_match)
                    if i == 7:
                        hn7_list.extend(report_match)
                        hn7_list.extend(sct_match)
                        hn7_list.extend(lexis_match)
                    if i == 8:
                        hn8_list.extend(report_match)
                        hn8_list.extend(sct_match)
                        hn8_list.extend(lexis_match)
                    if i == 9:
                        hn9_list.extend(report_match)
                        hn9_list.extend(sct_match)
                        hn9_list.extend(lexis_match)
                    if i == 10:
                        hn10_list.extend(report_match)
                        hn10_list.extend(sct_match)
                        hn10_list.extend(lexis_match)
                    if i == 11:
                        hn11_list.extend(report_match)
                        hn11_list.extend(sct_match)
                        hn11_list.extend(lexis_match)
                    if i == 12:
                        hn12_list.extend(report_match)
                        hn12_list.extend(sct_match)
                        hn12_list.extend(lexis_match)

    hn1_list = CleanCells(hn1_list)
    hn2_list = CleanCells(hn2_list)
    hn3_list = CleanCells(hn3_list)
    hn4_list = CleanCells(hn4_list)
    hn5_list = CleanCells(hn5_list)
    hn6_list = CleanCells(hn6_list)
    hn7_list = CleanCells(hn7_list)
    hn8_list = CleanCells(hn8_list)
    hn9_list = CleanCells(hn9_list)
    hn10_list = CleanCells(hn10_list)
    hn11_list = CleanCells(hn11_list)
    hn12_list = CleanCells(hn12_list)

    localrow = []

    localrow.append(entry)
    localrow.append(year)
    localrow.append(parties_string)
    localrow.append(court_string)
    localrow.append(circuit)
    localrow.append(Lexis_cite)
    #localrow.append(Fed_cite)
    localrow.append(hn1_text)
    localrow.append(hn1_text2)
    localrow.append(hn1_text3)
    localrow.append(hn1_list)
    localrow.append(hn2_text)
    localrow.append(hn2_text2)
    localrow.append(hn2_text3)
    localrow.append(hn2_list)
    localrow.append(hn3_text)
    localrow.append(hn3_text2)
    localrow.append(hn3_text3)
    localrow.append(hn3_list)
    localrow.append(hn4_text)
    localrow.append(hn4_text2)
    localrow.append(hn4_text3)
    localrow.append(hn4_list)
    localrow.append(hn5_text)
    localrow.append(hn5_text2)
    localrow.append(hn5_text3)
    localrow.append(hn5_list)
    localrow.append(hn6_text)
    localrow.append(hn6_text2)
    localrow.append(hn6_text3)
    localrow.append(hn6_list)
    localrow.append(hn7_text)
    localrow.append(hn7_text2)
    localrow.append(hn7_text3)
    localrow.append(hn7_list)
    localrow.append(hn8_text)
    localrow.append(hn8_text2)
    localrow.append(hn8_text3)
    localrow.append(hn8_list)
    localrow.append(hn9_text)
    localrow.append(hn9_text2)
    localrow.append(hn9_text3)
    localrow.append(hn9_list)
    localrow.append(hn10_text)
    localrow.append(hn10_text2)
    localrow.append(hn10_text3)
    localrow.append(hn10_list)
    localrow.append(hn11_text)
    localrow.append(hn11_text2)
    localrow.append(hn11_text3)
    localrow.append(hn11_list)
    localrow.append(hn12_text)
    localrow.append(hn12_text2)
    localrow.append(hn12_text3)
    localrow.append(hn12_list)
    outfilehandle.writerow(localrow)

infilehandle.close()
fout.close()
