import os
import argparse
import distutils.filelist as fu

parser = argparse.ArgumentParser()

parser.add_argument('--pkg', help="top level python package dir")
args = parser.parse_args()
modules = []
found = fu.findall(args.pkg)
os.system("cat /dev/null >> README.md")

for x in found: 
    if '__' not in x and '.pyc' not in x and '.py' in x: 
        os.system("pydoc3 {} >> README.md".format(x))