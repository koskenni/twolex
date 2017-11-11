# ksk2lexc :
# converts KSK entries into LEXC entries

import re, sys, hfst, argparse
argparser = argparse.ArgumentParser("python3 ksk2lexc.py",
                                     description="Converts KSK entries into LEXC format")
argparser.add_argument("-k", "--ksk")
argparser.add_argument("-l", "--lexc", default="samp-words.lexc")
argparser.add_argument("-f", "--fst", default="fin-conv.fst")
args = argparser.parse_args()


fstfile = hfst.HfstInputStream(args.fst)
fst = fstfile.read()
fst.lookup_optimize()
outf = open(args.lexc, "w")
entrylist = []
multich = set()
def find_multichars(str):
    lst = re.findall(r"\{[a-zåäöšžØ]+\}", str)
    for sym in lst:
        multich.add(sym)
import affixmultich
linenum = 0
for linenl in sys.stdin:
    linenum += 1
    line = linenl.strip()
    lst = line.split(" ")
    if len(lst) < 2:
        print("LINE", linenum,
                  "HAS NOT ENOUGH FIELDS:", '"' + line + '"')
        continue
    word = re.sub(r"[0-9]+$", r"", lst[0])
    if len(lst) > 2 and lst[2] == "*":
        infl = lst[1] + lst[2]
    else:
        infl = lst[1]
    if not re.match(r"^[a-zšžåäö]+$", word) and re.match(r"^V[0-9][0-9][*]?", infl):
        print("", linenum, ":", '"' + line + '"')
        continue
    if infl == "V41" and re.match(r"^[hjklmnprstv]*[äöye].*t[aä]$", word):
        infl = "V41ä"
    elif infl == "V42" and re.match(r"^.*nt(aa|ää)$", word):
        infl = "V42n"
    symlist = list(word)
    symlist.append(infl)
    symtup = tuple(symlist)
    res = fst.lookup(symtup)
    if not res:
        print(linenum, ':', line)
    for r, w in res:
        mf, cont = re.split(r" +", r)
        find_multichars(mf)
        entrylist.append(r)

for sym in affixmultich.features:
    multich.add(sym)
for sym in affixmultich.multichars:
    multich.add(sym)
print("Multichar_Symbols", file=outf)
print(" ".join(sorted(multich)), file=outf)
print("LEXICON Root", file=outf)
for entry in entrylist:
    print(entry, ';', file=outf)
