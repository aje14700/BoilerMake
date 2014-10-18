#Created by AJ Edelbrock
#For BoilerMake 10-18-14
#tests for using PyscoPy as voice recongition 

#from psychopy import microphone as mic
#silence_const = .014
#
#print "Silence loundness: " + str(mic.getRMS("silence.wav")[0]) + " " + str(mic.getRMS("silence.wav")[0]>silence_const)
#print "Talking loundness: " + str(mic.getRMS("normal talk.wav")[0]) + " " + str(mic.getRMS("normal talk.wav")[0]>silence_const)
#print "Yelling loundness: " + str(mic.getRMS("yell.wav")[0]) + " " + str(mic.getRMS("yell.wav")[0]>silence_const)
#
#from psychopy.microphone import Speech2Text as st
#sound = st("computer2.wav")
#response = sound.getResponse()
#print response.word, response.confidence

import speech_recognition as sr
r = sr.Recognizer()
with sr.WavFile("temp0.wav") as source:              # use "test.wav" as the audio source
    audio = r.record(source)                        # extract audio data from the file

try:
    print("Transcription: " + r.recognize(audio))   # recognize speech using Google Speech Recognition
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")
