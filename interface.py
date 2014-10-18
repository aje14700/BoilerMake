#Created by AJ Edelbrock
#for Purdue BoilerMake 10-18-14
#framework for voice controlled light system

port = 12345
server_ip = '192.168.43.159'
import socket, threading
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
        connected = True
        return s.accept()

    def send(self, sock):
        while(connected):
            if(data!=data_old):
                sock.send(bytes(data, 'UTF-8'))
                data_old = data
            sleep(.5)
    
    def main(self):
        sock = self.start()
        send_thread = threading.Thread(target=send, args=(sock,))
        send_thread.start()
        
        while(connected):
            ask = input("data value")
            if(ask==""):
                connected = False
            else:
                data = ask
        

#Client class, runs on raspberry pi to receive commands
class Client:
    data = "000"
    connected = False
    
    def start(self):
        s = socket.socket()
        s.connect((host, port))
        connected = True
        return s

    def set_pin(self, pin, num):
        if(data[num]=='0'):
            GPIO.output(pin, True)
        else:
            GPIO.output(pin, False)
    
    def main(self):
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        sock = self.start()
        while(connected):
            data_received = sock.recv(10)
            data = data_received.decode('UTF-8')
            print data
            self.set_pin(16, 0)
            self.set_pin(18, 1)
        GPIO.cleanup()
            
        
