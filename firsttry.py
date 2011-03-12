def inputter(conn):
    text = ""
    while text != "quit":
        text = raw_input()
        conn.write(text + "\n")
        
# Start as a new thread!
def outputter(conn):
    import time
    try:
        while(True):
            text = conn.read_very_eager()
            if text != "":
                # Any way to stop print from printing anything
                # after it prints text?
                print text,
                text = ""
            time.sleep(0.1)
    except EOFError:
        print "So this is goodbye..."
        return

import telnetlib 
import thread

session = telnetlib.Telnet()

host = "discworld.atuin.net"
port = 4242

session.open(host, port)


thid = thread.start_new_thread(outputter, (session,))

inputter(session)    
