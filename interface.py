#Created by AJ Edelbrock
#for Purdue BoilerMake 10-18-14
#framework for voice controlled light system

port = 12345
server_ip = '192.168.43.159'
import socket, threading, time
#Server class, sends commands and works with sound input
class Server:
    data = "000"
    data_old = "000"
    connected = False
    
    def start(self):
        s = socket.socket()
        s.bind((server_ip, port))
        print("Listening for client")
        s.listen(1)
        self.connected = True
        return s.accept()

    def send(self, sock):
        while(self.connected):
            if(self.data!=self.data_old):
                sock.send(self.data.encode('UTF-8'))
                self.data_old = self.data
            time.sleep(.5)
    
    def main(self):
        (sock, (ipclient, ipport)) = self.start()
        send_thread = threading.Thread(target=self.send, args=(sock,))
        send_thread.start()
        
        while(self.connected):
            ask = str(input("data value"))
            if(ask==""):
                connected = False
            else:
                self.data = ask
        

#Client class, runs on raspberry pi to receive commands
class Client:
    
    data = "000"
    connected = False
    
    def start(self):
        s = socket.socket()
        s.connect((server_ip, port))
        self.connected = True
        return s

    def set_pin(self, pin, num):
        import RPi.GPIO as GPIO
        if(self.data[num]=='0'):
            GPIO.output(pin, True)
        else:
            GPIO.output(pin, False)
    
    def main(self):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        sock = self.start()
        while(self.connected):
            data_received = sock.recv(10)
            self.data = data_received.decode('UTF-8')
            print self.data
            self.set_pin(16, 0)
            self.set_pin(18, 1)
        GPIO.cleanup()
            
        
