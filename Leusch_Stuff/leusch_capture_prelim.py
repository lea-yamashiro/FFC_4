# Capture for Leuschner

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

# defines the number of samples to capture as data
sdr0 = ugradio.sdr.SDR(device_index=0, direct=True, center_freq=1420.8e6,
                       sample_rate=3.2e6, gain=0, fir_coeffs=None)

sdr1 = ugradio.sdr.SDR(device_index=1, direct=True, center_freq=1420.8e6,
                       sample_rate=3.2e6, gain=0, fir_coeffs=None)

# Data Capture
for i in range(1):

	#Data Capturing:
	#1. Define SDRs
	#2. Capture data
	#3. Add up real and imaginary
	#4. Get Fourier-transformed power

	current_time = time.time() # gives unix time since epoch, i.e. jan 1st, 1970

	data = ugradio.sdr.capture_data([sdr0, sdr1], nsamples=2048, nblocks=10)

	pwr0 = shift(np.mean(perform_power(fft(data[0])), axis=0))
	pwr1 = shift(np.mean(perform_power(fft(data[1])), axis=0))

	# saves the data as an npz file in Projecs/radio_lab/lab2/data
	np.savez(f'testing_SDR0_1420p8_3_{i}.npz', data=pwr0, time=current_time)
	np.savez(f'testing_SDR1_1420p8_3_{i}.npz', data=pwr1, time=current_time)

	# show myself the log power spectra
	#fig, ax = plt.subplots(1,2)
	#ax[0].semilogy(pwr0)
	#ax[0].set_title('SDR 0')
	#ax[1].semilogy(pwr1)
	#ax[1].set_title('SDR 1')
	#plt.show()
