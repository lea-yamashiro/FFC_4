# Capture for Leuschner

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import ugradio
from rtlsdr import RtlSdr
import leusch
from ugradio import leo
import astropy as astropy
from astropy.coordinates import SkyCoord                         # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5         # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude       # Angles
from astropy.time import Time
from __future__ import print_function
import socket, serial, time, math, sys
import subprocess

# 1. Define functions, load in coordinates table

ra_pointing = pd.read_csv('RA_Sorted.csv') # coordinates table

def leusch_gal_to_AltAz(L,B): # function to spit out time-sensitive altitude and azimuth from gal. coordinates

    # set galactic coordinates 
    galactic_coords = SkyCoord(l = L*u.deg, b = B*u.deg, frame = 'galactic')
    # set Leuschner observation location (latitude, longtidue, elevation)
    leusch_coords = EarthLocation(lat = leo.lat*u.deg, lon = -leo.lon*u.deg, height = leo.alt*u.m) 
    # set observation time in UNIX 
    observation_time = astropy.time.Time(time.time(), format = 'unix')
    # convert to AltAz using astropy transformation 
    alt_az_coords = galactic_coords.transform_to(AltAz(obstime = observation_time, location = leusch_coords))
    # extract altitude and azimuth from the coordinates 
    alt_point = alt_az_coords.alt
    az_point = alt_az_coords.az 
    # store them in array
    AltAz_pointers = [alt_point, az_point]
	
    return AltAz_pointers


def fft(signal): # for Fourier transform
	return np.fft.fft(signal)

def perform_power(signal): # getting power spectra from FFT
	return np.abs((signal))**2



# 2. Initialize SDRs, Initialize Leuschner Telescope

# both SDR polarizations
sdr0 = ugradio.sdr.SDR(device_index=0, direct=False, center_freq=1420e6,
                       sample_rate=3.2e6, gain=20, fir_coeffs=None) # for first SDR, marked SDR0 -- note: LO? 
sdr1 = ugradio.sdr.SDR(device_index=1, direct=False, center_freq=1420e6,
                       sample_rate=3.2e6, gain=20, fir_coeffs=None) # for second SDR, marked SDR1

# telescope initialization
telescope = leusch.LeuschTelescope(host=HOST_ANT, port=PORT, 
								   delta_alt=DELTA_ALT_ANT, delta_az=DELTA_AZ_ANT)

# IF we want to use the Noise diode: 
noise = leusch.LeuschNoise(host=HOST_NOISE_SERVER, port=PORT, verbose=False)
noise.on # turn on noise diode

# 3. set for loop for pointing and collecting data

for i in range(len(ra_pointing)): 
	
    alt_az = leusch_gal_to_AltAz(ra_pointing.loc[i][0], ra_pointing.loc[i][1]) # iterate for alt, applying leuschner alt-az function to ra_pointing dataframe 
    telescope.point(alt_az[0], alt_az[1], wait = True) # point telescope to iterating 
	
    current_time = time.time() # grab unix time of observation once finished pointing
    data = ugradio.sdr.capture_data([sdr0, sdr1], nsamples=2048, nblocks=10000) # run data-capture function within SDR module
    
    d0 = data[0][...,0]+1j*data[0][...,1] # adding up real and imaginary data 
    d1 = data[1][...,0]+1j*data[1][...,1]

    pwr0 = np.mean(perform_power(fft(d0)), axis=0) # applying power function 
    pwr1 = np.mean(perform_power(fft(d1)), axis=0)

	# saves the data as an npz file, with filename structure: spec(index)_L(galactic longitude)_B(galactic latitude).npz
    np.savez(f'spec{i}_L{ra_pointing.loc[i][0]}_B{ra_pointing.loc[i][0]}.npz'.format(str), 
		  data0=[pwr0], data1=[pwr1], time=current_time, 
		  coords=ra_pointing[i], altaz = alt_az)

