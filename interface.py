#Created by AJ Edelbrock
#for Purdue BoilerMake 10-18-14
#framework for voice controlled light system

port = 12345
server_ip = '192.168.43.159'
secret_phrase = "abba"
import socket, threading, time
#Server class, sends commands and works with sound input
class Server:
    #a is 1, b is 0
    data = "bbb"
    data_old = "aaa"
    connected = False
    
    def start(self):
        s = socket.socket()
        s.bind((server_ip, port))
        print("Listening for client")
        s.listen(1)
        self.connected = True
        return s.accept()

        
    def voice(self):
        import pyaudio, wave
        from array import array
        from struct import pack
        import speech_recognition as sr
        CHUNK_SIZE = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        SILENCE = 5000


        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK_SIZE)
        while(self.connected):
            r = array('h')
            sound_data = array('h', stream.read(CHUNK_SIZE))
            while(max(sound_data)<SILENCE):
                sound_data = array('h', stream.read(CHUNK_SIZE))
            recording = True
            silent_count = 0
            print "recording"
            while(recording):
                sound_data = array('h', stream.read(CHUNK_SIZE))
                r.extend(sound_data)
                level = max(sound_data)
                if (level>SILENCE):
                    silent_count = 0
                else:
                    silent_count += 1
                    if(silent_count>10):
                        recording = False
            print "finished recording"
            r = pack('<' + ('h'*len(r)), *r)
            wav = wave.open("temp.wav", 'wb')
            wav.setnchannels(1)
            wav.setsampwidth(p.get_sample_size(FORMAT))
            wav.setframerate(RATE)
            wav.writeframes(r)
            wav.close()
            rec = sr.Recognizer()
            with sr.WavFile("temp.wav") as source:
                audio = rec.record(source)
            try:
                said = str(rec.recognize(audio))
                if (said=="computer light on"):
                    self.data='a' + self.data[1:]
                elif (said=="computer light off"):
                    self.data='b' + self.data[1:]
                else:
                    print "Not a command"
            except LookupError:                                 # speech is unintelligible
                print("Could not understand audio")
        stream.stop_stream()
        stream.close()
        p.terminate()



        
    def send(self, sock):
        while(self.connected):
            if(self.data!=self.data_old):
                sock.send(self.data.encode('UTF-8'))
                self.data_old = self.data
            time.sleep(.1)

    def connection(self):
        (sock, (ipclient, ipport)) = self.start()
        send_thread = threading.Thread(target=self.send, args=(sock,))
        send_thread.start()

    def checkEmail(self):
        import poplib
        from email import parser
        import email
        #p = Parser()
        self.connected = True
        while(self.connected):
            pop = poplib.POP3_SSL('pop.gmail.com')
            pop.user('room.lights@gmail.com')
            pop.pass_('room123456789')
            
            #print "checking email"
            time.sleep(1)
            #Get messages from server:
            messages = [pop.retr(i) for i in range(1, len(pop.list()[1]) + 1)]
            # Concat message pieces:
            messages = ["\n".join(mssg[1]) for mssg in messages]
            #Parse message intom an email object:
            messages = [parser.Parser().parsestr(mssg) for mssg in messages]
            for message in messages:
                for part in message.walk():
                    if part.get_content_type():
                        body = str(part.get_payload(decode=True)).strip()
                        if("<td>" in body):
                            first = body.find("<td>")
                            second = body.find("</td>", first + 4)
                            body = body[first+4:second].strip()
                            if(body[:len(secret_phrase)]==secret_phrase):
                                self.data = body[len(secret_phrase):]
                        elif(body.find("<")==-1 and body!="None"):
                            body = body.strip()
                            if(body[:len(secret_phrase)]==secret_phrase):
                                self.data = body[len(secret_phrase):]
            
            pop.quit()
            del pop

    def startEmail(self):
        self.connected = True
        email_thread = threading.Thread(target=self.checkEmail)
        email_thread.start()
        if(email_thread.getName()=="Thread-1"):
            self.connection()
            raw_input("Press enter to stop")
            self.connected = False
                  
    def main(self):
        self.connection()
        voice_thread = threading.Thread(target=self.voice)
        voice_thread.start()
        self.startEmail()
##        while(self.connected):
##            ask = raw_input("data value")
##            if(ask==""):
##                self.connected = False
##            else:
##                self.data = ask
        




    
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
        if(self.data[num]=='b'):
            GPIO.output(pin, True)
        else:
            GPIO.output(pin, False)
    
    def main(self):
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        sock = self.start()
        while(self.connected):
            data_received = sock.recv(10)
            self.data = data_received.decode('UTF-8')
            if (self.data==""):
                self.connected = False
            else:
                print self.data
                self.set_pin(16, 0)
                self.set_pin(18, 1)
        GPIO.cleanup()
