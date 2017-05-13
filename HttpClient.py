# -*- coding: utf-8 -*-
__author__ = 'MarioJ'

import socket
import time
import urlparse
import os

os.environ['no_proxy'] = '127.0.0.1,localhost'

# This Class is a generic abstration of a client http request
# it determines the url and port that socket will be connected
class Client(object):
    __AGENT = "HTTPTool/1.0"
    __TYPE = "application/x-www-form-urlencoded"
    __CRLF = '\r\n'

    def __init__(self, url):

        newUrl, port, params = self.parseUrl(url)

        url = urlparse.urlparse(newUrl)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = url.netloc
        self.path = url.path
        self.port = port
        self.params = params

        # connect to host and retrieve content
        self.connect()

    def parseUrl(self, url):

        try:
            # get the begin index from port number, for discovery if it is using token ':'
            indexInit = int(url.index(':', 5)) + 1
            # get the end index from port number, for discovery if it's using token '/' that indicate final
            indexEnd = int(url.index('/', indexInit))

            # Here we extract port number using two index above
            port = int(url[indexInit:indexEnd])

        except:
            print "Default Port"
            port = 80

        # Than replacing the port number found by '' for clear url
        url = url.replace(':' + str(port), '')

        try:

            # here we get the begin index where start the parameters pass to url
            indexInit = int(url.index('?')) + 1

            # then we extract params using found index above
            params = url[indexInit:]

            url = url.replace('?' + params, '')

        except:
            print "No params"
            params = ''

        return url, port, params


    def connect(self):
        self.socket.connect((self.host, self.port))
        print "Connected at %s port %s\n" % (self.host, self.port)

    def recv(self):

        data = ''
        part = None

        while part != '':
            part = self.socket.recv(1024)
            data += part

        return data

    def GET(self):
        self.socket.send('GET %s HTTP/1.1%sHost: %s%s' % (self.path, self.__CRLF, self.host, self.__CRLF + self.__CRLF))
        return self.recv()

    def POST(self):
        self.socket.send('POST %s HTTP/1.1%sHost: %s%sUser-Agent: %s%sContent-Type: %s%sContent-Length: %d%s%s' %
                         (self.path, self.__CRLF,
                          self.host, self.__CRLF, self.__AGENT, self.__CRLF, self.__TYPE, self.__CRLF, len(self.params),
                          self.__CRLF + self.__CRLF,
                          self.params))

        return self.recv()

    def close(self):
        self.socket.shutdown(1)
        self.socket.close()