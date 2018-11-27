## reads and extracts info from txt files of published opinions from USCOA
## downloaded from LexisNexis
## written for python 2.6.*
##
## modified version of LexisOpinionParse.py by
## Kevin Quinn
## UC Berkeley
## 5/13/2010
##
## modifications by
## Rachael Hinkle
## 6/7/2013

import os
import re
import csv
import string
import operator
import pickle
import sys
from sets import Set

mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"

## function to expand abbreviated month names
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

## function to convert month names to numbers
def month2number(mstring):
    mnumber = -999
    if (mstring == "January"):
        mnumber = "01"
    if (mstring == "February"):
        mnumber = "02"
    if (mstring == "March"):
        mnumber = "03"
    if (mstring == "April"):
        mnumber = "04"
    if (mstring == "May"):
        mnumber = "05"
    if (mstring == "June"):
        mnumber = "06"
    if (mstring == "July"):
        mnumber = "07"
    if (mstring == "August"):
        mnumber = "08"
    if (mstring == "September"):
        mnumber = "09"
    if (mstring == "October"):
        mnumber = "10"
    if (mstring == "November"):
        mnumber = "11"
    if (mstring == "December"):
        mnumber = "12"
    return mnumber

## function to convert circuit names to numbers, DC Circuit == 12
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

def Capitalize(nstring):
    if(len(nstring) > 1 and not re.match("MC|Mc|Mac|MAC|O'|Van|VAN", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1:])
    if(re.match("MC|Mc", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1]) + string.upper(nstring[2]) + string.lower(nstring[3:])
    if(re.match("MAC|Mac", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1:3]) + string.upper(nstring[3]) + string.lower(nstring[4:])
    if(re.match("O\'", nstring)):
        nstring = string.upper(nstring[0]) + nstring[1] + string.upper(nstring[2]) + string.lower(nstring[3:])
    if(re.match("Van\s|VAN\s", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1:4]) + string.upper(nstring[4]) + string.lower(nstring[5:])
    if(len(nstring) == 1):
        nstring = string.upper(nstring)
    return nstring

def lastname(nstring):
    last_name = ""
    nstring = string.strip(nstring)
    nstring = re.sub("BY THE COURT", "", nstring)
    nstring = re.sub("PER CURIAM[;]*", "", nstring)
    nstring = re.sub(", (Jr\.|JR\.|III|Sr\.|SR\.)", "", nstring)
    #nstring = re.sub("\(In Part\)", "", nstring)
    #nstring = re.sub("[\s]+", " ", nstring)
    names_holder = re.split("\s", nstring)
    if(len(names_holder) == 1):
        last_name = names_holder[0]
    if(len(names_holder) == 2 and not re.search(",", nstring)):
        last_name = names_holder[1]
    if(len(names_holder) == 2 and re.search(",", nstring)):
        last_name = names_holder[0]
    if(len(names_holder) == 3 and not re.search(",", nstring)):
        last_name = names_holder[2]
    if(len(names_holder) == 3 and re.search(",", nstring)):
        last_name = names_holder[0]
    if(len(names_holder) == 4 and not re.search(",", nstring)):
        last_name = names_holder[2] + " " + names_holder[3]
    if(len(names_holder) == 4 and re.search(",", nstring)):
        last_name = names_holder[0] + " " + names_holder[1]
    last_name = re.sub(",", "", last_name)
    last_name = re.sub("\.", "", last_name)
    last_name = Capitalize(last_name)
    return last_name

def firstname(nstring):
    first_name = ""
    nstring = string.strip(nstring)
    nstring = re.sub("BY THE COURT", "", nstring)
    nstring = re.sub("PER CURIAM[;]*", "", nstring)
    nstring = re.sub(", (Jr\.|JR\.|III|Sr\.|SR\.)", "", nstring)
    #nstring = re.sub("\(In Part\)", "", nstring)
    #nstring = re.sub("[\s]+", " ", nstring)
    names_holder = re.split("\s", nstring)
    if(len(names_holder) == 2 and not re.search(",", nstring)):
        first_name = names_holder[0]
    if(len(names_holder) == 2 and re.search(",", nstring)):
        first_name = names_holder[1]
    if(len(names_holder) == 3 and not re.search(",", nstring)):
        first_name = names_holder[0]
    if(len(names_holder) == 3 and re.search(",", nstring)):
        first_name = names_holder[1]
    if(len(names_holder) == 4 and not re.search(",", nstring)):
        first_name = names_holder[0]
    if(len(names_holder) == 4 and re.search(",", nstring)):
        first_name = names_holder[2]
    first_name = re.sub(",", "", first_name)
    first_name = Capitalize(first_name)
    return first_name

def middlename(nstring):
    middle_name = ""
    nstring = string.strip(nstring)
    nstring = re.sub("BY THE COURT", "", nstring)
    nstring = re.sub("PER CURIAM[;]*", "", nstring)
    nstring = re.sub(", (Jr\.|JR\.|III|Sr\.|SR\.)", "", nstring)
    #nstring = re.sub("\(In Part\)", "", nstring)
    #nstring = re.sub("[\s]+", " ", nstring)
    names_holder = re.split("\s", nstring)
    if(len(names_holder) == 3 and not re.search(",", nstring)):
        middle_name = names_holder[1]
    if(len(names_holder) == 3 and re.search(",", nstring)):
        middle_name = names_holder[2]
    if(len(names_holder) == 4 and not re.search(",", nstring)):
        middle_name = names_holder[1]
    if(len(names_holder) == 4 and re.search(",", nstring)):
        middle_name = names_holder[3]
    middle_name = re.sub(",", "", middle_name)
    middle_name = Capitalize(middle_name)
    return middle_name

def namesuffix(nstring):
    suffix = ""
    nstring = string.strip(nstring)
    nstring = re.sub("BY THE COURT", "", nstring)
    nstring = re.sub("PER CURIAM[;]*", "", nstring)
    #nstring = re.sub("\(In Part\)", "", nstring)
    #nstring = re.sub("[\s]+", " ", nstring)
    if(re.search("Jr\.|JR\.", nstring)):
        suffix = "Jr."
    if(re.search("III", nstring)):
        suffix = "III"
    if(re.search("II", nstring)):
        suffix = "II"
    if(re.search("Sr\.|SR\.", nstring)):
        suffix = "Sr."
    return suffix

with open("agencyList.txt", "rb") as fp:   # Unpickling
    agencylist = pickle.load(fp)

# .csv file where extracted metadata will be stored
fout = open(mydir + "adminMetadata_AgencyCounts_Jun8_1.csv", "wb")
outfilehandle = csv.writer(fout,
                           delimiter=",",
                           quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)

