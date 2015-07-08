'''
Automation to run effects over all .avi files in current directory
Ryan McGill
2015

'''
import os
from drakify import drakify

directory = os.getcwd()
fiels = os.listdir(os.getcwd())

for fiel in fiels:
		print 'running on ', directory + '/' + fiel
		video = drakify(directory + '/' + fiel)
		video.run_canny_flat(700,700,1.5)
		video.run_canny_flat(500,500,1.5)
		video.run_canny_flat(300,300,1.5)
		video.run_canny_echo(500,500,10)
		video.run_canny_echo(500,500,5)
		video.run_add_and_echo(10)

print 'automate_drakify.py is complete!'