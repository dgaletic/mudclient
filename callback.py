COMPRESS = chr(85)
COMPRESS2 = chr(86)

import zlib
import telnetlib
import time

compressor = None

def tcallback(tsocket, tcommand, toption):
    print "WE GOT SOMETHIN"
    print "Command: ", ord(tcommand)
    print "Option: ", ord(toption)
    if tcommand == telnetlib.WILL:
        if toption == COMPRESS2:
            print "We got a COMPRESS2 request from the server"
            # respond to the server that we accept
            # TODO: Is this ok? Server doesn't respond to it by
            # sending IAC SB COMPRESS2 IAC SE
            tsocket.send(telnetlib.IAC + telnetlib.DO + COMPRESS2   )

# the server may begin compression at any time by sending a 
# IAC SB COMPRESS2 IAC SE sequence, immediately followed by the start # of the compressed stream. 
    elif tcommand == telnetlib.SB:
        print "IAC SB"
        if toption == COMPRESS2:
            # After IAC DO COMPRESS2, server responds by
            # 250 0 240 0 instead of 250 86 240 0(SB COMPRESS2) 
            print "Server says: Next thing be compressed."
            # compressor = zlib.compressobj()
            # Actually the next thing will be IAC SE, but 
            # that is caught by the callback, not the displaying func.
            pass
    elif tcommand == telnetlib.SE:
            print "IAC SE; (hackish) starting compression now"
            compressor = zlib.compressobj()
            # Nothing for now.
            pass

