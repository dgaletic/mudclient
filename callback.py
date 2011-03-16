COMPRESS = chr(85)
COMPRESS2 = chr(86)

import zlib
import telnetlib

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
            tsocket.send(telnetlib.IAC)
            tsocket.send(telnetlib.DO)
            tsocket.send(COMPRESS2)
            tsocket.send("\n")

# the server may begin compression at any time by sending a 
# IAC SB COMPRESS2 IAC SE sequence, immediately followed by the start # of the compressed stream. 
    if tcommand == telnetlib.SB:
        if toption == COMPRESS2:
            # All right, we're compressing! So:
            # the next thing we receive will be compressed.
            # set the global compression object
            print "Server says: Next thing be compressed."
            compressor = zlib.compressobj()
            # Actually the next thing will be IAC SE, but 
            # that is caught by the callback, not the displaying func.
            pass
    if tcommand == telnetlib.SE:
            print "IAC SE"
            # Nothing for now.
            pass

