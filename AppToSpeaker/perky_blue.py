#! /usr/bin/python

import time
import subprocess
import shlex
import os
import signal

from bluetooth import *

class MusicAppServer:

    def playSong(self, target, client_sock):
	if target == 'Kalimba':
		audiofile = target + '.mp3'
		commandline = 'mplayer -af resample=48000:0:2 -slave -quiet -ao alsa:device=default=Set %s' % audiofile
		proc = subprocess.Popen(shlex.split(commandline), stdin=subprocess.PIPE)
		paused = 0

		while (proc.poll() is None):
                        data = client_sock.recv(1024).strip()
                        if len(data) == 0: break
                        print("received [%s]" % data)
                        client_sock.sendall('OK')

                        if (data == 'stop'):
                                if (proc.poll() is None):
					proc.stdin.write('stop\n')
				break

                        elif ((data == 'pause') and (paused == 0)):
                                proc.stdin.write('pause\n')
                                paused = 1

                        elif ((data == 'play') and (paused == 1)):
                                proc.stdin.write('pause\n')
                                paused = 0

			elif (data == 'volume up'):
				proc.stdin.write('volume +1\n')

			elif (data == 'volume down'):
                                proc.stdin.write('volume -1\n')

	elif target == 'GoodLife':
		audiofile = target + '.mp3'
		commandline = 'mplayer -af resample=48000:0:2 -slave -quiet -ao alsa:device=default=Set %s' % audiofile
                proc = subprocess.Popen(shlex.split(commandline), stdin=subprocess.PIPE)
		paused = 0

		while (proc.poll() is None):
			data = client_sock.recv(1024).strip()
        	        if len(data) == 0: break
        	       	print("received [%s]" % data)
               		client_sock.sendall('OK')

			if (data == 'stop'):
				if (proc.poll() is None):
                                        proc.stdin.write('stop\n')
                                break

			elif ((data == 'pause') and (paused == 0)):
				proc.stdin.write('pause\n')
				paused = 1

			elif ((data == 'play') and (paused == 1)):
				proc.stdin.write('pause\n')
				paused = 0

			elif (data == 'volume up'):
                                proc.stdin.write('volume +1\n')

                        elif (data == 'volume down'):
                                proc.stdin.write('volume -1\n')

	elif target == 'Nocturne':
                audiofile = target + '.mp3'
                commandline = 'mplayer -af resample=48000:0:2 -slave -quiet -ao alsa:device=default=Set %s' % audiofile
                proc = subprocess.Popen(shlex.split(commandline), stdin=subprocess.PIPE)
                paused = 0

                while (proc.poll() is None):
                        data = client_sock.recv(1024).strip()
                        if len(data) == 0: break
                        print("received [%s]" % data)
                        client_sock.sendall('OK')

                        if (data == 'stop'):
                                if (proc.poll() is None):
                                        proc.stdin.write('stop\n')
                                break

                        elif ((data == 'pause') and (paused == 0)):
                                proc.stdin.write('pause\n')
                                paused = 1

                        elif ((data == 'play') and (paused == 1)):
                                proc.stdin.write('pause\n')
                                paused = 0

			elif (data == 'volume up'):
                                proc.stdin.write('volume +1\n')

                        elif (data == 'volume down'):
                                proc.stdin.write('volume -1\n')

	elif ((target == 'pause') or (target == 'stop')):
		print 'A song must be playing'

	elif target == 'play':
		print 'Select a song to play'

	else:
		print 'attempting to download or play file: %s' % target
		audiofile = target + '.mp3'
		if (not os.path.isfile(audiofile)):
			os.system('wget %s' %target)
		if (os.path.isfile(audiofile)):
			commandline = 'mplayer -af resample=48000:0:2 -slave -quiet -ao alsa:device=default=Set %s' % audiofile
	                proc = subprocess.Popen(shlex.split(commandline), stdin=subprocess.PIPE)
              		paused = 0

	                while (proc.poll() is None):
	                        data = client_sock.recv(1024).strip()
        	                if len(data) == 0: break
                        	print("received [%s]" % data)
                        	client_sock.sendall('OK')

                        	if (data == 'stop'):
                                	if (proc.poll() is None):
                                        	proc.stdin.write('stop\n')
                                	break

                        	elif ((data == 'pause') and (paused == 0)):
                                	proc.stdin.write('pause\n')
                                	paused = 1

                        	elif ((data == 'play') and (paused == 1)):
                                	proc.stdin.write('pause\n')
                                	paused = 0

				elif (data == 'volume up'):
	                                proc.stdin.write('volume +1\n')

	                        elif (data == 'volume down'):
        	                        proc.stdin.write('volume -1\n')

		else:
			print 'ready for next command'


    def execute(self):
	# try to automatically make device bluetooth discoverable
	#os.system("echo 'discoverable yes\npairable yes\nquit' | bluetoothctl")

        service_uuid = "00001101-0000-1000-8000-00805F9B34FB"

        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", PORT_ANY))
        server_sock.listen(1)

        port = server_sock.getsockname()[1]

        advertise_service(server_sock, "MusicApp", service_id = service_uuid, service_classes = [service_uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])

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
