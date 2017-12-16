"""lookuptest.py

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

import hfst, sys

fil = hfst.HfstInputStream('guesser.fst')
fst = fil.read()
print("\nENTER FORMS OF A WORD:\n")
while True:
    remaining = set()
    first = True
    while True:
        linenl = sys.stdin.readline()
        if not linenl: exit()
        line = linenl.strip()
        if line == "":
            print("GIVING UP THIS WORD\n\n")
            break
        if line[0] == '-':
            res = fst.lookup(line[1:], output="tuple")
        else:
            res = fst.lookup(line, output="tuple")
        entries = set()
        for r,w in res:
            entries.add(r)
        if first:
            first = False
            remain = entries
        elif line[0] == '-':
            remain = remaining - entries
        else:
            remain = remaining & entries
        if len(remain) == 1:
            print("\n" + "="*18)
            print(list(remain)[0], ";")
            print("="*18 + "\n")
            break
        elif len(remain) == 0:
            print("DOES NOT FIT! IGNORED.")
        else:
            print("        ", remain)
            remaining = remain



