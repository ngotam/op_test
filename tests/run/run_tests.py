import os
import sys

print (sys.path)

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

__author__ = 'asanghavi'


import argparse

from core_framework import core_lib

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument('-file', nargs=1)
    opts = ap.parse_args()
    my_dir = sys.argv[0]
    print("Curr dir is %s" %my_dir)
    my_info = my_dir.split('/')
    driver_info = my_info[-1]
    print(my_info)

    core_lib.run_tests()




