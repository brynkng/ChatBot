#!/usr/bin/python
import os
import sys
import fnmatch

for root, dirnames, filenames in os.walk('.'):
    if fnmatch.filter(filenames, '*.py'):
        sys.path.append(root)