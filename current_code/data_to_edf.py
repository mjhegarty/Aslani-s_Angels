import scipy.io
#from pprint import pprint
from array import *
#import pyedflib
#from datetime import date, datetime
import numpy


########### Sine Curve Testing ###########
# y1 = -2*sin(t1);
# y2 = 3*sin(t2-pi/4);
ver = 0
patientID = 'sinTesting'
recordID = 'test'
startDate = '10.01.19' # dd.mm.yy
startTime = '14.45.00' # hh.mm.ss
numDataRecords = 10
recordDur = 1

label = ['sin1','sin2']
numSignals = len(label)
transducer = ['auto','manual']
units = ['uV', 'mV']
physicalMins = [-2, -3]
physicalMaxs = [2, 3]
digitalMins = [-32768, -32768]
digitalMaxs = [32767, 32767]
prefiltering = ['filter1', 'filter2']
samplingFreqs = [200, 400]
headerBytes = 256 + numSignals*256

cellArray = scipy.io.loadmat('sinData.mat')

values = cellArray['values']
outputFile = 'testSinConversion.edf'
############################################


########### From Shawn's EDF File ###########
# ver = 0
# patientID = 'pat1X'
# recordID = 'test'
# startDate = '10.01.19' # dd.mm.yy
# startTime = '14.45.00' # hh.mm.ss
# numDataRecords = 856
# recordDur = 1
# #numSignals = 33

# label = ['EEG F3-A2','EEG F4-A1','EEG A1-A2','EEG C3-A2','EEG C4-A1','EEG O1-A2','EEG O2-A1','EOG LOC-A2','EOG ROC-A2','EMG Chin',
# 'Leg 1 ','Leg 2','ECG I','RR','ECG II','Snore','Snore','Flow Patient','Flow Patient','Effort THO','Effort ABD','SpO2','Pleth','Body',
# 'Flow Patient','xPAP CPAP','xPAP IPAP','xPAP EPAP','Leak Total','PulseRate','PressCheck','ECG IIHF','Technical']

# numSignals = len(label)
# transducer = []

# units = ['uV','uV','uV','uV','uV','uV','uV','uV','uV','uV','uV','uV','uV','','uV','','','','','','','','','','lmin','cmH2O','cmH2O',
# 'cmH2O','lmin','','','uV','']

# physicalMins = [-313,-313,-313,-313,-313,-313,-313,-313,-313,-78,-78,-78,-8333,0,-8333,-100,-100,-100,-100,-100,-100,0,-100,0,
# -3276.8,0,0,0,-3276.8,0,0,-8333,0]

# physicalMaxs = [313,313,313,313,313,313,313,313,313,78,78,78,8333,200,8333,100,100,100,100,100,100,102.3,100,255,3276.7,655.35,
# 655.35,655.35,3276.7,255,65535,8333,65535]

# digitalMins = [-32768,-32768,-32768,-32768,-32768,-32768,-32768,-32768,-32768,-32768,-32768,-32768,-32768,0,-32768,-32768,-32768,
# -32768,-32768,-32768,-32768,0,-32768,0,-32768,-32768,-32768,-32768,-32768,0,-32768,-32768,-32768]

# digitalMaxs = [32767,32767,32767,32767,32767,32767,32767,32767,32767,32767,32767,32767,32767,200,32767,32767,32767,32767,32767,
# 32767,32767,1023,32767,255,32767,32767,32767,32767,32767,255,32767,32767,32767]

# prefiltering = []

# samplingFreqs = [200,200,200,200,200,200,200,200,200,200,200,200,200,10,200,500,500,100,100,100,100,1,100,1,10,1,1,1,10,1,1,1000,200]

# headerBytes = 256 + numSignals*256

# cellArray = scipy.io.loadmat('data.mat')

# values = cellArray['values']

#outputFile = 'testConversion.edf'
#############################################

header_ver = str(ver) + (8-len(str(ver)))*' ' # Version of data format (8 ASCII)
header_patientID = patientID + (80-len(patientID))*' ' # Patient identification (80 ASCII)
header_recordID = recordID + (80-len(recordID))*' ' # Recording identification (80 ASCII)
header_startDate = startDate # Start date dd.mm.yy (8 ASCII)
header_startTime = startTime # Start time hh.mm.ss (8 ASCII)

