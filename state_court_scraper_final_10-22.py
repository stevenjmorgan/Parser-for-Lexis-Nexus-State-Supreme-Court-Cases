# -*- coding: utf-8 -*-

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
## 9/19/2011
##
## modified for state courts by
## Michael Nelson
## Summer, 2017

import os
import re
import csv
import string
import operator
import datetime
import time

#mydir = "C:/Users/Steve/Dropbox/PSU2018-2019/RA/Scraper/"
mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"
#mydir = "C:/Users/steve/Dropbox/PSU2018-2019/RA/Scraper/"
#mydir = "C:/Users/steve/OneDrive/Desktop/"

def expandmonth(mstring2):
    mstring2 = re.sub("Jan\.", "January", mstring2)
    mstring2 = re.sub("Feb\.", "February", mstring2)
    mstring2 = re.sub("Mar\.", "March", mstring2)
    mstring2 = re.sub("Apr\.", "April", mstring2)
    mstring2 = re.sub("Aug\.", "August", mstring2)
    mstring2 = re.sub("Sept\.", "September", mstring2)
    mstring2 = re.sub("Oct\.", "October", mstring2)
    mstring2 = re.sub("Nov\.", "November", mstring2)
    mstring2 = re.sub("Dec\.", "December", mstring2)
    return mstring2

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

def Capitalize(nstring):
    if(len(nstring) > 1 and not re.match("MC|Mc|Mac|MAC", nstring)): #O'|Van|VAN
        nstring = string.upper(nstring[0]) + string.lower(nstring[1:])
    if(re.match("MC|Mc|mc", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1]) + string.upper(nstring[2]) + string.lower(nstring[3:])
    if(re.match("MAC|Mac", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1:3]) + string.upper(nstring[3]) + string.lower(nstring[4:])
    if(re.match("MACY|Macy|MacY", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1]) + string.upper(nstring[2]) + string.lower(nstring[3:])
    if(re.match("Van\s|VAN\s", nstring)):
        nstring = string.upper(nstring[0]) + string.lower(nstring[1:4]) + string.upper(nstring[4]) + string.lower(nstring[5:])
    if(len(nstring) == 1):
        nstring = string.upper(nstring)
    return nstring

def lastname(nstring):
    last_name = ""
    nstring = re.sub(",", "", nstring)
    nstring = string.strip(nstring)
    nstring = re.sub("BY THE COURT", "", nstring)
    nstring = re.sub("PER CURIAM[;]*", "", nstring)
    nstring = re.sub(", (Jr\.|JR\.|III|Sr\.|SR\.)", "", nstring)
    names_holder = re.split("\s", nstring)
    if(len(names_holder) == 1):
        last_name = names_holder[0]
    if(len(names_holder) == 2): #and not re.search(",", nstring)):
        last_name = names_holder[1]
    if(len(names_holder) == 3 and not re.search(",", nstring)):
        last_name = names_holder[2]
    if(len(names_holder) == 3 and re.search(",", nstring)):
        last_name = names_holder[2]
    if(len(names_holder) == 4): #and not re.search(",", nstring)):
        last_name = names_holder[2] + " " + names_holder[3]
    if(len(names_holder) == 4 and re.search(",", nstring)):
        last_name = names_holder[0] + " " + names_holder[1]
    last_name = re.sub(",", "", last_name)
    last_name = re.sub("\.", "", last_name)
    last_name = Capitalize(last_name)
    return last_name

def firstname(nstring):
    first_name = ""
    nstring = nstring.strip()
    nstring = re.sub("BY THE COURT", "", nstring)
    nstring = re.sub("PER CURIAM[;]*", "", nstring)
    nstring = re.sub(", (Jr\.|JR\.|III|Sr\.|SR\.)", "", nstring)
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
    if(re.search("Jr\.|JR\.", nstring)):
        suffix = "Jr."
    if(re.search("III", nstring)):
        suffix = "III"
    if(re.search("II", nstring)):
        suffix = "II"
    if(re.search("Sr\.|SR\.", nstring)):
        suffix = "Sr."
    return suffix

def first_sentence(value):
    """ Take just the first sentence of the HTML passed in.
    """
    words = value.split()
    # Collect words until the result is a sentence.
    sentence = ""
    while words:
        if sentence:
            sentence += " "
        sentence += words.pop(0)
        if not re.search(r'[.?!][)"]*$', sentence):
            # End of sentence doesn't end with punctuation.
            continue
        #if words and not re.search(r'^[("]*[A-Z0-9]', words[0]):
            # Next sentence has to start with upper case.
            continue
        if re.search(r'(Mr\.|Mrs\.|Ms\.|Dr\.| [A-Z]\.)$', sentence):
            # If the "sentence" ends with a title or initial, then it probably
            # isn't the end of the sentence.
            continue
        if sentence.count('(') != sentence.count(')'):
            # A sentence has to have balanced parens.
            continue
        if sentence.count('"') % 2:
            # A sentence has to have an even number of quotes.
            continue
        break

    return sentence

def state_ab(value):
    if(re.search("Alabama", value)):
        state_abbr = "AL"
        return state_abbr
    elif (re.search("Alaska", value)):
        state_abbr = "AK"
        return state_abbr
    elif (re.search("Arkansas", value)):
        state_abbr = "AR"
        return state_abbr
    elif (re.search("Arizona", value)):
        state_abbr = "AZ"
        return state_abbr
    elif (re.search("California", value)):
        state_abbr = "CA"
        return state_abbr
    elif (re.search("Colorado", value)):
        state_abbr = "CO"
        return state_abbr
    elif (re.search("Connecticut", value)):
        state_abbr = "CT"
        return state_abbr
    elif (re.search("Delaware", value)):
        state_abbr = "DE"
        return state_abbr
    elif (re.search("Florida", value)):
        state_abbr = "FL"
        return state_abbr
    elif (re.search("Georgia", value)):
        state_abbr = "GA"
        return state_abbr
    elif (re.search("Hawaii", value)):
        state_abbr = "HI"
        return state_abbr
    elif (re.search("Hawai'i", value)):
        state_abbr = "HI"
        return state_abbr
    elif (re.search("Idaho", value)):
        state_abbr = "ID"
        return state_abbr
    elif (re.search("Illinois", value)):
        state_abbr = "IL"
        return state_abbr
    elif (re.search("Indiana", value)):
        state_abbr = "IN"
        return state_abbr
    elif (re.search("Iowa", value)):
        state_abbr = "IA"
        return state_abbr
    elif (re.search("Kansas", value)):
        state_abbr = "KS"
        return state_abbr
    elif (re.search("Kentucky", value)):
        state_abbr = "KY"
        return state_abbr
    elif (re.search("Louisiana", value)):
        state_abbr = "LA"
        return state_abbr
    elif (re.search("Maine", value)):
        state_abbr = "ME"
        return state_abbr
    elif (re.search("Maryland", value)):
        state_abbr = "MD"
        return state_abbr
    elif (re.search("Massachusetts", value)):
        state_abbr = "MA"
        return state_abbr
    elif (re.search("Michigan", value)):
        state_abbr = "MI"
        return state_abbr
    elif (re.search("Minnesota", value)):
        state_abbr = "MN"
        return state_abbr
    elif (re.search("Mississippi", value)):
        state_abbr = "MS"
        return state_abbr
    elif (re.search("Missouri", value)):
        state_abbr = "MO"
        return state_abbr
    elif (re.search("Montana", value)):
        state_abbr = "MT"
        return state_abbr
    elif (re.search("Nebraska", value)):
        state_abbr = "NE"
        return state_abbr
    elif (re.search("Nevada", value)):
        state_abbr = "NV"
        return state_abbr
    elif (re.search("New Hampshire", value)):
        state_abbr = "NH"
        return state_abbr
    elif (re.search("New Jersey", value)):
        state_abbr = "NJ"
        return state_abbr
    elif (re.search("New Mexico", value)):
        state_abbr = "NM"
        return state_abbr
    elif (re.search("New York", value)):
        state_abbr = "NY"
        return state_abbr
    elif (re.search("North Carolina", value)):
        state_abbr = "NC"
        return state_abbr
    elif (re.search("North Dakota", value)):
        state_abbr = "ND"
        return state_abbr
    elif (re.search("Ohio", value)):
        state_abbr = "OH"
        return state_abbr
    elif (re.search("Supreme Court of Oklahoma", value)):
        state_abbr = "OK-SC"
        return state_abbr
    elif (re.search("Oregon", value)):
        state_abbr = "OR"
        return state_abbr
    elif (re.search("Pennsylvania", value)):
        state_abbr = "PA"
        return state_abbr
    elif (re.search("Rhode Island", value)):
        state_abbr = "RI"
        return state_abbr
    elif (re.search("South Carolina", value)):
        state_abbr = "SC"
        return state_abbr
    elif (re.search("Tennessee", value)):
        state_abbr = "TN"
        return state_abbr
    elif (re.search("Texas", value)):
        state_abbr = "TX-SC"
        return state_abbr
    elif (re.search("Utah", value)):
        state_abbr = "UT"
        return state_abbr
    elif (re.search("Vermont", value)):
        state_abbr = "VT"
        return state_abbr
    elif (re.search("Washington", value)):
        state_abbr = "WA"
        return state_abbr
    elif (re.search("West Virginia", value)):
        state_abbr = "WV"
        return state_abbr
    elif (re.search("Wisconsin", value)):
        state_abbr = "WI"
        return state_abbr
    elif (re.search("Wyoming", value)):
        state_abbr = "WY"
        return state_abbr

#time.sleep(600)

# .csv file where extracted metadata will be stored
mydir2 = 'C:/Users/sum410/Dropbox/PSU2018-2019/Summer/MN/'
#mydir2 = 'C:/Users/steve/OneDrive/Desktop/'
#mydir2 = 'C:/Users/steve/Dropbox/PSU2018-2019/Summer/MN/'
fout = open(mydir2 + "EAWPost1990_9-7.csv", "wb") #EAWPost1990    ############################
outfilehandle = csv.writer(fout,
                           delimiter=",",
                           quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)
check = open(mydir2 + "check_recusals_EAWPost1990_9-7.csv", "wb") #EAWPost1990
recuse_handle = csv.writer(check,
                           delimiter=",",
                           quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)

master = open(mydir + "States_MasterFile_Import.csv", "rb")

# Create your own label for each column of the metadata .csv file
localrow = []
localrow.append("Email")
localrow.append("FirstName")
localrow.append("LastName")
localrow.append("court")
localrow.append("date")
localrow.append("state")
localrow.append("panel_state")
localrow.append("parties")
localrow.append("docket")
localrow.append("citestring")
localrow.append("LexisCite")
localrow.append("WestLaw")
localrow.append("attorneys")
localrow.append("judges")
localrow.append("judgeNP")
localrow.append("Judge1_Last_Name")
localrow.append("Judge1_Vote")
localrow.append("Judge1_code")
localrow.append("Judge2_Last_Name")
localrow.append("Judge2_Vote")
localrow.append("Judge2_code")
localrow.append("Judge3_Last_Name")
localrow.append("Judge3_Vote")
localrow.append("Judge3_code")
localrow.append("Judge4_Last_Name")
localrow.append("Judge4_Vote")
localrow.append("Judge4_code")
localrow.append("Judge5_Last_Name")
localrow.append("Judge5_Vote")
localrow.append("Judge5_code")
localrow.append("Judge6_Last_Name")
localrow.append("Judge6_Vote")
localrow.append("Judge6_code")
localrow.append("Judge7_Last_Name")
localrow.append("Judge7_Vote")
localrow.append("Judge7_code")
localrow.append("Judge8_Last_Name")
localrow.append("Judge8_Vote")
localrow.append("Judge8_code")
localrow.append("Judge9_Last_Name")
localrow.append("Judge9_Vote")
localrow.append("Judge9_code")
localrow.append("Judge10_Last_Name")
localrow.append("Judge10_Vote")
localrow.append("Judge10_code")
localrow.append("Judge11_Last_Name")
localrow.append("Judge11_Vote")
localrow.append("Judge11_code")
localrow.append("dissent")
localrow.append("dissent_no")
localrow.append("dissent_name")
localrow.append("dissent_1")
localrow.append("dissent_2")
localrow.append("dissent_3")
localrow.append("dissent_4")
localrow.append("dissent_5")
localrow.append("concurrence")
localrow.append("concur_no")
localrow.append("concur_name")
localrow.append("check")
outfilehandle.writerow(localrow)
recuse_handle.writerow(localrow)

# Name of folder where all cases are located (and nothing else)
dirname = mydir + "EAWPost1990/"
dirlist = os.listdir(dirname)
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

#dirlist = [file for file in dirlist if len(file) > 20]

