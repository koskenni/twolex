""" pat-proc.py: produces either a converter or a guesser from *pat.csv

Copyright © 2017, Kimmo Koskenniemi

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
import csv, re, argparse
from collections import OrderedDict

multichs = set()

definitions = OrderedDict()

patterns = OrderedDict()

conts = OrderedDict()

def extract_multichs(regexp):
    global multichs, definitions
    rege = re.sub(r"([][()|+*: ]|\.[iul]|\.o\.)+", ",", regexp)
    lst = re.split(r",", rege)
    for nm in lst:
        if len(nm) > 1 and (nm not in definitions):
            multichs.add(nm)
    return

def add_perc(str):
    return re.sub(r"([{}])", r"%\1", str)

def proj_down_regex(str):
    lst = re.split(r"([\]\[\|\+\* ]+|\.[iul]|\.o\.)", str)
    downlst = [re.sub(r"([a-zåäöøØ0]):({[a-zåäöøØ]+}|0)", r"\2", el) for el in lst]
    reslst = [re.sub(r"^0$", r"", el) for el in downlst]
    res = "".join(reslst)
    res = re.sub(r"\s+\[\s*\|\s*\]\s*", r" ", res)
    res = re.sub(r"\s+", r" ", res)
    res = re.sub(r"\s+$", r"", res)
    return res

def invert_regex(str):
    lst = re.split(r"([\]\[\|\+\* ]|\.[iul]|\.o\.)+", str)
    invlst = [re.sub(r"([a-zåäöø0]):({[a-zåäöø]+})", r"\2:\1", el) for el in lst]
    invlst = [re.sub(r"0", r"ø", el) for el in invlst]
    return "".join(invlst)

def ksk2entrylex():
    for name in conts:
        multichs.add(name)
    print("Multichar_Symbols")
    print(" ", " ".join(sorted(multichs)))
    print("Definitions")
    for dn in definitions.keys():
        print(" ", dn, "=", add_perc(definitions[dn]), ";")
    print("LEXICON Root")
    for name in sorted(patterns.keys()):
        for pat in patterns[name]:
            print("<", add_perc(pat), ">", name, ";")
    for name in conts:
        print("LEXICON", name)
        print(re.sub(r"(0)", r"%\1", name) + ":% " + conts[name], "# ;")
    return

def ksk2guesserlex():
    global conts, patterns
    import affixmultich
    print("Multichar_Symbols")
    print(" ", " ".join(sorted(multichs |
                                   affixmultich.nexts |
                                   affixmultich.multichars)))
    print("Definitions")
    for dn in definitions.keys():
        downde = proj_down_regex(definitions[dn])
        print(" ", dn, "=", add_perc(downde), ";")
    print("LEXICON Root")
    for name in patterns:
        for pat in patterns[name]:
            downpat = proj_down_regex(pat)
            print("<", add_perc(downpat), ">", conts[name], ";")
    return

argparser = argparse.ArgumentParser("python3 di2mi-to-di2mi.py",
                                        description="Writes either a converter or a guesser")
argparser.add_argument("-p", "--patterns")
argparser.add_argument("-c", "--continuations")
argparser.add_argument("-m", "--mode", choices = ['c', 'g'],
                           help="'g' for guesser, 'c' for converter",
                           default="c")
args = argparser.parse_args()

patfile = open(args.patterns, "r")
patrdr = csv.DictReader(patfile, delimiter=';')
prevID = ";;;"
for r in patrdr:
    i, nx, mfon = r['ID'], r['NEXT'], r['MPHON']
    id = prevID if i == '' else i
    prevID = id
    if id == "Define":
        definitions[nx] = mfon
    elif id == "Root":
        regex = re.sub(r"^\s*<(.*)>\s*$", r"\1", mfon)
        if nx in patterns:
            patterns[nx].append(regex)
        else:
            patterns[nx] = [regex]

patfile.close()

contfile = open(args.continuations, "r")
contrdr = csv.DictReader(contfile, delimiter=';')
for r in contrdr:
    id, nx = r['ID'], r['NEXT']
    conts[id] = nx

for ic,el in patterns.items():
    for e in el:
        extract_multichs(e)
for dn,pe in definitions.items():
    extract_multichs(pe)
for name in conts:
    multichs.add(conts[name])

if args.mode == 'c':
    ksk2entrylex()
elif args.mode == 'g':
    ksk2guesserlex()
else:
    print("value of --mode must be either 'g' or 'c'")
