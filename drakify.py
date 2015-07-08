'''
Video effects made for music videos.
Ryan McGill
2015

'''

import cv2
import cv2.cv as cv
import sys
import os
import numpy as np
sys.path.append('/Users/RyanJamesMcGill/opencv/samples/python2')
import video

class drakify:
	"""
	Class that contains logic for video effects using OpenCV. 
	"""
	def __init__(self, fp):
		"""
		Initialize with filepath to .avi file you want to alter.
		"""
		self._fps = 23.92
		self._capture_size  = (1920, 1080)
		self._fourcc = cv.CV_FOURCC('m','p','4','v')
		self._directory = os.path.split(fp)[0]
		self._file_name = os.path.splitext(os.path.split(fp)[1])[0]
		self._file_ext = os.path.splitext(os.path.split(fp)[1])[1]
		self._capture = video.create_capture(fp)

	def create_writer(self, file_name_append):
		"""
		Create and open video writer. Returns a VideoWriter with @file_name_append appended to objects current filepath
		"""
		file_name = self._directory + '/' + self._file_name + '_' + file_name_append + '.avi'
		writer = cv2.VideoWriter()
		success = writer.open(file_name,self._fourcc,self._fps,self._capture_size,1)
		if success != True:
			print 'Error creating VideoWriter'
			quit()
		return writer

	def generate_canny_frame(self, img, thresh1, thresh2):
		"""
		Function that returns a black and white RGB canny edge image
		"""
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		edge = cv2.Canny(gray, thresh1, thresh2, apertureSize = 5)
		cvis = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)
		return cvis

	def run_canny_flat(self, thresh1, thresh2, color_constant):
		"""
		Basic canny edge effect, @thresh1 and @thresh2 used for sensitivity of effect
		"""
		output = self.create_writer('CannyFlat_' + str(thresh1) + '_' + str(thresh2))
		self._capture.set(cv.CV_CAP_PROP_POS_FRAMES, 1)
		status = 0
		while (status < 1):	
			print 'Canny Flat: ' + self._file_name + self._file_ext, '-- Status:', status*100
			flag, img = self._capture.read()
			img = cv2.resize(img, self._capture_size)
			cvis = self.generate_canny_frame(img, thresh1, thresh2)
			cvis[np.where((cvis == [255,255,255]).all(axis = 2))] = [(color_constant)*x for x in [111, 222, 333]]
			output.write(cvis) #write video frame
			status = self._capture.get(cv.CV_CAP_PROP_POS_AVI_RATIO)

	def run_canny_echo(self, thresh1, thresh2, echo_count):
		"""
		Canny edge effect with echo
		"""
		output = self.create_writer('CannyEcho_' + str(thresh1) + '_' + str(thresh2) + '_' + str(echo_count))
		self._capture.set(cv.CV_CAP_PROP_POS_FRAMES, 1)
		status = 0
		image_array = []


		for item in range(echo_count):
			flag, img = self._capture.read()
			img = cv2.resize(img, self._capture_size)
			cvis = self.generate_canny_frame(img, thresh1, thresh2)
			image_array.append(cvis)

		while (status < 1):
			print 'Canny Echo: ' + self._file_name + self._file_ext, '-- Status:', status*100

			for item in range(echo_count):
				#loop to color images
				multiplier = ((echo_count - item) / float(echo_count)) ** 2
				image_array[item][np.where( (image_array[item] != [0,0,0]).all(axis = 2) )] =  \
											[[222*multiplier, 255*multiplier, 100*multiplier]]
			
			for item in reversed(range(echo_count)):
				#loop to stack images
				if(item == echo_count-1):
					output_image = image_array[item]
				else:
					output_image += image_array[item]
			output.write(output_image)

			for item in reversed(range(echo_count)):
				#iterate images
				if(item > 0):
					image_array[item] = image_array[item - 1]
				else:
					flag, img = self._capture.read()
					img = cv2.resize(img, self._capture_size)
					cvis = self.generate_canny_frame(img, thresh1, thresh2)
					image_array[0] = cvis
			status = self._capture.get(cv.CV_CAP_PROP_POS_AVI_RATIO)

	def run_add_and_echo(self, echo_count):
		"""
		Image add echo effect
		"""
		output = self.create_writer('AddAndEcho')
		self._capture.set(cv.CV_CAP_PROP_POS_FRAMES, 1)
		status = 0
		image_array = []

		for item in range(echo_count):
			flag, img = self._capture.read()
			img = cv2.resize(img, self._capture_size)
			image_array.append(img)

		while (status < 1):
			print 'Image Add and Echo: ' + self._file_name + self._file_ext, '-- Status:', status*100
			for item in reversed(range(echo_count)):
				#loop to stack images
				if(item == echo_count-1):
					output_image = image_array[item]
				else:
					output_image += image_array[item]
			output.write(output_image)

			for item in reversed(range(echo_count)):
				#iterate images
				if(item > 0):
					image_array[item] = image_array[item - 1]
				else:
					flag, img = self._capture.read()
					img = cv2.resize(img, self._capture_size)
					image_array[0] = img
			status = self._capture.get(cv.CV_CAP_PROP_POS_AVI_RATIO)


