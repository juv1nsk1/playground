import socket, sys, string
from decimal import *

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

#Connect to remote server
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

#Now receive data
reply = s.recv(4096)

message = "list\n"
try :
    s.sendall(message)
except socket.error:
    print 'Send failed'
    sys.exit()

#Now receive data
reply = s.recv(4096)
lmod =  reply.split(" ")

for imod in lmod:
    reply=""
    print imod
    message = ("fetch %s\n" % imod)
    s.sendall(message)
    reply = s.recv(4096)
    for lkvs in reply.split("\n"):
        kvs= ""
        key= ""
        value= ""
        if lkvs.find(".value")>0:
            kvs = lkvs.split(".value")
            key=kvs[0]
            value=Decimal(kvs[1])
            print "modulo %s K: %s V: %d" % (imod,key,value)
