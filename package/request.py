class Request(object):
    def __init__(self, request):
        header_end = -1
        while header_end == -1:
            header_end = request.find('\r\n\r\n')   # indicate where header off
            header_string = request[:header_end]
            # content carried stands behind header + \r\n\r\n (+4)
            self.data = request[header_end + 4:]
            string_list = header_string.split(' ')

            self.method = string_list[0]
            self.path = string_list[1]

            self.headerLines = header_string.split(  # header lines = request - request lines
                '\r\n', 1)[1]

            if(self.headerLines.find('Cookie: logged=') != -1):  # if cookie keyword in header
                self.cookie = self.headerLines[-1]
            else:
                self.cookie = ''
