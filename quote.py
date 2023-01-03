#!python3
import sys


for line in sorted(sys.stdin.readlines()):
    print(f"'{line.strip()}',")
