import numpy as np
val = "00E6686000E68F7000E6B680"
numChars = len(val)
n=8
numPoints = int(numChars / n)
wavelengths = np.zeros((numPoints,))
valArray = [val[i:i+n] for i in range(0, numChars, n)]
for k in range(len(valArray)):
    wavelengths[k] = float(int(valArray[k],16)) / (1e4)
print(wavelengths)
