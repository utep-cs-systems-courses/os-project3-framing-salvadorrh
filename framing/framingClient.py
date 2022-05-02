#! /usr/bin/env python3

# Framing client program
# Based on Dr. Freudenthal's echoClient.py
import socket, sys, re
sys.path.append("../lib") # For parameters. Python paths. For interpreter to search.
import params
import archiver

print("****** Attempting to create Client ******")

switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-d', '--delay'), 'delay', "0"),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

progname = "framingClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server) # Split string by the occurrences of the pattern
    serverPort = int(serverPort)
except:
    print("\tCan't parse server: port from '%s'" % server)
    sys.exit(1)

s = None # Creating socket

# getaddrinfo translates the host and port arguments into a sequence of tuples that contains
# all of the necessary information to create a socket.
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("\tCreating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto) # Creates an object of type socket
    except socket.error as msg:
        print(" ERROR: %s" % msg)
        s = None
        continue
    try:
        print("Attempting to connect to %s" % repr(sa))
        # Connects a TCP based client socket to TCP based server socket. Socket Address
        s.connect(sa)
    except socket.error as msg:
        print("\tError: %s" % msg)
        s.close()
        s = None
        continue
    break

# Failed in connecting to port with socket
if s is None:
    print("\tCould not open socket.")
    sys.exit(1)


    
delay = float(paramMap['delay']) # Delay before reading (default is 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(int(delay))
    print("Done sleeping.")

while 1:
    user_response = input("Terminate Client? (Y/N) ")
    if user_response == "Y":
        print("Terminating client!")
        s.send("Terminate".encode())
        break
    else:
        s.send("Continue!".encode())
        
    files_to_send = input("What files do you want to send? ")
    files_to_send = files_to_send.split()
    data = archiver.create_archiver(s, files_to_send)
    s.send(data)

    from_server = s.recv(1024).decode()
    print("Received: '%s'" % data)

s.send("Terminating Client!!".encode())
#while 1:
#    data = s.recv(1024).decode()
 #   print("Received: '%s'" % data)
  #  if len(data) == 0:
   #     break

print("\tZero length read. Closing. :)") # Finished reading
s.close()
