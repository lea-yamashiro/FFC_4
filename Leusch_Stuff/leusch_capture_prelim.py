# Capture for Leuschner


from __future__ import print_function
import socket, serial, time, math, sys
import subprocess
try: import thread
except(ImportError): import _thread as thread
try:
    import RPi.GPIO as GPIO # necessary for LeuschNoiseServer
except(ImportError):
    pass
import numpy as np
import matplotlib.pyplot as plt
import sys
import ugradio
import time
from rtlsdr import RtlSdr


# Define Function/Constants
def fft(signal):
	return np.fft.fft(signal)
	
def perform_power(signal):
	return np.abs((signal))**2
	
def shift(signal):
	return np.fft.fftshift(signal)

freqs = np.fft.fftshift(np.fft.fftfreq(2048, 1/3.2e6))

# Data Capture 
for i in range(1):
	
	'''
	Data Capturing: 
	1. Define SDRs 
	2. Capture data 
	3. Add up real and imaginary 
	4. Get Fourier-transformed power spectra only
	5. Save spectra
	'''
	
    current_time = time.time() # gives unix time since epoch, i.e. jan 1st, 1970
	
	# defines the number of samples to capture as data
	sdr0 = ugradio.sdr.SDR(device_index=0, direct=True, center_freq=1420e6, 
                       sample_rate=3.2e6, gain=0, fir_coeffs=None)

    sdr1 = ugradio.sdr.SDR(device_index_1, direct=True, center_freq=1420e6, 
                       sample_rate=3.2e6, gain=0, fir_coeffs=None)

    data = ugradio.sdr.capture_data([sdr0, sdr1], nsamples=2048, nblocks=10)
	
    
    d = data[...,0]+1j*data[...,1]
	
    pwr = shift(np.mean(perform_power(fft(d)), axis=0))

	# saves the data as an npz file in Projecs/radio_lab/lab2/data
	np.savez(f'FFC/Testing/testing_{i}.npz', data=pwr, time=current_time)

    # show myself the log power spectra 
    plt.semilogy(pwr)
    plt.show()