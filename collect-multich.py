# collect-multich.py
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

multichars = set()
nexts = set()
features = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][a-zšžåäöA-ZØ]+[}]", str)
    for mch in lst:
        multichars.add(mch)
    return

aff = open("affixes-v.csv")
rdr = csv.DictReader(aff, delimiter=';')
for r in rdr:
    if r["NEXT"] == '' or r["NEXT"][0] == '!':
        continue
    if re.match(r"^.*[/][vsapd]$", r["ID"]):
        nexts.add(r["ID"])
    collect_multichars(r["MPHON"])
    if r['FEAT'] != '':
        featlist = re.split(" +", r['FEAT'])
        f = '+' + '+'.join(featlist)
        for feat in featlist:
            features.add("+" + feat)

muf = open("affixmultich.py", 'w')
print("multichars =", multichars, file=muf)
print("nexts =", nexts,  file=muf)
print("features =", features, file=muf)
