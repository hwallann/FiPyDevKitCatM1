from network import LTE
import time
import re
import machine
import utime
import pycom

class StartIot():

    def __init__(self):
        print("self.lte = LTE()...")
        self.lte = LTE()
        print("Call initModem ...")
        self.initModem()


    # METHOD FOR PRETTY PRINTING AT COMMANDS
    def send_at_cmd_pretty(self, cmd):
        print("Sending: " + cmd)
        response = self.lte.send_at_cmd(cmd)
        if response != None:
            lines=response.split('\r\n')
            print("Response is:< ")
            for line in lines:
                if len(line.strip()) != 0:
                    print(line)
            print(">")
        else:
            print("Response is None...")
        return response

    # SETUP AND START THE MODEM - ATTACH TO THE NETWORK
    def initModem(self):
        print ("Starting modem...")
        self.send_at_cmd_pretty('AT+CFUN=0')
        self.send_at_cmd_pretty('AT+CGDCONT=1,"IP","mda.ee"')
        self.send_at_cmd_pretty('AT+CFUN=1')
        self.send_at_cmd_pretty('AT+CSQ')
        print("Wait 5 seconds...")
        # Waiting 12 seconds

        timer_start = utime.ticks_ms()
        while 0==0:
            if (utime.ticks_ms() - timer_start) > 5000:
                break
            machine.idle()

        self.send_at_cmd_pretty('AT+CSQ')
        print("Wait 5 seconds...")
        # Waiting 12 seconds

        timer_start = utime.ticks_ms()
        while 0==0:
            if (utime.ticks_ms() - timer_start) > 5000:
                break
            machine.idle()
        self.send_at_cmd_pretty('AT+CEREG?')


        print ("Waiting for attachement...")
        timer_start = utime.ticks_ms()
        while not self.lte.isattached():
            if (utime.ticks_ms() - timer_start) > 60000:
                machine.reset()
            machine.idle()
        else:
            print ("Attached, send AT+CGDCONT? to see the IP address")
            self.send_at_cmd_pretty('AT+CGDCONT?')
            self.send_at_cmd_pretty('AT+CEREG?')

    # CONNECT TO THE NETWORK
    def connect(self):
        if not self.lte.isattached():
            raise Exception('NOT ATTACHED... call initModem() first')
        print ("Waiting for connection...")
        self.send_at_cmd_pretty('AT+CEREG?')
        self.lte.connect()
        # Wait until we get connected to network
        while not self.lte.isconnected():
            machine.idle()
        print ("Connected!")

    # OPEN SOCKET AND SEND DATA
    def send(self, data):
        if not self.lte.isconnected():
            raise Exception('NOT CONNECTED')

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        IP_address = socket.getaddrinfo('172.16.15.14', 1234)[0][-1]
        print ("IP address: ", IP_address)
        s.connect(IP_address)
        print ("data is: ", data)
        s.send(data)
        s.close()

    def disconnect(self):
        if self.lte.isconnected():
            self.lte.disconnect()

    def dettach(self):
        if self.lte.isattached():
            self.lte.dettach()
        self.lte.send_at_cmd('AT+CFUN=0')
        print("Modem offline")
