# entryharvester.py

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

import hfst, sys, argparse

argparser = argparse.ArgumentParser("python3 corpguesser.py",
                                    description="Produces lexicon entries using also corpus data")
argparser.add_argument("-g", "--guesser",
                        default="fin-guess.fst",
                        help="a guesser fst")
argparser.add_argument("-c", "--corp-entries",
                        default="../guessing/r-guesser.fst",
                        help="fst composed out of a word list fst and a guesser fst")
argparser.add_argument("-u", "--unique", type=int, default=0,
                        help="if > 0 then accept an entry which has a sufficient set of word forms in corpus")
args = argparser.parse_args()

guesser_fil = hfst.HfstInputStream(args.guesser)
guesser_fst = guesser_fil.read()
guesser_fil.close()
guesser_fst.invert()
guesser_fst.minimize()
guesser_fst.lookup_optimize()

def unique_entry(word_forms):
    remaining = {0}
    first = True
    for word_form in word_forms:
        entries_and_weights = guesser_fst.lookup(word_form, output="tuple")
        entries = set()
        for e,w in entries_and_weights:
            entries.add(e)
        if remaining == {0}:
            remaining = entries
        else:
            remaining = remaining & entries
        if not remaining:
            break
    return remaining

corp_fil = hfst.HfstInputStream(args.corp_entries)
corp_fst = corp_fil.read()
corp_fil.close()
corp_fst.minimize()
corp_fst.lookup_optimize()

def check_corp(entry, word_form):
    result = corp_fst.lookup(entry, output="tuple")
    corp_words = [wd for wd,wg in result]
    word_form_set = set(corp_words)
    word_form_set.add(word_form)
    word_forms = list(word_form_set)
    #entries = unique_entry(word_forms)
    return word_forms

def nextline():
    linenl = sys.stdin.readline()
    if not linenl:
        exit()
    return linenl.strip()

print("\nENTER FORMS OF A WORD:\n")
while True:
    word_form = nextline()
    res = guesser_fst.lookup(word_form, output="tuple")
    remaining = set()
    weight = {}
    for r,w in res:
        remaining.add(r)
        weight[r] = w
    dic = {}
    for entry in remaining:
        words = check_corp(entry, word_form)
        if args.unique > 1:
            print(' '*8, entry, words)
        dic[entry] = set(words)
    di = list(dic.items())
    ce_list = [(e, ws) for (e, ws) in di if ws]
    max_len = max([len(ws) for e,ws in ce_list])
    #print("celist:", ce_list)###
    best_len = -1
    i = 0
    entry_list = []
    for e, ws in ce_list:
        ents = unique_entry(list(ws))
        if len(ents) == 1:
            if len(ws) > best_len:
                best_len = len(ws)
                best_ent = e
            i = i + 1
            entry_list.append((e,ws))
            print(" "*4+"(", i, ") <<", e, ">>", ", ".join(list(ws)))
    if args.unique > 0 and best_len >= max_len:
        remaining = set([best_ent])
    else:
        print(" "*8, [(e, weight[e]) for e in remaining])
    while len(remaining) > 1:
        line = nextline()
        if line == "":
            print("GIVING UP THIS WORD\n\n")
            break
        if line[0] == '-':
            res = guesser_fst.lookup(line[1:], output="tuple")
        else:
            res = guesser_fst.lookup(line, output="tuple")
        entries = set([r for r,w in res])
        saved = remaining
        if line[0] == '-':
            remaining = remaining - entries
        else:
            remaining = remaining & entries
        if not remaining:
            print("DOES NOT FIT! IGNORED.")
            remaining = saved
        elif len(remaining) > 1:
            print(" "*8, [(e, weight[e]) for e in remaining], "\n")

    if len(remaining) == 1:
        e = list(remaining)[0]
        print("\n" + "="*18)
        print(e, ";", weight[e])
        print("="*18 + "\n")
