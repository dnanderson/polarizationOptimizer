# ---------------------------------------------------------------------------- #
# Sweep parameters
# ---------------------------------------------------------------------------- #
lambda_start    = 1550 #1500 is lower limit
lambda_stop     = 1630 #1630 is limit
duration        = 5
trigger_step    = 0.01
sample_rate     = 100e3   # DO NOT CHANGE
filename_prefix = "sample_device"
data_directory  = "demo_2/"
power_dBm       = 1

# ---------------------------------------------------------------------------- #
# Import libraries
# ---------------------------------------------------------------------------- #

import nidaqmx
from TSL550 import TSL550
import serial.tools.list_ports
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from testSweep import *
from scipy.signal import find_peaks
from scipy.stats import linregress
import os
import scipy.io as sio
from pathlib import Path
import time

# ---------------------------------------------------------------------------- #
# Check input
# ---------------------------------------------------------------------------- #

# Check laser's sweep rate
laser_sweep_rate = (lambda_stop - lambda_start) / duration
if laser_sweep_rate > 100 or laser_sweep_rate < 0.5:
    raise AttributeError("Invalid laser sweep speed of %f. Must be between 0.5 and 100 nm/s." % laser_sweep_rate)

#TODO: Check for the triggers input too...

# Create directory if needed
foldername = Path(os.getcwd(), data_directory)
print(foldername)
if not os.path.exists(foldername):
    os.makedirs(foldername)
# ---------------------------------------------------------------------------- #
# Setup devices
# ---------------------------------------------------------------------------- #

# Initialize laser
laser = initLaser()
isOn = laser.on()
laser.power_dBm(power_dBm)
laser.openShutter()
laser.sweep_set_mode(continuous=True, twoway=True, trigger=False, const_freq_step=False)
laser.trigger_enable_output()
print(laser.trigger_set_mode("Step"))
print(laser.trigger_set_step(trigger_step))

# Get number of samples to record. Add buffer just in case.
numSamples= int(duration * 2 * sample_rate)
print(numSamples)

time.sleep(0.3)

# Initialize DAQ
task = initTask(channel=["ai0","ai1"],sampleRate = sample_rate, samples_per_chan=numSamples)

# ---------------------------------------------------------------------------- #
# Run sweep
# ---------------------------------------------------------------------------- #

laser.sweep_wavelength(start=lambda_start,stop=lambda_stop,duration=duration,number=1)
data = np.array(task.read(number_of_samples_per_channel=numSamples,timeout=3*duration))

wavelength_logging = laser.wavelength_logging()

# ---------------------------------------------------------------------------- #
# Process data
# ---------------------------------------------------------------------------- #

peaks, _ = find_peaks(data[1,:], height=3, distance=5)

print('==========================================')
print("Expected number of wavelength points: %d" % int(laser.wavelength_logging_number()))
print("Actual wavelength points measured: %d" % len(peaks))
print('==========================================')

device_data = data[0,peaks[0]:peaks[-1]]
device_time = np.arange(0,device_data.size) / sample_rate

modPeaks          = peaks - peaks[0]
modTime           = modPeaks / sample_rate
z                 = np.polyfit(modTime, wavelength_logging, 2)
p                 = np.poly1d(z)
device_wavelength = p(device_time)


device_wavelength_mod = hash(tuple(device_wavelength))
device_data_mod = hash(tuple(device_data))

# ---------------------------------------------------------------------------- #
# Visualize and save results
# ---------------------------------------------------------------------------- #

plt.figure()
plt.plot(device_wavelength,device_data)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Power (au)')
plt.grid(True)
plt.tight_layout()
plt.savefig(data_directory + filename_prefix + ".png")
sio.savemat(data_directory + filename_prefix + ".mat",{'wavelength':device_wavelength_mod,'power':device_data_mod})
np.save(data_directory + filename_prefix + ".npy",np.squeeze(device_wavelength),np.squeeze(device_data))
plt.show()

# ---------------------------------------------------------------------------- #
# Cleanup devices
# ---------------------------------------------------------------------------- #
task.close()