# Use (uncomment) following line to test code on a small handful of cases
#cleandirlist = cleandirlist[838:872]
for entry in cleandirlist: ## each entry is a txt file with an opinion 0:1025
    # initialize all variables to be used
    infilepath = dirname + entry
    infilehandle = open(infilepath)
    txtlines = infilehandle.readlines()
    action_number = 0
    case_with_preamble = False
    searchterms_line = False
    blank_after_searchterms = False
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
    blank_after_appellant_attorney = False
    jud_dissent = 0
    opinion_word_count = 0
    amicus = 0
    localrow = []
    action_number = 0
    judges_part_string = ""
    searchterms_string = ""
    shep_treat = ""
    parties_string = ""
    docketnum = ""
    court_string = ""
    cite_string = ""
    Fed_cite = ""
    Lexis_cite = ""
    West_cite = ""
    action_string = ""
    per_curiam = 0
    unanimous = 0
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
    pubdef = 0
    prose = 0
    attorney_string = ""
    pc_holder = ""
    judges_string = ""
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
    judge4_ln = ""
    judge4_fn = ""
    judge4_mn = ""
    judge4_suf = ""
    judge4_full = ""
    judge5_ln = ""
    judge5_fn = ""
    judge5_mn = ""
    judge5_suf = ""
    judge5_full = ""
    judge6_ln = ""
    judge6_fn = ""
    judge6_mn = ""
    judge6_suf = ""
    judge6_full = ""
    judge7_ln = ""
    judge7_fn = ""
    judge7_mn = ""
    judge7_suf = ""
    judge7_full = ""
    judge8_ln = ""
    judge8_fn = ""
    judge8_mn = ""
    judge8_suf = ""
    judge8_full = ""
    judge9_ln = ""
    judge9_fn = ""
    judge9_mn = ""
    judge9_suf = ""
    judge9_full = ""
    judge10_ln = ""
    judge10_fn = ""
    judge10_mn = ""
    judge10_suf = ""
    judge10_full = ""
    judge11_ln = ""
    judge11_fn = ""
    judge11_mn = ""
    judge11_suf = ""
    judge11_full = ""
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
    dissent5_ln = ""
    dissent5_fn = ""
    dissent5_mn = ""
    dissent5_suf = ""
    dissent5_full = ""
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
    no_part_list = []      ####
    no_part_string = ""    ####
    full_judges_holder = []
    judges_holder = []
    dissent_holder = []
    concur_holder = []
    no_part = False
    no_part_dich = 0
    shep_line = False
    blank_after_shep = False
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
    attorney_line = False
    #appellee_attorney_line = False
    opin_by_line = False
    opinion_line = False
    dissent_by_line = False
    concur_by_line = False
    dissent_author_1 = ""
    dissent_author_2 = ""
    dissent_author_3 = ""
    dissent_author_4 = ""
    dissent_author_5 = ""
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
    unwritten_dissent = 0
    firstcite_line = False
    firstcite_string = ""
    blank_after_firstcite = False
    caseid = str(re.split("\.", entry)[0])
    print "\n" + entry
    pet_str = ""
    res_str = ""
    opinion_start = False
    dissent_line = False
    concur_line = False
    blank_after_action = False
    line_before_first = False
    judge1_vote = ""
    judge2_vote = ""
    judge3_vote = ""
    judge4_vote = ""
    judge5_vote = ""
    judge6_vote = ""
    judge7_vote = ""
    judge8_vote = ""
    judge9_vote = ""
    judge10_vote = ""
    judge11_vote = ""
    panel = 0
    judges_np = ""
    state_abbr = ""
    judge_np_list = []
    judge_np1 = ""
    judge_np2 = ""
    judge_np3 = ""
    judge_np4 = ""
    other_dissent_string = ""
    other_dissent_judges = []
    silent_dissent = False
    silent_judge1 = ""
    silent_judge2 = ""
    silent_judge3 = ""
    silent_judge4 = ""
    silent_judge5 = ""
    first_dissent = False
    other_dissent = ""
    new_date = ""
    date_bool = False
    between = False
    non_panel_judge_string = ""
    other_dissent_holder = []
    part_judges = ""
    judge1_code = ""
    judge2_code = ""
    judge3_code = ""
    judge4_code = ""
    judge5_code = ""
    judge6_code = ""
    judge7_code = ""
    judge8_code = ""
    judge9_code = ""
    judge10_code = ""
    judge11_code = ""
    one_month = datetime.timedelta(365*3) #/12
    judges_AL = []
    MD_date = False
    dock = False
    docket = False
    check_recuse = False
    check_recuse_case = 0
    start = datetime.datetime.strptime('1/1/1800', '%m/%d/%Y').date()
    end = datetime.datetime.strptime('12/31/2100', '%m/%d/%Y').date()
    date_format = datetime.datetime.strptime('1/1/1800', '%m/%d/%Y').date()

	# each txtline is one "line" in the text file: the end of a line is determined by \n
    for txtline in txtlines:
        # proceeding logic of script based on boolean operators causes all text prior to the line beginning with "Copy Citation" to be ignored
        if (re.search("^Copy Citation",txtline)):
            line_before_first = True

        if (line_before_first and re.search("(COURT|Court)", txtline) and not re.search("^1 ", txtline)):
            ## the court in which the case was heard
            line_before_first = False
            court_line = True
            court_string = court_string + txtline
            court_string = court_string.strip()
            print court_string
            state_abbr = state_ab(court_string) ###function to return state abbreviations

        if (re.search("Alabama|Arizona|Connecticut|Delaware|Florida|Idaho|Massachusetts|Mississippi|Montana|Nevada|New Hampshire|Virginia", court_string)):
            # all cases in states that hear cases in panels are given a value of 1
            panel = 1

        if re.search("West Virginia", court_string):
            # the prior if statement matches "Virginia" in "West Virginia"; this corrects the incorrect panel assignment value
            panel = 0

        if(court_line and re.search("Jan|Feb|Mar|Apr|May|June|July|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC", txtline)) and state_abbr != "MD" and not re.search("Argued$", txtline): #re.match("^[\s]+$", txtline)):
            ## this is the blank line after court
            # stores date and action of court (i.e. Decided, Released, Filed)
            blank_after_firstcite = False
            court_line = False
            blank_after_court = True
            #print txtline
            action_line = True
            if (len(action_string) < 1):
                action_string = action_string + txtline
            dock = True

        if len(action_string) < 2:
            MD_date = True

        if state_abbr == "MD" and re.match("Jan|Feb|Mar|Apr|May|June|July|Aug|Sep|Oct|Nov|Dec", txtline) and MD_date == True:
            action_string = txtline
            MD_date = False
            blank_after_firstcite = False
            court_line = False
            blank_after_court = True
            #print txtline
            action_line = True

        if(action_line): #and re.match("^[\s]+$", txtline)):
            # parse out unnecessary text from action string (Date and Procedural Documentation of Publication) for only the date to remain
            blank_after_court = False
            blank_after_action = True
            action_line = False
            if re.search("Argued; ;", action_string):
                action_string = action_string.split("Argued; ;", 1)[1]
            if re.search("Argued ;", action_string):
                action_string = action_string.split("Argued ;", 1)[1]
            if re.search("Argued;", action_string):
                action_string = action_string.split("Argued;", 1)[1]
            if re.search("Argued and submitted ;", action_string):
                action_string = action_string.split("Argued and submitted ;", 1)[1]
            if re.search("Argued and submitted;", action_string):
                action_string = action_string.split("Argued and submitted;", 1)[1]
            if re.search("Submitted ;", action_string):
                action_string = action_string.split("Submitted ;", 1)[1]
            if re.search("Submitted;", action_string):
                action_string = action_string.split("Submitted;", 1)[1]
            if re.search("Submitted on Briefs ;", action_string):
                action_string = action_string.split("Submitted on Briefs ;", 1)[1]
            if re.search("Submitted on Briefs;", action_string):
                action_string = action_string.split("Submitted on Briefs;", 1)[1]
            if re.search("Heard in the Supreme Court ;", action_string):
                action_string = action_string.split("Heard in the Supreme Court ;", 1)[1]
            if re.search("Heard in the Supreme Court;", action_string):
                action_string = action_string.split("Heard in the Supreme Court;", 1)[1]
            if re.search("Heard ;", action_string):
                action_string = action_string.split("Heard ;", 1)[1]
            if re.search("Heard;", action_string):
                action_string = action_string.split("Heard;", 1)[1]
            if re.search("Session;", action_string):
                action_string = action_string.split("Session;", 1)[1]
            if re.search("Session ;", action_string):
                action_string = action_string.split("Session ;", 1)[1]
            if re.search("Argument ;", action_string):
                action_string = action_string.split("Argument ;", 1)[1]
            if re.search("Argument;", action_string):
                action_string = action_string.split("Argument;", 1)[1]
            print action_string
            action_string = expandmonth(action_string)
            action_string = re.sub(":", ",", action_string)
            action_string = re.sub(";", ",", action_string)
            action_string = re.sub("\*", "", action_string)
            action_string = re.sub("Argued and Submitted ", "Argued and Submitted, ", action_string)
            action_string = re.sub("Argued ", "Argued, ", action_string)
            action_string = re.sub(", Decided ", "", action_string)
            action_string = re.sub("Supplemental Briefing Submitted ", "Supplemental Briefing Submitted, ", action_string)
            action_string = re.sub(", Released", "", action_string)
            action_string = re.sub(", RELEASED", "", action_string)
            action_string = re.sub(", Filed", "", action_string)
            action_string = re.sub("Submitted Under Third Circuit Rule 12\(6\) ", "Submitted Under Third Circuit Rule 12(6), ", action_string)
            action_string = re.sub("Cause argued ", "Cause argued, ", action_string)

            split_action = re.split("\n", action_string)
            action1 = string.strip(split_action[0])
            action2 = string.strip(split_action[1])
            action2 = re.split(", ", action2)
            action1 = re.split(", ", action1)

            if(len(split_action) < 2):
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
            action_string = re.sub("Decided|decided|DECIDED", " ", action_string)
            action_string = re.sub("Filed|filed|FILED", " ", action_string)
            # one case has incorrect formatting of the date and it causes the program to break when calling teh strptime function
            if action_string == "December 22 1995":
                action_string = "December 22, 1995"

            # Dates from Maryland cases do not parse correctly
            if action_string != "Court of Appeals of Maryland":
                x = re.search("\d{4}", action_string)
                # store in x the position of the last digit of the year
                try:
                    x = x.end()
                except:
                    pass
                if new_date == "":
                    date_bool = True
                if(x != -1 and date_bool):
                    new_date = action_string[:x]
                    date_bool = False
                if(x == -1):
                    new_date = action_string

            if state_abbr != "MC":
                # format dates so they match the format from the state judge master file
                new_date = re.sub("April,", "April", new_date)
                new_date = re.sub("On ", "", new_date)
                try:
                    date_format = datetime.datetime.strptime(new_date, '%B %d, %Y').date()
                except:
                    date_format = datetime.datetime.strptime('1/1/1800', '%m/%d/%Y').date()

            elif state_abbr == "MC":
                date_format = datetime.datetime.strptime('1/1/1800', '%m/%d/%Y').date()

            # match state abbrevation and date decided from case and state master file to produce a list of judges who were on the bench at time of decision for cases heard in non-panel state
            with open(mydir + "States_MasterFile_Import.csv", "rb") as f:
                reader = csv.reader(f)
                next(f)
                for row in reader:
                    state = row[0]
                    name = row[3]
                    if len(row[4]) == 4 and row[0] != "MC":
                        row[4] = "1/1/" + row[4]
                    if len(row[5]) == 4 and row[0] != "MC": #and (panel == 0 or ((state_abbr == "AL" or state_abbr == "FL"))) and len(judge6_ln) > 2 and len(judge9_ln) < 2:
                        row[5] = "1/1/" + row[5]
                        #print state_abbr
                    #print(len(row[4]))
                    if len(row[4]) != 4 and row[0] != "MC" and (panel == 0 or ((state_abbr == "AL" or state_abbr == "FL" or state_abbr == "NH"))) and ((len(judge6_ln) > 2 or len(judge3_ln) < 2) and len(judge9_ln) < 2) and state_abbr:
                        start = datetime.datetime.strptime(row[4], '%m/%d/%Y').date()
                        end = datetime.datetime.strptime(row[5], '%m/%d/%Y').date()
                    if ((panel == 0 or ((state_abbr == "AL" or state_abbr == "FL" or state_abbr == "NH") and state_abbr != "AK" and (len(judge6_ln) > 2) and len(judge9_ln) < 2)) and start <= date_format <= end):
                        between = True
                        #print state_abbr
                    if ((state == state_abbr) and between and row[0] != "MC" and row[2] == 0 and state_abbr != "AK" and (panel == 0 or (state_abbr == "AL" or state_abbr == "FL" or state_abbr == "NH")) and (len(judge6_ln) > 2 or len(judge3_ln) < 2) and len(judge9_ln) < 2):
                        if non_panel_judge_string == "":
                            non_panel_judge_string = non_panel_judge_string + row[3]
                        else:
                            non_panel_judge_string = non_panel_judge_string + ", " + row[3]
                    if row[3] == judge1_ln:
                        judge1_code = row[1]
                    between = False

                #judges_string = judges_string + ", " + non_panel_judge_string
                non_panel_list = non_panel_judge_string.split(",")
                non_panel_list.sort()
            master.close()

        if (docketnum == "") or not re.search("[0-9]", docketnum):

            if(not re.search("LEXIS", txtline) and re.search("^([\d]+$|Docket|Misc|No\.|Nos\.|SC |File Nos. |File No. |Arizona Supreme Court No. |L. A. Nos. |SCWC-|Cause No. |Supreme Court Cause Number |S[\d][\d]|A[\d][\d]|S. Ct. NO. |[\d] Div. |CASE NO.:|L.A. No. |\[NO NUMBER|\[No number in original|[\w]-|Supreme Court Case |Supreme Court No. |Supreme Court No. |Supreme Court Case No. |Law Docket No. |SUPREME COURT DOCKET NO. |Record No. |SUPREME COURT DOCKET NO. |Sac. No. |\([\d]+\)|\(SC |NO|C\.A\.|\# [\d]|[\d][\d][\d][\d]-|SJC-|Decision No. |DA |CA |[\d][\d]-|91-|Opinion No\.|DOCKET|Case No|[\d][\d][\d][\d][\d][\d][\d], [\d][\d][\d][\d][\d][\d][\d]|S[\d][\d][\d][\d][\d][\d]|Yor-[\d][\d]|Cum-[\d][\d]|C[\d]-[\d]|Case Number:|S.C. No. |NO.|Appeal No. |Supreme Court Nos. |S.F. No. |SCCQ-[\d]|[\d][\d][\d][\d][\d]-|Indiana Supreme Court Cause No. |[\d]|[\d][\d][\d][\d][\d][\d][\d])", txtline) and not re.search("Supreme Court of Pennsylvania",txtline) and not re.search("Supreme Court of Delaware",txtline) and not re.search("Court of Appeals of New York",txtline) and not re.search("^1. ",txtline)  and not re.search("^2. ",txtline) and not re.search("^3. ",txtline) and not re.search("^4. ",txtline) and not re.search("^5. ",txtline)):
                ## the docket number
                docket_line = True
                action_line = False
                blank_after_action = True
                docketnum = docketnum + txtline

        ##OLDER PA (and some DE) CASES DON'T HAVE DOCKETS.  THIS FIXES THE ISSUE
            elif(blank_after_action and not re.search("^([\d]+$|Docket|Misc|No\.|Nos\.|SC |File Nos. |File No. |Arizona Supreme Court No. |L. A. Nos. |SCWC-|Cause No. |Supreme Court Cause Number |S[\d][\d]|A[\d][\d]|S. Ct. NO. |[\d] Div. |CASE NO.:|L.A. No. |\[NO NUMBER|\[No number in original|[\w]-|Supreme Court Case |Supreme Court No. |Supreme Court No. |Supreme Court Case No. |Law Docket No. |SUPREME COURT DOCKET NO. |Record No. |SUPREME COURT DOCKET NO. |Sac. No. |\([\d]+\)|\(SC |NO|C\.A\.|\# [\d]|[\d][\d][\d][\d]-|SJC-|Decision No. |DA |CA |[\d][\d]-|91-|Opinion No\.|DOCKET|Case No|[\d][\d][\d][\d][\d][\d][\d], [\d][\d][\d][\d][\d][\d][\d]|S[\d][\d][\d][\d][\d][\d]|Yor-[\d][\d]|Cum-[\d][\d]|C[\d]-[\d]|Case Number:|S.C. No. |NO.|Appeal No. |Supreme Court Nos. |S.F. No. |SCCQ-[\d]|[\d][\d][\d][\d][\d]-|Indiana Supreme Court Cause No. |[\d]|[\d][\d][\d][\d][\d][\d].)", txtline) and re.search("Supreme Court of Pennsylvania",txtline) or re.search("Supreme Court of Delaware",txtline) or re.search("Court of Appeals of New York",txtline)):
                ## the docket number
                docketnum = docketnum + txtline
                docket_line = True
                action_line = False
                blank_after_docket = True

        if(re.match("^Reporter", txtline) and not opinion_start):
            ## this is the "Reporter" line after docket number
            blank_after_action = False
            docket_line = False
            blank_after_docket = True
            if(re.search(" > ", docketnum)):
                docketnum = ""

        # Store all citations listed by Lexis
        if((blank_after_docket) and re.search("LEXIS", txtline) and re.search("[\w]+", txtline) and not opinion_start):
            ## the citation block
            cite_line = True
            cite_string = cite_string + txtline
            cite_string = re.sub("[\s]+", " ", cite_string)
            cite_string = re.sub("[\*]+", "", cite_string)
            cite_string = re.sub("\xc2", "", cite_string)
            cite_string = re.sub("\xa0", "", cite_string)
            West_cite = cite_string.split("|")[0]
            #print West_cite

        if(cite_line and re.match("^[\s]+$", txtline)):
            ## done with citation block
            blank_after_docket = False
            cite_line = False
            blank_after_cite = True
            all_cites = re.split(" [\|] ", cite_string)
            ####print all_cites
            ##Fed_cite = [cite for cite in all_cites if re.search("[\s]F\.(2|3)d", cite)]
            Lexis_cite = [cite for cite in all_cites if re.search("LEXIS", cite)]
            try:
            ##    Fed_cite = string.strip(Fed_cite[0])
                Lexis_cite = string.strip(Lexis_cite[0])
            except:
                print "Problem with citation"

        if(blank_after_cite and re.match("[\w]+", txtline)):
            ## the parties
            parties_line = True
            parties_string = parties_string + txtline
            #print txtline.replace("\n", "")

        # Store names of parties to the case
        if (parties_line and re.match("^[\s]+$", txtline)):
            ## done with parties block
            blank_after_cite = False
            parties_line = False
            blank_after_parties = True
            parties_string = re.sub("[\s]+", " ", parties_string)

        # Store text in Prior and Subsequent History lines
        if(re.match("^Subsequent History:", txtline)):
            sub_history_line = True
            parties_line = False
        if(sub_history_line and re.search("[\w]+", txtline)):
            sub_history_string = sub_history_string + txtline
        if (prior_history_line and re.match("^[\s]+$", txtline)):
            prior_history_string = re.sub("Prior History:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("Prior History:", "", prior_history_string)
            prior_history_string = re.sub("\[\**\d*\]", "", prior_history_string)
            prior_history_string = re.sub("\xa0", " ", prior_history_string)
            prior_history_string = re.sub("\n|\r", " ", prior_history_string)
            prior_history_string = string.strip(prior_history_string)
            sub_history_line = False

        if(re.match("^Prior History:", txtline)):
            prior_history_line = True
            parties_line = False
        if(prior_history_line and re.search("[\w]+", txtline)):
            prior_history_string = prior_history_string + txtline
        if (prior_history_line and re.match("^[\s]+$", txtline)):
            prior_history_string = re.sub("Prior History:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("Prior History:", "", prior_history_string)
            prior_history_string = re.sub("Procedural Posture:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("Procedural Posture:", "", prior_history_string)
            prior_history_string = re.sub("\xa0", " ", prior_history_string)
            prior_history_string = re.sub("\n|\r", " ", prior_history_string)
            prior_history_string = re.sub("\[\**\d*\]", "", prior_history_string)
            prior_history_string = string.strip(prior_history_string)
            prior_history_line = False

        if(re.match("^Procedural Posture:", txtline) and prior_history_string == ""):
            prior_history_line = True
            parties_line = False
        if(prior_history_line and re.search("[\w]+", txtline)):
            prior_history_string = prior_history_string + txtline
        if (prior_history_line and re.match("^[\s]+$", txtline)):
            prior_history_string = re.sub("Prior History:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("Prior History:", "", prior_history_string)
            prior_history_string = re.sub("Procedural Posture:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("Procedural Posture:", "", prior_history_string)
            prior_history_string = re.sub("\xa0", " ", prior_history_string)
            prior_history_string = re.sub("\n|\r", " ", prior_history_string)
            prior_history_string = re.sub("\[\**\d*\]", "", prior_history_string)
            prior_history_string = string.strip(prior_history_string)
            prior_history_line = False

        ###RKH USES OUTCOME instead of DISPOSITION because not every case has a DISPOSITION
        if (re.match("^Disposition:", txtline) and disposition_string == ""):
            ## disposition of case
            disposition_line = True
            #print disposition_string
        if (disposition_line and re.search("[\w]+", txtline)):
            ## disposition lines with text
            disposition_string = disposition_string + txtline
            #print disposition_string
        if (disposition_line and re.match("^[\s]+$", txtline)):
            ## blank line after disposition line
            disposition_string = re.sub("Disposition:", "", disposition_string)
            disposition_string = re.sub("Outcome:", "", disposition_string)
            disposition_string = re.sub("\xa0", " ", disposition_string)
            disposition_string = re.sub("\n|\r", " ", disposition_string)
            disposition_string = re.sub("\[.+\]", "", disposition_string)
            disposition_string = string.strip(disposition_string)
            #print disposition_string
            disposition_line = False

        # Store outcome of case
        if (re.match("^Outcome:", txtline)):
            ## disposition of case
            disposition_line = True
            #print disposition_string
        if (disposition_line and re.search("[\w]+", txtline)):
            ## disposition lines with text
            disposition_string = disposition_string + txtline
            #print disposition_string
        if (disposition_line and re.match("^[\s]+$", txtline)):
            ## blank line after disposition line
            disposition_string = re.sub("Outcome:", "", disposition_string)
            disposition_string = re.sub("Disposition:", "", disposition_string)
            disposition_string = re.sub("\xa0", " ", disposition_string)
            disposition_string = re.sub("\n|\r", " ", disposition_string)
            disposition_string = re.sub("\[.+\]", "", disposition_string)
            disposition_string = re.sub("\[\**\d*\]", "", disposition_string)
            disposition_string = string.strip(disposition_string)
            #print disposition_string
            disposition_line = False

        # Search for presence of Per Curiam opinion
        if re.search("^Opinion", txtline):
            first_dissent = True
        if (re.search("Opinion By: (PER CURIAM)|(Per Curiam)", txtline)):
            #pc_holder = pc_holder + "Per Curiam. "
            per_curiam = 1
        if (re.search("PER CURIAM", txtline)):
            #pc_holder = pc_holder + "Per Curiam. "
            per_curiam = per_curiam + 1
        if (re.search("^[\s]*Per Curiam[\.:\s]*$", txtline)):
            per_curiam = 1
            #print pc_holder + "\n"

        # Search for judges that join in dissenting opinions but are not listed as such in the judge line
        if((first_dissent == True and re.search("dissents\.$|dissent\.$|dissenting\.$", txtline) and len(txtline) < 100 and not re.search("I respectfully dissent\.|I dissent\.|I therefore respectfully dissent\.", txtline)) or (re.search("joined\.$", txtline) and re.search("dissent", txtline))):
            #print repr(txtline)
            first_dissent = False
            other_dissent = re.sub(" and", ",", txtline)
            other_dissent = re.sub("filed a dissenting opinion", "", other_dissent)
            other_dissent = re.sub("delivered the Opinion of the Court", "", other_dissent)
            other_dissent = re.sub("All the Justices concur", "", other_dissent)
            other_dissent = re.sub("\[\**\d\]", "", other_dissent)
            other_dissent = re.sub("C\.J\.", "", other_dissent)
            other_dissent = re.sub(" C\.", "", other_dissent)
            other_dissent = re.sub("\[\*\*[0-9]+\]", "", other_dissent)
            other_dissent = re.sub("For those reasons", "", other_dissent)
            other_dissent = re.sub("dissenting", "", other_dissent)
            other_dissent = re.sub("dissents\.|dissent\.|dissents|dissent", "", other_dissent)
            other_dissent = re.sub("J\.;", "", other_dissent)
            other_dissent = re.sub("C\.J\.|JJ\.|J\.J\.|J\.|C\. J\.", "", other_dissent)
            #print other_dissent
            if re.search("deliver", other_dissent):
                other_dissent = other_dissent.split(".", 1)[1]
            if re.search("filed a concurring opinion", other_dissent):
                other_dissent = other_dissent.split(".", 1)[1]
            #print other_dissent
            other_dissent = re.sub("joined\.|joined|joins|join|JOINS|JOIN", "", other_dissent)
            other_dissent = re.sub("in the|IN THE", "", other_dissent)
            other_dissent = re.sub("in this", "", other_dissent)
            other_dissent = re.sub("in which", "", other_dissent)
            other_dissent = re.sub("Special Justice", "", other_dissent)
            other_dissent = re.sub("JUSTICES|Justices|justices|JUSTICE|Justice|justice", "", other_dissent)
            other_dissent = re.sub("\xc2", "", other_dissent)
            other_dissent = re.sub("CHIEF|Chief|chief", "", other_dissent)
            other_dissent = re.sub("Order affirmed, with costs", "", other_dissent)
            other_dissent = re.sub("Opinion by|opinion by|OPINION BY", "", other_dissent)
            other_dissent = re.sub("Judges|judges|JUDGES|judge|Judge|JUDGE", "", other_dissent)
            other_dissent = re.sub("concurs|CONCURS|concur|CONCUR", "", other_dissent)
            other_dissent = re.sub("\xa0", "", other_dissent)
            other_dissent = re.sub("In Part", "", other_dissent)
            other_dissent = re.sub("in part\.", "", other_dissent)
            other_dissent = re.sub("in part", "", other_dissent)
            other_dissent = re.sub("\[\*\*\*[\w]+\]", "", other_dissent)
            other_dissent = re.sub("I respectfully", "", other_dissent)
            other_dissent = re.sub("respectfully|RESPECTFULLY|Respectfully", "", other_dissent)
            #other_dissent = re.sub("")
#            other_dissent = re.sub("\s", "", other_dissent)
            other_dissent = re.sub("this", "", other_dissent)
            other_dissent = re.sub("with whom", "", other_dissent)
            other_dissent = re.sub("except", "", other_dissent)
            other_dissent = re.sub(" who", "", other_dissent)
            other_dissent = re.sub("reversed|REVERSED|reverse|REVERSE", "", other_dissent)
            other_dissent = re.sub("authorizes me to state", "", other_dissent)
            other_dissent = re.sub("that she", "", other_dissent)
            other_dissent = re.sub("the views expressed", "", other_dissent)
            other_dissent = re.sub("foregoing", "", other_dissent)
            other_dissent = re.sub(" JR\.| JR", "", other_dissent)
            other_dissent = re.sub(" SR\.| SR", "", other_dissent)
            other_dissent = re.sub("specially|Specially|SPECIALLY", "", other_dissent)
            other_dissent = re.sub("Order affirmed, with costs", "", other_dissent)
            other_dissent = re.sub("affirmed|AFFIRMED", "", other_dissent)
            other_dissent = re.sub("reason|reasons", "", other_dissent)
            other_dissent = re.sub("'", "", other_dissent)
            other_dissent = re.sub("Justice", "", other_dissent)

            other_dissent = re.sub("filed an opinion", "", other_dissent)
            other_dissent = re.sub("concurring in part", "", other_dissent)
            other_dissent = re.sub("Part I", "", other_dissent)
            other_dissent = re.sub("in part", "", other_dissent)
            other_dissent = re.sub("Part|part", "", other_dissent)
            dissent = 1
            other_dissent_holder = other_dissent.split(",")
            other_dissent_holder = filter(None, other_dissent_holder)

        if (re.search("^<truncate>", txtline)):
            trunc_text = True

        if (re.search("^</truncate>", txtline)):
            trunc_text = False

        if (re.match("^Counsel:", txtline) and not opinion_line):
                attorney_line = True

        # Store attorneys for appellee and appellant
        if (attorney_line and re.search("^Judges|^Opinion", txtline) and not opinion_start and not re.search("^Opinion No.",txtline)):
                attorney_line = False
                attorney_string = re.sub("Counsel:\[\**\d*\]", "", attorney_string)
                attorney_string = re.sub("Counsel:", "", attorney_string)
                attorney_string = re.sub("\[\**\d*\]", "", attorney_string)
                attorney_string = re.sub("\xa0", " ", attorney_string)
                attorney_string = re.sub("\xc2", " ", attorney_string)
                attorney_string = re.sub("\n|\r", " ", attorney_string)
                attorney_string = string.strip(attorney_string)
                attorney_line = False

        if(attorney_line):
            attorney_string = attorney_string + txtline
            attorney_string = re.sub("Counsel:\[\**\d*\]", "", attorney_string)
            attorney_string = re.sub("Counsel:", "", attorney_string)
            attorney_string = re.sub("\[\**\d*\]", "", attorney_string)
            attorney_string = re.sub("\xa0", " ", attorney_string)
            attorney_string = re.sub("\xc2", " ", attorney_string)
            attorney_string = re.sub("\n|\r", " ", attorney_string)
            attorney_string = string.strip(attorney_string)
            attorney_line = False

            if (re.search("Public|public|PUBLIC|defender|DEFENDER|Defender", attorney_string)):
                pubdef = 1

            if (re.search("(pro se)|(Pro se)|(Pro Se)|(pro Se)", attorney_string)):
                prose = 1

        if (re.match("^Judges:", txtline) and not trunc_text):
            ## judges hearing case
            judges_line = True
        if (judges_line and re.search("[\w]+", txtline)):
            ## judges lines with text
            judges_string = judges_string + txtline #+ ", " + non_panel_judge_string

        if (judges_line and re.match("^[\s]+$", txtline)):
            # new line or some whitespace after judges line



            # Store and parse text of judges that recused themselves from the case
            if (re.search("((N|n)ot (P|p)articipat(e|ing)|(R|r)ecus(e|es|ed)|RECUSED|(T|t)ak(e|es) no part| sitting for| disqualified|took no part|NOT PARTICIPATING|sitting in lieu of|sitting for)", judges_string)):
                no_part = True
                no_part_dich = 1

                if len(re.findall('not participating|recusal|recused|disqualif|sitting for', judges_string)) > 1 or (re.search('not participating|recusal|recused|disqualif|sitting for', judges_string) and len(judges_string) > 300):
                    check_recuse = True
                    check_recuse_case = 1

                full_judges_holder = re.sub(", (J|JJ)\.", " ", judges_string)
                full_judges_holder = re.sub(" O\.", "", full_judges_holder)
                full_judges_holder = re.sub(" C\.", "", full_judges_holder)
                full_judges_holder = re.sub(" W\.", "", full_judges_holder)
                full_judges_holder = re.split("\. ", full_judges_holder)
                no_part_string = [sentence for sentence in full_judges_holder if re.search("((N|n)ot (P|p)articipat(e|ing)|(R|r)ecus(e|es|ed)|RECUSED| sitting for| disqualified|took no part|(T|t)ak(e|es) no part)|NOT PARTICIPATING|sitting in lieu of", sentence)]
                no_part_string = str(no_part_string)
                no_part_string = re.sub("(N|n)ot (P|p)articipat(e|ing).*", "", no_part_string)
                no_part_string = re.sub("NOT PARTICIPATING", "", no_part_string)
                no_part_string = re.sub("Recus(es|ed|e)", "", no_part_string)
                no_part_string = re.sub("took no part in the consideration or decision of this case", "", no_part_string)
                no_part_string = re.sub("took no part in the decison", "", no_part_string)
                no_part_string = re.sub('sat but', '', no_part_string)
                if re.search("except", no_part_string):
                    no_part_string = no_part_string.split("except", 1)[1]
                if re.search("in place of", no_part_string):
                    no_part_string = no_part_string.split("in place of", 1)[1]
                if re.search("IN PLACE OF", no_part_string):
                    no_part_string = no_part_string.split("IN PLACE OF", 1)[1]
                if re.search("sitting for", no_part_string):
                    no_part_string = no_part_string.split("sitting for", 1)[1]
                if re.search("sitting in lieu of", no_part_string):
                    no_part_string = no_part_string.split("sitting in lieu of", 1)[1]
                if re.search("Concurring", no_part_string):
                    no_part_string = no_part_string.split("Concurring", 1)[1]
                no_part_string = re.sub("who is disqualified", "", no_part_string)
                no_part_string = re.sub(", sitting for Justice", "", no_part_string)
                no_part_string = re.sub("recus(es|ed|e)|RECUSED\n|RECUSED", "", no_part_string)
                no_part_string = re.sub("^[\s]+", "", no_part_string)
                no_part_string = re.sub("[\s]*\*[\s]*", "", no_part_string)
                no_part_string = re.sub("'", "", no_part_string)
                no_part_string = re.sub("\[", "", no_part_string)
                no_part_string = re.sub("Spaulding", "", no_part_string)
                no_part_string = re.sub("District Court Judge", "", no_part_string)
                no_part_string = re.sub("John McKeon|JOHN McKEON", "", no_part_string)
                no_part_string = re.sub("\]", "", no_part_string)
                no_part_string = re.sub("(Him|him|Her|her|Them|them)sel(f|ves)", "", no_part_string)
                no_part_string = re.sub("All the Justices concur, except", "", no_part_string)
                no_part_string = re.sub("(J|j)ustices,*", "", no_part_string)
                no_part_string = re.sub("(J|j)ustice,*", "", no_part_string)
                no_part_string = re.sub("JUSTIC(E|ES),*", "", no_part_string)
                no_part_string = re.sub("Former Chief", "", no_part_string)
                no_part_string = re.sub("Former", "", no_part_string)
                no_part_string = re.sub("[\s]*(did|does)[\s]*", "", no_part_string)
                no_part_string = re.sub("CJ\.", "", no_part_string)
                no_part_string = re.sub(", (J|JJ|C\.J)\.,*", "", no_part_string)
                no_part_string = re.sub("[\s] s[\s]*", "", no_part_string)
                no_part_string = re.sub("J\.", " ", no_part_string)
                no_part_string = re.sub("[\s]$", "", no_part_string)
                no_part_string = re.sub(",[\s]+(,|\.)$", "", no_part_string)
                no_part_string = re.sub("\.[\s]*$", "", no_part_string)
                no_part_string = re.sub(",[\s]*$", "", no_part_string)
                no_part_string = re.sub("\\xc2\\xa0", "", no_part_string)
                no_part_string = re.sub(" s ", "", no_part_string)
                no_part_string = re.sub("\xc2|\\xc2", "", no_part_string)
                no_part_string = re.sub("\xa0|\\xa0", "", no_part_string)
                no_part_string = re.sub("\xc2\xa0GLAZE", "", no_part_string)
                no_part_string = re.sub("Judges:", "", no_part_string)
                no_part_string = re.sub("AND", "and", no_part_string)
                no_part_string = re.sub("Boucier", "Bourcier", no_part_string)
                no_part_string = re.sub(", ,", ",", no_part_string)
                no_part_string = re.sub(",", "", no_part_string)
                no_part_string = re.sub("\.", "", no_part_string)
                no_part_string = re.sub("Chief|CHIEF", "", no_part_string)
                no_part_string = re.sub("\n|\\n", "", no_part_string)
                no_part_string = re.sub("who take no part", "", no_part_string)
                no_part_string = no_part_string.rstrip('\\n')
                no_part_string = re.sub(' and', ',', no_part_string)
                no_part_string = re.sub('deeming', '', no_part_string)
                no_part_string = re.sub('disqualified', '', no_part_string)
                no_part_string = re.sub('retired', '', no_part_string)
                no_part_string = no_part_string.strip()
                no_part_string = no_part_string.upper()
                judges_np = no_part_string
                judges_np = re.sub("\\xc2", "", judges_np)
                judges_np = re.sub("\xc2\xa0", "", judges_np)
                judges_np = re.sub(" and", "", judges_np )
                judge_np_list = judges_np.split(" ")
                judge_np_list = filter(None, judge_np_list)
                if len(judge_np_list) > 4:
                    judge_np_list = judge_np_list[2]
                    judges_np = judge_np_list
                judge_np1 = ""
                judge_np2 = ""
                judge_np3 = ""
                judge_np4 = ""

            # Parse judges text and store list of judges that decided case
            judges_string = re.sub("Judges:|Judges|JUDGES", "", judges_string)
            judges_string = re.sub("judge|Judge|JUDGE", "", judges_string)
            judges_string = re.sub(" delivered the Opinion of the Court\.| DELIVERED THE OPINION OF THE COURT\.|Delivered the Opinion of the Court\.", ",", judges_string)
            judges_string = re.sub("BEFORE THE ENTIRE", "", judges_string)
            judges_string = re.sub("Supreme Court", "", judges_string)
            judges_string = re.sub("Court", "", judges_string)
            judges_string = re.sub("court", "", judges_string)
            judges_string = re.sub("\xc3\x8d", "i", judges_string)
            judges_string = re.sub(" Sr\.| SR\.", "", judges_string)
            judges_string = re.sub(" Jr\.| JR\.", "", judges_string)
            judges_string = re.sub(" Mr\.| MR\.", "", judges_string)
            judges_string = re.sub(" Sr| SR", "", judges_string)
            judges_string = re.sub(" Jr| JR", "", judges_string)
            judges_string = re.sub(" at the", "", judges_string)
            judges_string = re.sub('S94X1612', '', judges_string)
            judges_string = re.sub('CDK, BJJ, JPV', '', judges_string)
            judges_string = re.sub('AD HOC|Ad Hoc|ad hoc', '', judges_string)
            judges_string = re.sub('all who sat', '', judges_string)
            judges_string = re.sub('reasons to be assigned|reason to be assigned', '', judges_string)
            judges_string = re.sub('grant the application', '', judges_string)
            judges_string = re.sub('Procedural Due Process', '', judges_string)
            judges_string = re.sub(" Mr| MR", "", judges_string)
            judges_string = re.sub("F\.X\. HENNESSEY", "HENNESSY", judges_string)
            judges_string = re.sub("are of the opinion", "", judges_string)
            judges_string = re.sub("should be granted", "", judges_string)
            judges_string = re.sub("and in the judgment", "", judges_string)
            judges_string = re.sub("and the judgment", "", judges_string)
            judges_string = re.sub("was an appointed", "", judges_string)
            judges_string = re.sub("S93A0786", "", judges_string)
            judges_string = re.sub("S93X0787", "", judges_string)
            judges_string = re.sub("III-A", "", judges_string)
            judges_string = re.sub("I-V", "", judges_string)
            judges_string = re.sub(" VII", "", judges_string)
            judges_string = re.sub("Parts V\(C\), VI, VII and VIII", "", judges_string)
            judges_string = re.sub("Parts V\(C\), VI, VII, and VIII", "", judges_string)
            judges_string = re.sub("Parts I, II, IV and V\(A\)", "", judges_string)
            judges_string = re.sub("Part III and V\(B\)", "", judges_string)
            judges_string = re.sub("Parts V\(C\), VI, VII and VIII", "", judges_string)
            judges_string = re.sub("Messrs\.", "", judges_string)
            judges_string = re.sub("stead", "", judges_string)
            judges_string = re.sub("MOTION FOR EXPEDITED APPEAL IS GRANTED", "", judges_string)
            judges_string = re.sub("REQUEST FOR ORAL ARGUMENT IS DENIED", "", judges_string)
            judges_string = re.sub("Section IV\(D\)", "", judges_string)
            judges_string = re.sub('part one|Part one|Part One', '', judges_string)
            judges_string = re.sub("parts I, II, and III", "", judges_string)
            judges_string = re.sub("respect|RESPECT|Respect", "", judges_string)
            judges_string = re.sub('Whistle-Blower Act', '', judges_string)
            judges_string = re.sub('Arkansas', '', judges_string)
            judges_string = re.sub("action was submitted", "", judges_string)
            judges_string = re.sub("Subscribing to the Opinion and Assigning Additional Reasons", "", judges_string)
            judges_string = re.sub("Pursuant to Ariz\. Const\. art\. VI|pursuant to Ariz\. Const\. art\. VI|Pursuant to Ariz\. Const\. art\. 6|pursuant to Ariz\. Const\. art\. 6", "", judges_string)
            judges_string = re.sub("Arizona Constitution", "", judges_string)
            judges_string = re.sub("Pursuant to art\. VI\.|Pursuant to article VI", "", judges_string)
            judges_string = re.sub("pursuant|Pursuant", "", judges_string)
            judges_string = re.sub(" and Justices", ",", judges_string)
            judges_string = re.sub("None", "", judges_string)
            judges_string = re.sub("\xe2\x80\x94", "", judges_string)
            judges_string = re.sub("PANEL: ", "", judges_string)
            judges_string = re.sub("\$110W\.", "", judges_string)
            judges_string = re.sub(" but, on administrative leave,", "", judges_string)
            judges_string = re.sub("et al.", "", judges_string)
            judges_string = re.sub("Ex parte Reneau L\. Gates \(re\: v\. Palm Harbor Homes\, Inc\.\, et al\.\)", "", judges_string)
            judges_string = re.sub("We Concur|WE CONCUR|We concur", ", ", judges_string)
            judges_string = re.sub("All the|all the|ALL THE", "", judges_string)
            judges_string = re.sub("Circuit|circuit|CIRCUIT", "", judges_string)
            judges_string = re.sub("except", "", judges_string)
            judges_string = re.sub("Special Justices", "", judges_string)
            judges_string = re.sub("Terminix International v\. Jackson", "", judges_string)
            judges_string = re.sub("Special Justice", "", judges_string)
            judges_string = re.sub("Associate Justice", "", judges_string)
            judges_string = re.sub("Point II", "", judges_string)
            judges_string = re.sub("Special Chief Justice", "", judges_string)
            judges_string = re.sub("Chief Justice", "", judges_string)
            judges_string = re.sub("Justice\.", "", judges_string)
            judges_string = re.sub("for affirmance|For affirmance", "", judges_string)
            judges_string = re.sub("affirmance|Affirmance|AFFIRMANCE", "", judges_string)
            judges_string = re.sub("'s|'S", "", judges_string)
            judges_string = re.sub("\(No\.\s\d*\)", "", judges_string)
            judges_string = re.sub("AFFIRMED|Affirmed|affirmed", "", judges_string)
            judges_string = re.sub("AFFIRM|Affirm|affirm", "", judges_string)
            judges_string = re.sub("grant the petition", "", judges_string)
            judges_string = re.sub("petition|Petition|PETITION", "", judges_string)
            judges_string = re.sub("Granted|granted|GRANTED", "", judges_string)
            judges_string = re.sub("abstaining|Abstaining|ABSTAINING", "", judges_string)
            judges_string = re.sub("No\.\s\d*", "", judges_string)
            judges_string = re.sub("Senior", "", judges_string)
            judges_string = re.sub("Supr\.|Supr", "", judges_string)
            judges_string = re.sub("\xe2\x80\x94", "", judges_string)
            judges_string = re.sub("Chief Justice", ",", judges_string)
            judges_string = re.sub("Chief Judge", "", judges_string)
            judges_string = re.sub("--", ",", judges_string)
            judges_string = re.sub(" but ", "", judges_string)
            judges_string = re.sub("Justices|JUSTICES|justices", "", judges_string)
            judges_string = re.sub("JUSTICE\.", "", judges_string)
            judges_string = re.sub("JUSTICE|Justice|justice", "", judges_string)
            judges_string = re.sub("announced|Announced|ANNOUNCED", "", judges_string)
            judges_string = re.sub("\*Link to the text of the note", "", judges_string)
            judges_string = re.sub("Ariz\.Const\.", "", judges_string)
            judges_string = re.sub("art\. VI", "", judges_string)
            judges_string = re.sub(" art\.", "", judges_string)
            judges_string = re.sub("Link to the text of the note", "", judges_string)
            judges_string = re.sub("to the", "", judges_string)
            judges_string = re.sub("prior", "", judges_string)
            judges_string = re.sub("oral argument|argument", "", judges_string)
            judges_string = re.sub("resigned", "", judges_string)
            judges_string = re.sub("chief|Chief|CHIEF", "", judges_string)
            judges_string = re.sub("AUTHOR", "", judges_string)
            judges_string = re.sub("nonrecusal|NONRECUSAL|Nonrecusal", "", judges_string)
            judges_string = re.sub("deeming", "", judges_string)
            judges_string = re.sub("temporary", "", judges_string)
            judges_string = re.sub("has filed", "", judges_string)
            judges_string = re.sub("filed:", "", judges_string)
            judges_string = re.sub("filed a|file a", "", judges_string)
            judges_string = re.sub("President", "", judges_string)
            judges_string = re.sub("Intermediate|intermediate|INTERMEDIATE", "", judges_string)
            judges_string = re.sub("Associate|ASSOCIATE|associate", "", judges_string)
            judges_string = re.sub("reasons|REASONS|Reasons|reason|REASON|Reason", "", judges_string)
            judges_string = re.sub("Superior", "", judges_string)
            judges_string = re.sub("constituting the", "", judges_string)
            judges_string = re.sub("En Banc|en Banc", "", judges_string)
            judges_string = re.sub("In Banc", "", judges_string)
            judges_string = re.sub("cases|Cases|CASES", "", judges_string)
            judges_string = re.sub("disagreeing|disagreement|disagree", "", judges_string)
            judges_string = re.sub("agreement|Agreement|AGREEMENT", "", judges_string)
            judges_string = re.sub('"', "", judges_string)
            judges_string = re.sub(" all | All | ALL ", "", judges_string)
            judges_string = re.sub("Present|PRESENT|present", "", judges_string)
            judges_string = re.sub("APPEALS", "", judges_string)
            judges_string = re.sub(" THE", "", judges_string)
            judges_string = re.sub("\xc3\x81", "a", judges_string)
            judges_string = re.sub("WITHOUT", "", judges_string)
            judges_string = re.sub("WITH", "", judges_string)
            judges_string = re.sub("ASSIGNED BY REASON OF VACANCY|VACANCY|Vacancy", "", judges_string)
            judges_string = re.sub("THIS", "", judges_string)
            judges_string = re.sub("PELICONES|Pelicones", "", judges_string)
            judges_string = re.sub("member|Member|MEMBER", "", judges_string)
            judges_string = re.sub("disposition|Disposition|DISPOSITION", "", judges_string)
            judges_string = re.sub(" right| Right| RIGHT", "", judges_string)
            judges_string = re.sub("DISSENTS", "", judges_string)
            judges_string = re.sub("WRITTEN|written|Written", "", judges_string)
            judges_string = re.sub("WITHOUT|without", "", judges_string)
            judges_string = re.sub("\xc3\xa9", "e", judges_string)
            judges_string = re.sub(" took| TOOK| Took", "", judges_string)
            judges_string = re.sub("Rule IV", "", judges_string)
            judges_string = re.sub(" IV", "", judges_string)
            judges_string = re.sub("C\. J\.,", "", judges_string)
            judges_string = re.sub(" J\.,", "", judges_string)
            judges_string = re.sub("assignment|Assignment|ASSIGNMENT", "", judges_string)
            judges_string = re.sub("assigning", "", judges_string)
            judges_string = re.sub("assigned", "", judges_string)
            judges_string = re.sub("assigns", "", judges_string)
            judges_string = re.sub("assign", "", judges_string)
            judges_string = re.sub("assigned|Assigned|ASSIGNED|ASSIGNS|Assigns|assigns", "", judges_string)
            judges_string = re.sub(" as ", "", judges_string)
            judges_string = re.sub('"Agreement to Arbitrate"', "", judges_string)
            judges_string = re.sub("Arbitrate\"", "", judges_string)
            judges_string = re.sub("files a", "", judges_string)
            judges_string = re.sub("former|Former|FORMER", "", judges_string)
            judges_string = re.sub("Honor|honor|HONOR", "", judges_string)
            judges_string = re.sub(" Hon.", "", judges_string)
            judges_string = re.sub("Hon\. J\.", "", judges_string)
            judges_string = re.sub("C\.J\.,|Sp\.JJ|Sp\.J\.|Sp\. J\.|C\.J,|J\.P\.T\.|CJ,||A\.J\.V\.C\.J\.,|JJ\.,|Sp\.J\.|Js,|JS,|JJ\.,|JJ,|D\.J\.,|P\.J\.,|P\.\sJ\.,|C\.J\.,|J\.,|J\.| J,|C\. J\.,", "", judges_string)
            judges_string = re.sub("C\.J\.|C\.J|CJ|JJ\.|Js|JS|JJ\.|JJ|D\.J\.|P\.J\.|P\.\sJ\.|C\.J\.|J\.|J\.|C\. J\.", "", judges_string)
            judges_string = re.sub("C\.J\.|C\.J|CJ|JJ\.|Js|JS|JJ\.|JJ|D\.J\.|P\.J\.|P\.\sJ\.|C\.J\.|J\.|J\.|C\. J\.", "", judges_string)
            judges_string = re.sub("Sp\.J\.", "", judges_string)
            judges_string = re.sub("Part II\.A", "", judges_string)
            judges_string = re.sub("Part II\.B", "", judges_string)
            judges_string = re.sub("Parts II", "", judges_string)
            judges_string = re.sub("Parts I", "", judges_string)
            judges_string = re.sub("Part II", "", judges_string)
            judges_string = re.sub("Part I", "", judges_string)
            judges_string = re.sub("Part XII", "", judges_string)
            judges_string = re.sub("WoWe", "", judges_string)
            judges_string = re.sub("foregoing|Foregoing|FOREGOING", "", judges_string)
            judges_string = re.sub(" for| For| FOR", "", judges_string)
            judges_string = re.sub("", "", judges_string)
            judges_string = re.sub("[\(\[].*?[\)\]]", "", judges_string)
            judges_string = re.sub("III", "", judges_string)
            judges_string = re.sub("II\(\w\)", "", judges_string)
            judges_string = re.sub("III\(\w\)", "", judges_string)
            judges_string = re.sub(" II", "", judges_string)
            judges_string = re.sub("III", "", judges_string)
            judges_string = re.sub("Associate", "", judges_string)
            judges_string = re.sub("Vice", "", judges_string)
            judges_string = re.sub("\[\**\d*\]", "", judges_string)
            judges_string = re.sub("Arbitrate|arbitrate|ARBITRATE", "", judges_string)
            judges_string = re.sub("\xc2", "", judges_string)
            judges_string = re.sub("BENCH|Bench|bench", "", judges_string)
            judges_string = re.sub("(Before: |BEFORE: )", "", judges_string)
            judges_string = re.sub("\xa0", " ", judges_string)
            judges_string = re.sub("\/", "", judges_string)
            judges_string = re.sub("\n|\r", " ", judges_string)
            judges_string = re.sub("\(see p", " ", judges_string)
            judges_string = re.sub("\(\d\)", "", judges_string)
            judges_string = re.sub("\d", "", judges_string)
            judges_string = re.sub("\(", "", judges_string)
            judges_string = re.sub("\)", "", judges_string)
            judges_string = re.sub("\sI,", "", judges_string)
            judges_string = re.sub(" or ", "", judges_string)
            judges_string = re.sub("Saylor|SAYLOR", "Saylor, ", judges_string)
            judges_string = re.sub(" BY", "", judges_string)
            judges_string = re.sub(" FOR", "", judges_string)
            judges_string = re.sub("I;", "", judges_string)
            judges_string = re.sub("Voting|VOTING|voting", "", judges_string)
            judges_string = re.sub("Surrogate", "", judges_string)
            judges_string = re.sub("\'", "", judges_string)			#makes matching of judge names possible: O'Connor -> OConnor
            judges_string = re.sub("judgment|JUDGMENT", "", judges_string)
            judges_string = re.sub("SeeStuart|seestuart", "See, Stuart", judges_string)
            if(re.search("unanimous view of the court|unanimous", judges_string)):
                unanimous = 1
            judges_string = re.sub("unanimous view of the court", "", judges_string)
            judges_string = re.sub("unanimous", "", judges_string)
            judges_string = re.sub("Took no|Took No|took no|TOOK NO", "", judges_string)
            judges_string = re.sub(" No,", "", judges_string)
            judges_string = re.sub("separately|Separately|SEPARATELY", "", judges_string)
            judges_string = re.sub("separate|Separate|SEPARATE", "", judges_string)
            judges_string = re.sub("in place of", "", judges_string)
            judges_string = re.sub("sections,", "", judges_string)
            judges_string = re.sub("Sections,", "", judges_string)
            judges_string = re.sub("sections", "", judges_string)
            judges_string = re.sub("section,", "", judges_string)
            judges_string = re.sub("Section,", "", judges_string)
            judges_string = re.sub("section", "", judges_string)
            judges_string = re.sub("constituting,", "", judges_string)
            judges_string = re.sub("en banc,|en banc|En banc|En Banc|EN BANC", "", judges_string)
            judges_string = re.sub("\[", "", judges_string)
            judges_string = re.sub("\]", ",", judges_string)
            judges_string = re.sub("concur in part and dissent in part|CONCUR IN PART AND DISSENT IN PART", " ", judges_string)
            judges_string = re.sub("concurs in part and dissents in part|CONCURS IN PART AND DISSENTS IN PART", " ", judges_string)
            judges_string = re.sub("concurs in the result, without opinion\.", "", judges_string)
            judges_string = re.sub("all concurring", "", judges_string)
            judges_string = re.sub("III-D", "", judges_string)
            judges_string = re.sub("See separate opinion", "", judges_string)
            judges_string = re.sub("concurring|Concurring|CONCURRING", "", judges_string)
            judges_string = re.sub("concurrence|Concurrence|CONCURRENCE|Concurrence:", "", judges_string)
            judges_string = re.sub("concurs", ",", judges_string)
            judges_string = re.sub("concurred", ",", judges_string)
            judges_string = re.sub("concur in", "", judges_string)
            judges_string = re.sub("Concurs:|CONCURs:", "", judges_string)
            judges_string = re.sub("concurs|Concurs|CONCURS", "", judges_string)
            judges_string = re.sub("concur\.", ",", judges_string)
            judges_string = re.sub("concur|Concur", "", judges_string)
            judges_string = re.sub("CONCUR", ",", judges_string)
            judges_string = re.sub("does", "", judges_string)
            judges_string = re.sub("consideration", "", judges_string)
            judges_string = re.sub("Md\.", "", judges_string)
            judges_string = re.sub("Temporarily", "", judges_string)
            judges_string = re.sub("Link to, text thee", "", judges_string)
            judges_string = re.sub("assigns reasons", "", judges_string)
            judges_string = re.sub("Appeals", "", judges_string)
            judges_string = re.sub("retired|RETIRED|Retired|Ret|ret\.", "", judges_string)
            judges_string = re.sub("assigned|Assigned|ASSIGNED|assignment|Assignment|ASSIGNNMENT", "", judges_string)
            judges_string = re.sub("The ", "", judges_string)
            judges_string = re.sub(" sat", "", judges_string)
            judges_string = re.sub("delivered|delivers|Delivers|Delivered", "", judges_string)
            judges_string = re.sub("PARTICIPATING", "", judges_string)
            judges_string = re.sub("participating", "", judges_string)
            judges_string = re.sub("PARTICIPATING", "", judges_string)
            judges_string = re.sub("participating", "", judges_string)
            judges_string = re.sub("Participating", "", judges_string)
            judges_string = re.sub("did not participate", "", judges_string)
            judges_string = re.sub("did not sit", "", judges_string)
            judges_string = re.sub("did not", "", judges_string)
            judges_string = re.sub("Maricopa County", "", judges_string)
            judges_string = re.sub("County", "", judges_string)
            judges_string = re.sub("WRITTEN BY:|Written by:", "", judges_string)
            judges_string = re.sub("herein", "", judges_string)
            judges_string = re.sub("not participate", "", judges_string)
            judges_string = re.sub("participate", "", judges_string)
            judges_string = re.sub("Presiding|PRESIDING", "", judges_string)
            judges_string = re.sub("specially|Specially|SPECIALLY", "", judges_string)
            judges_string = re.sub("special|Special|SPECIAL", "", judges_string)
            judges_string = re.sub("Pro Tempore", "", judges_string)
            judges_string = re.sub("pro-tem|Pro-Tem|PRO-TEM", "", judges_string)
            judges_string = re.sub("concurring", "", judges_string)
            judges_string = re.sub("Concurring", "", judges_string)
            judges_string = re.sub("concurs in the result, without opinion\.", "", judges_string)
            judges_string = re.sub("no opinion", "", judges_string)
            judges_string = re.sub("opinion\.", ",", judges_string)
            judges_string = re.sub("OPINIONS|OPINIONs|opinions|Opinions", "", judges_string)
            judges_string = re.sub("opinion", "", judges_string)
            judges_string = re.sub("Opinion", "", judges_string)
            judges_string = re.sub(" full ", "", judges_string)
            judges_string = re.sub("statement", "", judges_string)
            judges_string = re.sub("files|file|FILES|FILE", "", judges_string)
            judges_string = re.sub("Judicial Circuit", "", judges_string)
            judges_string = re.sub("Part III", "", judges_string)
            judges_string = re.sub("parties", "", judges_string)
            judges_string = re.sub("no part|NO PART|No Part", "", judges_string)
            judges_string = re.sub("partial", "", judges_string)
            judges_string = re.sub("part", "", judges_string)
            judges_string = re.sub("Part", "", judges_string)
            judges_string = re.sub("PART", "", judges_string)
            if not re.search('WHICHARD', judges_string):
                judges_string = re.sub("which|Which|WHICH", "", judges_string)
            judges_string = re.sub("DENIED|denied", "", judges_string)
            judges_string = re.sub("Majority|majority|MAJORITY", "", judges_string)
            judges_string = re.sub("Heard|heard|HEARD", "", judges_string)
            judges_string = re.sub("joining|JOINING|Joining", "", judges_string)
            judges_string = re.sub("joined|JOINED|Joined", "", judges_string)
            judges_string = re.sub("joins|JOINS|Joins", "", judges_string)
            judges_string = re.sub("join|JOIN|Join", "", judges_string)
            judges_string = re.sub("takes|taking|Taking|TAKING", "", judges_string)
            judges_string = re.sub(" that", "", judges_string)
            judges_string = re.sub("as to the rationale", "", judges_string)
            judges_string = re.sub("the judgment", "", judges_string)
            judges_string = re.sub("rationale", "", judges_string)
            judges_string = re.sub("T\.Y\.|T\. Y\.", "", judges_string)
            judges_string = re.sub("A\.M\.", "", judges_string)
            judges_string = re.sub("F\.E\.", "", judges_string)
            judges_string = re.sub("N\.C\.", "", judges_string)
            judges_string = re.sub("Paul H\.", "", judges_string)
            judges_string = re.sub("Russell A\.", "", judges_string)
            judges_string = re.sub("G\. Barry", "", judges_string)
            judges_string = re.sub(" A\.| B\.| C\.| D\.| E\.| F\.| G\.| H\.| I\.| J\.| K\.| L\.| M\.| N\.| O\.| P\.| Q\.| R\.| S\.| T\.| U\.| V\.| W\.| X\.| Y\.| Z\.|", "", judges_string)
            judges_string = re.sub(" A\.| B\.| C\.| D\.| E\.| F\.| G\.| H\.| I\.| J\.| K\.| L\.| M\.| N\.| O\.| P\.| Q\.| R\.| S\.| T\.| U\.| V\.| W\.| X\.| Y\.| Z\.|", "", judges_string)
            judges_string = re.sub(" A\.| B\.| C\.| D\.| E\.| F\.| G\.| H\.| I\.| J\.| K\.| L\.| M\.| N\.| O\.| P\.| Q\.| R\.| S\.| T\.| U\.| V\.| W\.| X\.| Y\.| Z\.|", "", judges_string)
            judges_string = re.sub(" A\.| B\.| C\.| D\.| E\.| F\.| G\.| H\.| I\.| J\.| K\.| L\.| M\.| N\.| O\.| P\.| Q\.| R\.| S\.| T\.| U\.| V\.| W\.| X\.| Y\.| Z\.|", "", judges_string)
            judges_string = re.sub(" A\.| B\.| C\.| D\.| E\.| F\.| G\.| H\.| I\.| J\.| K\.| L\.| M\.| N\.| O\.| P\.| Q\.| R\.| S\.| T\.| U\.| V\.| W\.| X\.| Y\.| Z\.|", "", judges_string)
            judges_string = re.sub("\.", ",", judges_string)
            judges_string = re.sub("BEFORE", "", judges_string)
            judges_string = re.sub("would", "", judges_string)
            judges_string = re.sub("this", "", judges_string)
            judges_string = re.sub("only", "", judges_string)
            judges_string = re.sub("without", "", judges_string)
            judges_string = re.sub("with", "", judges_string)
            judges_string = re.sub(" out", "", judges_string)
            judges_string = re.sub("also", "", judges_string)
            judges_string = re.sub(" of", "", judges_string)
            judges_string = re.sub(" view", "", judges_string)
            judges_string = re.sub(" Not", "", judges_string)
            judges_string = re.sub(" not", "", judges_string)
            judges_string = re.sub(" NOT", "", judges_string)
            judges_string = re.sub(" whom", "", judges_string)
            judges_string = re.sub(" who", "", judges_string)
            judges_string = re.sub("filed", "", judges_string)
            judges_string = re.sub("expressing", "", judges_string)
            judges_string = re.sub("but dissents", "", judges_string)
            judges_string = re.sub("but dissent", "", judges_string)
            judges_string = re.sub("but not the dissent", "", judges_string)
            judges_string = re.sub("dissented", "", judges_string)
            judges_string = re.sub("issued", ",", judges_string)
            judges_string = re.sub("foregoing", "", judges_string)
            judges_string = re.sub("agree", "", judges_string)
            judges_string = re.sub("Opposed|opposed|OPPOSED", "", judges_string)
            judges_string = re.sub("dissents", "", judges_string)
            judges_string = re.sub("dissenting", "", judges_string)
            judges_string = re.sub("DISSENTING", "", judges_string)
            judges_string = re.sub("ENTIRE COURT", "", judges_string)
            judges_string = re.sub(" as", "", judges_string)
            judges_string = re.sub("reversal", "", judges_string)
            judges_string = re.sub("none", "", judges_string)
            judges_string = re.sub("Twelfth|Eleventh|Fifth|Tenth|Ninth|Eigth|Seventh|Sixth", "", judges_string)
            judges_string = re.sub("Mr", "", judges_string)
            judges_string = re.sub('remandment', '', judges_string)
            judges_string = re.sub("remand", "", judges_string)
            judges_string = re.sub("overruling", "", judges_string)
            judges_string = re.sub("rehearing", "", judges_string)
            judges_string = re.sub("OPINION", "", judges_string)
            judges_string = re.sub("COURT", "", judges_string)
            judges_string = re.sub("ONLY", "", judges_string)
            judges_string = re.sub("IN RESULT", "", judges_string)
            judges_string = re.sub(" IN ", "", judges_string)
            judges_string = re.sub("Dissenting", "", judges_string)
            judges_string = re.sub("Dissents", "", judges_string)
            judges_string = re.sub("dissent\.", ",", judges_string)
            judges_string = re.sub("dissent", "", judges_string)
            judges_string = re.sub("Dissent", "", judges_string)
            judges_string = re.sub("recuses|RECUSES|Recuses", "", judges_string)
            judges_string = re.sub("recused|RECUSED|Recused", "", judges_string)
            judges_string = re.sub("recuse|RECUSE|Recuse", "", judges_string)
            judges_string = re.sub("SEPARATELY", "", judges_string)
            judges_string = re.sub("PRO-TEM", "", judges_string)
            judges_string = re.sub("reserves", "", judges_string)
            judges_string = re.sub("is disqualified|disqualified|disqualification", "", judges_string)
            judges_string = re.sub("recused themselves", "", judges_string)
            judges_string = re.sub("recused", "", judges_string)
            judges_string = re.sub("Recused", "", judges_string)
            judges_string = re.sub("deceased", "", judges_string)
            judges_string = re.sub("in the result", "", judges_string)
            judges_string = re.sub("the result", "", judges_string)
            judges_string = re.sub("result|Result|RESULT", "", judges_string)
            judges_string = re.sub(" acting ", "", judges_string)
            judges_string = re.sub(" and ", ",", judges_string)
            judges_string = re.sub(" AND ", ",", judges_string)
            judges_string = re.sub(" an", ",", judges_string)
            judges_string = re.sub("application|Application|APPLICATION", ", ", judges_string)
            judges_string = re.sub("dismissed|Dismissed|DISMISSED", ", ", judges_string)
            judges_string = re.sub("entitled|Entitled|ENTITLED", ", ", judges_string)
            judges_string = re.sub("appeal|Appeal|APPEAL", ", ", judges_string)
            judges_string = re.sub(" the ", ", ", judges_string)
            judges_string = re.sub(" as to", ", ", judges_string)
            judges_string = re.sub("decision", ", ", judges_string)
            judges_string = re.sub("final", ", ", judges_string)
            judges_string = re.sub(" in a", "", judges_string)
            judges_string = re.sub("in the", "", judges_string)
            judges_string = re.sub(" In | in ", "", judges_string)
            judges_string = re.sub(" in,", "", judges_string)
            judges_string = re.sub(" of", "", judges_string)
            judges_string = re.sub(" OF", "", judges_string)
            judges_string = re.sub(" from", "", judges_string)
            judges_string = re.sub("herself", "", judges_string)
            judges_string = re.sub("himself", "", judges_string)
            judges_string = re.sub("themselves", "", judges_string)
            judges_string = re.sub("expresses", "", judges_string)
            judges_string = re.sub("ii", "", judges_string)
            judges_string = re.sub(" cases| Cases", "", judges_string)
            judges_string = re.sub("case", "", judges_string)
            judges_string = re.sub("Case", "", judges_string)
            judges_string = re.sub(" by", "", judges_string)
            judges_string = re.sub("heard", "", judges_string)
            judges_string = re.sub("DENVIRSTITH", "STITH", judges_string)
            judges_string = re.sub("considered", "", judges_string)
            judges_string = re.sub("decided", "", judges_string)
            judges_string = re.sub("time", "", judges_string)
            judges_string = re.sub("submission", "", judges_string)
            judges_string = re.sub("\&", "", judges_string)
            judges_string = re.sub("were designated", "", judges_string)
            judges_string = re.sub("is designated|designated|designation", "", judges_string)
            judges_string = re.sub(" All |ALL ", "", judges_string)
            judges_string = re.sub("is sitting", "", judges_string)
            judges_string = re.sub("sitting|SITTING|Sitting", "", judges_string)
            judges_string = re.sub(" sit", "", judges_string)
            judges_string = re.sub(" superior", "", judges_string)
            judges_string = re.sub(" under", "", judges_string)
            judges_string = re.sub("Cavanaugh|CAVANAUGH", "Cavanagh", judges_string)
            judges_string = re.sub("WHOLE|Whole|whole", "", judges_string)
            judges_string = re.sub("deny", "", judges_string)
            judges_string = re.sub("Matter|MATTER|matter", "", judges_string)
            judges_string = re.sub(" otherwise|Otherwise|OTHERWISE", "", judges_string)
            judges_string = re.sub(" leave", "", judges_string)
            judges_string = re.sub(" others| other| Other| OTHER", "", judges_string)
            judges_string = re.sub(" vote|votes to", "", judges_string)
            judges_string = re.sub("RSA", "", judges_string)
            judges_string = re.sub("memorandum", "", judges_string)
            judges_string = re.sub("took no", "", judges_string)
            judges_string = re.sub("syllabus", "", judges_string)
            judges_string = re.sub("Appellate District", "", judges_string)
            judges_string = re.sub("District|district", "", judges_string)
            judges_string = re.sub("Administrative", "", judges_string)
            judges_string = re.sub("i-v", "", judges_string)
            judges_string = re.sub("follows", "", judges_string)
            judges_string = re.sub("Judicial", "", judges_string)
            judges_string = re.sub("By:", "", judges_string)
            judges_string = re.sub("Panel:", "", judges_string)
            judges_string = re.sub(":\s", "", judges_string)
            judges_string = re.sub(":", "", judges_string)
            judges_string = re.sub("authored|Authored|AUTHORED", "", judges_string)
            judges_string = re.sub(" to ", "", judges_string)
            judges_string = re.sub("DISSENT", "", judges_string)
            judges_string = re.sub(" each", "", judges_string)
            judges_string = re.sub("Jr|jr|JR", "", judges_string)
            judges_string = re.sub("denial", "", judges_string)
            judges_string = re.sub("Sr|sr|SR", "", judges_string)
            judges_string = re.sub("Deceased|deceased|DECEASED", "", judges_string)
            judges_string = re.sub("lead|LEAD|Lead", "", judges_string)
            judges_string = re.sub(" was | WAS | Was", "", judges_string)
            judges_string = re.sub(" other", "", judges_string)
            judges_string = re.sub("writing", "", judges_string)
            judges_string = re.sub("Writ|writ|WRIT", "", judges_string)
            judges_string = re.sub("take|TAKE|Take", "", judges_string)
            judges_string = re.sub("Issued|issued|ISSUED", "", judges_string)
            judges_string = re.sub("Madame|MADAME|madame", "", judges_string)
            judges_string = re.sub("Visiting|VISITING|visiting", "", judges_string)
            judges_string = re.sub("acting|ACTING|Acting", "", judges_string)
            judges_string = re.sub("having|Having|HAVING", "", judges_string)
            judges_string = re.sub("reverse", "", judges_string)
            judges_string = re.sub("O'NEILL to|O'NEILLto", "O'NEILL", judges_string)
            judges_string = re.sub(" is ", "", judges_string)
            judges_string = re.sub("Third", "", judges_string)
            judges_string = re.sub(" John ", "", judges_string)
            judges_string = re.sub("Boucier", "Bourcier", judges_string)
            judges_string = re.sub(" to ", "", judges_string)
            judges_string = re.sub(",to ", "", judges_string)
            judges_string = re.sub("Ralmon", "Almon", judges_string)
            judges_string = re.sub("Fabec", "Fabe", judges_string)
            judges_string = re.sub(" ir ", "", judges_string)
            judges_string = re.sub("Estaugh", "Eastaugh", judges_string)
            judges_string = re.sub("Modification", "", judges_string)
            judges_string = re.sub("Vacation", "", judges_string)
            judges_string = re.sub(",d,", "", judges_string)
            judges_string = re.sub("Division Two|Two", "", judges_string)
            judges_string = re.sub("Division Six", "", judges_string)
            judges_string = re.sub("dS", "", judges_string)
            judges_string = re.sub("NOTE", "", judges_string)
            judges_string = re.sub("dI", "", judges_string)
            judges_string = re.sub("dX", "", judges_string)
            judges_string = re.sub("were", "", judges_string)
            judges_string = re.sub("pursuant", "", judges_string)
            judges_string = re.sub("determination ", "", judges_string)
            judges_string = re.sub("Division One", "", judges_string)
            judges_string = re.sub("article IV", "", judges_string)
            judges_string = re.sub("Article|ARTICLE|article", "", judges_string)
            judges_string = re.sub("Arizona", "", judges_string)
            judges_string = re.sub("Second", "", judges_string)
            judges_string = re.sub("Council", "", judges_string)
            judges_string = re.sub("Chairperson", "", judges_string)
            judges_string = re.sub("not on panel|on panel|panel", "", judges_string)
            judges_string = re.sub("Division Four", "", judges_string)
            judges_string = re.sub("to conviction|conviction", "", judges_string)
            judges_string = re.sub("to sentence|sentence", "", judges_string)
            judges_string = re.sub("additional", "", judges_string)
            judges_string = re.sub("following", "", judges_string)
            judges_string = re.sub("subscribes|subscribe", "", judges_string)
            judges_string = re.sub("ORAL ARGUMENT", "", judges_string)
            judges_string = re.sub("DENIAL", "", judges_string)
            judges_string = re.sub(" ONE ", "", judges_string)
            judges_string = re.sub("TWO", "", judges_string)
            judges_string = re.sub("THREE", "", judges_string)
            judges_string = re.sub(" have", "", judges_string)
            judges_string = re.sub("unconstitutional", "", judges_string)
            judges_string = re.sub("follow", "", judges_string)
            judges_string = re.sub("chapter", "", judges_string)
            judges_string = re.sub("Lesson", "Leeson", judges_string)
            judges_string = re.sub("Before", "", judges_string)
            judges_string = re.sub("Per Curiam|Curiam", "", judges_string)
            judges_string = re.sub("causesubmitted", "", judges_string)
            judges_string = re.sub("on briefs|briefs|brief", "", judges_string)
            judges_string = re.sub("Division", "", judges_string)
            judges_string = re.sub("absent", "", judges_string)
            judges_string = re.sub(" IV,", "", judges_string)
            judges_string = re.sub(" when", "", judges_string)
            judges_string = re.sub(" inof", "", judges_string)
            judges_string = re.sub("Order", "", judges_string)
            judges_string = re.sub("absent", "", judges_string)
            judges_string = re.sub(" to ", "", judges_string)
            judges_string = re.sub("tohis ", "", judges_string)
            judges_string = re.sub("toother|TOOTHER|to other", "", judges_string)
            judges_string = string.strip(judges_string)
            judges_string = re.sub(", ,", ",", judges_string)
            judges_string = re.sub("s V", "", judges_string)
            judges_string = re.sub(" VI,", "", judges_string)
            judges_string = re.sub('DENVIR STITH', 'Stith', judges_string)
            judges_string = re.sub('remainder|Remainder|REMAINDER', '', judges_string)
            judges_string = re.sub(' Wo,', '', judges_string)
            judges_string = re.sub(' Eighth', '', judges_string)
            judges_string = re.sub('its entirety', '', judges_string)
            judges_string = re.sub('entirety', '', judges_string)
            judges_string = re.sub('holdings', '', judges_string)
            judges_string = re.sub(' SPL,', '', judges_string)
            judges_string = re.sub(' Five', '', judges_string)
            judges_string = re.sub('APPENDIX', '', judges_string)
            judges_string = re.sub(' Votes', '', judges_string)
            judges_string = re.sub('Chancellor', '', judges_string)
            judges_string = re.sub(' guilt', '', judges_string)
            judges_string = re.sub(' the ', '', judges_string)
            judges_string = re.sub(' the,', '', judges_string)
            judges_string = re.sub('issuance', '', judges_string)
            judges_string = re.sub(' inin', '', judges_string)
            judges_string = re.sub('Process', '', judges_string)
            judges_string = re.sub('transfer', '', judges_string)
            judges_string = re.sub('Indiana', '', judges_string)
            judges_string = re.sub('emphasize', '', judges_string)
            judges_string = re.sub('non-hearsay', '', judges_string)
            judges_string = re.sub('hearsay', '', judges_string)
            judges_string = re.sub('Section II|Section', '', judges_string)
            judges_string = re.sub('section|SECTION', '', judges_string)
            judges_string = re.sub('impermissible', '', judges_string)
            judges_string = re.sub('excellent|Excellent|Excellence|excellence', '', judges_string)
            judges_string = re.sub('sexually predatory', '', judges_string)
            judges_string = re.sub('Ten Broeck', '', judges_string)
            judges_string = re.sub(' First', '', judges_string)
            judges_string = re.sub('error', '', judges_string)
            judges_string = re.sub('believings|believing', '', judges_string)
            judges_string = re.sub('Doctor|doctor', '', judges_string)
            judges_string = re.sub('dsigning', '', judges_string)
            judges_string = re.sub('Plurality', '', judges_string)
            judges_string = re.sub('Maryland', '', judges_string)
            judges_string = re.sub('question|Question|QUESTION', '', judges_string)
            judges_string = re.sub('before|Before|BEFORE', '', judges_string)
            judges_string = re.sub(' Yes | yes ', '', judges_string)
            judges_string = re.sub(' Yes,| yes,', '', judges_string)
            judges_string = re.sub('unanimouns', '', judges_string)
            judges_string = re.sub('circumstance|Circumstances|CIRCUMSTANCES', '', judges_string)
            judges_string = re.sub(' action', '', judges_string)
            judges_string = re.sub('concludes', '', judges_string)
            judges_string = re.sub('addressed', '', judges_string)
            judges_string = re.sub(' commit', '', judges_string)
            judges_string = re.sub(' was | was,', '', judges_string)
            judges_string = re.sub(' and ', '', judges_string)
            judges_string = re.sub(' trial', '', judges_string)
            judges_string = re.sub('captioned|caption', '', judges_string)
            judges_string = re.sub(' swer,| swer ', '', judges_string)
            judges_string = re.sub('directions|direction', '', judges_string)
            judges_string = re.sub(' enter', '', judges_string)
            judges_string = re.sub('against', '', judges_string)
            judges_string = re.sub('summary', '', judges_string)
            judges_string = re.sub('Considered', '', judges_string)
            judges_string = re.sub('proceedings', '', judges_string)
            judges_string = re.sub(' entire', '', judges_string)
            judges_string = re.sub(' favor', '', judges_string)
            judges_string = re.sub('discrimination', '', judges_string)
            judges_string = re.sub('claim', '', judges_string)
            judges_string = re.sub('further', '', judges_string)
            judges_string = re.sub('expressed', '', judges_string)
            judges_string = re.sub('discussion', '', judges_string)
            judges_string = re.sub('submitted', '', judges_string)
            judges_string = re.sub('consent', '', judges_string)
            judges_string = re.sub('stating', '', judges_string)
            judges_string = re.sub('NYCRR', '', judges_string)
            judges_string = re.sub('accepted', '', judges_string)
            judges_string = re.sub('dismiss', '', judges_string)
            judges_string = re.sub('granting', '', judges_string)
            judges_string = re.sub('relator', '', judges_string)
            judges_string = re.sub('pronouncement', '', judges_string)
            judges_string = re.sub('reversal', '', judges_string)
            judges_string = re.sub('balance', '', judges_string)
            judges_string = re.sub(' two', '', judges_string)
            judges_string = re.sub('answers', '', judges_string)
            judges_string = re.sub('counsel', '', judges_string)
            judges_string = re.sub('record', '', judges_string)
            judges_string = re.sub('boxertrain', '', judges_string)
            judges_string = re.sub(' rule', '', judges_string)
            judges_string = re.sub(' Rules', '', judges_string)
            judges_string = re.sub('improvidently', '', judges_string)
            judges_string = re.sub(' text', '', judges_string)
            judges_string = re.sub(' after', '', judges_string)
            judges_string = re.sub('February', '', judges_string)
            judges_string = re.sub('reserve', '', judges_string)
            
            judges_string = re.sub('EXPRESSED', '', judges_string)
            judges_string = re.sub('expressed', '', judges_string)
            judges_string = re.sub('Expressed', '', judges_string)
            judges_string = re.sub('icipation', '', judges_string)
            judges_string = re.sub('ICIPATION', '', judges_string)
            judges_string = re.sub('issues', '', judges_string)
            judges_string = re.sub('Issues', '', judges_string)
            judges_string = re.sub('ISSUES', '', judges_string)
            judges_string = re.sub('issue', '', judges_string)
            judges_string = re.sub('Issue', '', judges_string)
            judges_string = re.sub('ISSUE', '', judges_string)
            judges_string = re.sub(' the ', '', judges_string)
            judges_string = re.sub(' The ', '', judges_string)
            judges_string = re.sub(' The ', '', judges_string)
            judges_string = re.sub(' THE,', '', judges_string)
            judges_string = re.sub(' the,', '', judges_string)
            judges_string = re.sub(' THE,', '', judges_string)
            judges_string = re.sub(',the ', '', judges_string)
            judges_string = re.sub(',The ', '', judges_string)
            judges_string = re.sub(',THE ', '', judges_string)
            judges_string = re.sub(' has ', '', judges_string)
            judges_string = re.sub(' Has ', '', judges_string)
            judges_string = re.sub(' HAS ', '', judges_string)
            judges_string = re.sub(' Has,', '', judges_string)
            judges_string = re.sub(' has,', '', judges_string)
            judges_string = re.sub(' HAS,', '', judges_string)
            judges_string = re.sub(',has ', '', judges_string)
            judges_string = re.sub(',Has ', '', judges_string)
            judges_string = re.sub(',HAS ', '', judges_string)
            judges_string = re.sub('judgment', '', judges_string)
            judges_string = re.sub('Judgment', '', judges_string)
            judges_string = re.sub('JUDGMENT', '', judges_string)
            judges_string = re.sub('subscribing', '', judges_string)
            judges_string = re.sub('Subscribing', '', judges_string)
            judges_string = re.sub('SUBSCRIBING', '', judges_string)
            judges_string = re.sub('additional', '', judges_string)
            judges_string = re.sub('Additional', '', judges_string)
            judges_string = re.sub('ADDITIONAL', '', judges_string)
            judges_string = re.sub(' fees', '', judges_string)
            judges_string = re.sub(' Fees', '', judges_string)
            judges_string = re.sub(' FEES', '', judges_string)
            judges_string = re.sub(' IALS ', '', judges_string)
            judges_string = re.sub(' ials ', '', judges_string)
            judges_string = re.sub(' IALS,', '', judges_string)
            judges_string = re.sub(' ials,', '', judges_string)
            judges_string = re.sub('D-D', '', judges_string)
            judges_string = re.sub('d-d', '', judges_string)
            judges_string = re.sub('I-', '', judges_string)
            judges_string = re.sub('i-', '', judges_string)
            judges_string = re.sub('V-V', '', judges_string)
            judges_string = re.sub('v-v', '', judges_string)
            judges_string = re.sub('FOURTH', '', judges_string)
            judges_string = re.sub('fourth', '', judges_string)
            judges_string = re.sub('Fourth', '', judges_string)
            judges_string = re.sub('Designation', '', judges_string)
            judges_string = re.sub('designation', '', judges_string)
            judges_string = re.sub('DESIGNATION', '', judges_string)
            judges_string = re.sub('appellate', '', judges_string)
            judges_string = re.sub('Appellate', '', judges_string)
            judges_string = re.sub('APPELLATE', '', judges_string)
            judges_string = re.sub('opinon', '', judges_string)
            judges_string = re.sub('Opinon', '', judges_string)
            judges_string = re.sub('OPINON', '', judges_string)
            judges_string = re.sub('TEMPORARILY', '', judges_string)
            judges_string = re.sub('temporarily', '', judges_string)
            judges_string = re.sub('Temporarily', '', judges_string)
            judges_string = re.sub(' for ', '', judges_string)
            judges_string = re.sub(' For ', '', judges_string)
            judges_string = re.sub(' FOR ', '', judges_string)
            judges_string = re.sub(' For,', '', judges_string)
            judges_string = re.sub(' for,', '', judges_string)
            judges_string = re.sub(' FOR,', '', judges_string)
            judges_string = re.sub(',for ', '', judges_string)
            judges_string = re.sub(',For ', '', judges_string)
            judges_string = re.sub(',FOR ', '', judges_string)
            judges_string = re.sub(' will ', '', judges_string)
            judges_string = re.sub(' Will ', '', judges_string)
            judges_string = re.sub(' WILL ', '', judges_string)
            judges_string = re.sub(' Will,', '', judges_string)
            judges_string = re.sub(' will,', '', judges_string)
            judges_string = re.sub(' WILL,', '', judges_string)
            judges_string = re.sub(',will ', '', judges_string)
            judges_string = re.sub(',Will ', '', judges_string)
            judges_string = re.sub(',WILL ', '', judges_string)
            judges_string = re.sub(' adds ', '', judges_string)
            judges_string = re.sub(' Adds ', '', judges_string)
            judges_string = re.sub(' ADDS ', '', judges_string)
            judges_string = re.sub(' Adds,', '', judges_string)
            judges_string = re.sub(' adds,', '', judges_string)
            judges_string = re.sub(' ADDS,', '', judges_string)
            judges_string = re.sub(',adds ', '', judges_string)
            judges_string = re.sub(',Adds ', '', judges_string)
            judges_string = re.sub(',ADDS ', '', judges_string)
            judges_string = re.sub('settlements', '', judges_string)
            judges_string = re.sub('Settlements', '', judges_string)
            judges_string = re.sub('SETTLEMENTS', '', judges_string)
            judges_string = re.sub('notes', '', judges_string)
            judges_string = re.sub('Notes', '', judges_string)
            judges_string = re.sub('NOTES', '', judges_string)
            judges_string = re.sub('--', '', judges_string)
            judges_string = re.sub(' ity ', '', judges_string)
            judges_string = re.sub(' ITY ', '', judges_string)
            judges_string = re.sub(' Ity ', '', judges_string)
            judges_string = re.sub(' Ity,', '', judges_string)
            judges_string = re.sub(' ity,', '', judges_string)
            judges_string = re.sub(' ITY,', '', judges_string)
            judges_string = re.sub(',ity ', '', judges_string)
            judges_string = re.sub(',Ity ', '', judges_string)
            judges_string = re.sub(',ITY ', '', judges_string)
            judges_string = re.sub(' on ', '', judges_string)
            judges_string = re.sub(' ON ', '', judges_string)
            judges_string = re.sub(' On ', '', judges_string)
            judges_string = re.sub(' On,', '', judges_string)
            judges_string = re.sub(' on,', '', judges_string)
            judges_string = re.sub(' ON,', '', judges_string)
            judges_string = re.sub(',on ', '', judges_string)
            judges_string = re.sub(',On ', '', judges_string)
            judges_string = re.sub(',ON ', '', judges_string)
            judges_string = re.sub('settlement', '', judges_string)
            judges_string = re.sub('Settlement', '', judges_string)
            judges_string = re.sub('SETTLEMENT', '', judges_string)
            judges_string = re.sub('order', '', judges_string)
            judges_string = re.sub('Order', '', judges_string)
            judges_string = re.sub('ORDER', '', judges_string)
            judges_string = re.sub('adopt', '', judges_string)
            judges_string = re.sub('Adopt', '', judges_string)
            judges_string = re.sub('ADOPT', '', judges_string)
            judges_string = re.sub('THERABLEMCCLINTOCK', '', judges_string.upper())
            judges_string = re.sub(' ins ', '', judges_string)
            judges_string = re.sub(' INS ', '', judges_string)
            judges_string = re.sub(' Ins ', '', judges_string)
            judges_string = re.sub(' Ins,', '', judges_string)
            judges_string = re.sub(' ins,', '', judges_string)
            judges_string = re.sub(' INS,', '', judges_string)
            judges_string = re.sub(',ins ', '', judges_string)
            judges_string = re.sub(',Ins ', '', judges_string)
            judges_string = re.sub(',INS ', '', judges_string)
            judges_string = re.sub('docket', '', judges_string)
            judges_string = re.sub('Docket', '', judges_string)
            judges_string = re.sub('DOCKET', '', judges_string)
            judges_string = re.sub('retirement', '', judges_string)
            judges_string = re.sub('Retirement', '', judges_string)
            judges_string = re.sub('RETIREMENT', '', judges_string)
            judges_string = re.sub(' ard ', '', judges_string)
            judges_string = re.sub(' ARD ', '', judges_string)
            judges_string = re.sub(' Ard ', '', judges_string)
            judges_string = re.sub(' Ard,', '', judges_string)
            judges_string = re.sub(' ard,', '', judges_string)
            judges_string = re.sub(' ARD,', '', judges_string)
            judges_string = re.sub(',ard ', '', judges_string)
            judges_string = re.sub(',Ard ', '', judges_string)
            judges_string = re.sub(',ARD ', '', judges_string)
            judges_string = re.sub(' to ', '', judges_string)
            judges_string = re.sub(' TO ', '', judges_string)
            judges_string = re.sub(' To ', '', judges_string)
            judges_string = re.sub(' To,', '', judges_string)
            judges_string = re.sub(' to,', '', judges_string)
            judges_string = re.sub(' TO,', '', judges_string)
            judges_string = re.sub(',to ', '', judges_string)
            judges_string = re.sub(',To ', '', judges_string)
            judges_string = re.sub(',TO ', '', judges_string)
            judges_string = re.sub(' likes ', '', judges_string)
            judges_string = re.sub(' LIKES ', '', judges_string)
            judges_string = re.sub(' Likes ', '', judges_string)
            judges_string = re.sub(' Likes,', '', judges_string)
            judges_string = re.sub(' likes,', '', judges_string)
            judges_string = re.sub(' LIKES,', '', judges_string)
            judges_string = re.sub(',likes ', '', judges_string)
            judges_string = re.sub(',Likes ', '', judges_string)
            judges_string = re.sub(',LIKES ', '', judges_string)
            judges_string = re.sub('VI-XI', '', judges_string)
            judges_string = re.sub('vi-xi', '', judges_string)
            judges_string = re.sub('I-IV', '', judges_string)
            judges_string = re.sub('i-iv', '', judges_string)
            judges_string = re.sub('heard', '', judges_string)
            judges_string = re.sub('Heard', '', judges_string)
            judges_string = re.sub('HEARD', '', judges_string)
            judges_string = re.sub(' not ', '', judges_string)
            judges_string = re.sub(' NOT ', '', judges_string)
            judges_string = re.sub(' Not ', '', judges_string)
            judges_string = re.sub(' Not,', '', judges_string)
            judges_string = re.sub(' not,', '', judges_string)
            judges_string = re.sub(' NOT,', '', judges_string)
            judges_string = re.sub(',not ', '', judges_string)
            judges_string = re.sub(',Not ', '', judges_string)
            judges_string = re.sub(',NOT ', '', judges_string)
            judges_string = re.sub('chief', '', judges_string)
            judges_string = re.sub('Chief', '', judges_string)
            judges_string = re.sub('CHIEF', '', judges_string)
            judges_string = re.sub(' sp ', '', judges_string)
            judges_string = re.sub(' SP ', '', judges_string)
            judges_string = re.sub(' Sp ', '', judges_string)
            judges_string = re.sub(' Sp,', '', judges_string)
            judges_string = re.sub(' sp,', '', judges_string)
            judges_string = re.sub(' SP,', '', judges_string)
            judges_string = re.sub(',sp ', '', judges_string)
            judges_string = re.sub(',Sp ', '', judges_string)
            judges_string = re.sub(',SP ', '', judges_string)
            judges_string = re.sub('associate', '', judges_string)
            judges_string = re.sub('Associate', '', judges_string)
            judges_string = re.sub('ASSOCIATE', '', judges_string)
            judges_string = re.sub(' j ', '', judges_string)
            judges_string = re.sub(' J ', '', judges_string)
            judges_string = re.sub(' j,', '', judges_string)
            judges_string = re.sub(' J,', '', judges_string)
            judges_string = re.sub(',j ', '', judges_string)
            judges_string = re.sub(',J ', '', judges_string)
            judges_string = re.sub('bear', '', judges_string)
            judges_string = re.sub('Bear', '', judges_string)
            judges_string = re.sub('BEAR', '', judges_string)
            judges_string = re.sub('vacancy', '', judges_string)
            judges_string = re.sub('Vacancy', '', judges_string)
            judges_string = re.sub('VACANCY', '', judges_string)
            judges_string = re.sub('modification', '', judges_string)
            judges_string = re.sub('Modification', '', judges_string)
            judges_string = re.sub('MODIFICATION', '', judges_string)
            judges_string = re.sub('acceptance', '', judges_string)
            judges_string = re.sub('Acceptance', '', judges_string)
            judges_string = re.sub('ACCEPTANCE', '', judges_string)
            judges_string = re.sub('professional', '', judges_string)
            judges_string = re.sub('Professional', '', judges_string)
            judges_string = re.sub('PROFESSIONAL', '', judges_string)
            judges_string = re.sub('at-will', '', judges_string)
            judges_string = re.sub('AT-WILL', '', judges_string)
            judges_string = re.sub('At-Will', '', judges_string)                                                
            judges_string = re.sub('At-will', '', judges_string)                                                
            judges_string = re.sub(' the ', '', judges_string)
            judges_string = re.sub(' THE ', '', judges_string)
            judges_string = re.sub(' The ', '', judges_string)
            judges_string = re.sub(' The,', '', judges_string)
            judges_string = re.sub(' the,', '', judges_string)
            judges_string = re.sub(' THE,', '', judges_string)
            judges_string = re.sub(',the ', '', judges_string)
            judges_string = re.sub(',The ', '', judges_string)
            judges_string = re.sub(',THE ', '', judges_string)            
            judges_string = re.sub(' BEEN ', '', judges_string.upper())
            judges_string = re.sub(' BEEN,', '', judges_string.upper())
            judges_string = re.sub(',BEEN ', '', judges_string.upper())
            judges_string = re.sub('ACCORDINGLY', '', judges_string.upper())
            judges_string = re.sub('APPOINTMENT', '', judges_string.upper())
            judges_string = re.sub('AGREE', '', judges_string.upper())
            judges_string = re.sub(' MENT ', '', judges_string.upper())
            judges_string = re.sub(' MENT,', '', judges_string.upper())
            judges_string = re.sub(',MENT ', '', judges_string.upper())
            judges_string = re.sub(' BY ', '', judges_string.upper())
            judges_string = re.sub(' BY,', '', judges_string.upper())
            judges_string = re.sub(',BY ', '', judges_string.upper())
            judges_string = re.sub(' IS ', '', judges_string.upper())
            judges_string = re.sub(' IS,', '', judges_string.upper())
            judges_string = re.sub(',IS ', '', judges_string.upper())                       
            judges_string = re.sub('ATTACHED', '', judges_string.upper())
            judges_string = re.sub('ORDER', '', judges_string.upper())
            judges_string = re.sub('CONSTITUTIONALITY', '', judges_string.upper())
            if state != 'Georgia':
                judges_string = re.sub('grant|Grant|GRANT', '', judges_string)
            if state != 'Alabama':
                judges_string = re.sub(' See| see', '', judges_string)
            #print judges_string
            judges_line = False
            judges_part_string = first_sentence(judges_string)
            judges_holder = re.sub("\*|\d", "", judges_part_string)
            judges_holder = re.sub("Before:* ", "", judges_holder)
            judges_holder = re.sub(", (Circuit|Circuit) (J|j)udge[s]?\.?", "", judges_holder)
            judges_holder = re.sub(", (District|DISTRICT) (J|j)udge[s]?\.?", "", judges_holder)
            judges_holder = re.sub("Chief Judge", "", judges_holder)
            judges_holder = re.sub("Senior Judge", "", judges_holder)
            judges_holder = re.sub("Justice[s]", "", judges_holder)
            judges_holder = re.sub("Chief District Judge", "", judges_holder)
            judges_holder = re.sub("Associate Justice", "", judges_holder)
            judges_holder = re.sub("Administrative Justice", "", judges_holder)
            judges_holder = re.sub("Administrative Judge", "", judges_holder)
            judges_holder = re.sub("(P|p)ro (T|t)em", "", judges_holder)
            judges_holder = re.sub(", (Jr\.|JR\.|Jr|jr)", "", judges_holder)
            judges_holder = re.sub(", (Sr\.|SR\.)", "Sr.", judges_holder)
            judges_holder = re.sub(", III", "III", judges_holder)
            judges_holder = re.sub(", II", "II", judges_holder)
            judges_holder = re.sub(";", ",", judges_holder)
            judges_holder = re.sub(",[\s]*,", ",", judges_holder)
            judges_holder = re.sub(" and ", ", ", judges_holder)
            judges_holder = re.sub(" \. ", " ", judges_holder)
            judges_holder = re.sub("[\s]+", " ", judges_holder)
            judges_holder = re.sub("C\.J\.,|Supr\. J\.|J\.P\.T\.|Sp\.J\.|S\.J\.|P\.JJ\.|JJ\.,|JJ\.|D\.J\.,|P\.J\.,|C\.J\.|J\.,|J\.|C\. J\.", ",", judges_holder)
            judges_holder = re.sub("\xc3\xa1", "a", judges_holder)
            judges_holder = re.split(",", judges_holder)
            judges_holder = judges_holder + non_panel_list
            judges_holder = [word for word in judges_holder if word != ""]
            judges_holder = [word.strip() for word in judges_holder]
            judges_holder = [word.upper() for word in judges_holder]
            judges_holder = [word for word in judges_holder if len(word) > 2]
            judges_holder = list(set(judges_holder))

            # Apply functions to judge names to format the names of each justice uniformly
            if (len(judges_holder) == 1):
                judge1_ln = lastname(judges_holder[0])
                judge1_fn = firstname(judges_holder[0])
                judge1_mn = middlename(judges_holder[0])
                judge1_suf = namesuffix(judges_holder[0])
                judge1_full = judge1_ln + ", " + judge1_fn + " " + judge1_mn + " " + judge1_suf
                judge1_full = re.sub("[\s]+", " ", judge1_full)
                judge1_full = re.sub(", $", "", judge1_full)
                if len(judge1_ln) < 2:
                    judge1_ln = ""
                    judge1_vote = ""

            if (len(judges_holder) > 1):
                judge1_ln = lastname(judges_holder[0])
                judge1_fn = firstname(judges_holder[0])
                judge1_mn = middlename(judges_holder[0])
                judge1_suf = namesuffix(judges_holder[0])
                judge1_full = judge1_ln + ", " + judge1_fn + " " + judge1_mn + " " + judge1_suf
                judge1_full = re.sub("[\s]+", " ", judge1_full)
                judge1_full = re.sub(", $", "", judge1_full)
                if len(judge1_ln) < 2:
                    judge1_ln = ""
                    judge1_vote = ""

                #print judges_holder[0]
                judge2_ln = lastname(judges_holder[1])
                #print judge2_ln
                judge2_fn = firstname(judges_holder[1])
                judge2_mn = middlename(judges_holder[1])
                judge2_suf = namesuffix(judges_holder[1])
                judge2_full = judge2_ln + ", " + judge2_fn + " " + judge2_mn + " " + judge2_suf
                judge2_full = re.sub("[\s]+", " ", judge2_full)
                judge2_full = re.sub(", $", "", judge2_full)
                if len(judge2_ln) < 2:
                    judge2_ln = ""
                    judge2_vote = ""

            if (len(judges_holder) > 2):

                judge3_ln = lastname(judges_holder[2])
                judge3_fn = firstname(judges_holder[2])
                judge3_mn = middlename(judges_holder[2])
                judge3_suf = namesuffix(judges_holder[2])
                judge3_full = judge3_ln + ", " + judge3_fn + " " + judge3_mn + " " + judge3_suf
                judge3_full = re.sub("[\s]+", " ", judge3_full)
                judge3_full = re.sub(", $", "", judge3_full)
                if len(judge3_ln) < 2:
                    judge3_ln = ""
                    judge3_vote = ""

            if (len(judges_holder) > 3):

                judge4_ln = lastname(judges_holder[3])
                judge4_fn = firstname(judges_holder[3])
                judge4_mn = middlename(judges_holder[3])
                judge4_suf = namesuffix(judges_holder[3])
                judge4_full = judge4_ln + ", " + judge4_fn + " " + judge4_mn + " " + judge4_suf
                judge4_full = re.sub("[\s]+", " ", judge4_full)
                judge4_full = re.sub(", $", "", judge4_full)
                if len(judge4_ln) < 2:
                    judge4_ln = ""
                    judge4_vote = ""

            if (len(judges_holder) > 4):

                judge5_ln = lastname(judges_holder[4])
                judge5_fn = firstname(judges_holder[4])
                judge5_mn = middlename(judges_holder[4])
                judge5_suf = namesuffix(judges_holder[4])
                judge5_full = judge5_ln + ", " + judge5_fn + " " + judge5_mn + " " + judge5_suf
                judge5_full = re.sub("[\s]+", " ", judge5_full)
                judge5_full = re.sub(", $", "", judge5_full)
                if len(judge5_ln) < 2:
                    judge5_ln = ""
                    judge5_vote = ""

            if (len(judges_holder) > 5):
                judge6_ln = lastname(judges_holder[5])
                judge6_fn = firstname(judges_holder[5])
                judge6_mn = middlename(judges_holder[5])
                judge6_suf = namesuffix(judges_holder[5])
                judge6_full = judge6_ln + ", " + judge6_fn + " " + judge6_mn + " " + judge6_suf
                judge6_full = re.sub("[\s]+", " ", judge6_full)
                judge6_full = re.sub(", $", "", judge6_full)
                if len(judge6_ln) < 2:
                    judge6_ln = ""
                    judge6_vote = ""

            if (len(judges_holder) > 6):

                judge7_ln = lastname(judges_holder[6])
                judge7_fn = firstname(judges_holder[6])
                judge7_mn = middlename(judges_holder[6])
                judge7_suf = namesuffix(judges_holder[6])
                judge7_full = judge7_ln + ", " + judge7_fn + " " + judge7_mn + " " + judge7_suf
                judge7_full = re.sub("[\s]+", " ", judge7_full)
                judge7_full = re.sub(", $", "", judge7_full)
                if len(judge7_ln) < 2:
                    judge7_ln = ""
                    judge7_vote = ""

            if (len(judges_holder) > 7):

                judge8_ln = lastname(judges_holder[7])
                judge8_fn = firstname(judges_holder[7])
                judge8_mn = middlename(judges_holder[7])
                judge8_suf = namesuffix(judges_holder[7])
                judge8_full = judge8_ln + ", " + judge8_fn + " " + judge8_mn + " " + judge8_suf
                judge8_full = re.sub("[\s]+", " ", judge8_full)
                judge8_full = re.sub(", $", "", judge8_full)
                if len(judge8_ln) < 2:
                    judge8_ln = ""
                    judge8_vote = ""

            if (len(judges_holder) > 8):

                judge9_ln = lastname(judges_holder[8])
                judge9_fn = firstname(judges_holder[8])
                judge9_mn = middlename(judges_holder[8])
                judge9_suf = namesuffix(judges_holder[8])
                judge9_full = judge9_ln + ", " + judge9_fn + " " + judge9_mn + " " + judge9_suf
                judge9_full = re.sub("[\s]+", " ", judge9_full)
                judge9_full = re.sub(", $", "", judge9_full)
                if len(judge9_ln) < 2:
                    judge9_ln = ""
                    judge9_vote = ""

            if (len(judges_holder) > 9):

                judge10_ln = lastname(judges_holder[9])
                judge10_fn = firstname(judges_holder[9])
                judge10_mn = middlename(judges_holder[9])
                judge10_suf = namesuffix(judges_holder[9])
                judge10_full = judge10_ln + ", " + judge10_fn + " " + judge10_mn + " " + judge10_suf
                judge10_full = re.sub("[\s]+", " ", judge10_full)
                judge10_full = re.sub(", $", "", judge10_full)
                if len(judge10_ln) < 2:
                    judge10_ln = ""
                    judge10_vote = ""
            if (len(judges_holder) > 10):

                judge11_ln = lastname(judges_holder[10])
                judge11_fn = firstname(judges_holder[10])
                judge11_mn = middlename(judges_holder[10])
                judge11_suf = namesuffix(judges_holder[10])
                judge11_full = judge11_ln + ", " + judge11_fn + " " + judge11_mn + " " + judge11_suf
                judge11_full = re.sub("[\s]+", " ", judge11_full)
                judge11_full = re.sub(", $", "", judge11_full)
                if len(judge11_ln) < 2:
                    judge11_ln = ""
                    judge11_vote = ""

            if (len(judges_holder) > 11):
                check_case = 1

            if len(judge_np_list) == 0:
                judge_np1 = ""

            elif len(judge_np_list) == 1:
                judge_np1 = judge_np_list[0].strip()
                judge_np1 = re.sub(",", "", judge_np1)
                judge_np1 = re.sub("\\xc2\\xa0", "", judge_np1)
                if len(judge_np1) > 10:
                    judge_np1 = judge_np1.split(' ', 1)[0]

            elif len(judge_np_list) == 2:
                judge_np1 = judge_np_list[0].strip()
                judge_np1 = re.sub(",", "", judge_np1)
                judge_np2 = judge_np_list[1].strip()
                judge_np2 = re.sub(",", "", judge_np2)

            elif len(judge_np_list) > 2:
                judge_np1 = judge_np_list[0].strip()
                judge_np1 = re.sub(",", "", judge_np1)
                judge_np2 = judge_np_list[1].strip()
                judge_np2 = re.sub(",", "", judge_np2)
                judge_np3 = judge_np_list[2].strip()
                judge_np3 = re.sub(",", "", judge_np3)

            judge_np1 = re.sub("\.", "", judge_np1)
            judge_np2 = re.sub("\.", "", judge_np2)
            judge_np3 = re.sub("\.", "", judge_np3)
            judge_np1 = re.sub("\\\\n", "", judge_np1)
            judge_np2 = re.sub("\\\\n", "", judge_np2)
            judge_np3 = re.sub("\\\\n", "", judge_np3)
            judge_np1 = re.sub("\n", "", judge_np1)
            judge_np2 = re.sub("\n", "", judge_np2)
            judge_np3 = re.sub("\n", "", judge_np3)
            judge_np1 = re.sub(", Chief", "", judge_np1)
            judge_np2 = re.sub(", Chief", "", judge_np2)
            judge_np3 = re.sub(", Chief", "", judge_np3)
            judge_np1 = re.sub("Judges:", "", judge_np1)
            judge_np2 = re.sub("Judges:", "", judge_np2)
            judge_np3= re.sub("Judges:", "", judge_np3)
            judge_np1 = re.sub("All the  concur, except", "", judge_np1)
            judge_np2 = re.sub("All the  concur, except", "", judge_np2)
            judge_np3 = re.sub("All the  concur, except", "", judge_np3)
            judge_np1 = re.sub("\xc2\xa0:", "", judge_np1)
            judge_np2 = re.sub("\xc2\xa0:", "", judge_np2)
            judge_np3 = re.sub("\xc2\xa0:", "", judge_np3)
            judge_np1 = re.sub(", ", "", judge_np1)
            judge_np2 = re.sub(", ", "", judge_np2)
            judge_np3 = re.sub(", ", "", judge_np3)
            judge_np1 = judge_np1.strip()
            judge_np2 = judge_np2.strip()
            judge_np3 = judge_np3.strip()
            judge_np1 = Capitalize(judge_np1)
            judge_np2 = Capitalize(judge_np2)
            judge_np3 = Capitalize(judge_np3)

            judge1_ln = lastname(judge1_ln)
            judge2_ln = lastname(judge2_ln)
            judge3_ln = lastname(judge3_ln)
            judge4_ln = lastname(judge4_ln)
            judge5_ln = lastname(judge5_ln)
            judge6_ln = lastname(judge6_ln)
            judge7_ln = lastname(judge7_ln)
            judge8_ln = lastname(judge8_ln)
            judge9_ln = lastname(judge9_ln)
            #print judge1_ln, judge2_ln, judge3_ln, judge4_ln, judge5_ln, judge6_ln, judge7_ln, judge8_ln, judge9_ln

            # Remove justices that did not participate based on previously stored list of non-participating judges; remove votes from these justices as well
            if (judge1_ln == judge_np1 or judge1_ln == judge_np2 or judge1_ln == judge_np3 or judge1_ln == judge_np4):
                judge1_ln = ""
                judge1_vote = ""

            if (judge2_ln == judge_np1 or judge2_ln == judge_np2 or judge2_ln == judge_np3 or judge2_ln == judge_np4):
                judge2_ln = ""
                judge2_vote = ""

            if (judge3_ln == judge_np1 or judge3_ln == judge_np2 or judge3_ln == judge_np3 or judge3_ln == judge_np4):
                judge3_ln = ""
                judge3_vote = ""

            if (judge4_ln == judge_np1 or judge4_ln == judge_np2 or judge4_ln == judge_np3 or judge4_ln == judge_np4):
                judge4_ln = ""
                judge4_vote = ""

            if (judge5_ln == judge_np1 or judge5_ln == judge_np2 or judge5_ln == judge_np3 or judge5_ln == judge_np4):
                judge5_ln = ""
                judge5_vote = ""

            if (judge6_ln == judge_np1 or judge6_ln == judge_np2 or judge6_ln == judge_np3 or judge6_ln == judge_np4):
                judge6_ln = ""
                judge6_vote = ""

            if (judge7_ln == judge_np1 or judge7_ln == judge_np2 or judge7_ln == judge_np3 or judge7_ln == judge_np4):
                judge7_ln = ""
                judge7_vote = ""

            if (judge8_ln == judge_np1 or judge8_ln == judge_np2 or judge8_ln == judge_np3 or judge8_ln == judge_np4):
                judge8_ln = ""
                judge8_vote = ""

            if (judge9_ln == judge_np1 or judge9_ln == judge_np2 or judge9_ln == judge_np3 or judge9_ln == judge_np4):
                judge9_ln = ""
                judge9_vote = ""

            if (judge10_ln == judge_np1 or judge10_ln == judge_np2 or judge10_ln == judge_np3 or judge10_ln == judge_np4):
                judge10_ln = ""
                judge10_vote = ""

            if (judge11_ln == judge_np1 or judge11_ln == judge_np2 or judge11_ln == judge_np3 or judge11_ln == judge_np4 ):
                judge11_ln = ""
                judge11_vote = ""

            # Determine if a dissenting opinion is present
            if (re.search("dissent|DISSENT|dissents|Dissents|dissenting|Dissenting|DISSENTING", judges_string)):
                jud_dissent = 1

            # Determine if a decision was unanimous
            if (re.search("(U|u)nanimous|UNANIMOUS", judges_string)):
                unanimous = 1

        if(unanimous == 1 and re.search("concurred\.", txtline)): ###build out to parse judge list into single judges
            new_judges = txtline
            new_judges = re.sub("C\.\sJ\.,", "", new_judges)
            new_judges = re.sub("J\.,", "", new_judges)
            new_judges = re.sub(" and", "", new_judges)
            new_judges = re.sub("concurred\.", "", new_judges)
            new_judges = re.sub("\[\*+[0-9]+\]", "", new_judges)
            new_judges = re.sub("\s", "", new_judges)
            new_judges = new_judges.split(",")
            judges_holder = [judges_holder.pop(0)] + new_judges
            if (len(judges_holder) > 1):
                judge1_ln = lastname(judges_holder[0])
                judge2_ln = lastname(judges_holder[1])
            if (len(judges_holder) > 2):
                judge3_ln = lastname(judges_holder[2])
            if (len(judges_holder) > 3):
                judge4_ln = lastname(judges_holder[3])
            if (len(judges_holder) > 4):
                judge5_ln = lastname(judges_holder[4])
            if (len(judges_holder) > 5):
                judge6_ln = lastname(judges_holder[5])
            if (len(judges_holder) > 6):
                judge7_ln = lastname(judges_holder[6])
            if (len(judges_holder) > 7):
                judge8_ln = lastname(judges_holder[7])
            if (len(judges_holder) > 8):
                judge9_ln = lastname(judges_holder[8])

        # Store name of justice writing the majority opinion and format name
        if (re.match("^Opinion by:", txtline) and not trunc_text):
            opin_by_line = True
        if (opin_by_line and re.search("[\w]+", txtline)):
            opin_by_string = opin_by_string + txtline
        if (opin_by_line and re.match("^[\s]+$", txtline)):
            # blank line after opinion by line
            opin_by_string = re.sub("Opinion by:", "", opin_by_string)
            opin_by_string = re.sub("FOR THE COURT;", "", opin_by_string)
            opin_by_string = re.sub("\[\*+\d+\]", "", opin_by_string)
            opin_by_string = re.sub("\*[\d]*", "", opin_by_string)
            opin_by_string = re.sub(", Circuit Judge", "", opin_by_string)
            opin_by_string = re.sub("Chief Justice:", "", opin_by_string)
            opin_by_string = re.sub("\xc2", "", opin_by_string)
            opin_by_string = re.sub("'", "", opin_by_string)
            opin_by_string = re.sub("Sr\.|SR\.|Jr\.|JR\.", "", opin_by_string)
            opin_by_string = re.sub("\xa0", "", opin_by_string)
            opin_by_string = re.sub("C\.\sJ\.|C\.J\.|J\.J\.|J\.\sJ\.|J\.", "", opin_by_string)
            opin_by_string = re.sub("T\.Y\.|T\. Y\.", "", opin_by_string)
            opin_by_string = re.sub(" C\.", "", opin_by_string)
            opin_by_string = re.sub("\xc3\x81", "a", opin_by_string)
            opin_by_string = re.sub("III", "", opin_by_string)
            opin_by_string = re.sub("\xc3\x81", "a", opin_by_string)
            opin_by_string = re.sub(" ILL| ill", "ONEILL", opin_by_string)
            opin_by_string = re.sub("Justice|JUSTICE", "", opin_by_string)
            opin_by_string = re.sub('DENVIR STITH|DENVIRSTITH', 'Stith', opin_by_string)
            opin_by_string = re.sub("Judge|judge", "", opin_by_string)
            opin_by_string = string.strip(opin_by_string)
            opin_by_line = False
            author_ln = lastname(opin_by_string)
            author_fn = firstname(opin_by_string)
            author_mn = middlename(opin_by_string)
            author_suf = namesuffix(opin_by_string)
            author_full = author_ln + ", " + author_fn + " " + author_mn + " " + author_suf
            author_full = re.sub("[\s]+", " ", author_full)
            author_full = re.sub(", $", "", author_full)

            if(Capitalize(judge1_ln) != Capitalize(author_ln)):
                judge11_ln = judge10_ln
                judge10_ln = judge9_ln
                judge9_ln = judge8_ln
                judge8_ln = judge7_ln
                judge7_ln = judge6_ln
                judge6_ln = judge5_ln
                judge5_ln = judge4_ln
                judge4_ln = judge3_ln
                judge3_ln = judge2_ln
                judge2_ln = judge1_ln
                judge1_ln = author_ln
                judge11_vote = judge10_vote
                judge10_vote = judge9_vote
                judge9_vote = judge8_vote
                judge8_vote = judge7_vote
                judge7_vote = judge6_vote
                judge6_vote = judge5_vote
                judge5_vote = judge4_vote
                judge4_vote = judge3_vote
                judge3_vote = judge2_vote
                judge2_vote = judge1_vote
                judge1_vote = 1

        if (re.match("^Opinion", txtline) and not trunc_text and not blank_after_firstcite and not re.search("^Opinion No.",txtline)):
            opinion_line = True
            opinion_start = True
        if (re.match(re.escape("********** Print Completed **********"), txtline) or re.match("APPENDIX", txtline) or re.match("^CONCUR BY:", txtline) or re.match("^DISSENT BY:", txtline)):
            opinion_line = False

        if opinion_line:
            op_string = txtline
            op_holder = re.sub("^Opinion", " ", op_string)
            op_holder = re.sub("\xa0", " ", op_holder)
            op_holder = re.sub("\n|\r", " ", op_holder)
            op_holder = re.sub("\[\*+[0-9]+\]", " ", op_holder)
            op_holder = string.strip(op_holder)
            op_holder = re.split("\s+", op_holder)
            op_holder = [word for word in op_holder if word != ""]
            opinion_word_count += len(op_holder)
            judge1_vote = 1
            if (re.search("AMICUS|amicus|Amicus", op_string)):
                amicus = 1

        if (re.search("^Dissent", txtline)):
            dissent_line = True

        # If Lexis lists a line beginning with "Dissent:", store the justices listed after
        if (re.match("^Dissent by:|^DISSENT BY:", txtline) and not trunc_text):
            dissent_by_line = True
            dissent = 1
        if (dissent_by_line and re.search("[\w]+", txtline)):
            dissent_by_string = dissent_by_string + txtline

        # Format dissenting justice names
        if (dissent_by_line and re.match("^[\s]+$", txtline)):
            silent_dissent = True
            dissent_by_string = string.strip(dissent_by_string)
            dissent_by_string = re.sub("\n", "", dissent_by_string)
            dissent_by_string = re.sub("Dissent by:|DISSENT BY:", "", dissent_by_string)
            dissent_by_string = re.sub("\[.+\]", "", dissent_by_string)
            dissent_by_string = re.sub("[\s]*\(In[\s]*(P|p)art\)", "", dissent_by_string)
            dissent_by_string = re.sub("\*\d+", "", dissent_by_string)
            dissent_by_string = re.sub("dissenting:|dissenting", "", dissent_by_string)
            dissent_by_string = re.sub("Justice|JUSTICE", "", dissent_by_string)
            dissent_by_string = re.sub("\d+", "", dissent_by_string)
            dissent_by_string = re.sub("\xc2", "", dissent_by_string)
            dissent_by_string = re.sub("\xa0", "", dissent_by_string)
            dissent_by_string = re.sub("J;", "", dissent_by_string)
            dissent_by_string = re.sub("C\.J\.|C\. J\.|J\.J\.|JJ\.|J\. J\.|J\.", "", dissent_by_string)
            dissent_by_string = re.sub("[\(\[].*?[\)\]]", "", dissent_by_string)
            dissent_by_string = re.sub("'", "", dissent_by_string)
            dissent_by_string = re.sub("affirmed", "", dissent_by_string)
            dissent_by_string = re.sub("filed an opinion concurring in part and  in part", "", dissent_by_string)
            dissent_by_string = re.sub("concurring in part", "", dissent_by_string)
            dissent_by_string = re.sub("in which", "", dissent_by_string)
            dissent_by_string = re.sub("of which", "", dissent_by_string)
            dissent_by_string = re.sub("joined", "", dissent_by_string)
            dissent_by_string = re.sub("Part I", "", dissent_by_string)
            dissent_by_string = re.sub("Part", "", dissent_by_string)
            dissent_by_string = re.sub("in part", "", dissent_by_string)
            dissent_by_string = re.sub("and in", "", dissent_by_string)
            dissent_by_string = re.sub(" by", "", dissent_by_string)
            dissent_by_string = re.sub(" and", "", dissent_by_string)
            dissent_by_string = re.sub("as to", "", dissent_by_string)
            dissent_by_string = re.sub("filed a", "", dissent_by_string)
            dissent_by_string = re.sub("\.", ",", dissent_by_string)
            dissent_by_string = re.sub("[\s]*;", ";", dissent_by_string)
            dissent_holder = re.split(";|,", dissent_by_string)
            dissent_holder = filter(None, dissent_holder)
            dissent_holder = [name for name in dissent_holder if name.strip()]
            num_dissent = len(dissent_holder)
            dissent_by_line = False
            try:
                dissent1_ln = lastname(dissent_holder[0]).strip()
            except:
                pass
            dissent1_ln = dissent1_ln.strip()
            dissent1_ln = re.sub("\xa0", "", dissent1_ln)
            dissent1_ln = Capitalize(dissent1_ln)
            try:
                dissent1_fn = firstname(dissent_holder[0])
                dissent1_mn = middlename(dissent_holder[0])
                dissent1_suf = namesuffix(dissent_holder[0])
            except:
                pass
            if (len(dissent_holder) > 1):
                dissent2_ln = lastname(dissent_holder[1]).strip()
                dissent2_fn = firstname(dissent_holder[1])
                dissent2_mn = middlename(dissent_holder[1])
                dissent2_suf = namesuffix(dissent_holder[1])
            if (len(dissent_holder) > 2):
                dissent3_ln = lastname(dissent_holder[2]).strip()
                dissent3_fn = firstname(dissent_holder[2])
                dissent3_mn = middlename(dissent_holder[2])
                dissent3_suf = namesuffix(dissent_holder[2])
            if (len(dissent_holder) > 3):
                dissent4_ln = lastname(dissent_holder[3]).strip()
                dissent4_fn = firstname(dissent_holder[3])
                dissent4_mn = middlename(dissent_holder[3])
                dissent4_suf = namesuffix(dissent_holder[3])
            if (len(dissent_holder) > 4):
                dissent5_ln = lastname(dissent_holder[4]).strip()
                dissent5_fn = firstname(dissent_holder[4])
                dissent5_mn = middlename(dissent_holder[4])
                dissent5_suf = namesuffix(dissent_holder[4])
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
            dissent5_full = dissent4_ln + ", " + dissent5_fn + " " + dissent5_mn + " " + dissent5_suf
            dissent5_full = re.sub("[\s]+", " ", dissent5_full)
            dissent5_full = re.sub(", $", "", dissent5_full)

        # Store justices that concurred in dissenting opinions, format names, and store in a list
        if (silent_dissent == True and re.search("concurs\.$|concur\.$|concurred\.$", txtline)):
            other_dissent_string = txtline
            other_dissent_string = re.sub("\xa0", "", other_dissent_string)
            other_dissent_string = re.sub(" C\.J\.,| C\. J\.|JJ\.| J\.|C\.J\.", "", other_dissent_string)
            other_dissent_string = re.sub(" and", ",", other_dissent_string)
            other_dissent_string = re.sub("'", "", other_dissent_string)
            other_dissent_string = re.sub(" concurred\.", "", other_dissent_string)
            other_dissent_string = re.sub(" concur\.\n| concurs\.\n", "", other_dissent_string)
            other_dissent_string = re.sub("affirmed", "", other_dissent_string)
            other_dissent_string = re.sub("whom", "", other_dissent_string)
            other_dissent_string = other_dissent_string.strip()
            other_dissent_judges = other_dissent_string.split(",")
            other_dissent_judges[:] = [item for item in other_dissent_judges if item != '']
            if len(other_dissent_judges) > 0:
                silent_judge1 = other_dissent_judges[0].strip()
                dissent_by_string = dissent_by_string + ", " + Capitalize(lastname(silent_judge1))
                dissent_holder = dissent_holder + [silent_judge1]
                num_dissent += 1
            if len(other_dissent_judges) > 1:
                silent_judge2 = other_dissent_judges[1].strip()
                dissent_by_string = dissent_by_string + ", " + Capitalize(lastname(silent_judge2))
                num_dissent += 1
                dissent_holder = dissent_holder + [silent_judge2]
            if len(other_dissent_judges) > 2:
                silent_judge3 = other_dissent_judges[2].strip()
                dissent_by_string = dissent_by_string + ", " + Capitalize(lastname(silent_judge3))
                num_dissent += 1
                dissent_holder = dissent_holder + [silent_judge3]
            if len(other_dissent_judges) > 3:
                silent_judge4 = other_dissent_judges[3].strip()
                dissent_by_string = dissent_by_string + ", " + Capitalize(lastname(silent_judge4))
                num_dissent += 1
                dissent_holder = dissent_holder + [silent_judge4]

            if silent_judge4 == silent_judge1 or silent_judge4 == silent_judge2 or silent_judge4 == silent_judge3:
                silent_judge4 = ""

            if silent_judge3 == silent_judge1 or silent_judge3 == silent_judge2:
	            silent_judge3 = ""

            if silent_judge2 == silent_judge1:
			    silent_judge2 = ""

            silent_dissent = False

        # Search for concurring judge
        if (re.search("Concur", txtline)):
            concur_line = True

        # Store number of concurring justice and parse/format names of concurring justices (stored in string)
        if (re.match("^Concur by:", txtline) and not trunc_text):
            concur_by_line = True
            concur = concur + 1
        if (concur_by_line and re.search("[\w]+", txtline)):
            concur_by_string = concur_by_string + txtline
        if (concur_by_line and re.match("^[\s]+$", txtline)):
            concur_by_string = string.strip(concur_by_string)
            concur_by_string = re.sub("\n", " ", concur_by_string)
            concur_by_string = re.sub("Concur by: ", "", concur_by_string)
            concur_by_string = re.sub("\[.+\]", "", concur_by_string)
            concur_by_string = re.sub("\xc2", "", concur_by_string)
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

	# Format all justices listed as dissenting (both those that wrote an opinion and those that signed on)
    dissent_holder = [word for word in dissent_holder if word != ""]
    dissent_holder = dissent_holder + other_dissent_holder
    dissent_holder = [word.upper().strip() for word in dissent_holder]
    dissent_holder = list(set(dissent_holder))
    if len(dissent_holder)==0:
        dissent_author_1 = ""
        dissent_author_2 = ""
        dissent_author_3 = ""
        dissent_author_4 = ""
    if len(dissent_holder)==1:
        dissent_author_1 = dissent_holder[0].strip()
        dissent_author_1 = re.sub("\xa0*", "", dissent_author_1)
        dissent_author_1 = re.sub("\(In\s*part\)", "", dissent_author_1)
        dissent_author_1 = lastname(dissent_author_1)
        dissent_author_1 = Capitalize(dissent_author_1)
        dissent_author_2 = ""
        dissent_author_3 = ""
        dissent_author_4 = ""
    if len(dissent_holder)==2:
        dissent_author_1 = dissent_holder[0].strip()
        dissent_author_1 = dissent_author_1.strip()
        dissent_author_1 = re.sub("\xa0", "", dissent_author_1)
        dissent_author_1 = re.sub("\(In", "", dissent_author_1)
        dissent_author_1 = re.sub("J\.", "", dissent_author_1)
        dissent_author_1 = re.sub("J;", "", dissent_author_1)
        dissent_author_1 = Capitalize(lastname(dissent_author_1))
        dissent_author_2 = dissent_holder[1].strip()
        dissent_author_2 = re.sub("\xa0", "", dissent_author_2)
        dissent_author_2 = re.sub("\In\spart\)", "", dissent_author_2)
        dissent_author_2 = Capitalize(lastname(dissent_author_2))
        dissent_author_3 = ""
        dissent_author_4 = ""
    if len(dissent_holder)==3:
        dissent_author_1 = dissent_holder[0].strip()
        dissent_author_1 = dissent_author_1.strip()
        dissent_author_1 = re.sub("[\xa0]*", "", dissent_author_1)
        dissent_author_1 = re.sub("\In\spart\)", "", dissent_author_1)
        dissent_author_1 = Capitalize(lastname(dissent_author_1))
        dissent_author_2 = dissent_holder[1].strip()
        dissent_author_2 = re.sub("\xa0", "", dissent_author_2)
        dissent_author_2 = re.sub("\In\spart\)", "", dissent_author_2)
        dissent_author_2 = Capitalize(lastname(dissent_author_2))
        dissent_author_3 = dissent_holder[2].strip()
        dissent_author_3 = dissent_author_3.strip()
        dissent_author_3 = re.sub("[\xa0]*", "", dissent_author_3)
        dissent_author_3 = re.sub("\In\spart\)", "", dissent_author_3)
        dissent_author_3 = Capitalize(lastname(dissent_author_3))
        dissent_author_4 = ""
    if len(dissent_holder)==4:
        dissent_author_1 = dissent_holder[0].strip()
        dissent_author_1 = dissent_author_1.strip()
        dissent_author_1 = re.sub("[\xa0]*", "", dissent_author_1)
        dissent_author_1 = re.sub("\In\spart\)", "", dissent_author_1)
        dissent_author_1 = Capitalize(lastname(dissent_author_1))
        dissent_author_2 = dissent_holder[1].strip()
        dissent_author_2 = re.sub("\xa0", "", dissent_author_2)
        dissent_author_2 = re.sub("\In\spart\)", "", dissent_author_2)
        dissent_author_2 = Capitalize(lastname(dissent_author_2))
        dissent_author_3 = dissent_holder[2].strip()
        dissent_author_3 = dissent_author_3.strip()
        dissent_author_3 = re.sub("[\xa0]*", "", dissent_author_3)
        dissent_author_3 = re.sub("\In\spart\)", "", dissent_author_3)
        dissent_author_3 = Capitalize(lastname(dissent_author_3))
        dissent_author_4 = dissent_holder[3].strip()
        dissent_author_4 = dissent_author_4.strip()
        dissent_author_4 = re.sub("[\xa0]*", "", dissent_author_4)
        dissent_author_4 = re.sub("\In\spart\)", "", dissent_author_4)
        dissent_author_4 = Capitalize(lastname(dissent_author_4))
        dissent_author_5 = ""
    if len(dissent_holder)==5:
        dissent_author_1 = dissent_holder[0].strip()
        dissent_author_1 = dissent_author_1.strip()
        dissent_author_1 = re.sub("[\xa0]*", "", dissent_author_1)
        dissent_author_1 = re.sub("\In\spart\)", "", dissent_author_1)
        dissent_author_1 = Capitalize(lastname(dissent_author_1))
        dissent_author_2 = dissent_holder[1].strip()
        dissent_author_2 = re.sub("\xa0", "", dissent_author_2)
        dissent_author_2 = re.sub("\In\spart\)", "", dissent_author_2)
        dissent_author_2 = Capitalize(lastname(dissent_author_2))
        dissent_author_3 = dissent_holder[2].strip()
        dissent_author_3 = dissent_author_3.strip()
        dissent_author_3 = re.sub("[\xa0]*", "", dissent_author_3)
        dissent_author_3 = re.sub("\In\spart\)", "", dissent_author_3)
        dissent_author_3 = Capitalize(lastname(dissent_author_3))
        dissent_author_4 = dissent_holder[3].strip()
        dissent_author_4 = dissent_author_4.strip()
        dissent_author_4 = re.sub("[\xa0]*", "", dissent_author_4)
        dissent_author_4 = re.sub("\In\spart\)", "", dissent_author_4)
        dissent_author_4 = Capitalize(lastname(dissent_author_4))
        dissent_author_5 = dissent_holder[4].strip()
        dissent_author_5 = dissent_author_5.strip()
        dissent_author_5 = re.sub("[\xa0]*", "", dissent_author_5)
        dissent_author_5 = re.sub("\In\s*part\)", "", dissent_author_5)
        dissent_author_5 = Capitalize(lastname(dissent_author_5))
    if len(dissent_author_1) < 2:
        dissent_author_1 = ""
    if len(dissent_author_2) < 2:
        dissent_author_2 = ""
    if len(dissent_author_3) < 2:
        dissent_author_3 = ""
    if len(dissent_author_4) < 2:
        dissent_author_4 = ""
    if len(dissent_author_5) < 2:
        dissent_author_5 = ""
    if dissent_line and dissent==0:
        dissent=1
        num_dissent=1
    if concur_line and concur==0:
        concur=1
        num_concur=1

    #Assign vote values for each justice based on dissenting judges values
    if dissent_author_1 == judge2_ln or dissent_author_2 == judge2_ln or dissent_author_3 == judge2_ln or dissent_author_4 == judge2_ln or dissent_author_5 == judge2_ln and len(judge2_ln) > 0:
        judge2_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge2_ln and dissent_author_2 != judge2_ln and dissent_author_3 != judge2_ln and dissent_author_4 != judge2_ln and dissent_author_5 != judge2_ln and len(judge2_ln) > 0:
		judge2_vote = 1
    else:
        judge2_vote = ""
    if dissent_author_1 == judge3_ln or dissent_author_2 == judge3_ln or dissent_author_3 == judge3_ln or dissent_author_4 == judge3_ln or dissent_author_5 == judge3_ln and len(judge3_ln) > 0:
        judge3_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge3_ln and dissent_author_2 != judge3_ln and dissent_author_3 != judge3_ln and dissent_author_4 != judge3_ln and dissent_author_5 != judge3_ln and len(judge3_ln) > 0:
		judge3_vote = 1
    else:
        judge3_vote = ""
    if dissent_author_1 == judge4_ln or dissent_author_2 == judge4_ln or dissent_author_3 == judge4_ln or dissent_author_4 == judge4_ln or dissent_author_5 == judge4_ln and len(judge4_ln) > 0:
        judge4_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge4_ln and dissent_author_2 != judge4_ln and dissent_author_3 != judge4_ln and dissent_author_4 != judge4_ln and dissent_author_5 != judge4_ln and len(judge4_ln) > 0:
		judge4_vote = 1
    else:
        judge4_vote = ""
    if dissent_author_1 == judge5_ln or dissent_author_2 == judge5_ln or dissent_author_3 == judge5_ln or dissent_author_4 == judge5_ln or dissent_author_5 == judge5_ln and len(judge5_ln) > 0:
        judge5_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge5_ln and dissent_author_2 != judge5_ln and dissent_author_3 != judge5_ln and dissent_author_4 != judge5_ln and dissent_author_5 != judge5_ln and len(judge5_ln) > 0:
		judge5_vote = 1
    else:
        judge5_vote = ""
    if dissent_author_1 == judge6_ln or dissent_author_2 == judge6_ln or dissent_author_3 == judge6_ln or dissent_author_4 == judge6_ln or dissent_author_5 == judge6_ln and len(judge6_ln) > 0:
        judge6_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge6_ln and dissent_author_2 != judge6_ln and dissent_author_3 != judge6_ln and dissent_author_4 != judge6_ln and dissent_author_5 != judge6_ln and len(judge6_ln) > 0:
		judge6_vote = 1
    else:
        judge6_vote = ""
    if dissent_author_1 == judge7_ln or dissent_author_2 == judge7_ln or dissent_author_3 == judge7_ln or dissent_author_4 == judge7_ln or dissent_author_5 == judge7_ln and len(judge7_ln) > 0:
        judge7_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge7_ln and dissent_author_2 != judge7_ln and dissent_author_3 != judge7_ln and dissent_author_4 != judge7_ln and dissent_author_5 != judge7_ln and len(judge7_ln) > 0:
        judge7_vote = 1
    else:
        judge7_vote = ""
    if dissent_author_1 == judge8_ln or dissent_author_2 == judge8_ln or dissent_author_3 == judge8_ln or dissent_author_4 == judge8_ln or dissent_author_5 == judge8_ln and len(judge8_ln) > 0:
        judge8_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge8_ln and dissent_author_2 != judge8_ln and dissent_author_3 != judge8_ln and dissent_author_4 != judge8_ln and dissent_author_5 != judge8_ln and len(judge8_ln) > 0:
		judge8_vote = 1
    else:
        judge8_vote = ""
    if dissent_author_1 == judge9_ln or dissent_author_2 == judge9_ln or dissent_author_3 == judge9_ln or dissent_author_4 == judge9_ln or dissent_author_5 == judge9_ln and len(judge9_ln) > 0:
        judge9_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge9_ln and dissent_author_2 != judge9_ln and dissent_author_3 != judge9_ln and dissent_author_4 != judge9_ln and dissent_author_5 != judge9_ln and len(judge9_ln) > 0:
		judge9_vote = 1
    else:
        judge9_vote = ""
    if dissent_author_1 == judge10_ln or dissent_author_2 == judge10_ln or dissent_author_3 == judge10_ln or dissent_author_4 == judge10_ln or dissent_author_5 == judge10_ln and len(judge10_ln) > 0:
        judge10_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge10_ln and dissent_author_2 != judge10_ln and dissent_author_3 != judge10_ln and dissent_author_4 != judge10_ln and dissent_author_5 != judge10_ln and len(judge10_ln) > 0:
		judge10_vote = 1
    else:
        judge10_vote = ""
    if dissent_author_1 == judge11_ln or dissent_author_2 == judge11_ln or dissent_author_3 == judge11_ln or dissent_author_4 == judge11_ln or dissent_author_5 == judge11_ln and len(judge11_ln) > 0:
        judge11_vote = 0 #dissent_author_1
    elif dissent_author_1 != judge11_ln and dissent_author_2 != judge11_ln and dissent_author_3 != judge11_ln and dissent_author_4 != judge11_ln and dissent_author_5 != judge11_ln and len(judge11_ln) > 0:
		judge11_vote = 1
    else:
        judge11_vote = ""

    #Remove vote values from columns without judges
    if judge1_ln == "":
        judge1_vote = ""
    if judge2_ln == "":
        judge2_vote = ""
    if judge3_ln == "":
        judge3_vote = ""
    if judge4_ln == "":
        judge4_vote = ""
    if judge5_ln == "":
        judge5_vote = ""
    if judge6_ln == "":
        judge6_vote = ""
    if judge7_ln == "":
        judge7_vote = ""
    if judge8_ln == "":
        judge8_vote = ""
    if judge9_ln == "":
        judge9_vote = ""
    if judge10_ln == "":
        judge10_vote = ""
    if judge11_ln == "":
        judge11_vote = ""

    #Remove non-ASCII characters from Lexis citation values
    Lexis_cite = re.sub("\xa0", "", Lexis_cite)
    Lexis_cite = re.sub("\xc2", "", Lexis_cite)

    #Remove duplicate judges from judge last name columns
    if(judge9_ln == judge2_ln or judge9_ln == judge3_ln or judge9_ln == judge4_ln or judge9_ln == judge5_ln or judge9_ln == judge6_ln or judge9_ln == judge7_ln or judge9_ln == judge8_ln or judge9_ln == judge1_ln):
        judge9_ln = ""
        judge9_vote = ""
    if(judge8_ln == judge2_ln or judge8_ln == judge3_ln or judge8_ln == judge4_ln or judge8_ln == judge5_ln or judge8_ln == judge6_ln or judge8_ln == judge7_ln or judge8_ln == judge9_ln or judge8_ln == judge1_ln):
        judge8_ln = ""
        judge8_vote = ""
    if(judge7_ln == judge2_ln or judge7_ln == judge3_ln or judge7_ln == judge4_ln or judge7_ln == judge5_ln or judge7_ln == judge6_ln or judge7_ln == judge8_ln or judge7_ln == judge9_ln or judge7_ln == judge1_ln):
        judge7_ln = ""
        judge7_vote = ""
    if(judge6_ln == judge2_ln or judge6_ln == judge3_ln or judge6_ln == judge4_ln or judge6_ln == judge5_ln or judge6_ln == judge7_ln or judge6_ln == judge8_ln or judge6_ln == judge9_ln or judge6_ln == judge1_ln):
        judge6_ln = ""
        judge6_vote = ""
    if(judge5_ln == judge2_ln or judge5_ln == judge3_ln or judge5_ln == judge4_ln or judge5_ln == judge7_ln or judge5_ln == judge6_ln or judge5_ln == judge8_ln or judge5_ln == judge9_ln or judge5_ln == judge1_ln):
        judge5_ln = ""
        judge5_vote = ""
    if(judge4_ln == judge2_ln or judge4_ln == judge3_ln or judge4_ln == judge7_ln or judge4_ln == judge5_ln or judge4_ln == judge6_ln or judge4_ln == judge8_ln or judge4_ln == judge9_ln or judge4_ln == judge1_ln):
        judge4_ln = ""
        judge4_vote = ""
    if(judge3_ln == judge2_ln or judge3_ln == judge4_ln or judge3_ln == judge7_ln or judge3_ln == judge5_ln or judge3_ln == judge6_ln or judge3_ln == judge8_ln or judge3_ln == judge9_ln or judge3_ln == judge1_ln):
        judge3_ln = ""
        judge3_vote = ""
    if(judge2_ln == judge3_ln or judge2_ln == judge4_ln or judge2_ln == judge7_ln or judge2_ln == judge5_ln or judge2_ln == judge6_ln or judge2_ln == judge8_ln or judge2_ln == judge9_ln or judge2_ln == judge1_ln):
        judge2_ln = ""
        judge2_vote = ""
    if(judge10_ln == judge1_ln or judge10_ln == judge2_ln or judge10_ln == judge3_ln or judge10_ln == judge4_ln or judge10_ln == judge5_ln or judge10_ln == judge6_ln or judge10_ln == judge7_ln or judge10_ln == judge8_ln or judge10_ln == judge9_ln or judge10_ln == judge11_ln):
        judge10_ln = ""
        judge10_vote = ""
    if(judge11_ln == judge1_ln or judge11_ln == judge2_ln or judge11_ln == judge3_ln or judge11_ln == judge4_ln or judge11_ln == judge5_ln or judge11_ln == judge6_ln or judge11_ln == judge7_ln or judge11_ln == judge8_ln or judge11_ln == judge9_ln or judge11_ln == judge10_ln):
        judge11_ln = ""
        judge11_vote = ""

    #Fix vote values for cases where Lexis only reports judges that author a dissenting opinion in the dissent line
    if(silent_judge1 == judge1_ln and len(silent_judge1) > 0):
            judge1_vote = 0
    if(silent_judge1 == judge2_ln and len(silent_judge1) > 0):
        judge2_vote = 0
    if(silent_judge1 == judge3_ln and len(silent_judge1) > 0):
        judge3_vote = 0
    if(silent_judge1 == judge4_ln and len(silent_judge1) > 0):
        judge4_vote = 0
    if(silent_judge1 == judge5_ln and len(silent_judge1) > 0):
        judge5_vote = 0
    if(silent_judge1 == judge6_ln and len(silent_judge1) > 0):
        judge6_vote = 0
    if(silent_judge1 == judge7_ln and len(silent_judge1) > 0):
        judge7_vote = 0
    if(silent_judge1 == judge8_ln and len(silent_judge1) > 0):
        judge8_vote = 0
    if(silent_judge1 == judge9_ln and len(silent_judge1) > 0):
        judge9_vote = 0
    if(silent_judge2 == judge1_ln and len(silent_judge2) > 0):
        judge1_vote = 0
    if(silent_judge2 == judge2_ln and len(silent_judge2) > 0):
        judge2_vote = 0
    if(silent_judge2 == judge3_ln and len(silent_judge2) > 0):
        judge3_vote = 0
    if(silent_judge2 == judge4_ln and len(silent_judge2) > 0):
        judge4_vote = 0
    if(silent_judge2 == judge5_ln and len(silent_judge2) > 0):
        judge5_vote = 0
    if(silent_judge2 == judge6_ln and len(silent_judge2) > 0):
        judge6_vote = 0
    if(silent_judge2 == judge7_ln and len(silent_judge2) > 0):
        judge7_vote = 0
    if(silent_judge2 == judge8_ln and len(silent_judge2) > 0):
        judge8_vote = 0
    if(silent_judge2 == judge9_ln and len(silent_judge2) > 0):
        judge9_vote = 0
    if(silent_judge3 == judge1_ln and len(silent_judge3) > 0):
        judge1_vote = 0
    if(silent_judge3 == judge2_ln and len(silent_judge3) > 0):
        judge2_vote = 0
    if(silent_judge3 == judge3_ln and len(silent_judge3) > 0):
        judge3_vote = 0
    if(silent_judge3 == judge4_ln and len(silent_judge3) > 0):
        judge4_vote = 0
    if(silent_judge3 == judge5_ln and len(silent_judge3) > 0):
        judge5_vote = 0
    if(silent_judge3 == judge6_ln and len(silent_judge3) > 0):
        judge6_vote = 0
    if(silent_judge3 == judge7_ln and len(silent_judge3) > 0):
        judge7_vote = 0
    if(silent_judge3 == judge8_ln and len(silent_judge3) > 0):
        judge8_vote = 0
    if(silent_judge3 == judge9_ln and len(silent_judge3) > 0):
        judge9_vote = 0
    if(silent_judge4 == judge1_ln and len(silent_judge4) > 0):
        judge1_vote = 0
    if(silent_judge4 == judge2_ln and len(silent_judge4) > 0):
        judge2_vote = 0
    if(silent_judge4 == judge3_ln and len(silent_judge4) > 0):
        judge3_vote = 0
    if(silent_judge4 == judge4_ln and len(silent_judge4) > 0):
        judge4_vote = 0
    if(silent_judge4 == judge5_ln and len(silent_judge4) > 0):
        judge5_vote = 0
    if(silent_judge4 == judge6_ln and len(silent_judge4) > 0):
        judge6_vote = 0
    if(silent_judge4 == judge7_ln and len(silent_judge4) > 0):
        judge7_vote = 0
    if(silent_judge4 == judge8_ln and len(silent_judge4) > 0):
        judge8_vote = 0
    if(silent_judge4 == judge9_ln and len(silent_judge4) > 0):
        judge9_vote = 0
    if(silent_judge5 == judge1_ln and len(silent_judge5) > 0):
            judge1_vote = 0
    if(silent_judge5 == judge2_ln and len(silent_judge5) > 0):
        judge2_vote = 0
    if(silent_judge5 == judge3_ln and len(silent_judge5) > 0):
        judge3_vote = 0
    if(silent_judge5 == judge4_ln and len(silent_judge5) > 0):
        judge4_vote = 0
    if(silent_judge5 == judge5_ln and len(silent_judge5) > 0):
        judge5_vote = 0
    if(silent_judge5 == judge6_ln and len(silent_judge5) > 0):
        judge6_vote = 0
    if(silent_judge5 == judge7_ln and len(silent_judge5) > 0):
        judge7_vote = 0
    if(silent_judge5 == judge8_ln and len(silent_judge5) > 0):
        judge8_vote = 0
    if(silent_judge5 == judge9_ln and len(silent_judge5) > 0):
        judge9_vote = 0

    #Remove duplicate dissenting judge values from dissent columns
    if dissent_author_5 == dissent_author_1 or dissent_author_5 == dissent_author_2 or dissent_author_5 == dissent_author_3 or dissent_author_5 == dissent_author_4:
        dissent_author_5 = ""
    if dissent_author_4 == dissent_author_1 or dissent_author_4 == dissent_author_2 or dissent_author_4 == dissent_author_3:
        dissent_author_4 = ""
    if dissent_author_3 == dissent_author_1 or dissent_author_3 == dissent_author_2:
        dissent_author_3 = ""
    if dissent_author_2 == dissent_author_1:
        dissent_author_2 = ""

    # Remove instances of "Jr" and "Sr" so that the masterfile will match correctly
    if judge1_ln == "Jr|Sr":
        judge1_ln = ""
    if judge2_ln == "Jr|Sr":
        judge2_ln = ""
    if judge3_ln == "Jr|Sr":
        judge3_ln = ""
    if judge4_ln == "Jr|Sr":
        judge4_ln = ""
    if judge5_ln == "Jr|Sr":
        judge5_ln = ""
    if judge6_ln == "Jr|Sr":
        judge6_ln = ""
    if judge7_ln == "Jr|Sr":
        judge7_ln = ""
    if judge8_ln == "Jr|Sr":
        judge8_ln = ""
    if judge9_ln == "Jr|Sr":
        judge9_ln = ""
    if judge10_ln == "Jr|Sr":
        judge10_ln = ""
    if judge11_ln == "Jr|Sr":
        judge11_ln = ""

    #Move judges and votes to the left to fix blank cells
    if judge1_ln == "" or len(judge1_ln) < 2:
        judge1_ln = judge2_ln
        judge1_vote = judge2_vote
        judge2_ln = judge3_ln
        judge2_vote = judge3_vote
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge1_ln == "" or len(judge1_ln) < 2:
        judge1_ln = judge2_ln
        judge1_vote = judge2_vote
        judge2_ln = judge3_ln
        judge2_vote = judge3_vote
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge1_ln == "" or len(judge1_ln) < 2:
        judge1_ln = judge2_ln
        judge1_vote = judge2_vote
        judge2_ln = judge3_ln
        judge2_vote = judge3_vote
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge2_ln == "" or len(judge2_ln) < 2:
        judge2_ln = judge3_ln
        judge2_vote = judge3_vote
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge2_ln == "" or len(judge2_ln) < 2:
        judge2_ln = judge3_ln
        judge2_vote = judge3_vote
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge2_ln == "" or len(judge2_ln) < 2:
        judge2_ln = judge3_ln
        judge2_vote = judge3_vote
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge3_ln == "" or len(judge3_ln) < 2:
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge3_ln == "" or len(judge3_ln) < 2:
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge3_ln == "" or len(judge3_ln) < 2:
        judge3_ln = judge4_ln
        judge3_vote = judge4_vote
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge4_ln == "" or len(judge4_ln) < 2:
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge4_ln == "" or len(judge4_ln) < 2:
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge4_ln == "" or len(judge4_ln) < 2:
        judge4_ln = judge5_ln
        judge4_vote = judge5_vote
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge5_ln == "" or len(judge5_ln) < 2:
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge5_ln == "" or len(judge5_ln) < 2:
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge5_ln == "" or len(judge5_ln) < 2:
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge6_ln == "" or len(judge6_ln) < 2:
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge6_ln == "" or len(judge6_ln) < 2:
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge6_ln == "" or len(judge6_ln) < 2:
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge7_ln == "" or len(judge7_ln) < 2:
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge7_ln == "" or len(judge7_ln) < 2:
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge7_ln == "" or len(judge7_ln) < 2:
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge8_ln == "" or len(judge8_ln) < 2:
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge8_ln == "" or len(judge8_ln) < 2:
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge8_ln == "" or len(judge8_ln) < 2:
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge9_ln == "" or len(judge9_ln) < 2:
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge9_ln == "" or len(judge9_ln) < 2:
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge9_ln == "" or len(judge9_ln) < 2:
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge10_ln == "" or len(judge10_ln) < 2:
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge10_ln == "" or len(judge10_ln) < 2:
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    if judge10_ln == "" or len(judge10_ln) < 2:
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote

    #Remove duplicate judges from last judge name columns
    if(judge9_ln == judge2_ln or judge9_ln == judge3_ln or judge9_ln == judge4_ln or judge9_ln == judge5_ln or judge9_ln == judge6_ln or judge9_ln == judge7_ln or judge9_ln == judge8_ln or judge9_ln == judge1_ln):
        judge9_ln = ""
        judge9_vote = ""
    if(judge8_ln == judge2_ln or judge8_ln == judge3_ln or judge8_ln == judge4_ln or judge8_ln == judge5_ln or judge8_ln == judge6_ln or judge8_ln == judge7_ln or judge8_ln == judge9_ln or judge8_ln == judge1_ln):
        judge8_ln = ""
        judge8_vote = ""
    if(judge7_ln == judge2_ln or judge7_ln == judge3_ln or judge7_ln == judge4_ln or judge7_ln == judge5_ln or judge7_ln == judge6_ln or judge7_ln == judge8_ln or judge7_ln == judge9_ln or judge7_ln == judge1_ln):
        judge7_ln = ""
        judge7_vote = ""
    if(judge6_ln == judge2_ln or judge6_ln == judge3_ln or judge6_ln == judge4_ln or judge6_ln == judge5_ln or judge6_ln == judge7_ln or judge6_ln == judge8_ln or judge6_ln == judge9_ln or judge6_ln == judge1_ln):
        judge6_ln = ""
        judge6_vote = ""
    if(judge5_ln == judge2_ln or judge5_ln == judge3_ln or judge5_ln == judge4_ln or judge5_ln == judge7_ln or judge5_ln == judge6_ln or judge5_ln == judge8_ln or judge5_ln == judge9_ln or judge5_ln == judge1_ln):
        judge5_ln = ""
        judge5_vote = ""
    if(judge4_ln == judge2_ln or judge4_ln == judge3_ln or judge4_ln == judge7_ln or judge4_ln == judge5_ln or judge4_ln == judge6_ln or judge4_ln == judge8_ln or judge4_ln == judge9_ln or judge4_ln == judge1_ln):
        judge4_ln = ""
        judge4_vote = ""
    if(judge3_ln == judge2_ln or judge3_ln == judge4_ln or judge3_ln == judge7_ln or judge3_ln == judge5_ln or judge3_ln == judge6_ln or judge3_ln == judge8_ln or judge3_ln == judge9_ln or judge3_ln == judge1_ln):
        judge3_ln = ""
        judge3_vote = ""
    if(judge2_ln == judge3_ln or judge2_ln == judge4_ln or judge2_ln == judge7_ln or judge2_ln == judge5_ln or judge2_ln == judge6_ln or judge2_ln == judge8_ln or judge2_ln == judge9_ln or judge2_ln == judge1_ln):
        judge2_ln = ""
        judge2_vote = ""
    if(judge10_ln == judge1_ln or judge10_ln == judge2_ln or judge10_ln == judge3_ln or judge10_ln == judge4_ln or judge10_ln == judge5_ln or judge10_ln == judge6_ln or judge10_ln == judge7_ln or judge10_ln == judge8_ln or judge10_ln == judge9_ln or judge10_ln == judge11_ln):
        judge10_ln = ""
        judge10_vote = ""
    if(judge11_ln == judge1_ln or judge11_ln == judge2_ln or judge11_ln == judge3_ln or judge11_ln == judge4_ln or judge11_ln == judge5_ln or judge11_ln == judge6_ln or judge11_ln == judge7_ln or judge11_ln == judge8_ln or judge11_ln == judge9_ln or judge11_ln == judge10_ln):
        judge11_ln = ""
        judge11_vote = ""

    if (((state_abbr == "AL" or state_abbr == "FL" or panel == 0 or state_abbr == "NH") and state_abbr != "ME" and state_abbr != "MA" and (len(judge6_ln) > 2) or len(judge2_ln) < 2 or len(judge3_ln) < 2 or (len(judge5_ln) < 2 and panel == 0) and len(judge9_ln) < 2) or len(judge1_ln) < 2 and len(judge2_ln) < 2) or state_abbr != "AL" and len(judge7_ln) < 2:
        with open(mydir + "States_MasterFile_Import.csv", "rb") as f:
            reader = csv.reader(f)
            next(f)
            for row in reader:
                state = row[0]
                name = row[3]
                
                #start = datetime.datetime.strptime(row[4], '%m/%d/%Y').date()
                #end = datetime.datetime.strptime(row[5], '%m/%d/%Y').date() + datetime.timedelta(30)
                
                if len(row[4]) == 4 and row[0] != "MC":
                    row[4] = "1/1/" + row[4]
                if len(row[5]) == 4 and row[0] != "MC":
                    row[5] = "1/1/" + row[5]
                #print(len(row[4]), row[4])
                #if len(row[4]) == 8:
                #    start = datetime.datetime.strptime(row[4], '%m/%d/%Y').date()
                #    end = datetime.datetime.strptime(row[5], '%m/%d/%Y').date() + datetime.timedelta(30)
                if len(row[4]) != 4 and row[0] != "MC" and state_abbr != "AK" and (panel == 0 or ((state_abbr == "AL" or state_abbr == "FL" or state_abbr == "NH") and (len(judge6_ln) > 2) and len(judge9_ln) < 2 or len(judge3_ln) < 3) or len(judge5_ln) < 2) and state_abbr:
                    start = datetime.datetime.strptime(row[4], '%m/%d/%Y').date()
                    end = datetime.datetime.strptime(row[5], '%m/%d/%Y').date() + datetime.timedelta(30)
                if ((panel == 0 or ((state_abbr == "AL" or state_abbr == "FL" or state_abbr == "NH") and state_abbr != "AK" and ((len(judge6_ln) > 2) or len(judge2_ln) < 2 or len(judge3_ln) < 3 or len(judge5_ln) < 2) and len(judge9_ln) < 2)) and start <= date_format <= end):
                    between = True
                if ((state == state_abbr) and between and row[2] == "0" and state_abbr != "AK" and (panel == 0 or ((state_abbr == "AL" or state_abbr == "FL" or state_abbr == "NH") and (len(judge6_ln) > 2 or len(judge2_ln) < 2 or len(judge3_ln) < 3 or len(judge5_ln) < 2) and len(judge9_ln) < 2))):
                    if non_panel_judge_string == "":
                        non_panel_judge_string = non_panel_judge_string + Capitalize(lastname(row[3]))
                    else:
                        non_panel_judge_string = non_panel_judge_string + "," + Capitalize(lastname(row[3]))
                if state == state_abbr and row[2] == "0" and len(judge1_ln) < 2 and len(judge2_ln) < 2 and start <= date_format <= end:
                    #print row[3]
                    if non_panel_judge_string == "":
                        non_panel_judge_string = non_panel_judge_string + Capitalize(lastname(row[3]))
                    else:
                        non_panel_judge_string = non_panel_judge_string + "," + Capitalize(lastname(row[3]))
                    #print non_panel_judge_string
                if row[3] == judge1_ln:
                    judge1_code = row[1]
                    #print judge1_code
                between = False

            non_panel_list = non_panel_judge_string.split(",")
        master.close()
        judges_AL = non_panel_list

        if "Jr" in judges_AL:
            judges_AL.remove('Jr')
        #judges_AL = list(set(judges_AL))
        judges_AL.sort()
        #print judges_AL
        if judge1_ln in judges_AL:
            judges_AL.remove(judge1_ln)
        if judge2_ln in judges_AL:
            judges_AL.remove(judge2_ln)
        if judge3_ln in judges_AL:
            judges_AL.remove(judge3_ln)
        if judge4_ln in judges_AL:
            judges_AL.remove(judge4_ln)
        if judge5_ln in judges_AL:
            judges_AL.remove(judge5_ln)
        if judge6_ln in judges_AL:
            judges_AL.remove(judge6_ln)
        if judge7_ln in judges_AL:
            judges_AL.remove(judge7_ln)
        if judge8_ln in judges_AL:
            judges_AL.remove(judge8_ln)
        if judge_np1 in judges_AL:
            judges_AL.remove(judge_np1)
        if judge_np2 in judges_AL:
            judges_AL.remove(judge_np2)
        if judge_np3 in judges_AL:
            judges_AL.remove(judge_np3)
        if judge_np4 in judges_AL:
            judges_AL.remove(judge_np4)

        judges_AL = list(set(judges_AL))

        if len(judge1_ln) < 2 and len(judge2_ln) < 2 and len(judges_AL) > 0:
            judge1_ln = judges_AL[0]
            judge2_ln = judges_AL[1]
            judge1_vote = 1
            judge2_vote = 1

            if len(judge3_ln) < 2 and len(judges_AL) > 2:
                judge3_ln = judges_AL[2]
                judge3_vote = 1

            if len(judge4_ln) < 2 and len(judges_AL) > 3:
                judge4_ln = judges_AL[3]
                judge4_vote = 1

            if len(judge5_ln) < 2 and len(judges_AL) > 4:
                judge5_ln = judges_AL[4]
                judge5_vote = 1

            if len(judge6_ln) < 2 and len(judges_AL) > 5:
                judge6_ln = judges_AL[5]
                judge6_vote = 1

            if len(judge7_ln) < 2 and len(judges_AL) > 6:
                judge7_ln = judges_AL[6]
                judge7_vote = 1
                #print judge7_ln

            if len(judge8_ln) < 2 and len(judges_AL) > 7:
                judge8_ln = judges_AL[7]
                judge8_vote = 1

            if len(judge9_ln) < 2 and len(judges_AL) > 8:
                judge9_ln = judges_AL[8]
                judge9_vote = 1

        if len(judge2_ln) < 2 and len(judges_AL) > 0:
            judge2_ln = judges_AL[0]
            judge2_vote = 1
            if len(judge3_ln) < 2 and len(judges_AL) > 1:
                judge3_ln = judges_AL[1]
                judge3_vote = 1

            if len(judge4_ln) < 2 and len(judges_AL) > 2:
                judge4_ln = judges_AL[2]
                judge4_vote = 1

            if len(judge5_ln) < 2 and len(judges_AL) > 3:
                judge5_ln = judges_AL[3]
                judge5_vote = 1

            if len(judge6_ln) < 2 and len(judges_AL) > 4:
                judge6_ln = judges_AL[4]
                judge6_vote = 1

            if len(judge7_ln) < 2 and len(judges_AL) > 5:
                judge7_ln = judges_AL[5]
                judge7_vote = 1

            if len(judge8_ln) < 2 and len(judges_AL) > 6:
                judge8_ln = judges_AL[6]
                judge8_vote = 1

            if len(judge9_ln) < 2 and len(judges_AL) > 7:
                judge9_ln = judges_AL[7]
                judge9_vote = 1


        if len(judge3_ln) < 2 and len(judges_AL) > 0:
            judge3_ln = judges_AL[0]
            judge3_vote = 1

            if len(judge4_ln) < 2 and panel == 0 and len(judges_AL) > 1:
                judge4_ln = judges_AL[1]
                judge4_vote = 1

            if len(judge5_ln) < 2 and panel == 0 and len(judges_AL) > 2:
                judge5_ln = judges_AL[2]
                judge5_vote = 1

            if len(judge6_ln) < 2 and panel == 0 and len(judges_AL) > 3:
                judge6_ln = judges_AL[3]
                judge6_vote = 1

            if len(judge7_ln) < 2 and panel == 0 and len(judges_AL) > 4:
                judge7_ln = judges_AL[4]
                judge7_vote = 1

            if len(judge8_ln) < 2 and panel == 0 and len(judges_AL) > 5:
                judge8_ln = judges_AL[5]
                judge8_vote = 1

            if len(judge9_ln) < 2 and panel == 0 and len(judges_AL) > 6:
                judge9_ln = judges_AL[6]
                judge9_vote = 1

        if len(judge4_ln) < 2 and len(judges_AL) > 0 and panel == 0:
            judge4_ln = judges_AL[0]
            judge4_vote = 1

            if len(judge5_ln) < 2 and panel == 0 and len(judges_AL) > 1:
                judge5_ln = judges_AL[1]
                judge5_vote = 1

            if len(judge6_ln) < 2 and panel == 0 and len(judges_AL) > 2:
                judge6_ln = judges_AL[2]
                judge6_vote = 1

            if len(judge7_ln) < 2 and panel == 0 and len(judges_AL) > 3:
                judge7_ln = judges_AL[3]
                judge7_vote = 1

            if len(judge8_ln) < 2 and panel == 0 and len(judges_AL) > 4:
                judge8_ln = judges_AL[4]
                judge8_vote = 1

            if len(judge9_ln) < 2 and panel == 0 and len(judges_AL) > 5:
                judge9_ln = judges_AL[5]
                judge9_vote = 1

        if len(judge5_ln) < 2 and len(judges_AL) > 0 and panel == 0:
            judge5_ln = judges_AL[0]
            judge5_vote = 1

            if len(judge6_ln) < 2 and panel == 0 and len(judges_AL) > 1:
                judge6_ln = judges_AL[1]
                judge6_vote = 1

            if len(judge7_ln) < 2 and panel == 0 and len(judges_AL) > 2:
                judge7_ln = judges_AL[2]
                judge7_vote = 1

            if len(judge8_ln) < 2 and panel == 0 and len(judges_AL) > 3:
                judge8_ln = judges_AL[3]
                judge8_vote = 1

            if len(judge9_ln) < 2 and panel == 0 and len(judges_AL) > 4:
                judge9_ln = judges_AL[4]
                judge9_vote = 1

        if len(judge6_ln) < 2 and len(judges_AL) > 0 and panel == 0:
            judge6_ln = judges_AL[0]
            judge6_vote = 1
            if len(judge7_ln) < 2 and panel == 0 and len(judges_AL) > 1:
                judge7_ln = judges_AL[1]
                judge7_vote = 1

            if len(judge8_ln) < 2 and panel == 0 and len(judges_AL) > 2:
                judge8_ln = judges_AL[2]
                judge8_vote = 1

            if len(judge9_ln) < 2 and panel == 0 and len(judges_AL) > 3:
                judge9_ln = judges_AL[3]
                judge9_vote = 1

        if len(judge7_ln) < 2 and len(judges_AL) > 0 and panel == 0:
            judge7_ln = judges_AL[0]
            judge7_vote = 1

            if len(judge8_ln) < 2 and panel == 0 and len(judges_AL) > 1:
                judge8_ln = judges_AL[1]
                judge8_vote = 1

            if len(judge9_ln) < 2 and panel == 0 and len(judges_AL) > 2:
                judge9_ln = judges_AL[2]
                judge9_vote = 1

        if len(judge8_ln) < 2 and len(judges_AL) > 0 and panel == 0:
            judge8_ln = judges_AL[0]
            judge8_vote = 1

            if len(judge9_ln) < 2 and panel == 0 and len(judges_AL) > 1:
                judge9_ln = judges_AL[1]
                judge9_vote = 1

        if len(judge9_ln) < 2 and len(judges_AL) > 0 and panel == 0:
            judge9_ln = judges_AL[0]
            judge9_vote = 1

        if len(judge2_ln) < 2 and len(judge1_ln) > 2 and len(judges_AL) > 0 and state_abbr != "NH" and state_abbr != "NC" and state_abbr != "PA" and state_abbr != "RI" and state_abbr != "WV" and state_abbr != "WI" and state_abbr != "WY" and state_abbr != "AR" and state_abbr != "CO" and state_abbr != "GA" and state_abbr != "HI" and state_abbr != "MS" and state_abbr != "MO" and state_abbr != "MN":
            judge2_ln = judges_AL[0]
            judge3_ln = judges_AL[1]
            judge4_ln = judges_AL[2]
            judge5_ln = judges_AL[3]
            judge6_ln = judges_AL[4]
            judge7_ln = judges_AL[5]
            judge2_vote = 1
            judge3_vote = 1
            judge4_vote = 1
            judge5_vote = 1
            judge6_vote = 1
            judge7_vote = 1

        if len(judge2_ln) < 2 and len(judge1_ln) > 2 and len(judges_AL) > 0 and state_abbr != "NH" and state_abbr != "WV":
            judge2_ln = judges_AL[0]
            judge3_ln = judges_AL[1]
            judge4_ln = judges_AL[2]
            judge5_ln = judges_AL[3]
            judge2_vote = 1
            judge3_vote = 1
            judge4_vote = 1
            judge5_vote = 1

        if len(judge3_ln) < 2 and len(judge1_ln) > 2 and len(judge2_ln) > 2 and len(judges_AL) > 0 and state_abbr != "NH" and state_abbr != "NJ" and state_abbr != "NY" and state_abbr != "WV" and state_abbr != "AR" and state_abbr != "CO" and state_abbr != "GA" and state_abbr != "HI" and state_abbr != "MS" and state_abbr != "MO":
            judge3_ln = judges_AL[1]
            judge4_ln = judges_AL[2]
            judge5_ln = judges_AL[3]
            judge6_ln = judges_AL[4]
            judge3_vote = 1
            judge4_vote = 1
            judge5_vote = 1
            judge6_vote = 1

        else:
            if len(judges_AL) >= 1 and len(judge6_ln) < 2 and state_abbr != "NH":
                judge6_ln = judges_AL[0]
                judge6_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge7_ln) < 2 and len(judge6_ln) > 2 and state_abbr != "NH":
                judge7_ln = judges_AL[0]
                judge7_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge8_ln) < 2 and len(judge7_ln) > 2 and state_abbr != "NH":
                judge8_ln = judges_AL[0]
                judge8_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge9_ln) < 2 and len(judge8_ln) > 2 and state_abbr != "NH":
                judge9_ln = judges_AL[0]
                judge9_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge6_ln) < 2 and state_abbr != "NH":
                judge6_ln = judges_AL[0]
                judge6_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge7_ln) < 2 and len(judge6_ln) > 2 and state_abbr != "NH":
                judge7_ln = judges_AL[0]
                judge7_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge8_ln) < 2 and len(judge7_ln) > 2 and state_abbr != "NH":
                judge8_ln = judges_AL[0]
                judge8_vote = 1
                del judges_AL[0]
            if len(judges_AL) >= 1 and len(judge9_ln) < 2 and len(judge8_ln) > 2 and state_abbr != "NH":
                judge9_ln = judges_AL[0]
                judge9_vote = 1
                del judges_AL[0]

    #Move over dissenting judges to remove blank cells
    if(dissent_author_1 == ""):
        dissent_author_1 = dissent_author_2
        dissent_author_2 = dissent_author_3
        dissent_author_3 = dissent_author_4
        dissent_author_4 = dissent_author_5

    if(dissent_author_2 == ""):
        dissent_author_2 = dissent_author_3
        dissent_author_3 = dissent_author_4
        dissent_author_4 = dissent_author_5

    if(dissent_author_3 == ""):
        dissent_author_3 = dissent_author_4
        dissent_author_4 = dissent_author_5

    if(dissent_author_4 == ""):
        dissent_author_4 = dissent_author_5

    #Remove remaining duplicate dissenting authors
    if dissent_author_5 == dissent_author_1 or dissent_author_5 == dissent_author_2 or dissent_author_5 == dissent_author_3 or dissent_author_5 == dissent_author_4:
        dissent_author_5 = ""
    if dissent_author_4 == dissent_author_1 or dissent_author_4 == dissent_author_2 or dissent_author_4 == dissent_author_3:
        dissent_author_4 = ""
    if dissent_author_3 == dissent_author_1 or dissent_author_3 == dissent_author_2:
        dissent_author_3 = ""
    if dissent_author_2 == dissent_author_1:
        dissent_author_2 = ""

    #Correct dissent_no
    if dissent_author_1 != "":
        num_dissent = 1
    if dissent_author_2 != "":
        num_dissent = 2
    if dissent_author_3 != "":
        num_dissent = 3
    if dissent_author_4 != "":
        num_dissent = 4
    if dissent_author_5 != "":
        num_dissent = 5
    if len(dissent_author_1) < 2:
        num_dissent = 0

    # Pull in judge codes from state master file by matching state abbrevation, justice name, and time in office
    if judge1_code == "":
        with open(mydir + "States_MasterFile_Import.csv", "rb") as f:
            reader = csv.reader(f)
            next(f)
            for row in reader:
                state = row[0]
                name = row[3]
                if len(row[4]) == 4 and row[0] != "MC":
                    row[4] = "1/1/" + row[4]
                if len(row[5]) == 4 and row[0] != "MC":
                    row[5] = "1/1/" + row[5]
                if len(row[4]) != 4 and row[0] != "MC":
                    start = datetime.datetime.strptime(row[4], '%m/%d/%Y').date()
                    end = datetime.datetime.strptime(row[5], '%m/%d/%Y').date()

                #Format justice last names from each file to ensure accurate matching
                if (Capitalize(lastname(row[7])) == Capitalize(judge1_ln) or Capitalize(lastname(row[3])) == Capitalize(judge1_ln)) and judge1_code == "" and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge1_ln) > 1 and start <= date_format <= (end + one_month):
                    judge1_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge2_ln) or Capitalize(lastname(row[3])) == Capitalize(judge2_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge2_ln) > 1 and start <= date_format <= (end + one_month):
                    judge2_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge3_ln) or Capitalize(lastname(row[3])) == Capitalize(judge3_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge3_ln) > 1 and start <= date_format <= (end + one_month):
                    judge3_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge4_ln) or Capitalize(lastname(row[3])) == Capitalize(judge4_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge4_ln) > 1 and start <= date_format <= (end + one_month):
                    judge4_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge5_ln) or Capitalize(lastname(row[3])) == Capitalize(judge5_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge5_ln) > 1 and start <= date_format <= (end + one_month):
                    judge5_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge6_ln) or Capitalize(lastname(row[3])) == Capitalize(judge6_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge6_ln) > 1 and start <= date_format <= (end + one_month):
                    judge6_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge7_ln) or Capitalize(lastname(row[3])) == Capitalize(judge7_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge7_ln) > 1 and start <= date_format <= (end + one_month):
                    judge7_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge8_ln) or Capitalize(lastname(row[3])) == Capitalize(judge8_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge8_ln) > 1 and start <= date_format <= (end + one_month):
                    judge8_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge9_ln) or Capitalize(lastname(row[3])) == Capitalize(judge9_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge9_ln) > 1 and start <= date_format <= (end + one_month):
                    judge9_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge10_ln) or Capitalize(lastname(row[3])) == Capitalize(judge10_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge10_ln) > 1 and start <= date_format <= (end + one_month):
                    judge10_code = row[1]
                if (Capitalize(lastname(row[7])) == Capitalize(judge11_ln) or Capitalize(lastname(row[3])) == Capitalize(judge11_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge11_ln) > 1 and start <= date_format <= (end + one_month):
                    judge11_code = row[1]

    # Store "Did not match" if a justice did not match to a justice code
    if judge1_code == "" and len(judge1_ln) > 2:
        judge1_code = "Did not match"
    if judge2_code == "" and len(judge2_ln) > 2:
        judge2_code = "Did not match"
    if judge3_code == "" and len(judge3_ln) > 2:
        judge3_code = "Did not match"
    if judge4_code == "" and len(judge4_ln) > 2:
        judge4_code = "Did not match"
    if judge5_code == "" and len(judge5_ln) > 2:
        judge5_code = "Did not match"
    if judge6_code == "" and len(judge6_ln) > 2:
        judge6_code = "Did not match"
    if judge7_code == "" and len(judge7_ln) > 2:
        judge7_code = "Did not match"
    if judge8_code == "" and len(judge8_ln) > 2:
        judge8_code = "Did not match"
    if judge9_code == "" and len(judge9_ln) > 2:
        judge9_code = "Did not match"
    if judge10_code == "" and len(judge10_ln) > 2:
        judge10_code = "Did not match"
    if judge11_code == "" and len(judge11_ln) > 2:
        judge11_code = "Did not match"
    #print judge1_ln, judge2_ln, judge3_ln, judge4_ln, judge5_ln, judge6_ln, judge7_ln

    if (judge1_ln == judge_np1 or judge1_ln == judge_np2 or judge1_ln == judge_np3 or judge1_ln == judge_np4):
        judge1_ln = ""
        judge1_vote = ""
        judge1_code = ""

    if (judge2_ln == judge_np1 or judge2_ln == judge_np2 or judge2_ln == judge_np3 or judge2_ln == judge_np4):
        judge2_ln = ""
        judge2_vote = ""
        judge2_code = ""

    if (judge3_ln == judge_np1 or judge3_ln == judge_np2 or judge3_ln == judge_np3 or judge3_ln == judge_np4):
        judge3_ln = ""
        judge3_vote = ""
        judge3_code = ""

    if (judge4_ln == judge_np1 or judge4_ln == judge_np2 or judge4_ln == judge_np3 or judge4_ln == judge_np4):
        judge4_ln = ""
        judge4_vote = ""
        judge4_code = ""

    if (judge5_ln == judge_np1 or judge5_ln == judge_np2 or judge5_ln == judge_np3 or judge5_ln == judge_np4):
        judge5_ln = ""
        judge5_vote = ""
        judge5_code = ""

    if (judge6_ln == judge_np1 or judge6_ln == judge_np2 or judge6_ln == judge_np3 or judge6_ln == judge_np4):
        judge6_ln = ""
        judge6_vote = ""
        judge6_code = ""

    if (judge7_ln == judge_np1 or judge7_ln == judge_np2 or judge7_ln == judge_np3 or judge7_ln == judge_np4):
        judge7_ln = ""
        judge7_vote = ""
        judge7_code = ""

    if (judge8_ln == judge_np1 or judge8_ln == judge_np2 or judge8_ln == judge_np3 or judge8_ln == judge_np4):
        judge8_ln = ""
        judge8_vote = ""
        judge8_code = ""

    if (judge9_ln == judge_np1 or judge9_ln == judge_np2 or judge9_ln == judge_np3 or judge9_ln == judge_np4):
        judge9_ln = ""
        judge9_vote = ""
        judge9_code = ""

    if (judge10_ln == judge_np1 or judge10_ln == judge_np2 or judge10_ln == judge_np3 or judge10_ln == judge_np4):
        judge10_ln = ""
        judge10_vote = ""
        judge10_code = ""

    if (judge11_ln == judge_np1 or judge11_ln == judge_np2 or judge11_ln == judge_np3 or judge11_ln == judge_np4 ):
        judge11_ln = ""
        judge11_vote = ""
        judge11_code = ""


    if judge5_ln == judge2_ln or judge5_ln == judge1_ln or judge5_ln == judge3_ln or judge5_ln == judge4_ln:
        judge5_ln = ""
        judge5_vote = ""
        judge5_code = ""

    if judge6_ln == judge2_ln or judge6_ln == judge1_ln or judge6_ln == judge3_ln or judge6_ln == judge4_ln or judge6_ln == judge5_ln:
        judge6_ln = ""
        judge6_vote = ""
        judge6_code = ""

    if len(judge10_ln) < 2:
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote
        judge10_code = judge11_code
        judge11_ln = ""
        judge11_vote = ""
        judge11_code = ""

    if len(judge7_ln) < 2:
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge7_code = judge8_code
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge8_code = judge9_code
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge9_code = judge10_code
        judge10_ln = judge11_ln
        judge10_vote = judge11_vote
        judge10_code = judge11_code

    #Correct participating judges string
    part_judges = judge1_ln + ", " + judge2_ln + ", " + judge3_ln + ", " + judge4_ln + ", " + judge5_ln + ", " + judge6_ln + ", " + judge7_ln + ", " + judge8_ln + ", " + judge9_ln + ", " + judge10_ln + ", " + judge11_ln
    part_judges = re.sub(' ,', '', part_judges)
    part_judges = part_judges.rstrip(', ').upper()
    #print(part_judges)

    judge1_ln = judge1_ln.upper()
    judge2_ln = judge2_ln.upper()
    judge3_ln = judge3_ln.upper()
    judge4_ln = judge4_ln.upper()
    judge5_ln = judge5_ln.upper()
    judge6_ln = judge6_ln.upper()
    judge7_ln = judge7_ln.upper()
    judge8_ln = judge8_ln.upper()
    judge9_ln = judge9_ln.upper()
    judge10_ln = judge10_ln.upper()
    judge11_ln = judge11_ln.upper()

    if judge5_ln == judge2_ln or judge5_ln == judge1_ln or judge5_ln == judge3_ln or judge5_ln == judge4_ln:
        judge5_ln = ""
        judge5_vote = ""
        judge5_code = ""

    if judge6_ln == judge2_ln or judge6_ln == judge1_ln or judge6_ln == judge3_ln or judge6_ln == judge4_ln or judge6_ln == judge5_ln:
        judge6_ln = ""
        judge6_vote = ""
        judge6_code = ""

    if judge2_ln == judge6_ln:
        judge6_ln = ""
        judge6_vote = ""
        judge6_code = ""

    if len(judge4_ln) < 2:
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge4_ln) < 2:
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge5_ln) < 2:
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge1_ln) < 2:
        judge1_ln = judge2_ln
        judge2_ln = judge3_ln
        judge3_ln = judge4_ln
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge1_vote = judge2_vote
        judge2_vote = judge3_vote
        judge3_vote = judge4_vote
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge1_code = judge2_code
        judge2_code = judge3_code
        judge3_code = judge4_code
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge3_ln) < 2:
        judge3_ln = judge4_ln
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge3_vote = judge4_vote
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge3_code = judge4_code
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge5_ln) < 2:
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if judge9_ln == judge8_ln or judge9_ln == judge7_ln  or judge9_ln == judge6_ln or judge9_ln == judge5_ln or judge9_ln == judge4_ln or judge9_ln == judge3_ln or judge9_ln == judge2_ln  or judge9_ln == judge1_ln:
        judge9_ln = ""
        judge9_vote = ""
        judge9_code = ""

    if judge8_ln == judge7_ln or judge8_ln == judge6_ln or judge8_ln == judge5_ln or judge8_ln == judge4_ln or judge8_ln == judge3_ln or judge8_ln == judge2_ln  or judge8_ln == judge1_ln:
        judge8_ln = ""
        judge8_vote = ""
        judge8_code = ""

    if judge7_ln == judge6_ln or judge7_ln == judge5_ln or judge7_ln == judge4_ln or judge7_ln == judge3_ln or judge7_ln == judge2_ln  or judge7_ln == judge1_ln:
        judge7_ln = ""
        judge7_vote = ""
        judge7_code = ""

    if judge6_ln == judge2_ln:
        judge6_ln = ""
        judge6_vote = ""
        judge6_code = ""

    if judge5_ln == judge4_ln:
        judge5_ln = ""
        judge5_vote = ""
        judge5_code = ""
    #print judge1_ln, judge2_ln, judge3_ln, judge4_ln, judge5_ln, judge6_ln, judge7_ln


    if len(judge5_ln) < 2:
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge6_ln) < 2:
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge2_ln) < 2:
        judge2_ln = judge3_ln
        judge3_ln = judge4_ln
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge2_vote = judge3_vote
        judge3_vote = judge4_vote
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge2_code = judge3_code
        judge3_code = judge4_code
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge1_ln) < 2:
        judge1_ln = judge2_ln
        judge2_ln = judge3_ln
        judge3_ln = judge4_ln
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge1_vote = judge2_vote
        judge2_vote = judge3_vote
        judge3_vote = judge4_vote
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge1_code = judge2_code
        judge2_code = judge3_code
        judge3_code = judge4_code
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if len(judge8_ln) < 2:
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge10_ln = judge11_ln
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge10_vote = judge11_vote
        judge8_code = judge9_code
        judge9_code = judge10_code
        judge10_code = judge11_code

    if len(judge7_ln) < 2:
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge10_ln = judge11_ln
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge10_vote = judge11_vote
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code
        judge10_code = judge11_code


    if judge6_ln == "":
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if judge4_ln == "":
        judge4_ln = judge5_ln
        judge5_ln = judge6_ln
        judge6_ln = judge7_ln
        judge7_ln = judge8_ln
        judge8_ln = judge9_ln
        judge9_ln = judge10_ln
        judge4_vote = judge5_vote
        judge5_vote = judge6_vote
        judge6_vote = judge7_vote
        judge7_vote = judge8_vote
        judge8_vote = judge9_vote
        judge9_vote = judge10_vote
        judge4_code = judge5_code
        judge5_code = judge6_code
        judge6_code = judge7_code
        judge7_code = judge8_code
        judge8_code = judge9_code
        judge9_code = judge10_code

    if judge5_ln == judge4_ln:
        judge5_ln = judge6_ln
        judge5_vote = judge6_vote
        judge5_code = judge6_code
        judge6_ln = judge7_ln
        judge6_vote = judge7_vote
        judge6_code = judge7_code
        judge7_ln = judge8_ln
        judge7_vote = judge8_vote
        judge7_code = judge8_code
        judge8_ln = judge9_ln
        judge8_vote = judge9_vote
        judge8_code = judge9_code
        judge9_ln = judge10_ln
        judge9_vote = judge10_vote
        judge9_code = judge10_code

    if state_abbr == "CA" or state_abbr == "IL" or state_abbr == "PA" or state_abbr == "FL" or state_abbr == "KY" or state_abbr == "LA" or state_abbr == "ME" or state_abbr == "OH" or state_abbr == "CT" or state_abbr == "MD" or state_abbr == "MI" or state_abbr == "CO" or state_abbr == "GA" or state_abbr == "IA" or state_abbr == "MO" or state_abbr == "NE" or state_abbr == "NJ" or state_abbr == "NY" or state_abbr == "NC" or state_abbr == "OH" or state_abbr == "WI" or state_abbr == "AZ" or state_abbr == "AR" or state_abbr == "MT":
        judge8_ln = ""
        judge8_code = ""
        judge8_vote = ""
        judge9_ln = ""
        judge9_code = ""
        judge9_vote = ""

    if state_abbr == "ND" or state_abbr == "RI" or state_abbr == "VT" or state_abbr == "SC" or state_abbr == "UT" or state_abbr == "WY" or state_abbr == "HI":
        judge6_ln = ""
        judge6_vote = ""
        judge6_code = ""
        judge7_ln = ""
        judge7_vote = ""
        judge7_code = ""
        judge8_ln = ""
        judge8_vote = ""
        judge8_code = ""

    if state_abbr == "MS" or state_abbr == "OK-SC" or state_abbr == "WA":
        judge10_ln = ""
        judge10_vote = ""
        judge10_code = ""
        judge11_ln = ""
        judge11_vote = ""
        judge11_code = ""

    if len(dissent_by_string) > 2:
        dissent_by_string = dissent_by_string + " " + str(other_dissent_holder)
    if len(dissent_by_string) < 2:
        dissent_by_string = dissent_by_string + str(other_dissent_holder)
    dissent_by_string = re.sub("\[", "", dissent_by_string)
    dissent_by_string = re.sub("\]", "", dissent_by_string)
    dissent_by_string = re.sub("'", "", dissent_by_string)

    if state_abbr == "ID":
        panel = 0

    #print judge1_ln, judge2_ln, judge3_ln, judge4_ln, judge5_ln, judge6_ln, judge7_ln, judge8_ln, judge9_ln
    # For each case, write a row to the .csv file which contains the desired variables.
    localrow = []
    localrow.append("mjn15@psu.edu")
    localrow.append(Lexis_cite)
    localrow.append(entry)
    localrow.append(court_string)
    localrow.append(new_date)
    localrow.append(state_abbr)
    localrow.append(panel)
    localrow.append(parties_string)
    localrow.append(docketnum)
    localrow.append(cite_string.strip())
    localrow.append(Lexis_cite.strip())
    localrow.append(West_cite.strip())
    localrow.append(attorney_string)
    localrow.append(part_judges)
    localrow.append(judges_np)
    localrow.append(judge1_ln.upper())
    localrow.append(judge1_vote)
    localrow.append(judge1_code)
    localrow.append(judge2_ln.upper())
    localrow.append(judge2_vote)
    localrow.append(judge2_code)
    localrow.append(judge3_ln.upper())
    localrow.append(judge3_vote)
    localrow.append(judge3_code)
    localrow.append(judge4_ln.upper())
    localrow.append(judge4_vote)
    localrow.append(judge4_code)
    localrow.append(judge5_ln.upper())
    localrow.append(judge5_vote)
    localrow.append(judge5_code)
    localrow.append(judge6_ln.upper())
    localrow.append(judge6_vote)
    localrow.append(judge6_code)
    localrow.append(judge7_ln.upper())
    localrow.append(judge7_vote)
    localrow.append(judge7_code)
    localrow.append(judge8_ln.upper())
    localrow.append(judge8_vote)
    localrow.append(judge8_code)
    localrow.append(judge9_ln.upper())
    localrow.append(judge9_vote)
    localrow.append(judge9_code)
    localrow.append(judge10_ln.upper())
    localrow.append(judge10_vote)
    localrow.append(judge10_code)
    localrow.append(judge11_ln.upper())
    localrow.append(judge11_vote)
    localrow.append(judge11_code)
    localrow.append(dissent)
    localrow.append(num_dissent)
    localrow.append(dissent_by_string.upper())
    localrow.append(dissent_author_1.upper())
    localrow.append(dissent_author_2.upper())
    localrow.append(dissent_author_3.upper())
    localrow.append(dissent_author_4.upper())
    localrow.append(dissent_author_5.upper())
    localrow.append(concur)
    localrow.append(num_concur)
    localrow.append(concur_by_string.upper())
    localrow.append(check_recuse_case)
    if check_recuse == False:
        outfilehandle.writerow(localrow)

    if check_recuse == True:
        recuse_handle.writerow(localrow)
    check_recuse = False

# Finish writing to the .csv file and close it so the process is complete
infilehandle.close()
check.close()
fout.close()
master.close()
