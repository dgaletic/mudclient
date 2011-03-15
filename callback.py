telnetlib.COMPRESS = 85
telnetlib.COMPRESS2 = 86

def callback(tsocket, tcommand, toption):
    if tcommand == telnetlib.WILL:
        if toption == telnetlib.COMPRESS2:
            # set the global compression object
            # respond to the server that we accept
# the server may begin compression at any time by sending a 
# IAC SB COMPRESS2 IAC SE sequence, immediately followed by the start # of the compressed stream. 
            pass
    if tcommand == telnetlib.SB:
        if toption == telnetlib.COMPRESS2:
            # read the next thing, if it's IAC SE, we're compressed!
            pass
