import ugradio
import logging
import threading
import time
import astropy

from rtlsdr import RtlSdr
from astropy.time import Time
from astropy.coordinates import SkyCoord                     # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5     # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude   # angles

class FFC():
    def __init__(self):
        self.LeuschTelescope = ugradio.leusch.LeuschTelescope()
        self.Spectrometer    = ugradio.leusch.Spetrometer()
        self.SynthClient     = ugradio.agilent.SynthClient()
        self.SynthClient.set_frequency()
        self.LeuschNouse     = ugradio.leusch.LeuschNoise()
        self.ispointing      = False
        self.isrecording     = False

        self.leu = astropy.coordinates.EarthLocation(lat = 37.9183, lon = -122.1067, height = 304)

    def stop(self):
        self.isrecording = False
        self.ispointing  = False
        print('Stopping Observation...')
        self.thrd.join()
    
    def track(self):
        self.ispointing = True
        self.thrd       = threading.Thread(target=self._point)
        self.thrd.start()

    def _point(self):
        while self.ispointing:
            self.LeuschNoise.on()
            try:
                self.LeuschTelescope.point(alt, az)    # determine alt,az values!
            except(AssertionError):
                print('Out of range...')
                self.ispointing = False
            time.sleep(1)

    def record(self):
        self.isrecording = True
        self.thrd        = threading.Thread(target=self._record)
        self.thrd.start()

    def _recording(self):
        prevcount = None
        print('Recording data...')
        while self.isrecording:
            time.sleep(5)
            print('Appending data...')


''' need to define a "save" function, then that should be it? '''
