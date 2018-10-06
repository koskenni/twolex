all:  guesser.fst ksk-lemmatizer.fst

fin-pat-conv.lexc: fin-pat.csv pat-proc.py affixmultich.py
	python3.6 pat-proc.py -p fin-pat.csv > $@

fin-conv.fst: fin-pat-conv.lexc
	hfst-lexc -E -f openfst-tropical $< | hfst-minimize -E -o $@

fin-pat-guess.lexc: fin-pat.csv pat-proc.py affixmultich.py
	python3.6 pat-proc.py -m g -p fin-pat.csv > $@

affix-guess.lexc: affixes-v.csv affix-guesser.py
	python3.6 affix-guesser.py < affixes-v.csv > affix-guess.lexc

fin-guess-lex.fst: fin-pat-guess.lexc affix-guess.lexc
	hfst-lexc -E -f openfst-tropical fin-pat-guess.lexc affix-guess.lexc | hfst-minimize -E -o $@

fin-guess.fst: fin-guess-lex.fst rul.m2s.fst delete.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E -o $@

guesser.fst: fin-guess.fst
	hfst-invert -i $< | hfst-minimize -E | hfst-fst2fst -w -o $@

rul.m2s.fst: rul.m2s.twolc
	hfst-twolc -f openfst-tropical < $< -D -o $@

ksk-words.lexc: ~/Dropbox/lang/fin/ksk/ksk-v.dic ksk2lexc.py fin-conv.fst affixmultich.py
	python3.6 ksk2lexc.py -l $@ < $< > ksk-words.log

ksk-lex.fst: ksk-words.lexc affix-analys.lexc
	hfst-lexc -E -f openfst-tropical $< affix-analys.lexc | hfst-minimize -E -o $@

ksk-analys.fst: ksk-lex.fst rul.m2s.fst delete.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E | hfst-invert -o $@ 

ksk-lem.fst: ksk-analys.fst rul.m2s.fst delete.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E -o $@

ksk-lemmatizer.fst: ksk-lem.fst
	hfst-fst2fst -w -i $< -o $@

affix-analys.lexc: affixes-v.csv affix-analys.py
	python3.6 affix-analys.py < affixes-v.csv > $@

affixmultich.py: affixes-v.csv collect-multich.py
	python3.6 collect-multich.py

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -f openfst-tropical -o delete.fst

samp-words.lexc: ksk-v-samp.dic ksk2lexc.py fin-conv.fst affixmultich.py Makefile
	python3.6 ksk2lexc.py -l $@ < $< 

samp-lex.fst: samp-words.lexc affix-analys.lexc
	hfst-lexc -E -f openfst-tropical -o $@ samp-words.lexc affix-analys.lexc

samp-analys.fst: samp-lex.fst rul.m2s.fst delete.fst affixmultich.py Makefile
	hfst-compose-intersect -1 samp-lex.fst -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E > $@
	hfst-invert -i $@ -o samp-lookup.fst

samp-lem.fst: samp-lookup.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst -o $@
