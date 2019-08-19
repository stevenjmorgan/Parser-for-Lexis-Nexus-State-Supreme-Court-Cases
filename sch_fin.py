# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 12:10:31 2019

@author: steve
"""


import os
import re
import csv
import string
import operator
import datetime
import time

#mydir = "C:/Users/Steve/Dropbox/PSU2018-2019/RA/Scraper/"
#mydir = "C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/"
#mydir = "C:/Users/steve/Dropbox/PSU2018-2019/RA/Scraper/"
mydir = "C:/Users/steve/OneDrive/Desktop/"

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






# .csv file where extracted metadata will be stored
#mydir2 = 'C:/Users/sum410/Dropbox/PSU2018-2019/Summer/MN/'
mydir2 = 'C:/Users/steve/OneDrive/Desktop/'
#mydir2 = 'C:/Users/steve/Dropbox/PSU2018-2019/Summer/MN/'
fout = open(mydir2 + "SchFin_8-17.csv", "wb") #EAWPost1990    ############################
outfilehandle = csv.writer(fout,
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

# Name of folder where all cases are located (and nothing else)
dirname = mydir + "SchFin/"
dirlist = os.listdir(dirname)
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

#dirlist = [file for file in dirlist if len(file) > 20]

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
        #if (re.search("^Copy Citation",txtline)):
        #    line_before_first = True

        #if (line_before_first and re.search("(COURT|Court)", txtline) and not re.search("^1 ", txtline)):
            ## the court in which the case was heard
        #    line_before_first = False
        #    court_line = True
        #    court_string = court_string + txtline
        #    court_string = court_string.strip()
        #    print court_string
        #    state_abbr = state_ab(court_string) ###function to return state abbreviations

        #if (re.search("Alabama|Arizona|Connecticut|Delaware|Florida|Idaho|Massachusetts|Mississippi|Montana|Nevada|New Hampshire|Virginia", court_string)):
            # all cases in states that hear cases in panels are given a value of 1
        #    panel = 1


        # Lexis Cite
        if re.search('Citation:', txtline):
            #print txtline
            Lexis_cite = re.sub('Citation:','', txtline).strip()
       
        
        # Judges
        if re.match('^JUDGES:', txtline):
            judges_string = txtline
            
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
            #if state != 'Alabama':
            #    judges_string = re.sub(' See| see', '', judges_string)
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
            #judges_holder = judges_holder + non_panel_list
            judges_holder = [word for word in judges_holder if word != ""]
            judges_holder = [word.strip() for word in judges_holder]
            judges_holder = [word.upper() for word in judges_holder]
            judges_holder = [word for word in judges_holder if len(word) > 2]
            judges_holder = list(set(judges_holder))
            
            #print(judges_holder)
            
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
                
                
                # Pull in judge codes from state master file by matching state abbrevation, justice name, and time in office
#        if judge1_code == "":
#            with open(mydir + "States_MasterFile_Import.csv", "rb") as f:
#                reader = csv.reader(f)
#                next(f)
#                for row in reader:
#                    state = row[0]
#                    name = row[3]
#                    if len(row[4]) == 4 and row[0] != "MC":
#                        row[4] = "1/1/" + row[4]
#                    if len(row[5]) == 4 and row[0] != "MC":
#                        row[5] = "1/1/" + row[5]
#                    if len(row[4]) != 4 and row[0] != "MC":
#                        start = datetime.datetime.strptime(row[4], '%m/%d/%Y').date()
#                        end = datetime.datetime.strptime(row[5], '%m/%d/%Y').date()
#    
#                    #Format justice last names from each file to ensure accurate matching
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge1_ln) or Capitalize(lastname(row[3])) == Capitalize(judge1_ln)) and judge1_code == "" and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge1_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge1_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge2_ln) or Capitalize(lastname(row[3])) == Capitalize(judge2_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge2_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge2_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge3_ln) or Capitalize(lastname(row[3])) == Capitalize(judge3_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge3_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge3_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge4_ln) or Capitalize(lastname(row[3])) == Capitalize(judge4_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge4_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge4_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge5_ln) or Capitalize(lastname(row[3])) == Capitalize(judge5_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge5_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge5_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge6_ln) or Capitalize(lastname(row[3])) == Capitalize(judge6_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge6_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge6_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge7_ln) or Capitalize(lastname(row[3])) == Capitalize(judge7_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge7_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge7_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge8_ln) or Capitalize(lastname(row[3])) == Capitalize(judge8_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge8_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge8_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge9_ln) or Capitalize(lastname(row[3])) == Capitalize(judge9_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge9_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge9_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge10_ln) or Capitalize(lastname(row[3])) == Capitalize(judge10_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge10_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge10_code = row[1]
#                    if (Capitalize(lastname(row[7])) == Capitalize(judge11_ln) or Capitalize(lastname(row[3])) == Capitalize(judge11_ln)) and (row[0] == state_abbr or state_abbr == "OK" or state_abbr == "TX") and len(judge11_ln) > 1 and start <= date_format <= (end + one_month):
#                        judge11_code = row[1]
#
#        # Store "Did not match" if a justice did not match to a justice code
#        if judge1_code == "" and len(judge1_ln) > 2:
#            judge1_code = "Did not match"
#        if judge2_code == "" and len(judge2_ln) > 2:
#            judge2_code = "Did not match"
#        if judge3_code == "" and len(judge3_ln) > 2:
#            judge3_code = "Did not match"
#        if judge4_code == "" and len(judge4_ln) > 2:
#            judge4_code = "Did not match"
#        if judge5_code == "" and len(judge5_ln) > 2:
#            judge5_code = "Did not match"
#        if judge6_code == "" and len(judge6_ln) > 2:
#            judge6_code = "Did not match"
#        if judge7_code == "" and len(judge7_ln) > 2:
#            judge7_code = "Did not match"
#        if judge8_code == "" and len(judge8_ln) > 2:
#            judge8_code = "Did not match"
#        if judge9_code == "" and len(judge9_ln) > 2:
#            judge9_code = "Did not match"
#        if judge10_code == "" and len(judge10_ln) > 2:
#            judge10_code = "Did not match"
#        if judge11_code == "" and len(judge11_ln) > 2:
#            judge11_code = "Did not match"
#        #print judge1_ln, judge2_ln, judge3_ln, judge4_ln, judge5_ln, judge6_ln, judge7_ln

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
    localrow.append(judge1_ln)
    localrow.append(1)
    localrow.append(judge1_code)
    localrow.append(judge2_ln)
    localrow.append(1)
    localrow.append(judge2_code)
    localrow.append(judge3_ln)
    localrow.append(1)
    localrow.append(judge3_code)
    localrow.append(judge4_ln)
    localrow.append(1)
    localrow.append(judge4_code)
    localrow.append(judge5_ln)
    localrow.append(1)
    localrow.append(judge5_code)
    localrow.append(judge6_ln)
    localrow.append(1)
    localrow.append(judge6_code)
    localrow.append(judge7_ln)
    localrow.append(1)
    localrow.append(judge7_code)
    localrow.append(judge8_ln)
    localrow.append(1)
    localrow.append(judge8_code)
    localrow.append(judge9_ln)
    localrow.append(1)
    localrow.append(judge9_code)
    localrow.append(judge10_ln)
    localrow.append(1)
    localrow.append(judge10_code)
    localrow.append(judge11_ln)
    localrow.append(1)
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
#check.close()
fout.close()
master.close()
