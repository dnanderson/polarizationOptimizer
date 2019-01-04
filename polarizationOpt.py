import nidaqmx
from TSL550 import TSL550
from matplotlib import pyplot as plt
from scipy.optimize import minimize
from scipy import optimize
import numpy
import visa
from time import sleep
duration        = 5
sample_rate     = 100e3   # DO NOT CHANGE
numSamples= int(duration * 2 * sample_rate)

history = []

#def get100data():
    #with nidaqmx.Task() as task:
        # Configure task
        #task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        #task.timing.cfg_samp_clk_timing(10000, samps_per_chan = 100)
        # Read the data
        #data = task.read(number_of_samples_per_channel=100)
        #return data

#def J(x):
	# Channel 1 = x, Channel 2 = y, Channel 3 = z
    #gf.setPosition(x[0],1)
    #gf.setPosition(x[1],3)
    # Wait for transients to disappear
    #sleep(0.1)
    # Add this point to the path
    #path.append([x[0], x[1], getAverage()])
    # Negate the result, since we have a minimizing algorithm
    #print getAverage()
    #return (-1) * getAverage()

rm = visa.ResourceManager()
print(rm.list_resources())
controller = rm.open_resource('GPIB0::11::INSTR')
print(controller.query('*IDN?'))

def get100Data():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        task.timing.cfg_samp_clk_timing(10000, samps_per_chan = 10000)
        samples = task.read(number_of_samples_per_channel = 10000)
        #print(samples)
        return samples

def getAverage():
    sampleArray = numpy.array(get100Data())
    averageOfSampleArray = numpy.mean(sampleArray)
    history.append(averageOfSampleArray)
    return averageOfSampleArray

def changePadd(paddNumber, paddPosition):
    writeToControllerString = ':PADD' + str(paddNumber) + ':POSITION ' + str(paddPosition)
    print(writeToControllerString)
    controller.write(writeToControllerString)

def J(x):
    changePadd(1,x[0])
    changePadd(2,x[1])
    changePadd(3,x[2])
    changePadd(4,x[3])
    sleep(0.2)
    output = (-1) * getAverage()

    return output





x0 = numpy.array([200,720,200,400])
res = minimize(J, x0, method='nelder-mead', options={'xatol': 0.1, 'fatol': 1, 'disp': True})
bounds = ((0,999),(0,999),(0,999),(0,999))
#res = optimize.differential_evolution(J, bounds, maxiter = 100)
#res = optimize.shgo(J, bounds)
#res = optimize.basinhopping(J, x0)
plt.figure()
plt.plot(history)
plt.title("Nelder-Mead Optimization Algorithm for Polarization Controller")
plt.xlabel("Iterations of Optimization Algorithm")
plt.ylabel("DAQ Volts Readout (Volts)")
plt.show()
