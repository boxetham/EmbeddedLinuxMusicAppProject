#! /usr/bin/python

import gpio
import time
import subprocess
import shlex
import os

from bluetooth import *

class MusicAppServer:

    def playSong(self, target, client_sock):
	if target == 'Kalimba':
		audiofile = target + '.mp3'
		commandline = 'mplayer -ac mad -slave -quiet -ao alsa:device=default=Set %s' % audiofile
		proc = subprocess.Popen(shlex.split(commandline), stdin=subprocess.PIPE)
		running = 1
		paused = 0

		while (running):
                        data = client_sock.recv(1024).strip()
                        if len(data) == 0: break
                        print("received [%s]" % data)
                        client_sock.sendall('OK')

                        if (data == 'stop'):
                                proc.stdin.write('stop\n')
                                running = 0

                        elif ((data == 'pause') and (paused == 0)):
                                proc.stdin.write('pause\n')
                                paused = 1

                        elif ((data == 'play') and (paused == 1)):
                                proc.stdin.write('pause\n')
                                paused = 0


	elif target == 'GoodLife':
		audiofile = target + '.mp3'
		commandline = 'mplayer -speed 0.75 -cache 8192 -cache-min 99 -slave -quiet -ao alsa:device=default=Set %s' % audiofile
                proc = subprocess.Popen(shlex.split(commandline), stdin=subprocess.PIPE)
		running = 1
		paused = 0

		while (running):
			data = client_sock.recv(1024).strip()
        	        if len(data) == 0: break
        	       	print("received [%s]" % data)
               		client_sock.sendall('OK')

			if (data == 'stop'):
				proc.stdin.write('stop\n')
				running = 0

			elif ((data == 'pause') and (paused == 0)):
				proc.stdin.write('pause\n')
				paused = 1

			elif ((data == 'play') and (paused == 1)):
				proc.stdin.write('pause\n')
				paused = 0

	elif ((target == 'pause') or (target == 'stop')):
		print 'A song must be playing'

	elif target == 'play':
		print 'Select a song to play'

	else:
		print 'unknown remote command'


    def execute(self):

	os.system('bluetoothctl')

        service_uuid = "00001101-0000-1000-8000-00805F9B34FB"

        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        advertise_service(server_sock, "PerkyBlue", service_id = service_uuid, service_classes = [service_uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])

        print("awaiting RFCOMM connection on channel:%d" % port)

        client_sock, client_info = server_sock.accept()
        print("accepted connection from:", client_info)

        try:
            while True:
                data = client_sock.recv(1024).strip()
                if len(data) == 0: break
                print("received [%s]" % data)
                client_sock.sendall('OK')

		self.playSong(data, client_sock)
        except IOError:
            pass

        print("disconnected")

        client_sock.close()
        server_sock.close()
        print("all done")

print 'start'

if __name__ == '__main__':
    server = MusicAppServer()
    server.execute()

print 'stop'
