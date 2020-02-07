import time
import numpy
# values is a nested array with all the signals in the following order:
# values -> [[emg],[eog],[ecg],[eeg0],[eeg1],[eeg2],[nasalP],[airflow],[chestM0],[chestM1],[chestM2],[chestM3],[pulseO]]

def saveToEDF(filename,values):
	ver = 0
	patientID = 'patient'
	recordID = 'record'
	
	ts = time.localtime() # Structure -> (tm_year=2020, tm_mon=2, tm_mday=5, tm_hour=4, tm_min=7, tm_sec=59, tm_wday=2, tm_yday=36, tm_isdst=0)
	startDate = time.strftime("%d.%m.%y",ts) # dd.mm.yy
	startTime = time.strftime("%H.%M.%S",ts) # hh.mm.ss (24-hour clock)

	numDataRecords = 3600 # A hour's worth of records
	recordDur = 1 # 1 second for each data record
	
	label = ['EMG','EOG','ECG','EEG 1','EEG 2','EEG 3','Nasal Pressure','Airflow','Chest Motion 1','Chest Motion 2','Chest Motion 3','Chest Motion 4','Pulse Ox']
	numSignals = len(label)

	transducer = ['']*numSignals # Not sure what to put here so left it empty

	units = ['uV','mV','mV','uV','uV','uV','Pa','m/s','m/s','m/s','m/s','m/s','% O2'] # Units of the signals

	physicalMins = [0]*numSignals # Minimum values through the board
	physicalMaxs = [5]*numSignals # Need to change this based on the gains of each channel

	digitalMins = [-32768]*numSignals # Minimum digital value for 16-bit numbers
	digitalMaxs = [32767]*numSignals # Maximum digital value for 16-bit numbers

	prefiltering = ['']*numSignals # We can put the gains here once we know them

	samplingFreqs = [500,500,500,500,500,500,100,100,100,100,100,100,25]

	headerBytes = 256 + numSignals*256

	outputFile = filename

	## Formatting above information into ASCII
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

	## Write header record to file
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

	## Write values to file
	for rec in range(numDataRecords):
		for sig in range(numSignals):
			arr = numpy.array(values[sig][rec*samplingFreqs[sig]:(rec+1)*samplingFreqs[sig]])
			arr.astype('int16').tofile(file) # Binary (int16) format
	file.close()