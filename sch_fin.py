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
check = open(mydir2 + "check_recusals_SchFin_8-17.csv", "wb") #EAWPost1990
recuse_handle = csv.writer(check,
                           delimiter=",",
                           quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)

master = open(mydir + "States_MasterFile_Import.csv", "rb")