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
## Spring, 2012

import os, re, csv, string, operator
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

# .csv file where extracted metadata will be stored
fout = open(mydir + "state_headnotes.csv", "wb")
outfilehandle = csv.writer(fout,
                           delimiter=",",
                           quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)

# Create your own label for each column of the metadata .csv file
localrow = []
localrow.append("caseid")
localrow.append("filename")
#localrow.append("parties")
localrow.append("Unpublished")
localrow.append("numCoreTerms")
localrow.append("first_hn")
localrow.append("second_hn")
localrow.append("third_hn")
localrow.append("hn")
#localrow.append("Prior History")
#localrow.append("Sub History")
#localrow.append("Petion for Rehearing")
localrow.append("disposition")
localrow.append("attorneys")
localrow.append("publicDefender")
localrow.append("proSe")
#localrow.append("appellee attorneys")
#localrow.append("appellee public defender")
#localrow.append("appellee pro se")
#localrow.append("judges")
#localrow.append("judges participating")
localrow.append("judgeNP")
localrow.append("judgeNP_name")
#localrow.append("Judge1 Last Name")
#localrow.append("Judge1 First Name")
#localrow.append("Judge1 Full Name")
#localrow.append("Judge2 Last Name")
#localrow.append("Judge2 First Name")
#localrow.append("Judge2 Full Name")
#localrow.append("Judge3 Last Name")
#localrow.append("Judge3 First Name")
#localrow.append("Judge3 Full Name")
#localrow.append("Judge4 Last Name")
#localrow.append("Judge4 First Name")
#localrow.append("Judge4 Full Name")
#localrow.append("Judge5 Last Name")
#localrow.append("Judge5 First Name")
#localrow.append("Judge5 Full Name")
#localrow.append("Judge6 Last Name")
#localrow.append("Judge6 First Name")
#localrow.append("Judge6 Full Name")
#localrow.append("Judge7 Last Name")
#localrow.append("Judge7 First Name")
#localrow.append("Judge7 Full Name")
localrow.append("majority_name")
localrow.append("perCuriam")
localrow.append("unanimous")
localrow.append("dissent")
#localrow.append("unwrittenDissent")
localrow.append("dissent_no")
localrow.append("dissent_name")
localrow.append("concurrence")
localrow.append("concur_no")
localrow.append("concur_name")
outfilehandle.writerow(localrow)


# Name of folder where all cases are located (and nothing else)
dirname = mydir + "mandArb/"
#dirname = mydir + "AdminTxt/"
dirlist = os.listdir(dirname)
cleandirlist = []
for entry in dirlist:
    matchresult = re.match('.+\\.txt$', entry)
    if matchresult != None:
        cleandirlist.append(matchresult.group())

#dirlist = [file for file in dirlist if len(file) > 20]

# Use (uncomment) following line to test code on a small handful of cases
#cleandirlist = cleandirlist[0:10]

