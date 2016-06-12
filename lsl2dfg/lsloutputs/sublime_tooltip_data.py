#!/usr/bin/env python

# sublime.py - This is a LSL2dfg.py output module that outputs all the
# functions, events and constants in the database with their signatures,
# types and values.

import sys

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  def get_signature(element):
    sign = "\"{name}\": \"Function: {type} {name}("\
      .format(name=element["name"], type=element["type"] if element.has_key("type") else "void")
    first = True
    if "params" in element:
      cnt = 1;
      for param in element["params"]:
        if first:
          first = False
        else:
          sign = sign + ", "
        sign = sign + "{type} <a href=\\\"http://wiki.secondlife.com/wiki/{name}\\\">{name}</a>".format(idx=cnt, name=param["name"], type=param["type"])
        cnt += 1;
    sign = sign + ");"
    try:
      desc = element["desc"]["en"]["text"].replace('\n', '<br>').replace('"', '\\\"')
      sign = sign + "<p>{desc}</p>".format(desc=desc)
    except KeyError:
      sign = sign + "<p>[no description]</p>"
    sign = sign + "<p>{delay} Forced Delay, {energy} Energy</p>"\
      .format(delay=float(element["delay"]), energy=float(element["energy"]))
    sign = sign + "\""
    return sign

  # starting main sequence here

  functions = []
  for element in document:
    if 'status' not in element or element['status'] == 'normal':
      if element["cat"] == "function":
        functions.append(element)
  functions.sort(lambda x,y: cmp(x["name"],y["name"]))

  if infilename is not None:
    inf = open(infilename, "r")
  else:
    inf = sys.stdin

  try:
    inputlines = inf.readlines()

  finally:
    if infilename is not None:
      inf.close()

  if outfilename is not None:
    outf = open(outfilename, "w")
  else:
    outf = sys.stdout

  try:

    for line in inputlines:
      if not line.startswith("<<< LINES >>>"):
        outf.write(line)
      else:
        outf.write("\t")
        outf.write(",\n\t".join([get_signature(element) for element in functions]).encode('utf8'))
        outf.write("\n")

  finally:
    if outfilename is not None:
      outf.close()

pass