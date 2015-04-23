# python
import random, sys

"""
Randomizes the lines in a file
"""

if __name__ == '__main__':
    if(len(sys.argv) <= 1):
        print "FIle Name Required"
        sys.exit(0)

    lines = open(sys.argv[1]).readlines()
    random.shuffle(lines)
    open(sys.argv[1], 'w').writelines(lines)
