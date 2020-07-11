import socket
from threading import Thread
from package.server import *
from package.client import Account

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080         # Port to listen on (non-privileged ports are > 1023)


# generate list of accounts
accounts = generateAccounts()
sessions = []

if __name__ == "__main__":
    server = createServer(HOST, PORT)
    server.listen(5)  # listens for 5 connections at max
    print('Serving on port ', PORT)

    ACCEPT_THREAD = Thread(target=accept_connection,
                           args=(server, accounts,))
    ACCEPT_THREAD.start()   # Starts the infinite loop.
    ACCEPT_THREAD.join()    # Wait until all thread terminate
    server.close()
