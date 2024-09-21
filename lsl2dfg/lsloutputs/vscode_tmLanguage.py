#!/usr/bin/env python

import sys

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  constants_integer = []
  constants_string = []
  constants_float = []
  constants_compound = []
  events = []
  functions = []
  invalids = []
  for element in document:
    if 'status' not in element or element['status'] == 'normal':
      if element["cat"] == "constant":
        if element["type"] == "integer":
          constants_integer.append(element)
        elif element["type"] == "string":
          constants_string.append(element)
        elif element["type"] == "float":
          constants_float.append(element)
        elif element["type"] in ["vector", "rotation"]:
          constants_compound.append(element)
      elif element["cat"] == "event":
        events.append(element)
      elif element["cat"] == "function":
        functions.append(element)
    else:
        invalids.append(element)

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
      if "[@--$valid_constants_integer--@]" in line:
        line = line.replace("[@--$valid_constants_integer--@]", "(" + "|".join(map(lambda x: x["name"], constants_integer)) + ")")
      elif "[@--$valid_constants_string--@]" in line:
        line = line.replace("[@--$valid_constants_string--@]", "(" + "|".join(map(lambda x: x["name"], constants_string)) + ")")
      elif "[@--$valid_constants_float--@]" in line:
        line = line.replace("[@--$valid_constants_float--@]", "(" + "|".join(map(lambda x: x["name"], constants_float)) + ")")
      elif "[@--$valid_constants_compound--@]" in line:
        line = line.replace("[@--$valid_constants_compound--@]", "(" + "|".join(map(lambda x: x["name"], constants_compound)) + ")")
      elif "[@--$valid_events--@]" in line:
        line = line.replace("[@--$valid_events--@]", "(" + "|".join(map(lambda x: x["name"], events)) + ")")
      elif "[@--$valid_functions--@]" in line:
        line = line.replace("[@--$valid_functions--@]", "(" + "|".join(map(lambda x: x["name"], functions)) + ")")
      elif "[@--$invalids--@]" in line:
        line = line.replace("[@--$invalids--@]", "(" + "|".join(map(lambda x: x["name"], invalids)) + ")")
      elif "[@--$version--@]" in line:
        line = line.replace("[@--$version--@]", databaseversion)

      outf.write(line)

  finally:
    if outfilename is not None:
      outf.close()

pass
