#! /usr/bin/env python3

# File Server program

import socket, sys, re, os, time
import threading
import archiver

sys.path.append("../lib") # For parameters. Python paths. For interpreter to search.

import params  

print("****** Creating Server ******")

switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

progname = "framingServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''      # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

# Creates server socket
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.bind((listenAddr, listenPort))  # Connect your socket through a port
server_s.listen(4) # Allow only one outstanding request
# server_s is a factory for connected sockets

files_open = set() # Lock to not repeat files

# Waiting for file to not be used
def wait_for_file(file_name):
    while file_name in files_open:
        print("Wait 5s. File in used: %s" % file_name)
        time.sleep(5)
        

def client_handler(conn, address):
    print("Connect by address: ", address)
    conn.send("Trying to receive files!!".encode())
    #num_archived_files = conn.recv(2).decode()
    #print("Number of files: %s" % str(num_archived_files))
    #num_archived_files = int(num_archived_files)
    #if num_archived_files == 1:
    #    print("Correct number of files")

    first = False
    while 1:
        cont = conn.recv(9).decode()
        if cont == "Continue!":
            print("\nContinue Client!")
        elif cont == "Terminate":
            print("Terminate Client!")
            break
        else:
            print("ERROR")

        num_archived_files = conn.recv(2).decode()
        print("Number of files: %s" % str(num_archived_files))
        num_archived_files = int(num_archived_files)
            
        while num_archived_files:
            if first:
                conn.recv(1)
            first = True
            len_name_file = int(conn.recv(6).decode())
            print("Len of name: %s" % str(len_name_file))
            name_file = conn.recv(len_name_file).decode()
            print("Name of file: %s" % str(name_file))

            wait_for_file(name_file)
            files_open.add(name_file)

            num = 1
            while os.path.exists(str(num) + "-output-" + name_file):
                num += 1
        
            len_file = int(conn.recv(15).decode())
            print("Len of file: %s" % str(len_file))

            new_name_file = str(num) + "-output-" + name_file
            fd = os.open(new_name_file,os.O_CREAT | os.O_WRONLY)
        
            while len_file > 512:
                data = conn.recv(512)
                #print(data.decode())
                os.write(fd, data)
                len_file -= 512

            data = conn.recv(len_file)
            # print(data.decode())
            os.write(fd, data)
            files_open.remove(name_file)
            print("Removing file: %s" % name_file)
            conn.send("\nFile received:".encode() + name_file.encode())
            num_archived_files -= 1
            print("Finishing with file: %s\n" %new_name_file)
        break
            

    print("\n*****End of Client handler*****\n")
    conn.send("\nTerminated Client succesfully!!".encode())
    #conn.shutdown(socket.SHUT_WR)

accept = 0

while accept < 4:
    conn, address = server_s.accept() # Wait until incoming connection request (and accept it)
    # Thread will start function with arguments. THread becomes server
    thread = threading.Thread(target=client_handler, args=(conn, address))
    thread.start()
    accept += 1
