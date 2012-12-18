#!/usr/bin/env python

from commands import getoutput
import socket
from SocketServer import TCPServer, StreamRequestHandler
import sys

#election and snapshot vars
number = 4
result = ""

#host list:
nodes = []
port = ""
hostname = ""

class Handler(StreamRequestHandler):
    def handle(self):
        msg = self.rfile.readline().strip().lower()
        if (msg == 'snapshot'):
            snapshot()
            map (notify, outgoing)

def run_server(port=19835):
    serv = TCPServer(('', port), Handler)
    serv.allow_reuse_address = True
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print 'interrupted...'
    finally:
        serv.socket.close()

def snapshot():
    print 'Taking snapshot'
    
    #get data from outside
    hostname = getoutput('hostname')
    date = getoutput('date +%d%m%Y')
    uptime = getoutput('uptime').strip()

    filename = hostname + '-' + date + '.txt'
    print 'writing to', filename
    f = open(filename, 'w')
    wpair (f, 'number', number)
    wpair (f, 'result', result)
    wpair (f, 'hostname', hostname)
    wpair (f, 'time', '"'+uptime+'"')
    f.close()

def wpair(f, key, val):
    f.write (key+' = '+str(val)+'\n')

def notify(host):
    print 'Notifying', host
    port = 19835
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send("snapshot\n")
    s.close()

def readconf():
    global hosts, port, hostname
    with open("nodes") as fn: nodes = fn.readlines()
    with open("port") as fp: port = fn.readline()
    hostname = getoutput('hostname')
    print nodes, port, hostname

def main():
    global outgoing
    outgoing = sys.argv[1:]
    run_server()

if __name__ == "__main__":
    main()
