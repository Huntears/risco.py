#!/usr/bin/env python

"""example.py:
Provides an example for the use of risco.py
"""

from risco import Risco

def main():
    riscoapi = Risco()
    pin = 0000
    siteid = 000000
    riscoapi.authenticate("email", "password", pin, siteid)

if __name__ == "__main__":
    main()