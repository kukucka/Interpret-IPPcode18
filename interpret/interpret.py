#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO nechat nebo ne header
import xml.etree.ElementTree as ET
# EXTENSION STATI
# TODO poruseni formatu textu, udelat to pres catch?
# TODO je validni kdyz mam napirklad
# TODO replace zase nejaky special znaky z XML
# TODO chytit pripadne error z TE.parse
# TODO zkontrolovat jestli jsou spravne \xxx v interpretu i v parseru
# TODO READ Type je to string?
# TODO LF muzeme vlozit i kdyz je nedefinovany
# TODO  WRITE: jak ma koncit radek vypisu write EOL nebo ne
# TODO pokud je type="   string   " tak to neni validni ma to tak byt?
# TODO stringy muzou tam byt mezery nebo ne v XML
# TODO osetrit maximalni velikost integeru
# TODO whitespace nesmi byt e stringu
# TODO neexistujici soubor?
import argparse

import sys

from classes.Analyzer import Analyzer
from classes.Execute import Execute
# print("Heelllo")
# tree = ET.parse('C:\Interpret-IPPcode18\interpret\')
# root = tree.getroot()
# print(chr(40960) + 'abcd' + chr(240))
# print(ord('A'))
try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', '-s', type=str, dest='file', help='file containing XML')
    parser.add_argument('--insts', action="store_true", help='Print out amount of executed instructions.')
    parser.add_argument('--vars', action="store_true", help='Print max amount of variables initialized at once.')
    parser.add_argument('--stats', type=str, dest='stat_file', help='Print statistic based of argumentst to set file.')
    args = parser.parse_args()
    if args.file == None:
        exit(10)
    elif args.file == '':
        exit(10)
    else:
        file = args.file
except Exception as ex:
    print(type(ex))
    print(ex)
    exit(10)

if args.stat_file == None:
    statExist = False
elif args.stat_file == '':
    statExist = False
else:
    statExist = True

if not statExist:
    if args.insts or args.vars:
        exit(10)

if args.insts and args.vars:
    i = 0
    for value in sys.argv:
        if value == '--insts':
            insts_position = i
        elif value == '--vars':
            vars_position = i
        i += 1

cl = Analyzer(file)
dicOfVar = cl.analyzeXmlFile()
s = Execute(dicOfVar)
s.start()

if statExist:
    output_file=open(args.stat_file, "w")
    if args.insts and args.vars:
        if insts_position < vars_position:
            output_file.write(str(s.get_executed_inst()) + "\n")
            output_file.write(str(s.get_max_var()))
        else:
            output_file.write(str(s.get_max_var()) + "\n")
            output_file.write(str(s.get_executed_inst()))
    elif args.vars:
        output_file.write(str(s.get_max_var()))
    elif args.insts:
        output_file.write(str(s.get_executed_inst()))
    output_file.close()
