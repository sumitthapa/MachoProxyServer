
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
import asyncio
import threading
import random
import time

thread_list = []
class S(BaseHTTPRequestHandler):
    
    print("\n\n\n ******* Main class ****** \n\n\n")

    def do_POST(self):
        processcount = random.randint(1,101)
        processcount = threading.Thread(target=self.sendlinktoserverPost,args=(self.path,processcount,))
        processcount.start()
        processcount.join()

    def do_GET(self):

        if self.path=='http://travelraga.com/':
            self.wfile.write("This page is blocked by Macho proxy Server".encode('utf-8'))
        else:
            if self.command=='GET':
                processcount = random.randint(1,101)
                processcount = threading.Thread(target=self.sendlinktoserver,args=(self.path,processcount,))
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print("\n Get requests URL : ",self.path,", Time :",current_time)
                processcount.start()
                processcount.join()
            else:
                print("error: Method not found") 

    def sendlinktoserver(self,url,processcount):
        s = requests.Session()
        r = s.request('GET',url) #<----sending GET Request 
        self.send_response(200)
        self.end_headers()
        self.wfile.write(r.content)
         # sumit is writing logs here >> start
        new_path = 'logs.txt'
        tid=threading.currentThread().ident
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        logdata="Thread ID :"+str(tid)+", Time :"+str(current_time)+"\n URL :"+str(self.path)+str(self.headers)+"Source Ip :"+str(self.client_address)+str(self.address_string())+", HTTP version :"+str(self.request_version)+", HTTP Method :"+str(self.command)+"\n"
        writelogfile = open(new_path,'a')
        writelogfile.write(logdata)

    def sendlinktoserverPost(self,url,processcount):
        self.send_response(200)
        self.end_headers()
        s = requests.Session()
        r = s.request('POST',url)
        self.wfile.write(r.content)
         # sumit is writing logs here >> start
        """new_path = 'logs.txt'
        tid=threading.currentThread().ident
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        logdata="Thread ID :"+str(tid)+", Time :"+str(current_time)+"\n URL :"+str(self.path)+str(self.headers)+"Source Ip :"+str(self.client_address)+str(self.address_string())+", HTTP version :"+str(self.request_version)+", HTTP Method :"+str(self.command)+"\n"
        writelogfile = open(new_path,'a')
        writelogfile.write(logdata)"""

             # << stop writing logs
        

def run(server_class=HTTPServer, handler_class=S, port=8070):
    logging.basicConfig(level=logging.INFO)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd on port 8070...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        
        
