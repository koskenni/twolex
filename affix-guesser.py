# affix-guesser.py:
# builds a lexc file for guessing out of a csv file of affixes

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

feafile = open("affixmultich.py", 'w')
print("multichars =", multichars, file=feafile)
print("nexts =", nexts, file=feafile)
feafile.close()
    
