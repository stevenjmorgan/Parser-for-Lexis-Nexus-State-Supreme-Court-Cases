import re

'''string = ' 504 U.S. 555'
m = re.search('\\b(\\d{1,3})\\s([AFSNU]\\.\\s?[\\w\\.]+)\\s(\\d{1,4}|_{1,4})\\b', string)
if m:
    found = m.group()

    #print found


string2 = ' 112 S. Ct. 2130'
#m2 = re.search('\\b(\\d{1,3})\\s(S\\.)\\s(\\d{1,4}|_{1,4})\\b', string2)
m2 = re.search('\\b(\\d{1,3})\\s[S]\\.\\s[C][t]\\.\\s(\\d{1,4}|_{1,4})\\b', string2)
if m2:
    found2 = m2.group()

    print repr(found2)'''

string3 = '119 L. Ed. 2d 351'
m3 = re.search('\\b(\\d{1,3})\\s([A-Z]\\.)\\s([A-Z][a-z]\\.)\\s(\\d[a-z])\\s(\\d{1,3}|_{1,3})\\b', string3)
if m3:
    found3 = m3.group()
    print repr(found3)
