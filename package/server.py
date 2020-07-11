import socket
from threading import Thread
from package.client import Account
from package.request import Request

BUFFER_SIZE = 1024


def createServer(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    return server


def accept_connection(server, accounts):
    while True:
        connection, address = server.accept()
        handle_thread = Thread(target=handle_client,
                               args=(connection, accounts,))
        handle_thread.start()
        handle_thread.join()

        connection.close()


def load_File(fileName):
    try:
        # logout.html is a dummy file which tells us a logged-in user want to log out
        if(fileName == 'logout.html'):
            # redirect to index.html
            header = redirect_header('index.html')
            header += 'Set-Cookie: logged=0; path=/' + '\r\n'   # set cookie logged out
            fileContent = b''

        else:
            header = 'HTTP/1.1 200 OK\n'
            # check filename type
            if(fileName.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(fileName.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
            header += 'Content-Type: '+str(mimetype)+'\n\n'

            # open file , r => read , b => byte format
            file = open(fileName, 'rb')
            fileContent = file.read()
            file.close()

    except:
        # if open file failed or file's not found
        header = 'HTTP/1.1 404 Not Found\n\n'
        file = open('404.html', 'rb')
        fileContent = file.read()
        file.close()
    finally:
        return header, fileContent


def compare_un_pw(data, accounts):      # compare username and password
    header = 'HTTP/1.1 301 Moved Permanently' + '\r\n'  # redirect response header
    for account in accounts:
        data_string = 'name=' + account.getUsername() + '&pass=' + account.getPassword()
        if(data == data_string):        # if match in database => redirect to info page
            header += 'Location: /info.html' + '\r\n'
            header += 'Set-Cookie: logged=1; path=/' + '\r\n'    # set cookie to logged in
            return header.encode('utf-8')
    # else => redirect to 404 page
    header += 'Location: /404.html' + '\r\n'
    return header.encode('utf-8')


def redirect_header(newPath):           # return redirect header
    header = 'HTTP/1.1 302 Found' + '\r\n'
    header += 'Location: /' + newPath + '\r\n'
    return header


def handle_client(connection, accounts):
    try:
        # receive request from browser
        req = connection.recv(BUFFER_SIZE).decode('utf-8')
        request = Request(req)  # handle request
        if request:
            method = request.method
            if(method == 'GET'):
                # remove data after '?' in path
                myfile = request.path.split('?')[0]
                # Load index file as default
                if(myfile == '/'):
                    myfile = 'index.html'
                # use lstrip to remove '/' from file name
                myfile = myfile.lstrip('/')
                # load file
                header, response = load_File(myfile)
                final_response = header.encode('utf-8')
                final_response += response

                # if user've logged in
                if (request.cookie == '1'):
                    if(myfile == 'index.html'):  # auto redirect to info page
                        final_response = redirect_header(
                            'info.html').encode('utf-8')

                else:   # don't let user access to info page
                    if(myfile == 'info.html'):
                        # redirect to index page
                        final_response = redirect_header(
                            'index.html').encode('utf-8')   
                connection.send(final_response)

            elif(method == 'POST'):
                data = request.data
                response = compare_un_pw(data, accounts)    # compare form data
                connection.send(response)

        else:
            print('Client disconnected')

    except:
        print('Received request failed')
        connection.close()

# generate default database


def generateAccounts():
    account_list = []
    account_list.append(Account('admin', 'admin'))
    account_list.append(Account('18120514', 'ThienPhuc'))
    account_list.append(Account('BinhPhuong', '18120517'))
    return account_list
