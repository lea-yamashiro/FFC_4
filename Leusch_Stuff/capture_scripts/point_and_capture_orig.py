# Capture for Leuschner
import numpy as np
import matplotlib.pyplot as plt
import sys
import ugradio
from rtlsdr import RtlSdr
from ugradio import leusch
from ugradio import leo
import astropy as astropy
from astropy.coordinates import SkyCoord                         # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5         # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude       # Angles
from astropy.time import Time
import socket, serial, time, math, sys
import subprocess
import pandas as pd

# 1. Define functions, load in coordinates table

ra_pointing = pd.read_csv('RA_Sorted.csv') # coordinates table

def fft(signal): # for Fourier transform
	return np.fft.fft(signal)

def perform_power(signal): # getting power spectra from FFT
	return np.abs((signal))**2

MAX_SLEW_TIME = 220 # seconds

ALT_MIN, ALT_MAX = 15., 85. # Pointing bounds, degrees
AZ_MIN, AZ_MAX  = 5., 350. # Pointing bounds, degrees

ALT_STOW = 80. #85. # Position for stowing antenna
AZ_STOW = 180. # Position for stowing antenna

ALT_MAINT = 20. # Position for antenna maintenance
AZ_MAINT = 180. # Position for antenna maintenance

HOST_ANT = '192.168.1.156' # RPI host for antenna
HOST_NOISE_SERVER = '192.168.1.90' # RPI host for noise diode
PORT = 1420

HOST_SPECTROMETER = '10.0.1.2' # IP address of ROACH spectrometer

# Offsets (in deg) to subtract from crd to get encoder value to write
DELTA_ALT_ANT = -0.30  # (true - encoder) offset
DELTA_AZ_ANT  = -0.13  # (true - encoder) offset


# 2. Initialize SDRs, Initialize Leuschner Telescope

# both SDR polarizations
sdr0 = ugradio.sdr.SDR(device_index=0, direct=False, center_freq=1420e6,
                       sample_rate=3.2e6, gain=20, fir_coeffs=None) # for first SDR, marked SDR0 -- note: LO?
sdr1 = ugradio.sdr.SDR(device_index=1, direct=False, center_freq=1420e6,
                       sample_rate=3.2e6, gain=20, fir_coeffs=None) # for second SDR, marked SDR1
# telescope initialization
telescope = leusch.LeuschTelescope(host=HOST_ANT, port=PORT, delta_alt=DELTA_ALT_ANT, delta_az=DELTA_AZ_ANT)
# IF we want to use the Noise diode:
#noise = leusch.LeuschNoise(host=HOST_NOISE_SERVER, port=PORT, verbose=False)
#noise.on # turn on noise diode


# 3. set for loop for pointing and collecting data

flops = {}
point = 0
try:
    for i in range(len(ra_pointing)):
        jd = ugradio.timing.julian_date()
        alt, az = ugradio.coord.get_altaz(ra = ra_pointing.iloc[i,3], dec = ra_pointing.iloc[i,4],
                                          jd=jd, lat=leo.lat, lon = -leo.lon, alt=leo.alt)
        point += 1
        if (15 < alt < 85) and (5 < az < 350):
            telescope.point(alt, az, wait = True) # point telescope to iterating
            print('She is pointing at the spot')
            current_time = time.time() # grab unix time of observation once finished pointing
            data = ugradio.sdr.capture_data([sdr0, sdr1], nsamples=2048, nblocks=10000) # run data-capture function within SDR module
            d0 = data[0][...,0]+1j*data[0][...,1] # adding up real and imaginary data
            d1 = data[1][...,0]+1j*data[1][...,1]
            pwr0 = np.mean(perform_power(fft(d0)), axis=0) # applying power function
            pwr1 = np.mean(perform_power(fft(d1)), axis=0)
            # saves the data as an npz file, with filename structure: spec(index)_L(galactic longitude)_B(galactic latitude).npz
            np.savez(f'capture_042224/spec{i}_2_L{ra_pointing.iloc[i,1]:.0f}_B{ra_pointing.iloc[i,2]:.0f}.npz'.format(str),
                        data0=pwr0, data1=pwr1, time=current_time, missed=flops,
                        coords=ra_pointing.iloc[i], alt_az = [alt, az], jd=jd)
            print(f'File: spec{i} has been written'.format(str))
        else:
            print('flopped, moving on')
            flops.update({point:[alt,az]})
            continue
except KeyboardInterrupt:
    print('Done collecting')
    pass