# Create your own label for each column of the metadata .csv file
localrow = []
#localrow.append("caseID")
localrow.append("filename")
localrow.append("year")
#localrow.append("month")
localrow.append("parties")
#localrow.append("docketnum")
localrow.append("Court")
localrow.append("Circuit")
localrow.append("LexisCite")
localrow.append("ReporterCite")
#localrow.append("Unpublished")
#localrow.append("numCoreTerms")
localrow.append("first_hn")
localrow.append("second_hn")
localrow.append("third_hn")
#localrow.append("hn")
#localrow.append("hn2")
#localrow.append("hn3")
#localrow.append("coreterms")
#localrow.append("Prior History")
#localrow.append("Notice")
#localrow.append("Per Curiam")
#localrow.append("En Banc")
#localrow.append("Petion for Rehearing")
localrow.append("Dissent Num")
localrow.append("Concur Num")
#localrow.append("Ruling Date")
#localrow.append("Action/Date")
localrow.append("disposition")
#localrow.append("disp len") # New
#localrow.append("designation")
localrow.append("judges")
#localrow.append("judges short")
localrow.append("dissenting")
localrow.append("concurring")
localrow.append("Judge1")
localrow.append("Judge2")
localrow.append("Judge3")
localrow.append("Author")
localrow.append("FullTitle")
localrow.append("Agency")
localrow.append("CheckAgency")
#localrow.append("Check case")
#localrow.append("Subsequent History")
#localrow.append("Prior History")
#localrow.append("Case Summary")
#localrow.append("Procedural Posture")
#localrow.append("Overview")
#localrow.append("Outcome")
#localrow.append("Core Terms")
localrow.append("hn1")
localrow.append("hn2")
localrow.append("hn3")
localrow.append("hn4")
localrow.append("hn5")
localrow.append("hn6")
localrow.append("hn7")
localrow.append("hn8")
localrow.append("hn9")
localrow.append("hn10")
localrow.append("hn11")
localrow.append("hn12")
localrow.append("hn13")
localrow.append("hn14")
localrow.append("hn15")
localrow.append("hn17")
localrow.append("hn18")
localrow.append("hn19")
localrow.append("hn20")
localrow.append("hn21")
localrow.append("hn22")
localrow.append("hn23")
localrow.append("hn24")
localrow.append("hn25")
localrow.append("hn26")
localrow.append("hn27")
localrow.append("hn28")
localrow.append("hn29")
localrow.append("hn30")
#localrow.append("hnSovImmunity")
localrow.append("opinion_words") ## number of words in all opinions
#localrow.append("Short Opinion text")
#localrow.append("Designation")
#localrow.append("Header")
localrow.append("maxoccurrences")
localrow.append("maxagency")
for ag in agencylist:
    localrow.append(ag)
outfilehandle.writerow(localrow)


# Name of folder where all cases are located (and nothing else)
dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
#print dirlist
print len(dirlist)
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

#dirlist = [file for file in dirlist if len(file) > 20]

# Use (uncomment) following line to test code on a small handful of cases
cleandirlist = cleandirlist[42312:42313]

for entry in cleandirlist: ## each entry is a txt file with an opinion
    print entry
    infilepath = dirname + entry
    infilehandle = open(infilepath)
    txtlines = infilehandle.readlines()
    case_text = ''.join(txtlines)
    action_number = 0
    parties_line = False
    blank_after_parties = False
    docket_line = False
    blank_after_docket = False
    court_line = False
    blank_after_court = False
    fn_line = False
    cite_line = False
    blank_after_cite = False
    action_line = False
    disposition_line = False
    prior_history_line = False
    headnotes_line = False
    trunc_text = False
    judges_line = False
    opin_by_line = False
    opinion_line = False
    dissent_by_line = False
    concur_by_line = False
    opinion_word_count = 0
    localrow = []
    action_number = 0
    searchterms_string = ""
    shep_treat = ""
    parties_string = ""
    docketnum = ""
    court_string = ""
    cite_string = ""
    Fed_cite = ""
    Lexis_cite = ""
    action_string = ""
    per_curiam = 0
    action1 = ""
    date = ""
    action1_month = ""
    action1_day = ""
    action1_year = ""
    action1_date = ""
    action1_action = ""
    action2 = ""
    action2_month = ""
    action2_day = ""
    action2_year = ""
    action2_date = ""
    action2_action = ""
    prior_history_string = ""
    sub_history_string = ""
    disposition_string = ""
    pc_holder = ""
    judges_string = ""
    desjud = ""
    judge1_ln = ""
    judge1_fn = ""
    judge1_mn = ""
    judge1_suf = ""
    judge1_full = ""
    judge2_ln = ""
    judge2_fn = ""
    judge2_mn = ""
    judge2_suf = ""
    judge2_full = ""
    judge3_ln = ""
    judge3_fn = ""
    judge3_mn = ""
    judge3_suf = ""
    judge3_full = ""
    opin_by_string = ""
    author_ln = ""
    author_fn = ""
    author_mn = ""
    author_suf = ""
    author_full = ""
    dissent1_ln = ""
    dissent1_fn = ""
    dissent1_mn = ""
    dissent1_suf = ""
    dissent1_full = ""
    dissent2_ln = ""
    dissent2_fn = ""
    dissent2_mn = ""
    dissent2_suf = ""
    dissent2_full = ""
    dissent3_ln = ""
    dissent3_fn = ""
    dissent3_mn = ""
    dissent3_suf = ""
    dissent3_full = ""
    dissent4_ln = ""
    dissent4_fn = ""
    dissent4_mn = ""
    dissent4_suf = ""
    dissent4_full = ""
    concur1_ln = ""
    concur1_fn = ""
    concur1_mn = ""
    concur1_suf = ""
    concur1_full = ""
    concur2_ln = ""
    concur2_fn = ""
    concur2_mn = ""
    concur2_suf = ""
    concur2_full = ""
    concur3_ln = ""
    concur3_fn = ""
    concur3_mn = ""
    concur3_suf = ""
    concur3_full = ""
    concur4_ln = ""
    concur4_fn = ""
    concur4_mn = ""
    concur4_suf = ""
    concur4_full = ""
    concur5_ln = ""
    concur5_fn = ""
    concur5_mn = ""
    concur5_suf = ""
    concur5_full = ""
    concur6_ln = ""
    concur6_fn = ""
    concur6_mn = ""
    concur6_suf = ""
    concur6_full = ""
    concur7_ln = ""
    concur7_fn = ""
    concur7_mn = ""
    concur7_suf = ""
    concur7_full = ""
    concur_by_string = ""
    dissent_by_string = ""
    judges_holder = []
    dissent_holder = []
    concur_holder = []
    prelim = False
    shep_line = False
    blank_after_shep = False
    parties_line = False
    blank_after_parties = False
    docket_line = False
    blank_after_docket = False
    court_line = False
    blank_after_court = False
    cite_line = False
    blank_after_cite = False
    action_line = False
    disposition_line = False
    prior_history_line = False
    headnotes_line = False
    sub_history_line = False
    judges_line = False
    opin_by_line = False
    opinion_line = False
    dissent_by_line = False
    concur_by_line = False
    opinion_word_count = 0
    circuit = 0
    en_banc = ""
    dissent = 0
    concur = 0
    rehearing = ""
    check_case = 0
    op_string = ""
    unpublished = 0
    num_dissent = 0
    num_concur = 0
    caseid = "ID."
    listid = ""
    citeid = 0
    fed_cite_hol = []
    short_op = ""
    judge_string2 = ""
    judge1 = ""
    judge2 = ""
    judge3 = ""
    judge_holder2 = []

    localrow = []
    #listid =str(re.split("\.", entry)[0])
    #citeid = int(re.split("\.", entry)[1])
    #year = re.split("\.", entry)[2]

    #if citeid < 10:
    #    caseid += listid + ".00" + str(citeid)
    #else:
    #    if citeid < 100:
    #        caseid += listid + ".0" + str(citeid)
    #    else:
    #        caseid += listid + "." + str(citeid)

    listid = 5555
    caseid = 6666
    year = 0

    #print entry
    #print citeid
    #print caseid

    case_with_preamble = False
    notice_line = False
    notice_string = ""
    prior_history_line = False
    phist = ""
    subsequent_history_line = False
    shist = ""
    case_sum_line = False
    case_sum_string = ""
    proc_pos_line = False
    proc_pos_string = ""
    overview_line = False
    overview_string = ""
    outcome_line = False
    outcome_string = ""
    core_terms_line = False
    core_terms_string = ""

    desig_line = False
    desig_string = ""

    header_line = False
    header = ""

    finished_header = False
    finished_parties = False
    finished_court = False
    finished_date = False
    finished_docket = False
    finished_reporter = False
    finished_cite = False
    blank_cite_line = False
    finished_full_case = False
    full_case_name = ""
    action_year = 0
    headnote_string = ""
    headnote_tmp = ""
    headnote_holder = []
    coreterms_holder = []
    coreterms_line = False
    headnote_line = False
