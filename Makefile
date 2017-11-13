all: samp-analys.fst samp-lem.fst converter.fst guesser.fst ksk-analys.fst

fin-pat-conv.lexc: fin-pat.csv fin-i2c.csv pat-proc.py affixmultich.py Makefile
	python3 pat-proc.py -p fin-pat.csv -c fin-i2c.csv > $@

fin-conv.fst: fin-pat-conv.lexc Makefile
	hfst-lexc $< | hfst-minimize -o $@

converter.fst: fin-conv.fst Makefile
	hfst-fst2fst -i $< -O -o $@

fin-pat-guess.lexc: fin-pat.csv fin-i2c.csv pat-proc.py affixmultich.py Makefile
	python3 pat-proc.py -m g -p fin-pat.csv -c fin-i2c.csv > $@

affix-guess.lexc: affixes-v.csv affix-guesser.py Makefile
	python3 affix-guesser.py < affixes-v.csv > affix-guess.lexc

fin-guess-lex.fst: fin-pat-guess.lexc affix-guess.lexc
	hfst-lexc -o $@ fin-pat-guess.lexc affix-guess.lexc

fin-guess.lexc: fin-pat.csv fin-pat.csv pat-proc.py Makefile
	python3 pat-proc.py -m g -p fin-pat.csv -c fin-i2c.csv > $@

fin-guess.fst: fin-guess-lex.fst rul.m2s.fst delete.fst Makefile
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -o $@

guesser.fst: fin-guess.fst Makefile
	hfst-invert -i $< | hfst-minimize | hfst-fst2fst -O -o $@

rul.m2s.fst: rul.m2s.twolc
	hfst-twolc < $< -D -o $@

samp-words.lexc: ksk-v-samp.dic ksk2lexc.py converter.fst affixmultich.py Makefile
	python3 ksk2lexc.py -l $@ < $< 

samp-lex.fst: samp-words.lexc affix-analys.lexc
	hfst-lexc -o $@ samp-words.lexc affix-analys.lexc

samp-analys.fst: samp-lex.fst rul.m2s.fst delete.fst affixmultich.py Makefile
	hfst-compose-intersect -1 samp-lex.fst -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize > $@
	hfst-invert -i $@ -o samp-lookup.fst

samp-lem.fst: samp-lookup.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst -o $@

ksk-words.lexc: ~/Dropbox/lang/fin/ksk/ksk-v.dic ksk2lexc.py converter.fst affixmultich.py Makefile
	python3 ksk2lexc.py -l $@ < $< 

ksk-lex.fst: ksk-words.lexc affix-analys.lexc
	hfst-lexc -o $@ $< affix-analys.lexc

ksk-analys.fst: ksk-lex.fst rul.m2s.fst delete.fst Makefile
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize > $@
	hfst-invert -i $@ -o ksk-lookup.fst

ksk-lem.fst: ksk-lookup.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst -o $@

affix-analys.lexc: affixes-v.csv affix-analys.py
	python3 affix-analys.py < affixes-v.csv > $@

affixmultich.py: affixes-v.csv collect-multich.py
	python3 collect-multich.py

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -o delete.fst
