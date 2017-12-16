# affix-analys.py:
# builds a lexc file for analysis out of a csv file of affixes

copyright = """Copyright © 2017, Kimmo Koskenniemi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re, csv, sys

features = set()
multichars = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][a-zåäöVCØ]+[}]", str)
    for mch in lst:
        multichars.add(mch)
    return

rdr = csv.DictReader(sys.stdin, delimiter=';')
prevID = ",,"
for r in rdr:
    ##print(r)
    if r["NEXT"] == '' or r["NEXT"][0] == '!':
        continue
    ide = prevID if r["ID"] == '' else r["ID"]
    if prevID != ide:
        prevID = ide
        print("LEXICON %s" % ide)
    collect_multichars(r["MPHON"])
    if r['FEAT'] == '' and r['BASEF'] == '':
        r['BASEF'] = r['MPHON']
    if r['BASEF'] == "!":
        r['BASEF'] = ""
    if r['FEAT'] != '':
        featlist = re.split(" +", r['FEAT'])
        f = '+' + '+'.join(featlist)
        for feat in featlist:
            features.add("+" + feat)
    else: f = ''
    for n in re.split(" +", r["NEXT"]):
        if n != '':
            if r['BASEF'] + f == r['MPHON']:
                print("{}{} {};".format(r['BASEF'], f, n))
            else:
                print("{}{}:{} {};".format(r['BASEF'], f, r['MPHON'], n))

#feafile = open("affixmultich.py", 'w')
#print("features =",features, file=feafile)
#print("multichars =", multichars, file=feafile)
#feafile.close()
    
