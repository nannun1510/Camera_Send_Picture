"""
Server receiver of the file
"""
import socket
import tqdm
import os
import threading

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 4466
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
SERVER_DATA_PATH = "server_data"

def pls(client_socket,address):
    print(f"[+] {address} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    #print (filename)
    filename = os.path.basename(filename)
    filename = os.path.join(SERVER_DATA_PATH, filename)
    #print
    filesize = int(filesize)
    print (filename)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break

            f.write(bytes_read)
            progress.update(len(bytes_read))
    f.close
    client_socket.close
def main():
    #s = socket.socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen()
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    
    
    while(True): 
        client_socket, address = s.accept() 
        #pls(client_socket)
        thread = threading.Thread(target=pls,args=(client_socket,address))
        thread.start()

if __name__ == "__main__":
    main()