#    case_text = ""

    for txtline in txtlines:
 #       case_text = case_text + txtline.strip()

        if(finished_cite):
           finished_cite = False
           full_case_name = txtline
           full_case_name = str(txtline)
           full_case_name = string.strip(full_case_name)
           ##print full_case_name

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
            #print len(split_action)
            #print split_action
            #print action2
            #print action_string
            #print date + "\n"
            #print len(date)



        #if(blank_after_docket and re.search("[\w]+", txtline)):
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
            #print string.strip(parties_string)


##        if (docket_line and re.match("^[\s]+$", txtline)):
##            ## done with parties block
##            blank_after_docket = True
##            docket_line = False
##            docketnum = re.sub("[\s]+", " ", docketnum)

##        if(blank_after_parties and re.search("^[\s]+(Docket|Misc|No\.|Nos\.|Civ|Crim|NO|C\.A\.|CA |91-|DOCKET|Case No)", txtline)):
##            ## the docket number
##            docket_line = True
##            docketnum = docketnum + txtline

##        if(blank_after_parties and re.search("^[\s]{30,}[0-9]+-[0-9]+[\s]*$", txtline)):
##            ## the docket number
##            docket_line = True
##            docketnum = docketnum + txtline

##        if(docket_line and re.match("^[\s]+$", txtline)):
##            ## this is the blank line after docket number
##            blank_after_parties = False
##            docket_line = False
##            blank_after_docket = True
##            docketnum = string.strip(docketnum)
##            docketnum = re.sub("\s", "", docketnum)
##            #print docketnum + "\n"


##        if(court_line and re.match("^[\s]+$", txtline)):
##            ## this is the blank line after court
##            blank_after_docket = False
##            court_line = False
##            blank_after_court = True

##        if(blank_after_court and re.search("^[\s]+\*", txtline)):
##            ## the citation block
##            fn_line = True
##            blank_after_court = False
            #fn_string = fn_string + txtline

##        if(fn_line and re.match("^[\s]+$", txtline)):
##            #blank_after_fn = True
##            blank_after_court = True
##            fn_line = False


##        if(re.match("^NOTICE:", txtline)):
##            notice_line = True
##        if(notice_line and re.search("[\w]+", txtline)):
##            notice_string = notice_string + txtline
##        if (notice_line and re.match("^[\s]+$", txtline)):
##            notice_string = re.sub("NOTICE:\s+\[\*+[0-9]+\]\s+", "", notice_string)
##            notice_string = re.sub("NOTICE:\s*", "", notice_string)
##            notice_string = re.sub("\xa0", " ", notice_string)
##            notice_string = re.sub("\n|\r", " ", notice_string)
##            notice_string = string.strip(notice_string)
##            notice_line = False
##            #print notice_string

##        if(re.match("^SUBSEQUENT HISTORY:", txtline)):
##            subsequent_history_line = True
##        if(subsequent_history_line and re.search("[\w]+", txtline)):
##            shist = shist + txtline
##        if (subsequent_history_line and re.match("^[\s]+$", txtline)):
##            shist = re.sub("SUBSEQUENT HISTORY:\s+\[\*+[0-9]+\]\s+", "", shist)
##            shist = re.sub("SUBSEQUENT HISTORY:", "", shist)
##            shist = re.sub("\xa0", " ", shist)
##            shist = re.sub("\n|\r", " ", shist)
##            shist = string.strip(shist)
##            subsequent_history_line = False

        if(re.match("^PRIOR HISTORY:|^Prior History:", txtline)):
            prior_history_line = True
        if(prior_history_line and re.search("[\w]+", txtline)):
            phist = phist + txtline
        if (prior_history_line and re.match("^[\s]+$", txtline)):
            phist = re.sub("PRIOR HISTORY:\s+\[\*+[0-9]+\]\s+", "", phist)
            phist = re.sub("PRIOR HISTORY:", "", phist)
            phist = re.sub("\xa0", " ", phist)
            phist = re.sub("\n|\r", " ", phist)
            phist = string.strip(phist)
            prior_history_line = False

##        if(re.match("^CASE SUMMARY:", txtline)):
##            case_sum_line = True
##        if(case_sum_line and re.search("[\w]+", txtline)):
##            case_sum_string = case_sum_string + txtline
##        if (case_sum_line and re.match("^[\s]+$", txtline)):
##            case_sum_string = re.sub("CASE SUMMARY:\s+\[\*+[0-9]+\]\s+", "", case_sum_string)
##            case_sum_string = re.sub("CASE SUMMARY:\s*", "", case_sum_string)
##            case_sum_string = re.sub("\xa0", " ", case_sum_string)
##            case_sum_string = re.sub("\n|\r", " ", case_sum_string)
##            case_sum_string = string.strip(case_sum_string)
##            case_sum_line = False
##            #print case_sum_string

