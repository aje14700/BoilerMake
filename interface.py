#Created by AJ Edelbrock
#for Purdue BoilerMake 10-18-14
#framework for voice controlled light system

port = 12345
server_ip = '192.168.43.159'
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
        SILENCE = 3500


        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK_SIZE)
        while(this.connected):
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
                    self.data[0]='a'
                elif (said=="computer light off"):
                    self.data[0]='b'
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
    
    def main(self):
        (sock, (ipclient, ipport)) = self.start()
        send_thread = threading.Thread(target=self.send, args=(sock,))
        send_thread.start()
        voice_thread = threading.Thread(target=self.voice)
        voice_thread.start()
        
        while(self.connected):
            ask = raw_input("data value")
            if(ask==""):
                self.connected = False
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
        if(self.data[num]=='b'):
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
            if (self.data==""):
                self.connected = False
            else:
                print self.data
                self.set_pin(16, 0)
                self.set_pin(18, 1)
        GPIO.cleanup()
            
        
