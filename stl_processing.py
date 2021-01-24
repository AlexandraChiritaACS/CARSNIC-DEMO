from pylab import *
from rtlsdr import *
from matplotlib.pyplot import *
from scipy.fftpack import *
import requests
import json
from ast import literal_eval
import os

frq = [0.001e6, 0.002e6, 0.003e6, 0.004e6, 0.005e6,
       0.006e6, 0.007e6, 0.008e6, 0.009e6, 0.010e6, 0.011e6,
       0.012e6, 0.013e6, 0.014e6, 0.015e6, 0.016e6, 0.017e6,
       0.018e6, 0.019e6, 0.020e6, 355e6, 433e6]
frq1 = [95e6]

def is_valid(filename):
	url="https://northeurope.api.cognitive.microsoft.com/customvision/v3.0/Prediction/8fa281b7-7a7c-47c1-b170-676ea0d8b199/classify/iterations/Iteration2/image"
	headers={'content-type':'application/octet-stream','Prediction-Key':'e09004ba3d8d4cfcb6450875c3de53a8'}
	r =requests.post(url,data=open(filename,"rb"),headers=headers)
	data = literal_eval(r.content.decode('utf8'))
	p1 = data["predictions"][0]["probability"]
	t1 = data["predictions"][0]["tagName"]
	p2 = data["predictions"][1]["probability"]
	t2 = data["predictions"][1]["tagName"]
	if (p1 > p2):
		return t1
	return t2

sdr = RtlSdr()

while(1):
	# the camera picture - still in progress
	os.system('raspistill -o ex.jpeg')
	if (is_valid("ex.jpeg") == "good"):

		for f in frq:
			# configure device
			sdr.sample_rate = 2.4e6
			sdr.center_freq = f
			sdr.gain = 'auto'
			samples = sdr.read_samples(256*1024)
			fft_signal = ifft(fft(samples))		
			
			print("Plot " + str(f))	
			psd(fft_signal, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
			xlabel('Frequency (MHz)')
			ylabel('Relative power (dB)')
			
			savefig('sample.png')
			if (is_valid("sample.png") == "good"):
				print("Transmit canceling signal")
				os.system('./transmit.sh -' + str(f))
				
sdr.close()
