#Created by AJ Edelbrock
#For Purdue BoilerMake 10-18-14
#Testing using pyaudio
import pyaudio, wave
from array import array
from struct import pack
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
connected = True
SILENCE = 3500


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK_SIZE)
while(connected):
    while(1):
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
        wav = wave.open("temp" + ".wav", 'wb')
        wav.setnchannels(1)
        wav.setsampwidth(p.get_sample_size(FORMAT))
        wav.setframerate(RATE)
        wav.writeframes(r)
        wav.close()
