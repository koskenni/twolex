# ksk2lexc :
# converts KSK entries into LEXC entries

import re, sys, hfst, argparse
argparser = argparse.ArgumentParser("python3 ksk2lexc.py",
                                     description="Converts KSK entries into LEXC format")
argparser.add_argument("-k", "--ksk", default="~/Dropbox/lang/fin/ksk/ksk-v.dic")
argparser.add_argument("-l", "--lexc", default="ksk-words.lexc")
argparser.add_argument("-f", "--fst", default="fin-conv.fst")
argparser.add_argument("-c", "--codes", default="infl-codes.text")
args = argparser.parse_args()


fstfile = hfst.HfstInputStream(args.fst)
fst = fstfile.read()
fst.lookup_optimize()
outf = open(args.lexc, "w")
infl_set =  set(open(args.codes).read().split())
entrylist = []
multich = set()
def find_multichars(str):
    lst = re.findall(r"\{[a-zåäöšžØ']+\}", str)
    for sym in lst:
        multich.add(sym)
import affixmultich
linenum = 0
for linenl in sys.stdin:
    linenum += 1
    line = linenl.strip()
    if re.search(r"[/!Y]", line):
        continue
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
    if infl not in infl_set:
        continue
    if not re.match(r"^[a-zšžåäö']+$", word) and re.match(r"^V[0-9][0-9][*]?", infl):
        print("", linenum, ":", '"' + line + '"')
        continue
    #if infl == "V41" and re.match(r"^[hjklmnprstv]*[äöye].*t[aä]$", word):
    #    infl = "V41ä"
    #elif infl == "V42" and re.match(r"^.*nt(aa|ää)$", word):
    #    infl = "V42n"
    iclass = infl#.replace('0', 'O')
    symlist = list(word)
    symlist.append(iclass)
    symtup = tuple(symlist)
    res = fst.lookup(symtup)
    if not res:
        print(linenum, ':', line, "".join(symlist))
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
