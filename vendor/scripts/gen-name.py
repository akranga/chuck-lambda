#!/usr/bin/env python

import  random, os

def random_line_from_stream(afile):
  line = next(afile)
  for num, aline in enumerate(afile):
    if random.randrange(num + 2): continue
    line = aline
  return line

def random_line(filename):
  with open( filename, 'r') as stream:
    return random_line_from_stream(stream)

script_dir = os.path.dirname( os.path.realpath(__file__) )

adj  = random_line(script_dir + os.sep + 'names/adjectives.txt').strip()
noun = random_line(script_dir + os.sep + 'names/nouns.txt').strip()

name =  adj + "-" + noun

print "Like this name? \n\n {} \n\nThen enter command \n $ export ENV={} \n".format(name, name)
