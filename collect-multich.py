import re, csv, sys

multichars = set()
nexts = set()
features = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][a-zåäöVCØ]+[}]", str)
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
