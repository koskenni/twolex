# affix-analys.py:
# builds a lexc file for analysis out of a csv file of affixes

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
    
