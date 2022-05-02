#! /usr/bin/env python3

import os, sys, re
import socket

def create_archiver(archive, files):
    data = bytearray()
    print("FILES:")
    print(files)
    data += f'{len(files):02}'.encode()
    print("Number of files")
    print(data)
    if isinstance(archive, socket.socket):
        archive.send(data)
        print("Sending data through socket")
    else:
        archive.write(data)
    for file_name in files: # Get command files except for comman\d executing
        data += add_file(archive, file_name)
    return data
        
def add_metadata(archive, file_name, data):
    metadata = bytearray()
    metadata += f'{len(file_name):06}'.encode() + file_name.encode()
    metadata += f'{len(data):015}\n'.encode()
    return metadata
        
def add_file(archive, file_name):
    # Metadata and then data
    data = bytearray()
    try:
        with open(file_name, "rb") as file:
            data += file.read()
    except:
        os.write(1, ("No file exists with the name: %s!!" % file_name).encode())

    meta_data = add_metadata(archive, file_name, data)
    data = meta_data + data
    
    if isinstance(archive, socket.socket):
        archive.send(data)
        print("Sending data through socket")
    else:
        archive.write(data)

    return data
    
def unarchive(archive):
    # something else
    print(archive)
    

def main():
    num = 1
    data = bytearray()
    while os.path.exists("archiver" + str(num)):
        num += 1
        
    # Create archiver
    with open("archiver" + str(num), 'ab') as archive:
        files = sys.argv[1:]  # Get command files except for command executing
        data = create_archiver(archive, files)

    return data
    #unarchive(archive)
        
if __name__ == "__main__":
    main()
