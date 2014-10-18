#Created by AJ Edelbrock
#For BoilerMake 10-18-14
#runs a client object AFTER server is running
#MUST BE RUN AS SUDO FOR GPIO TO WORK
import interface
client = interface.Client()
client.main()
