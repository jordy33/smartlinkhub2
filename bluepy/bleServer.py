from btle import Peripheral,BTLEException
import struct
import math
import pexpect
import binascii
import socketserver
from threading import Thread

# https://gist.github.com/tsuna/1563257
elements=["f1:99:d1:ce:d9:1d random","de:2d:06:53:4b:ad random"]

class service(socketserver.BaseRequestHandler):
    def handle(self):
        data = 'dummy'
        isConnected=False
        print ("Client connected with: ", self.client_address)
        while len(data):
            data = self.request.recv(1024)
            #if len(data)!=0:  # If not null
            #    print("data [0]:",data[0])
            #    print("len data:",len(data))    
            if len(data)!=0 and data[0]==99 and isConnected==False:  #Connect command
                if data[1]>=48 and data[1]<=57:
                    try:
                        bleconn = Peripheral(elements[data[1]-48])
                    except BTLEException as e:
                        self.request.send(b'error connecting to device\r\n')
                        isConnected=False
                    else:
                        isConnected=True
                        self.request.send(b'connected\r\n')
            if len(data)!=0 and isConnected==True:
                cmd=data.rstrip(b'\r\n')
                print ("command:",cmd)
                if cmd!=b'':
                    try:
                        bleconn.writeCharacteristic(0x0011,cmd)
                    except BTLEException as e:
                        isConnected=False
                        self.request.send(b'error writing to device\r\n')
                    else:
                        isConnected=True
                        self.request.send(b'ok\r\n')
            if len(data)!=0 and isConnected==True and data[0]==100:
                cmd=data.rstrip(b'\r\n')
                print ("command:",cmd)
                if cmd!=b'':
                    bleconn.disconnect()
                    self.request.send(b'disconnected\r\n')
                    isConnected=False
        print("Client exited")
        if isConnected==True:
            bleconn.disconnect()
        self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    # activate bluetooth
    resp=pexpect.spawn('hciconfig hci0 up')
    resp.expect('.*')
    print ("Smartlink Server started at port 1520")
    server=ThreadedTCPServer(('',1520), service)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