##        if(re.match("^PROCEDURAL POSTURE:", txtline)):
##            proc_pos_line = True
##        if(proc_pos_line and re.search("[\w]+", txtline)):
##            proc_pos_string = proc_pos_string + txtline
##        if (proc_pos_line and re.match("^[\s]+$", txtline)):
##            proc_pos_string = re.sub("PROCEDURAL POSTURE:\s+\[\*+[0-9]+\]\s+", "", proc_pos_string)
##            proc_pos_string = re.sub("PROCEDURAL POSTURE:\s*", "", proc_pos_string)
##            proc_pos_string = re.sub("\xa0", " ", proc_pos_string)
##            proc_pos_string = re.sub("\n|\r", " ", proc_pos_string)
##            proc_pos_string = string.strip(proc_pos_string)
##            proc_pos_line = False
##            #print proc_pos_string

##        if(re.match("^OVERVIEW:", txtline)):
##            overview_line = True
##        if(overview_line and re.search("[\w]+", txtline)):
##            overview_string = overview_string + txtline
##        if (overview_line and re.match("^[\s]+$", txtline)):
##            overview_string = re.sub("OVERVIEW:\s+\[\*+[0-9]+\]\s+", "", overview_string)
##            overview_string = re.sub("OVERVIEW:\s*", "", overview_string)
##            overview_string = re.sub("\xa0", " ", overview_string)
##            overview_string = re.sub("\n|\r", " ", overview_string)
##            overview_string = string.strip(overview_string)
##            overview_line = False
##            #print overview_string
##
##        if(re.match("^OUTCOME:", txtline)):
##            outcome_line = True
##        if(outcome_line and re.search("[\w]+", txtline)):
##            outcome_string = outcome_string + txtline
##        if (outcome_line and re.match("^[\s]+$", txtline)):
##            outcome_string = re.sub("OUTCOME:\s+\[\*+[0-9]+\]\s+", "", outcome_string)
##            outcome_string = re.sub("OUTCOME:\s*", "", outcome_string)
##            outcome_string = re.sub("\xa0", " ", outcome_string)
##            outcome_string = re.sub("\n|\r", " ", outcome_string)
##            outcome_string = string.strip(outcome_string)
##            outcome_line = False
##            #print outcome_string