for entry in cleandirlist: ## each entry is a txt file with an opinion
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
    action_string = ""
    per_curiam = 0
    unanimous = 0
    action1 = ""
    date = ""
    coreterms = ""
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
    #appellee_pubdef = ""
    #appellee_prose = ""
    #appellee_attorney_string = ""
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
    no_part_string = " "
    full_judges_holder = []
    judges_holder = []
    dissent_holder = []
    concur_holder = []
    no_part = False
    no_part_dich = 0
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
    attorney_line = False
    headnote_line = False
    #appellee_attorney_line = False
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
    unwritten_dissent = 0
    #dissent_check = 0
    headnote_string = ""
    headnote_tmp = ""
    headnote_holder = []
    coreterms_holder = []
    coreterms_line = False

    localrow = []
    caseid = str(re.split("\.", entry)[0])
    #print caseid
    print entry


    for txtline in txtlines:
        if ((not case_with_preamble or blank_after_searchterms) and re.search("[\w]+", txtline)):
            ## the parties
            parties_line = True
            parties_string = parties_string + txtline
            #print txtline.replace("\n", "")
        if(re.match("^SUBSEQUENT HISTORY:", txtline)):
            sub_history_line = True
        if(sub_history_line and re.search("[\w]+", txtline)):
            sub_history_string = sub_history_string + txtline
        if (prior_history_line and re.match("^[\s]+$", txtline)):
            prior_history_string = re.sub("PRIOR HISTORY:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("PRIOR HISTORY:", "", prior_history_string)
            prior_history_string = re.sub("\[\**\d*\]", "", prior_history_string)
            prior_history_string = re.sub("\xa0", " ", prior_history_string)
            prior_history_string = re.sub("\n|\r", " ", prior_history_string)
            prior_history_string = string.strip(prior_history_string)
            sub_history_line = False


        if(re.match("^PRIOR HISTORY:", txtline)):
            prior_history_line = True
        if(prior_history_line and re.search("[\w]+", txtline)):
            prior_history_string = prior_history_string + txtline
        if (prior_history_line and re.match("^[\s]+$", txtline)):
            prior_history_string = re.sub("PRIOR HISTORY:\s+\[\*+[0-9]+\]\s+", "", prior_history_string)
            prior_history_string = re.sub("PRIOR HISTORY:", "", prior_history_string)
            prior_history_string = re.sub("\xa0", " ", prior_history_string)
            prior_history_string = re.sub("\n|\r", " ", prior_history_string)
            prior_history_string = re.sub("\[\**\d*\]", "", prior_history_string)
            prior_history_string = string.strip(prior_history_string)
            prior_history_line = False

        #Using OUTCOME instead of DISPOSITION because not every case has a DISPOSITION
        #if (re.match("^DISPOSITION:", txtline)):
        #    ## disposition of case
        #    disposition_line = True
        #    #print disposition_string
        #if (disposition_line and re.search("[\w]+", txtline)):
        #    ## disposition lines with text
        #    disposition_string = disposition_string + txtline
        #    #print disposition_string
        #if (disposition_line and re.match("^[\s]+$", txtline)):
        #    ## blank line after disposition line
        #    disposition_string = re.sub("DISPOSITION:", "", disposition_string)
        #    disposition_string = re.sub("\xa0", " ", disposition_string)
        #    disposition_string = re.sub("\n|\r", " ", disposition_string)
        #    disposition_string = re.sub("\[.+\]", "", disposition_string)
        #    disposition_string = string.strip(disposition_string)
        #    #print disposition_string
        #    disposition_line = False

        if (re.match("^OUTCOME:", txtline)):
            ## disposition of case
            disposition_line = True
            #print disposition_string
        if (disposition_line and re.search("[\w]+", txtline)):
            ## disposition lines with text
            disposition_string = disposition_string + txtline
            #print disposition_string
        if (disposition_line and re.match("^[\s]+$", txtline)):
            ## blank line after disposition line
            disposition_string = re.sub("OUTCOME:", "", disposition_string)
            disposition_string = re.sub("\xa0", " ", disposition_string)
            disposition_string = re.sub("\n|\r", " ", disposition_string)
            disposition_string = re.sub("\[.+\]", "", disposition_string)
            disposition_string = re.sub("\[\**\d*\]", "", disposition_string)
            disposition_string = string.strip(disposition_string)
            #print disposition_string
            disposition_line = False

            #if (re.search("affirm|Affirm|AFFIRM|reverse|Reverse|REVERSE", disposition_string)):
            #    rehearing = "NO"

            #if (re.search("vacate|Vacate|VACATE", disposition_string)):
            #    rehearing = "NO"

            #if (re.search("(P|p)etition for (R|r)ehearing", disposition_string) and rehearing != "NO"):
            #    rehearing = "YES"

        #if (re.search("Petition[s]* for Rehearing", txtline) and rehearing == ""):
        #    rehearing = "CHECK"

        #if (re.search("REHEARING", txtline) and rehearing != "YES"):
        #    rehearing = "TRUNCATE"

        if (re.match("^CORE TERMS:", txtline)):
            coreterms = txtline
            #print coreterms
            coreterms_holder = re.split(", ", coreterms)
            #print len(coreterms_holder)
            coreterms_line = True


        if (re.match("^LexisNexis\(R\) Headnotes", txtline)):
            headnote_line = True
            print txtline
        if (headnote_line and re.search(">", txtline)):
            #headnote_tmp = txtline + "|"
            headnote_string = headnote_string + txtline
            #print headnote_tmp
            #print headnote_line


        if (re.search("OPINION BY: (PER CURIAM)|(Per Curiam)", txtline)):
            #pc_holder = pc_holder + "Per Curiam. "
            per_curiam = 1
        if (re.search("PER CURIAM", txtline)):
            #pc_holder = pc_holder + "Per Curiam. "
            per_curiam = per_curiam + 1
        if (re.search("^[\s]*Per Curiam[\.:\s]*$", txtline)):
            per_curiam = 1
            #print pc_holder + "\n"

        # I had a problem with some cases that had sections I needed to exclude
        # I inserted tags by hand to delimit the parts I wanted to cut out.
        # The next four lines are code work to cut out those portions of my problem cases.
        if (re.search("^<truncate>", txtline)):
            trunc_text = True

        if (re.search("^</truncate>", txtline)):
            trunc_text = False

        if(re.match("^COUNSEL:", txtline)):
                attorney_line = True
                headnote_line = False

        if (attorney_line and re.search("^JUDGES|^OPINION", txtline)):
                attorney_line = False
                headnote_line = False

                attorney_string = re.sub("COUNSEL:\[\**\d*\]", "", attorney_string)
                attorney_string = re.sub("COUNSEL:", "", attorney_string)
                attorney_string = re.sub("\[\**\d*\]", "", attorney_string)
                attorney_string = re.sub("\xa0", " ", attorney_string)
                attorney_string = re.sub("\n|\r", " ", attorney_string)
                attorney_string = string.strip(attorney_string)
                attorney_line = False

        if(attorney_line):
            attorney_string = attorney_string + txtline
        #if (attorney_line and re.match("^[\s]+$", txtline)):
        #    attorney_string = re.sub("COUNSEL:\s+\[\*+[0-9]+\]\s+", "", attorney_string)
        #    attorney_string = re.sub("COUNSEL:", "", attorney_string)
        #    attorney_string = re.sub("\xa0", " ", attorney_string)
        #    attorney_string = re.sub("\n|\r", " ", attorney_string)
        #    attorney_string = string.strip(attorney_string)
        #    attorney_line = False

            if (re.search("Public|public|PUBLIC|defender|DEFENDER|Defender", attorney_string)):
                pubdef = 1

            if (re.search("(pro se)|(Pro se)|(Pro Se)|(pro Se)", attorney_string)):
                prose = 1

        if (re.match("^JUDGES:", txtline) and not trunc_text):
            ## judges hearing case
            judges_line = True
            headnote_line = False
        if (judges_line and re.search("[\w]+", txtline)):
            ## judges lines with text
            judges_string = judges_string + txtline
        if (judges_line and re.match("^[\s]+$", txtline)):
            # blank line after judges line
            judges_string = re.sub("JUDGES:", "", judges_string)
            judges_string = re.sub("\[\**\d*\]", "", judges_string)
            judges_string = re.sub("(Before: |BEFORE: )", "", judges_string)
            judges_string = re.sub("\xa0", " ", judges_string)
            judges_string = re.sub("\n|\r", " ", judges_string)
            judges_string = string.strip(judges_string)
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
            judges_holder = re.sub("Chief Justice", "", judges_holder)
            judges_holder = re.sub("Associate Justice", "", judges_holder)
            judges_holder = re.sub("(P|p)ro (T|t)em", "", judges_holder)
            judges_holder = re.sub(", (Jr\.|JR\.)", "Jr.", judges_holder)
            judges_holder = re.sub(", (Sr\.|SR\.)", "Sr.", judges_holder)
            judges_holder = re.sub(", III", "III", judges_holder)
            judges_holder = re.sub(", II", "II", judges_holder)
            judges_holder = re.sub(";", ",", judges_holder)
            judges_holder = re.sub(",[\s]*,", ",", judges_holder)
            judges_holder = re.sub(" and ", ", ", judges_holder)
            judges_holder = re.sub("[\s]+", " ", judges_holder)
            judges_holder = re.sub(",,", ",", judges_holder)
            judges_holder = re.sub(", \.", " ", judges_holder)
            #print judges_holder
            judges_holder = re.split(", ", judges_holder)
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

                judge4_ln = lastname(judges_holder[3])
                judge4_fn = firstname(judges_holder[3])
                judge4_mn = middlename(judges_holder[3])
                judge4_suf = namesuffix(judges_holder[3])
                judge4_full = judge4_ln + ", " + judge4_fn + " " + judge4_mn + " " + judge4_suf
                judge4_full = re.sub("[\s]+", " ", judge4_full)
                judge4_full = re.sub(", $", "", judge4_full)

            if (len(judges_holder) > 4):

                judge5_ln = lastname(judges_holder[4])
                judge5_fn = firstname(judges_holder[4])
                judge5_mn = middlename(judges_holder[4])
                judge5_suf = namesuffix(judges_holder[4])
                judge5_full = judge5_ln + ", " + judge5_fn + " " + judge5_mn + " " + judge5_suf
                judge5_full = re.sub("[\s]+", " ", judge5_full)
                judge5_full = re.sub(", $", "", judge5_full)

            if (len(judges_holder) > 5):

                judge6_ln = lastname(judges_holder[5])
                judge6_fn = firstname(judges_holder[5])
                judge6_mn = middlename(judges_holder[5])
                judge6_suf = namesuffix(judges_holder[5])
                judge6_full = judge6_ln + ", " + judge6_fn + " " + judge6_mn + " " + judge6_suf
                judge6_full = re.sub("[\s]+", " ", judge6_full)
                judge6_full = re.sub(", $", "", judge6_full)

            if (len(judges_holder) > 6):

                judge7_ln = lastname(judges_holder[6])
                judge7_fn = firstname(judges_holder[6])
                judge7_mn = middlename(judges_holder[6])
                judge7_suf = namesuffix(judges_holder[6])
                judge7_full = judge7_ln + ", " + judge7_fn + " " + judge7_mn + " " + judge7_suf
                judge7_full = re.sub("[\s]+", " ", judge7_full)
                judge7_full = re.sub(", $", "", judge7_full)

            if (len(judges_holder) > 7):
                check_case = 1
                #print judges_string

            if (re.search("((N|n)ot (P|p)articipat(e|ing)|(R|r)ecus(e|es|ed)|(T|t)ak(e|es) no part)", judges_string)):
                no_part = True
                no_part_dich = 1
                full_judges_holder = re.sub(", (J|JJ). ", "", judges_string)
                full_judges_holder = re.split("\. ", full_judges_holder)
                #print full_judges_holder
                no_part_string = [sentence for sentence in full_judges_holder if re.search("((N|n)ot (P|p)articipat(e|ing)|(R|r)ecus(e|es|ed))", sentence)]
                #print no_part_string
                no_part_string = str(no_part_string)
                no_part_string = re.sub("(N|n)ot (P|p)articipat(e|ing).*", "", no_part_string)
                no_part_string = re.sub("Recus(e|es|ed)", "", no_part_string)
                no_part_string = re.sub("recus(e|es|ed)", "", no_part_string)
                no_part_string = re.sub("^[\s]+", "", no_part_string)
                no_part_string = re.sub("[\s]*\*[\s]*", "", no_part_string)
                no_part_string = re.sub("'", "", no_part_string)
                no_part_string = re.sub("\[", "", no_part_string)
                no_part_string = re.sub("\]", "", no_part_string)
                no_part_string = re.sub("(Him|him|Her|her|Them|them)sel(f|ves)", "", no_part_string)
                no_part_string = re.sub("(J|j)ustices,*", "", no_part_string)
                no_part_string = re.sub("(J|j)ustice,*", "", no_part_string)
                no_part_string = re.sub("JUSTIC(E|ES),*", "", no_part_string)
                no_part_string = re.sub("[\s]*(did|does)[\s]*", "", no_part_string)
                no_part_string = re.sub(", (J|JJ|C.J).,*", "", no_part_string)
                no_part_string = re.sub("[\s] s[\s]*", "", no_part_string)
                #no_part_string = re.sub("[\s]$", "", no_part_string)
                no_part_string = re.sub(",[\s]+(,|\.)$", "", no_part_string)
                no_part_string = re.sub("\.[\s]*$", "", no_part_string)
                no_part_string = re.sub(",[\s]*$", "", no_part_string)
                #print no_part_string

            if (re.search("dissent|DISSENT|dissents|Dissents|dissenting|Dissenting|DISSENTING", judges_string)):
                jud_dissent = 1

            if (re.search("(U|u)nanimous|UNANIMOUS", judges_string)):
                unanimous = 1

        if (re.match("^OPINION BY:", txtline) and not trunc_text):
            ## opinion writer
            opin_by_line = True
        if (opin_by_line and re.search("[\w]+", txtline)):
            ## opinion by line with text
            opin_by_string = opin_by_string + txtline
        if (opin_by_line and re.match("^[\s]+$", txtline)):
            # blank line after opinion by line
            opin_by_string = re.sub("OPINION BY:", "", opin_by_string)
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
            #print author_full

        if (re.match("^OPINION", txtline) and not trunc_text):
            opinion_line = True
        if (re.match(re.escape("********** Print Completed **********"), txtline) or re.match("APPENDIX", txtline) or re.match("^CONCUR BY:", txtline) or re.match("^DISSENT BY:", txtline)):
            opinion_line = False

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
            if (re.search("AMICUS|amicus|Amicus", op_string)):
                amicus = 1

        if (re.match("^DISSENT BY:", txtline) and not trunc_text):
            dissent_by_line = True
            dissent = dissent + 1
        if (dissent_by_line and re.search("[\w]+", txtline)):
            dissent_by_string = dissent_by_string + txtline
        if (dissent_by_line and re.match("^[\s]+$", txtline)):
            dissent_by_string = string.strip(dissent_by_string)
            #dissent_by_string = string.lstrip(dissent_by_string)
            #dissent_by_string = string.rstrip(dissent_by_string)
            dissent_by_string = re.sub("\n", " ", dissent_by_string)
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

        if (re.match("^CONCUR BY:", txtline) and not trunc_text):
            concur_by_line = True
            concur = concur + 1
        if (concur_by_line and re.search("[\w]+", txtline)):
            concur_by_string = concur_by_string + txtline
        if (concur_by_line and re.match("^[\s]+$", txtline)):
            concur_by_string = string.strip(concur_by_string)
            #concur_by_string = string.lstrip(concur_by_string)
            #concur_by_string = string.rstrip(concur_by_string)
            concur_by_string = re.sub("\n", " ", concur_by_string)
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


        #if (re.search("petition for rehearing", op_string)):
        #    check_case = 1

        #if (re.search("(DECISION WITHOUT PUBLISHED OPINION)|(NOT FOR PUBLICATION)", txtline)):
        #    unpublished = 1

        #dissent_check = (dissent - jud_dissent)
        #if (dissent_check < 0):
        #    unwritten_dissent = 1

    #print concur_by_string
    #print dissent_holder
    #print concur_holder
    #print dissent1_ln
    #print dissent2_ln
    #print dissent3_ln
    #print dissent4_ln
    #print concur_by_string
    #print concur1_ln
    #print concur2_ln
    #print concur3_ln
    #print concur4_ln
    #print concur5_ln
    #print concur6_ln
    #print concur7_ln
    #print concur
    #print check_case

    unique_hn = []
    first_level_hn_holder = []
    split_hn_string = ""
    unique_first_hn_holder = []
    unique_first_two_hn_holder = []
    unique_first_three_hn_holder = []
    first_two_hn_holder = []
    first_three_hn_holder = []
    if (headnote_line == False):
        #print headnote_string
        #headnote_string = re.sub("\n","",headnote_string)
        #print headnote_string
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


    # For each case, write a row to the .csv file which contains the desired variables.
    localrow = []
    localrow.append(str(caseid))
    localrow.append(entry)
    #localrow.append(parties_string)
    localrow.append(unpublished)
    localrow.append(len(coreterms_holder))
    localrow.append(len(unique_first_hn_holder))
    localrow.append(len(unique_first_two_hn_holder))
    localrow.append(len(unique_first_three_hn_holder))
    localrow.append(unique_hn)
    #localrow.append(prior_history_string)
    #localrow.append(sub_history_string)
    #localrow.append(rehearing)
    localrow.append(disposition_string)
    localrow.append(attorney_string)
    localrow.append(pubdef)
    localrow.append(prose)
    #localrow.append(appellee_attorney_string)
    #localrow.append(appellee_pubdef)
    #localrow.append(appellee_prose)
    #localrow.append(judges_string)
    #localrow.append(judges_part_string)
    localrow.append(no_part_dich)
    localrow.append(no_part_string)
    #localrow.append(judge1_ln)
    #localrow.append(judge1_fn)
    #localrow.append(judge1_full)
    #localrow.append(judge2_ln)
    #localrow.append(judge2_fn)
    #localrow.append(judge2_full)
    #localrow.append(judge3_ln)
    #localrow.append(judge3_fn)
    #localrow.append(judge3_full)
    #localrow.append(judge4_ln)
    #localrow.append(judge4_fn)
    #localrow.append(judge4_full)
    #localrow.append(judge5_ln)
    #localrow.append(judge5_fn)
    #localrow.append(judge5_full)
    #localrow.append(judge6_ln)
    #localrow.append(judge6_fn)
    #localrow.append(judge6_full)
    #localrow.append(judge7_ln)
    #localrow.append(judge7_fn)
    #localrow.append(judge7_full)
    localrow.append(opin_by_string)
    localrow.append(per_curiam)
    localrow.append(unanimous)
    localrow.append(dissent)
    #localrow.append(unwritten_dissent)
    localrow.append(num_dissent)
    localrow.append(dissent_by_string)
    localrow.append(concur)
    localrow.append(num_concur)
    localrow.append(concur_by_string)
    outfilehandle.writerow(localrow)

# Finish writing to the .csv file and close it so the process is complete
infilehandle.close()
fout.close()
