import essentia.standard as ess
import numpy as np 
from random import randint
import math
import matplotlib.pyplot as plt

OUTPUT_DIRECTORY_AUDIO = "Path to output directory - audio"
OUTPUT_DIRECTORY_ANNOTATION = "Path to output directory - annotations"

for index in range(500):
	fs = 44100
	indexx = index + 1

	#Select random file subscript for the available files
	kickFile = randint(1,6)
	snareFile = randint(1,7)
	hatFile = randint (1,7)

	#Use Essentia to load the method
	kickLoader = ess.MonoLoader(filename = 'Samples/kick' + str(kickFile) + '.wav' )
	snareLoader = ess.MonoLoader(filename = 'Samples/snare' + str(snareFile) + '.wav' )
	hatLoader = ess.MonoLoader(filename = 'Samples/hat' + str(hatFile) + '.wav' )

	#Place samples in respective arrays
	kickArray = kickLoader()
	snareArray = snareLoader()
	hatArray = hatLoader()

	#Possible Grooves for each component for each time signature
	kickGrooves_4_4  = [[1,0,0,0],[1,1,0,0]]
	snareGrooves_4_4 = [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,1]]
	hatGrooves_4_4   = [[1,1,1,1]]

	kickGrooves_5_4  = [[1,0,0,0,0],[1,1,0,0,0],[1,0,1,0,0],[1,0,1,1,0],[1,0,0,1,0]]
	snareGrooves_5_4 = [[0,0,1,0,0],[0,0,0,1,0],[0,1,0,0,0],[0,1,1,0,1],[0,1,1,0,0],[0,0,1,0,1],[0,0,1,1,0],[0,0,0,1,1],
	                    [0,1,0,1,0]]
	hatGrooves_5_4   = [[1,1,1,1,1]]

	kickGroove_4_4   = kickGrooves_4_4[randint(0,1)]
	snareGroove_4_4  = snareGrooves_4_4[randint(0,3)]
	hatGroove_4_4    = hatGrooves_4_4[randint(0,0)]
	kickGroove_5_4   = kickGrooves_5_4[randint(0,4)]
	snareGroove_5_4  = snareGrooves_5_4[randint(0,8)]
	hatGroove_5_4    = hatGrooves_5_4[randint(0,0)]

	#Select Random Number of Bars for each 4/4 and 5/4. Should this not be just multiples of 4?
	bars_4_4 = [8,12,16,20,24,28,32]
	bars_5_4 = [8,12,16,20,24,28,32]

	num_4_4 = bars_4_4[randint(0,6)]
	num_5_4 = bars_4_4[randint(0,6)]

	#Select a random tempo value in miliseconds in human tempo range. Find values from some specific paper. 
	tempo_main = randint(190,340)

	num_beats = 4 * num_4_4 + 5 * num_5_4
	ideal_audio_time = float(num_beats * tempo_main) / 1000
	real_audio_time = ideal_audio_time + 10   # To account for tempo variability. 

	#Initializing arrays for kick, snare and hat
	kickAudio = np.zeros(int(math.ceil(real_audio_time*fs)))
	snareAudio = np.zeros(int(math.ceil(real_audio_time*fs)))
	hatAudio = np.zeros(int(math.ceil(real_audio_time*fs)))

	#Tempo variations
	intialLag = randint(100,300)
	tempo_arr = np.zeros(num_beats)
	tempo_arr[0] =  intialLag
	for i in range(1,num_beats):
	    tempo_arr[i] =  tempo_arr[i-1] + tempo_main + randint(-16,16) 
	    
	#Beat positions in mili_seconds
	beat_pos = tempo_arr / 1000

	#Metrical positions bar wise
	metrical_pos = np.zeros(num_beats)
	for i in range(4*num_4_4):
	    metrical_pos[i] = (i) % 4 + 1

	for i in range(5*num_5_4):
	    metrical_pos[i+4*num_4_4] = (i) % 5 + 1
	
	col_format = "{:<10}"*2 + "\n" 
	with open(str(OUTPUT_DIRECTORY_ANNOTATION) + str(indexx) + ".txt", "w") as foo:   
		for x in zip(beat_pos, metrical_pos):
			foo.write(col_format.format(*x))

	#Amplitude variations 

	#Kick
	amplitude_kick = np.zeros(num_beats)
	for i in range(num_beats):
	    #Downbeat
	    if (metrical_pos[i] == 1): 
	        amplitude_kick[i] = 1 + float(randint(-20,20)) / 100
	    #Upbeat
	    else:
	        amplitude_kick[i] = 0.75 + float(randint(-10,15)) /100

	#Snare
	amplitude_snare = np.zeros(num_beats)
	for i in range(num_beats):
	    amplitude_snare[i] = 0.75 + float(randint(-5,25)) / 100 

	    
	#Hi-hat
	amplitude_hat = np.zeros(num_beats)
	for i in range(num_beats):
	    #Downbeat
	    if (metrical_pos[i] == 1): 
	        amplitude_hat[i] = 1 + float(randint(-20,20)) / 100
	    #Upbeat
	    else:
	        amplitude_hat[i] = 0.75 + float(randint(-25,20)) / 100

	#Placing the audio at beat positions with both tempo and amplitude variability

	#Kick
	for i in range(4*num_4_4):
	    kickAudio[int(beat_pos[i] * fs):int(beat_pos[i] * fs) + kickArray.size] = amplitude_kick[i] * kickGroove_4_4[i % 4] * kickArray

	for i in range(5*num_5_4):    
	    kickAudio[int(beat_pos[i + 4*num_4_4] * fs):int(beat_pos[i + 4*num_4_4] * fs) + kickArray.size] = amplitude_kick[i + 4*num_4_4] * kickGroove_5_4[i % 5] * kickArray

	#Snare
	for i in range(4*num_4_4):
	        snareAudio[int(beat_pos[i] * fs):int(beat_pos[i] * fs) + snareArray.size] = amplitude_snare[i] * snareGroove_4_4[i % 4] * snareArray
	for i in range(5*num_5_4):    
	        snareAudio[int(beat_pos[i + 4*num_4_4] * fs):int(beat_pos[i + 4*num_4_4] * fs) + snareArray.size] = amplitude_snare[i + 4*num_4_4] * snareGroove_5_4[i % 5] * snareArray

	#Hat
	for i in range(num_beats):
	        hatAudio[int(beat_pos[i] * fs):int(beat_pos[i] * fs) + hatArray.size] = amplitude_hat[i] * hatArray
	
	#Adding together into one.
	x = float(randint(80,100))/100 
	file_time = fs * (beat_pos[num_beats-1] + x)
	print x, file_time/fs

	for i in range(int(file_time)): 
	    kickAudio[i] = kickAudio[i] + snareAudio[i] + hatAudio[i]

	#Writing to wav file
	writer = ess.MonoWriter(filename = str(OUTPUT_DIRECTORY_AUDIO) + str(indexx) + ".wav", format="wav")
	write = writer(kickAudio[0:int(file_time)].astype('single'))


