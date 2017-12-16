# affix-guesser.py:
# builds a lexc file for guessing out of a csv file of affixes

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
nexts = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][a-zåäöšžVCØ]+[}]", str)
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
    for n in re.split(" +", r["NEXT"]):
        if n == '': continue
        if re.search(r"/", ide):
            nexts.add(n)
            print("% {}:{} {};".format(ide, r['MPHON'], n))
        elif r['MPHON'] == "":
            print(" {};".format(n))
        else:
            print(":{} {};".format(r['MPHON'], n))

#feafile = open("affixmultich.py", 'w')
#print("multichars =", multichars, file=feafile)
#print("nexts =", nexts, file=feafile)
#feafile.close()
    
