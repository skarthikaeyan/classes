#!usr/bin/python3
"""Imported server Module"""

import server as s
try:
    CS = s.StartServer()

    CS.socketbind()
    CS.validate()
except KeyboardInterrupt as k:
    print('\n Thank you', )
