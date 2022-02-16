from http import server
from socket import *
import sys
import hashlib

# establish TCP connection with server with handshake
def connect_to_server(serverName, serverPort, studentKey):
    clientSocket.connect((serverName, serverPort))
    handshakeRequestMsg = f"STID_{studentKey}"
    clientSocket.send((handshakeRequestMsg).encode())

def login_to_server(password):
    loginReqMsg = f"LGIN_{password}"
    clientSocket.send(loginReqMsg.encode())
    serverLoginResCode = clientSocket.recv(4)
    return serverLoginResCode

studentKey = sys.argv[1]

# create TCP socket for server
serverName = '137.132.92.111'
serverPort = 4444
clientSocket = socket(AF_INET, SOCK_STREAM)

connect_to_server(serverName, serverPort, studentKey)

# get response msg from server
serverMessageCode = clientSocket.recv(4)

# connected
if serverMessageCode == b'200_':
    # guess password
    for i in range(10000):
        length = b''
        password = '{0:04}'.format(i)
        serverLoginResCode = login_to_server(password)

        # if correct password
        if serverLoginResCode == b'201_':

            # request the file
            clientSocket.send('GET__'.encode())
            serverResponseCode = clientSocket.recv(4)

            while True:
                read_character = clientSocket.recv(1)
                if read_character == b'_':
                    break
                else:
                    length += read_character

            length = int(length.decode())
            data = clientSocket.recv(length)
        
            md5 = str(hashlib.md5(data).hexdigest())
            hexademicalHash = f"PUT__{md5}"

            # write hexadecimal hash to server
            clientSocket.send(hexademicalHash.encode())

            serverDataResCode = clientSocket.recv(4)

            if serverDataResCode == b'203_':
                length = b''
                clientSocket.send(b'LOUT_')
                serverLogoutResCode = clientSocket.recv(4)

                if serverLogoutResCode == b'202_':
                    continue
                else:
                    clientSocket.send(b'LOUT_')
        else:
            continue
        
clientSocket.send('BYE__'.encode())