##        if(re.match("^CORE TERMS:", txtline)):
##            core_terms_line = True
##        if(core_terms_line and re.search("[\w]+", txtline)):
##            core_terms_string = core_terms_string + txtline
##        if (core_terms_line and re.match("^[\s]+$", txtline)):
##            core_terms_string = re.sub("CORE TERMS:\s+\[\*+[0-9]+\]\s+", "", core_terms_string)
##            core_terms_string = re.sub("CORE TERMS:\s*", "", core_terms_string)
##            core_terms_string = re.sub("\xa0", " ", core_terms_string)
##            core_terms_string = re.sub("\n|\r", " ", core_terms_string)
##            core_terms_string = string.strip(core_terms_string)
##            core_terms_line = False
##            #print core_terms_string

        if (re.match("^DISPOSITION:|Disposition", txtline)):
            ## disposition of case
            disposition_line = True
        if (disposition_line and re.search("[\w]+", txtline)):
            ## disposition lines with text
            disposition_string = disposition_string + txtline
        ##if (disposition_line and re.match("^[\s]+$", txtline)):
            #blank line after disposition line
            disposition_string = re.sub("DISPOSITION:", "", disposition_string)
            disposition_string = re.sub("Disposition:", "", disposition_string)
            disposition_string = re.sub("\xa0", " ", disposition_string)
            disposition_string = re.sub("\n|\r", " ", disposition_string)
            disposition_string = re.sub("\[.+\]", "", disposition_string)
            disposition_string = string.strip(disposition_string)
            #print disposition_string[0:4]
            #print len(disposition_string)
            disposition_line = False

            if len(disposition_string) > 401:
                disposition_string = disposition_string[0:400]

            if (re.search("affirm|Affirm|AFFIRM|reverse|Reverse|REVERSE", disposition_string)):
                rehearing = "NO"

            if (re.search("vacate|Vacate|VACATE", disposition_string)):
                rehearing = "NO"

            if (re.search("(P|p)etition for (R|r)ehearing", disposition_string) and rehearing != "NO"):
                rehearing = "YES"

        if (re.search("Petition[s]* for Rehearing", txtline) and rehearing == ""):
            rehearing = "CHECK"

        if (re.search("REHEARING", txtline) and rehearing != "YES"):
            rehearing = "TRUNCATE"

        if (re.match("^CORE TERMS:", txtline)):
            coreterms = txtline
            #print coreterms
            coreterms_holder = re.split(", ", coreterms)
            #print len(coreterms_holder)
            coreterms_line = True


        if (re.search("LexisNexis", txtline) and re.search("Headnotes", txtline)):
            headnote_line = True
            coreterms_line = False
            #print repr(txtline)
        if (headnote_line and re.search(">", txtline)):
            #headnote_tmp = txtline + "|"
            headnote_string = headnote_string + txtline
            #print repr(txtline)
            #print headnote_string
            #print headnote_tmp
            #print headnote_line

        if (re.search("OPINION BY: (PER CURIAM)|(Per Curiam)", txtline)):
            #pc_holder = pc_holder + "Per Curiam. "
            per_curiam = 1
            headnote_line = False
        if (re.search("PER CURIAM", txtline)):
            #pc_holder = pc_holder + "Per Curiam. "
            per_curiam = per_curiam + 1
            headnote_line = False
        if (re.search("^[\s]*Per Curiam[\.:\s]*$", txtline)):
            per_curiam = 1
            headnote_line = False
            #print pc_holder + "\n"


        if (re.match("^JUDGES:|^Judges:", txtline) and not trunc_text):
            ## judges hearing case
            judges_line = True
            headnote_line = False
        if (judges_line and re.search("[\w]+", txtline)):
            ## judges lines with text
            judges_string = judges_string + txtline
        ##if (judges_line and re.match("^[\s]+$", txtline)):
            # blank line after judges line
            judges_string = re.sub("JUDGES:", "", judges_string)
            judges_string = re.sub("Judges:", "", judges_string)
            judges_string = re.sub("\xa0", " ", judges_string)
            judges_string = re.sub("\n|\r", " ", judges_string)
            judges_string = string.strip(judges_string)
            #print judges_string
            judges_line = False
            judges_holder = re.sub("\[\**\d*\]", "", judges_string)
            judges_holder = re.sub("\*|\d", "", judges_holder)
            judges_holder = re.sub("Before:? ", "", judges_holder)
            judges_holder = re.sub("BEFORE:? ", "", judges_holder)
            judges_holder = re.sub("PRESENT:? ", "", judges_holder)
            judges_holder = re.sub("Present:? ", "", judges_holder)
            judges_holder = re.sub("Hon\. ", "", judges_holder)
            judges_holder = re.sub("HON\. ", "", judges_holder)
            judges_holder = re.sub("Honorable ", "", judges_holder)
            judges_holder = re.sub("HONORABLE ", "", judges_holder)
            judges_holder = re.sub(", (Circuit|Circuit) (J|j)udge[s]?\.?", "", judges_holder)
            judges_holder = re.sub(", (District|DISTRICT) (J|j)udge[s]?\.?", "", judges_holder)
            judges_holder = re.sub("Chief Judge", "", judges_holder)
            judges_holder = re.sub("Senior Judge", "", judges_holder)
            judges_holder = re.sub("Chief District Judge", "", judges_holder)
            judges_holder = re.sub("Associate Justice", "", judges_holder)
            judges_holder = re.sub(", (Jr\.|JR\.)", "Jr.", judges_holder)
            judges_holder = re.sub(", (Sr\.|SR\.)", "Sr.", judges_holder)
            judges_holder = re.sub(", III", "III", judges_holder)
            judges_holder = re.sub(", II", "II", judges_holder)
            judges_holder = re.sub(";", ",", judges_holder)

            judges_holder = re.sub(",[\s]*,", ",", judges_holder)
            judges_holder = re.sub(" and ", ", ", judges_holder)
            judges_holder = re.sub("[\s]+", " ", judges_holder)
            judges_holder = re.split(", ", judges_holder)
            #print judges_holder
            if (len(judges_holder) > 1):
                judge1_ln = lastname(judges_holder[0])
                judge1_fn = firstname(judges_holder[0])
                judge1_mn = middlename(judges_holder[0])
                judge1_suf = namesuffix(judges_holder[0])
                judge1_full = judge1_ln + ", " + judge1_fn + " " + judge1_mn + " " + judge1_suf
                judge1_full = re.sub("[\s]+", " ", judge1_full)
                judge1_full = re.sub(", $", "", judge1_full)

                judge2_ln = lastname(judges_holder[1])
                judge2_fn = firstname(judges_holder[1])
                judge2_mn = middlename(judges_holder[1])
                judge2_suf = namesuffix(judges_holder[1])
                judge2_full = judge2_ln + ", " + judge2_fn + " " + judge2_mn + " " + judge2_suf
                judge2_full = re.sub("[\s]+", " ", judge2_full)
                judge2_full = re.sub(", $", "", judge2_full)

            if (len(judges_holder) > 2):

                judge3_ln = lastname(judges_holder[2])
                judge3_fn = firstname(judges_holder[2])
                judge3_mn = middlename(judges_holder[2])
                judge3_suf = namesuffix(judges_holder[2])
                judge3_full = judge3_ln + ", " + judge3_fn + " " + judge3_mn + " " + judge3_suf
                judge3_full = re.sub("[\s]+", " ", judge3_full)
                judge3_full = re.sub(", $", "", judge3_full)
            if (len(judges_holder) > 3):
                check_case = 1
                #print judges_string


        if (re.match("^OPINION BY:|^Opinion by:", txtline) and not trunc_text):
            ## opinion writer
            opin_by_line = True
            headnote_line = False
        if (opin_by_line and re.search("[\w]+", txtline)):
            ## opinion by line with text
            opin_by_string = opin_by_string + txtline
        ##if (opin_by_line and re.match("^[\s]+$", txtline)):
            # blank line after opinion by line
            opin_by_string = re.sub("OPINION BY:", "", opin_by_string)
            opin_by_string = re.sub("Opinion by", "", opin_by_string)
            opin_by_string = re.sub("\[\*+\d+\]", "", opin_by_string)
            opin_by_string = re.sub("\*[\d]*", "", opin_by_string)
            opin_by_string = re.sub(", Circuit Judge", "", opin_by_string)
            opin_by_string = string.strip(opin_by_string)
            #print "Opinion writer: " + opin_by_string + "\n"
            opin_by_line = False
            #print opin_by_string
            author_ln = lastname(opin_by_string)
            author_fn = firstname(opin_by_string)
            author_mn = middlename(opin_by_string)
            author_suf = namesuffix(opin_by_string)
            author_full = author_ln + ", " + author_fn + " " + author_mn + " " + author_suf
            author_full = re.sub("[\s]+", " ", author_full)
            author_full = re.sub(", $", "", author_full)
            author_full = re.sub(", :", "", author_full)
            #print author_full

        if (re.match("^OPINION|^Opinion", txtline) and not trunc_text):
            prelim = False
            opinion_line = True
            headnote_line = False
        if (re.match(re.escape("********** Print Completed **********"), txtline) or re.match("APPENDIX", txtline) or re.match("^CONCUR BY:", txtline) or re.match("^DISSENT BY:", txtline)):
            opinion_line = False

        if(prelim and re.search("^\*[\s]+", txtline)):
            desjud += txtline

        if opinion_line:
            op_string = txtline
            op_holder = re.sub("^OPINION", " ", op_string)
            op_holder = re.sub("\xa0", " ", op_holder)
            op_holder = re.sub("\n|\r", " ", op_holder)
            op_holder = re.sub("\[\*+[0-9]+\]", " ", op_holder)
            #op_holder = re.sub("No opinion\.", " ", op_holder)
            op_holder = string.strip(op_holder)
            op_holder = re.split("\s+", op_holder)
            op_holder = [word for word in op_holder if word != ""]
            opinion_word_count += len(op_holder)
            if opinion_word_count < 150:
                short_op += op_string

        if (re.match("^DISSENT BY:|^Dissent by:", txtline) and not trunc_text):
            dissent_by_line = True
            dissent = dissent + 1
        if (dissent_by_line and re.search("[\w]+", txtline)):
            dissent_by_string = dissent_by_string + txtline
            dissent_by_line = False
        ##if (dissent_by_line and re.match("^[\s]+$", txtline)):
            dissent_by_string = string.strip(dissent_by_string)
            #dissent_by_string = string.lstrip(dissent_by_string)
            #dissent_by_string = string.rstrip(dissent_by_string)
            dissent_by_string = re.sub("\n", " ", dissent_by_string)
            dissent_by_string = re.sub("Dissent by: ", "", dissent_by_string)
            dissent_by_string = re.sub("DISSENT BY: ", "", dissent_by_string)
            dissent_by_string = re.sub("\[.+\]", "", dissent_by_string)
            dissent_by_string = re.sub("[\s]*\(In[\s]*(P|p)art\)", "", dissent_by_string)
            dissent_by_string = re.sub("\*\d+", "", dissent_by_string)
            dissent_by_string = re.sub("\d+", "", dissent_by_string)
            dissent_by_string = re.sub("[\s]*;", ";", dissent_by_string)
            dissent_holder = re.split("; ", dissent_by_string)
            num_dissent = len(dissent_holder)
            dissent_by_line = False
            dissent1_ln = lastname(dissent_holder[0])
            dissent1_fn = firstname(dissent_holder[0])
            dissent1_mn = middlename(dissent_holder[0])
            dissent1_suf = namesuffix(dissent_holder[0])
            if (len(dissent_holder) > 1):
                dissent2_ln = lastname(dissent_holder[1])
                dissent2_fn = firstname(dissent_holder[1])
                dissent2_mn = middlename(dissent_holder[1])
                dissent2_suf = namesuffix(dissent_holder[1])
            if (len(dissent_holder) > 2):
                dissent3_ln = lastname(dissent_holder[2])
                dissent3_fn = firstname(dissent_holder[2])
                dissent3_mn = middlename(dissent_holder[2])
                dissent3_suf = namesuffix(dissent_holder[2])
            if (len(dissent_holder) > 3):
                dissent4_ln = lastname(dissent_holder[3])
                dissent4_fn = firstname(dissent_holder[3])
                dissent4_mn = middlename(dissent_holder[3])
                dissent4_suf = namesuffix(dissent_holder[3])
            dissent1_full = dissent1_ln + ", " + dissent1_fn + " " + dissent1_mn + " " + dissent1_suf
            dissent1_full = re.sub("[\s]+", " ", dissent1_full)
            dissent1_full = re.sub(", $", "", dissent1_full)
            dissent2_full = dissent2_ln + ", " + dissent2_fn + " " + dissent2_mn + " " + dissent2_suf
            dissent2_full = re.sub("[\s]+", " ", dissent2_full)
            dissent2_full = re.sub(", $", "", dissent2_full)
            dissent3_full = dissent3_ln + ", " + dissent3_fn + " " + dissent3_mn + " " + dissent3_suf
            dissent3_full = re.sub("[\s]+", " ", dissent3_full)
            dissent3_full = re.sub(", $", "", dissent3_full)
            dissent4_full = dissent4_ln + ", " + dissent4_fn + " " + dissent4_mn + " " + dissent4_suf
            dissent4_full = re.sub("[\s]+", " ", dissent4_full)
            dissent4_full = re.sub(", $", "", dissent4_full)
            dissent_by_line = False

        if (re.match("^CONCUR BY:|^Concur by:", txtline) and not trunc_text):
            concur_by_line = True
            concur = concur + 1
        if (concur_by_line and re.search("[\w]+", txtline)):
            concur_by_string = concur_by_string + txtline
            concur_by_line = False
        #if (concur_by_line and re.match("^[\s]+$", txtline)):
            concur_by_string = string.strip(concur_by_string)
            #concur_by_string = string.lstrip(concur_by_string)
            #concur_by_string = string.rstrip(concur_by_string)
            concur_by_string = re.sub("\n", " ", concur_by_string)
            concur_by_string = re.sub("Concur by: ", "", concur_by_string)
            concur_by_string = re.sub("CONCUR BY: ", "", concur_by_string)
            concur_by_string = re.sub("\[.+\]", "", concur_by_string)
            concur_by_string = re.sub("[\s]*\(In[\s]*(P|p)art\)", "", concur_by_string)
            concur_by_string = re.sub("\*\d+", "", concur_by_string)
            concur_by_string = re.sub("\d+", "", concur_by_string)
            concur_by_string = re.sub("[\s]*;", ";", concur_by_string)
            concur_holder = re.split("; ", concur_by_string)
            num_concur = len(concur_holder)
            concur_by_line = False
            concur1_ln = lastname(concur_holder[0])
            concur1_fn = firstname(concur_holder[0])
            concur1_mn = middlename(concur_holder[0])
            concur1_suf = namesuffix(concur_holder[0])
            if (len(concur_holder) > 1):
                concur2_ln = lastname(concur_holder[1])
                concur2_fn = firstname(concur_holder[1])
                concur2_mn = middlename(concur_holder[1])
                concur2_suf = namesuffix(concur_holder[1])
            if (len(concur_holder) > 2):
                concur3_ln = lastname(concur_holder[2])
                concur3_fn = firstname(concur_holder[2])
                concur3_mn = middlename(concur_holder[2])
                concur3_suf = namesuffix(concur_holder[2])
            if (len(concur_holder) > 3):
                concur4_ln = lastname(concur_holder[3])
                concur4_fn = firstname(concur_holder[3])
                concur4_mn = middlename(concur_holder[3])
                concur4_suf = namesuffix(concur_holder[3])
            if (len(concur_holder) > 4):
                concur5_ln = lastname(concur_holder[4])
                concur5_fn = firstname(concur_holder[4])
                concur5_mn = middlename(concur_holder[4])
                concur5_suf = namesuffix(concur_holder[4])
            if (len(concur_holder) > 5):
                concur6_ln = lastname(concur_holder[5])
                concur6_fn = firstname(concur_holder[5])
                concur6_mn = middlename(concur_holder[5])
                concur6_suf = namesuffix(concur_holder[5])
            if (len(concur_holder) > 6):
                concur7_ln = lastname(concur_holder[6])
                concur7_fn = firstname(concur_holder[6])
                concur7_mn = middlename(concur_holder[6])
                concur7_suf = namesuffix(concur_holder[6])
            concur1_full = concur1_ln + ", " + concur1_fn + " " + concur1_mn + " " + concur1_suf
            concur1_full = re.sub("[\s]+", " ", concur1_full)
            concur1_full = re.sub(", $", "", concur1_full)
            concur2_full = concur2_ln + ", " + concur2_fn + " " + concur2_mn + " " + concur2_suf
            concur2_full = re.sub("[\s]+", " ", concur2_full)
            concur2_full = re.sub(", $", "", concur2_full)
            concur3_full = concur3_ln + ", " + concur3_fn + " " + concur3_mn + " " + concur3_suf
            concur3_full = re.sub("[\s]+", " ", concur3_full)
            concur3_full = re.sub(", $", "", concur3_full)
            concur4_full = concur4_ln + ", " + concur4_fn + " " + concur4_mn + " " + concur4_suf
            concur4_full = re.sub("[\s]+", " ", concur4_full)
            concur4_full = re.sub(", $", "", concur4_full)
            concur5_full = concur5_ln + ", " + concur5_fn + " " + concur5_mn + " " + concur5_suf
            concur5_full = re.sub("[\s]+", " ", concur5_full)
            concur5_full = re.sub(", $", "", concur5_full)
            concur6_full = concur6_ln + ", " + concur6_fn + " " + concur6_mn + " " + concur6_suf
            concur6_full = re.sub("[\s]+", " ", concur6_full)
            concur6_full = re.sub(", $", "", concur6_full)
            concur7_full = concur7_ln + ", " + concur7_fn + " " + concur7_mn + " " + concur7_suf
            concur7_full = re.sub("[\s]+", " ", concur7_full)
            concur7_full = re.sub(", $", "", concur7_full)



        if(re.search("en banc|En banc|En Banc|EN BANC|en Banc|In Banc|in banc", judges_string)):
            en_banc = "YES"

        if(re.search("EN BANC|IN BANC", txtline)):
            en_banc = "CHECK"

        #if (re.search("petition for rehearing", op_string)):
        #    check_case = 1

        if (re.search("(DECISION WITHOUT PUBLISHED OPINION)|(NOT FOR PUBLICATION)", txtline)):
            unpublished = 1


    if len(notice_string) > 0:
        unpublished = 1

    if opinion_word_count > 150:
        short_op = ""


    judge_string2 = judges_string

    # Process extraneous notation in judge string
    judge_string2 = re.sub("\[.*\]", "", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub(" and", ",", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub(";", ",", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub("[^A-Za-z\s\',\.]*", "", judge_string2)

    # Chop off stuff before judge list
    judge_string2 = re.sub("(Before|BEFORE):?[\s]*", "", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub("(Present|PRESENT):?[\s]*", "", judge_string2, re.IGNORECASE)

    # Chop off stuff after judge list
    judge_string2 = re.sub("[\s]*Opinion.*", "", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub("(?<=[A-Za-z]{3})\..*", "", judge_string2)

    # Get rid of titles
    judge_string2 = re.sub("Judges|JUDGES", "", judge_string2)
    judge_string2 = re.sub("Judge|JUDGE", "", judge_string2)
    judge_string2 = re.sub("Circuit|CIRCUIT", "", judge_string2)
    judge_string2 = re.sub("Chief|CHIEF", "", judge_string2)
    judge_string2 = re.sub("Senior|SENIOR", "", judge_string2)
    judge_string2 = re.sub("District|DISTRICT", "", judge_string2)
    judge_string2 = re.sub("sitting by designation", "", judge_string2)
    judge_string2 = re.sub("United States for the ", "", judge_string2)
    judge_string2 = re.sub("of", "", judge_string2)

    #Clean up formatting
    judge_string2 = re.sub(", J(r|R)\.", " Jr", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub(", S(r|R)\.", " Sr", judge_string2, re.IGNORECASE)
    judge_string2 = re.sub("[\s]+", " ", judge_string2)
    judge_string2 = re.sub(",+", ",", judge_string2)
    judge_string2 = re.sub(" ,", "", judge_string2)
    judge_string2 = re.sub("\.", "", judge_string2)
    judge_string2 = re.sub("[\s]+", " ", judge_string2)
    judge_string2 = re.sub(",?\s?$", "", judge_string2)

    judge_holder2 = re.split(", ", judge_string2)
    if len(judge_holder2) > 2:
        judge1 = judge_holder2[0]
        judge2 = judge_holder2[1]
        judge3 = judge_holder2[2]

    #print judges_string
    #print judge_string2

    header = re.sub("\s+", " ", header)

    lower_name_combine = ""
    #lower_name_combine = full_case_name.lower()
    lower_name_combine = re.sub(" ","",full_case_name)
    lower_name_combine = re.sub("\,","",lower_name_combine)
    lower_name_combine = re.sub("\'","",lower_name_combine)
    lower_name_combine = re.sub("\.","",lower_name_combine)
    lower_name_combine = lower_name_combine.lower()
    #print lower_name_combine

    agency = []
    agency = [ag for ag in agencylist if(ag in lower_name_combine)]

    agencyterms = ['office', 'agency', 'commission', 'department', 'bank', 'board', 'council', 'secretary', 'bureau', 'institute', 'administration', 'authority']
    checkagency = []
    checkagency = [ag1 for ag1 in agencyterms if(ag1 in lower_name_combine)]

    unique_hn = []
    first_level_hn_holder = []
    split_hn_string = ""
    unique_first_hn_holder = []
    unique_first_two_hn_holder = []
    unique_first_three_hn_holder = []
    first_two_hn_holder = []
    first_three_hn_holder = []
    ##if (headnote_line == False):
        #headnote_string = re.sub("\n","",headnote_string)
        #print headnote_string
    headnote_string = re.sub("'", "", headnote_string)
    hn1 = 0
    hn2 = 0
    hn3 = 0
    hn4 = 0
    hn5 = 0
    hn6 = 0
    hn7 = 0
    hn8 = 0
    hn9 = 0
    hn10 = 0
    hn11 = 0
    hn12 = 0
    hn13 = 0
    hn14 = 0
    hn15 = 0
    hn16 = 0
    hn17 = 0
    hn18 = 0
    hn19 = 0
    hn20 = 0
    hn21 = 0
    hn22 = 0
    hn23 = 0
    hn24 = 0
    hn25 = 0
    hn26 = 0
    hn27 = 0
    hn28 = 0
    hn29 = 0
    hn30 = 0
    hnDrop = 0

    if re.search("Administrative Law > Agency Rulemaking > Informal Rulemaking",headnote_string):
        hn1 = 1
    if re.search("Administrative Law > Agency Rulemaking > Notice & Comment Requirements",headnote_string):
        hn2 = 1
    if re.search("Administrative Law > Judicial Review",headnote_string):
        hn3 = 1
    if re.search("Administrative Law > Judicial Review > Administrative Record",headnote_string):
        hn4 = 1
    if re.search("Administrative Law > Judicial Review > General Overview",headnote_string):
        hn5 = 1
    if re.search("Administrative Law > Judicial Review > Remand & Remittitur",headnote_string):
        hn6 = 1
    if re.search("Administrative Law > Judicial Review > Remedies",headnote_string):
        hn7 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability",headnote_string):
        hn8 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Exhaustion of Remedies",headnote_string):
        hn9 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Factual Determinations",headnote_string):
        hn10 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > General Overview",headnote_string):
        hn11 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Jurisdiction & Venue",headnote_string):
        hn12 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Preclusion",headnote_string):
        hn13 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Preservation for Review",headnote_string):
        hn14 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Preservation for Review",headnote_string):
        hn15 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Reviewable Agency Action",headnote_string):
        hn16 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Ripeness",headnote_string):
        hn17 = 1
    if re.search("Administrative Law > Judicial Review > Reviewability > Standing",headnote_string):
        hn18 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review",headnote_string):
        hn19 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Abuse of Discretion",headnote_string):
        hn20 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Arbitrary & Capricious Standard of Review",headnote_string):
        hn21 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Clearly Erroneous Standard of Review",headnote_string):
        hn22 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Constitutional Right",headnote_string):
        hn23 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Deference to Agency Statutory Interpretation",headnote_string):
        hn24 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > De Novo Standard of Review",headnote_string):
        hn25 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Exceeding Statutory Authority",headnote_string):
        hn26 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > General Overview",headnote_string):
        hn27 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Rule Interpretation",headnote_string):
        hn28 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Substantial Evidence",headnote_string):
        hn29 = 1
    if re.search("Administrative Law > Judicial Review > Standards of Review > Unlawful Procedures",headnote_string):
        hn30 = 1
    if re.search("Administrative Law > Sovereign Immunity",headnote_string):
        hnDrop = 1

    headnote_string = re.sub("Estate, Gift & Trust Law", "Estate Gift & Trust Law", headnote_string)
    headnote_string = re.sub("Time, Place & Manner", "Time Place & Manner", headnote_string)
    headnote_string = re.sub("Expirations, Repeals & Suspensions", "Expirations Repeals & Suspensions", headnote_string)
    headnote_string = re.sub("IRC secs. 4041-4042, 4081-4084, 4091-4093, 4121", "IRC secs 4041-4042 4081-4084 4091-4093 4121", headnote_string)
    headnote_string = re.sub("\r", "", headnote_string)
    headnote_string = re.sub("\x0c", "", headnote_string)
    headnote_holder = re.split("\n", headnote_string)
    ##Last entry is empty, so need to delete it
    headnote_holder.pop()
    #print len(headnote_holder)
    #print headnote_holder
    unique_hn = Set(headnote_holder)
    #print list(unique_hn)
    #print len(unique_hn)

    for hn_number, hn in enumerate(unique_hn):
        split_hn_string = re.split(">",hn)
        #print split_hn_string
        first_level_hn_holder.append(split_hn_string[0])
        first_two_hn_holder.append(''.join(split_hn_string[0:2]))
        first_three_hn_holder.append(''.join(split_hn_string[0:3]))
    unique_first_hn_holder = Set(first_level_hn_holder)
    unique_first_two_hn_holder = Set(first_two_hn_holder)
    unique_first_three_hn_holder = Set(first_three_hn_holder)
    #print len(unique_first_hn_holder)
    #print unique_first_hn_holder
    #print len(unique_first_two_hn_holder)
    #print len(unique_first_three_hn_holder)

    case_text = case_text.strip()
    #case_text = case_text.replace("\n", "")
    #case_text = case_text.replace("\r", "")
    case_text = case_text.replace(" ", "")
    case_text = case_text.lower()
    #print case_text
    countagency = []
    maxagency = []
    #countagency = [for ag1 in agencyterms: case_text.count(ag1)]
    for ag in agencylist:
        #print ag
        countagency.append(case_text.count(ag))
    m = max(countagency)
    if m!=0:
        maxagencypos = [i for i, j in enumerate(countagency) if j == m]
        for ag in maxagencypos:
            maxagency.append(agencylist[ag])
        #print maxagency

    # For each case, write a row to the .csv file which contains the desired variables.
    localrow = []
    #localrow.append(caseid)
    localrow.append(entry)
    #localrow.append(desig_string)
    #localrow.append(header)
    localrow.append(year)
    #localrow.append(month)
    localrow.append(parties_string)
    #localrow.append(docketnum)
    localrow.append(court_string)
    localrow.append(circuit)
    localrow.append(Lexis_cite)
    localrow.append(Fed_cite)
    #localrow.append(unpublished)
    #localrow.append(len(coreterms_holder))
    localrow.append(len(unique_first_hn_holder))
    localrow.append(len(unique_first_two_hn_holder))
    localrow.append(len(unique_first_three_hn_holder))
    #localrow.append(unique_hn)
    #localrow.append(unique_first_two_hn_holder)
    #localrow.append(unique_first_three_hn_holder)
    #localrow.append(coreterms_holder)
    #localrow.append(prior_history_string)
    #localrow.append(notice_string)
    #localrow.append(per_curiam)
    #localrow.append(en_banc)
    #localrow.append(rehearing)
    localrow.append(num_dissent)
    localrow.append(num_concur)
    #localrow.append(dissent)
    #localrow.append(concur)
    #localrow.append(date)
    #localrow.append(action_string)
    localrow.append(disposition_string)
    #localrow.append(len(disposition_string))
    #localrow.append(desjud)
    #localrow.append(judges_string)
    localrow.append(judge_string2)
    localrow.append(dissent_by_string)
    localrow.append(concur_by_string)

    #localrow.append(judge1_ln)
    #localrow.append(judge1_fn)
    localrow.append(judge1)
    #localrow.append(judge2_ln)
    #localrow.append(judge2_fn)
    localrow.append(judge2)
    #localrow.append(judge3_ln)
    #localrow.append(judge3_fn)
    localrow.append(judge3)
    #localrow.append(opin_by_string)

    #localrow.append(author_ln)
    #localrow.append(author_fn)
    localrow.append(author_full)
    #localrow.append(author_suf)
    #localrow.append(dissent1_ln)
    #localrow.append(dissent1_fn)
    #localrow.append(dissent1_full)
    #localrow.append(dissent1_suf)
    #localrow.append(dissent2_ln)
    #localrow.append(dissent2_fn)
    #localrow.append(dissent2_full)
    #localrow.append(dissent2_suf)
    #localrow.append(dissent3_ln)
    #localrow.append(dissent3_fn)
    #localrow.append(dissent3_full)
    #localrow.append(dissent3_suf)
    #localrow.append(dissent4_ln)
    #localrow.append(dissent4_fn)
    #localrow.append(dissent4_full)
    #localrow.append(dissent4_suf)
    #localrow.append(concur1_ln)
    #localrow.append(concur1_fn)
    #localrow.append(concur1_full)
    #localrow.append(concur1_suf)
    #localrow.append(concur2_ln)
    #localrow.append(concur2_fn)
    #localrow.append(concur2_full)
    #localrow.append(concur2_suf)
    #localrow.append(concur3_ln)
    #localrow.append(concur3_fn)
    #localrow.append(concur3_full)
    #localrow.append(concur3_suf)
    #localrow.append(concur4_ln)
    #localrow.append(concur4_fn)
    #localrow.append(concur4_full)
    #localrow.append(concur4_suf)
    #localrow.append(concur5_ln)
    #localrow.append(concur5_fn)
    #localrow.append(concur5_full)
    #localrow.append(concur5_suf)
    #localrow.append(concur6_ln)
    #localrow.append(concur6_fn)
    #localrow.append(concur6_full)
    #localrow.append(concur6_suf)
    #localrow.append(concur7_ln)
    #localrow.append(concur7_fn)
    #localrow.append(concur7_full)
    #localrow.append(concur7_suf)
    #localrow.append(check_case)
    #localrow.append(shist)
    #localrow.append(phist)
    #localrow.append(case_sum_string)
    #localrow.append(proc_pos_string)
    #localrow.append(overview_string)
    #localrow.append(outcome_string)
    #localrow.append(core_terms_string)
    localrow.append(full_case_name)
    localrow.append(agency)
    localrow.append(hn1)
    localrow.append(hn2)
    localrow.append(hn3)
    localrow.append(hn4)
    localrow.append(hn5)
    localrow.append(hn6)
    localrow.append(hn7)
    localrow.append(hn8)
    localrow.append(hn9)
    localrow.append(hn10)
    localrow.append(hn11)
    localrow.append(hn12)
    localrow.append(hn13)
    localrow.append(hn14)
    localrow.append(hn15)
    localrow.append(hn16)
    localrow.append(hn17)
    localrow.append(hn18)
    localrow.append(hn19)
    localrow.append(hn20)
    localrow.append(hn21)
    localrow.append(hn22)
    localrow.append(hn23)
    localrow.append(hn24)
    localrow.append(hn25)
    localrow.append(hn26)
    localrow.append(hn27)
    localrow.append(hn28)
    localrow.append(hn29)
    localrow.append(hn30)
    localrow.append(hnDrop)
    localrow.append(opinion_word_count)
    #localrow.append(short_op)
    localrow.append(m)
    localrow.append(maxagency)
    for ag in countagency:
        localrow.append(ag)
    outfilehandle.writerow(localrow)

# Finish writing to the .csv file and close it so the process is complete
infilehandle.close()
fout.close()
