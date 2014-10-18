BoilerMake
==========
Code for voice reconition light system
Using a combination of a "server" with a microphone, and a raspberry pi as the "client", this program allows for voice recognition to turn on and off DIO, resulting in lights or other devices to be actuated.

When running the client on RPi, MUST RUN CLIENT AS SUDO

Dependencies
============
  Server
    
    pyaudio: http://people.csail.mit.edu/hubert/pyaudio/
    pip: apt-get install python-pip
    SpeechRecognition: pip install SpeechRecognition
      https://pypi.python.org/pypi/SpeechRecognition

  
  Client
  
    RPi.GPIO: https://pypi.python.org/pypi/RPi.GPIO 
 

Ignore
======
PsychoPy: http://www.psychopy.org/api/microphone.html 
     for debian: http://neuro.debian.net/install_pkg.html?p=psychopy 
     for other: http://sourceforge.net/projects/psychpy/files/ 
