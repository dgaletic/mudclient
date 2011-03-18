#!/usr/bin/env python

import telnetlib 
import thread
import zlib
import time

COMPRESS = chr(85)
COMPRESS2 = chr(86)

compressor = None
session = telnetlib.Telnet()

def tcallback(tsocket, tcommand, toption):
    print "WE GOT SOMETHIN"
    print "Command: ", ord(tcommand)
    print "Option: ", ord(toption)
    if tcommand == telnetlib.WILL:
        if toption == COMPRESS2:
            print "We got a COMPRESS2 request from the server"
            # respond to the server that we accept
            tsocket.send(telnetlib.IAC + telnetlib.DO + COMPRESS2)

    elif tcommand == telnetlib.SB:
        print "IAC SB, I wonder what we're negotiating"
        # we'll find out when we get IAC SE and read the sb_data!

    elif tcommand == telnetlib.SE:
            print "IAC SE"
            # Now, call the Telnet.read_sb_data() to figure what happened.
            sb_data = session.read_sb_data()
            print "sb_data:", sb_data
            # if that data is COMPRESS2, encrypted stream immediately follows
            if sb_data == COMPRESS2:
                compressor = zlib.decompressobj()

            pass

def inputter(conn):
    text = ""
    while text != "quit":
        text = raw_input() + "\n"
        conn.write(text)
        
# Start this as a new thread!
def outputter(conn):
    import time
    try:
        while(True):
            text = conn.read_very_eager()
            if text:
                # Any way to stop print from printing anything
                # after it prints text?
                if compressor:
                    text = compressor.decompress(text)
                print text,
                text = None 
            time.sleep(0.1)
    except EOFError:
        print "So this is goodbye..."
        return

host = "discworld.atuin.net"
port = 4242

session.set_option_negotiation_callback(tcallback)
session.open(host, port)

thid = thread.start_new_thread(inputter, (session,))
outputter(session)    
