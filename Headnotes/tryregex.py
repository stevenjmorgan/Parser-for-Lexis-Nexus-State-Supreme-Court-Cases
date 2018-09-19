import re

string = ' 504 U.S. 555'
m = re.search('\\b(\\d{1,3})\\s([AFSNU]\\.\\s?[\\w\\.]+)\\s(\\d{1,4}|_{1,4})\\b', string)
if m:
    found = m.group()

print found