header_headerBytes = str(headerBytes) + (8-len(str(headerBytes)))*' ' # Number of bytes in header record (8 ASCII)

header_reserved = 44*' ' # Reserved space (44 ASCII)
header_numDataRecords = str(numDataRecords) + (8-len(str(numDataRecords)))*' ' # Number of data records (8 ASCII), -1 if unknown
header_recordDur = str(recordDur) + (8-len(str(recordDur)))*' ' # Duration of each data record in seconds (8 ASCII)
header_numSignals = str(numSignals) + (4-len(str(numSignals)))*' ' # Number of signals in file (4 ASCII)

header_labels = ''

for signal in label: # Signal labels (16 ASCII each signal)
	header_labels = header_labels + signal + (16-len(signal))*' ' 

header_tranducer = ''

if len(transducer) != 0: # Transducers (80 ASCII each signal)
	for t in transducer:
		header_tranducer = header_tranducer + t + (80-len(t))*' '
else:
	header_tranducer = numSignals*80*' '

header_units = ''

for dim in units: # Units of signals (8 ASCII each signal)
	header_units = header_units + dim + (8-len(dim))*' '

header_physicalMins = ''

for minVal in physicalMins: # Physical minimums of signals (8 ASCII each signal)
	header_physicalMins = header_physicalMins + str(minVal) + (8-len(str(minVal)))*' '

header_physicalMaxs = ''

for maxVal in physicalMaxs: # Physical maximums of signals (8 ASCII each signal)
	header_physicalMaxs = header_physicalMaxs + str(maxVal) + (8-len(str(maxVal)))*' '

header_digitalMins = ''

for minVal in digitalMins: # Digital minimums of signals (8 ASCII each signal)
	header_digitalMins = header_digitalMins + str(minVal) + (8-len(str(minVal)))*' '

header_digitalMaxs = ''

for maxVal in digitalMaxs: # Digital maximums of signals (8 ASCII each signal)
	header_digitalMaxs = header_digitalMaxs + str(maxVal) + (8-len(str(maxVal)))*' '

header_prefiltering = ''

if len(prefiltering) != 0: # Prefiltering, like lowpass and highpass frequencies (80 ASCII each signal)
	for p in prefiltering:
		header_prefiltering = header_prefiltering + p + (80-len(p))*' '
else:
	header_prefiltering = numSignals*80*' '

header_samplingFreqs = ''

for freq in samplingFreqs: # Number of samples in one record (8 ASCII each signal)
	header_samplingFreqs = header_samplingFreqs + str(freq) + (8-len(str(freq)))*' '

header_reserved2 = numSignals*32*' ' # Reserved space (32 ASCII each signal)

# Write header record to file
file = open(outputFile, 'wb') # Regular ASCII format

file.write(header_ver.encode('ascii'))
file.write(header_patientID.encode('ascii'))
file.write(header_recordID.encode('ascii'))
file.write(header_startDate.encode('ascii'))
file.write(header_startTime.encode('ascii'))
file.write(header_headerBytes.encode('ascii'))
file.write(header_reserved.encode('ascii'))
file.write(header_numDataRecords.encode('ascii'))
file.write(header_recordDur.encode('ascii'))
file.write(header_numSignals.encode('ascii'))
file.write(header_labels.encode('ascii'))
file.write(header_tranducer.encode('ascii'))

file.write(header_units.encode('ascii'))
file.write(header_physicalMins.encode('ascii'))
file.write(header_physicalMaxs.encode('ascii'))
file.write(header_digitalMins.encode('ascii'))
file.write(header_digitalMaxs.encode('ascii'))
file.write(header_prefiltering.encode('ascii'))
file.write(header_samplingFreqs.encode('ascii'))
file.write(header_reserved2.encode('ascii'))

# Write data records to file
for rec in range(numDataRecords):
	pprint(rec)
	for sig in range(numSignals):
		# Next line looks weird because it is reading from Matlab data file
		arr = numpy.array(values[sig].tolist()[0].tolist()[0][rec*samplingFreqs[sig]:(rec+1)*samplingFreqs[sig]])
		arr.astype('int16').tofile(file) # Binary (int16) format

file.close()


