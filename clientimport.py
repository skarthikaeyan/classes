"""Importing client Package"""
import multiclient as mc
try:
    HOST = '192.168.1.5'
    PORT = 10000

    CLIENTOBJ = mc.StartClient(HOST, PORT)

    CLIENTOBJ.startconnection()
    CLIENTOBJ.startchat()
except KeyboardInterrupt as k:
    print("Thank you", )
