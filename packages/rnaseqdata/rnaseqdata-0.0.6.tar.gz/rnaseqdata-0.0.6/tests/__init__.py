import os
import sys

tests_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(tests_dir, 'data')
TMP_DIR = os.path.join(DATA_DIR, 'tmp')
if not os.path.isdir(TMP_DIR):
    os.mkdir(TMP_DIR)