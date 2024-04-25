# README for obs_042424 (from Lea for the Fourier Fan Club)
File organization for observation with Leuschner on April 24, 2024. For all main spectra, I set gain = 15. To my knowledge, I was able to collect all but 30 of the 324 pointings for the High Velocity Cloud. Would love if someone else could count the files to compare numbers. The scripts I used to collect this data are in 'Leusch_Stuff' under 'capture_scripts', and named according to the methodology described here! Feel free to check those out.

# Phase1
These are spectra before halfway mark, from index 0-162.

# Phase2
These are spectra after halfway mark, from index 163-324. 

# Noise_Spectra
I took spectra with the noise diode on for only select indices of that main RA_sorted.csv, once at the beginning, once in the middle, once at the end (this is what Parsons told me to do). These noise spectra have corresponding non-noise spectra named with identical numerical indices. The noise ones are labeled as 'NoiseSpec{i}..'. The comparison of spectra with 'noise on' to the equivalent spectra without noise is how we figure out how much to multiply the signal by (the way we did in Lab 2). I think it's the same thing where we just apply that formula. However I did NOT get frequency-switched Noise Spectra, so not exactly sure if this will work the same.

# fixed
After finishing the main observation, I did my best to track down which indices the pointer hadn't been able to reach, and ran the collection script again to see if I could still catch them. HOWEVER, PROBLEM: I forgot to change the gain from 20 to 15 on this script before running it. So, here, Gain = 20. I think that we can still calibrate with this, but probably going to need to take this set again.

Further: The data points I know were missed in the main collection (Phase1 and Phase2) are coordinates with the following indices in the main DataFrame (was not able to get ALL of these with the messed up gain, only some): 

missed_042424 = [0, 1, 2, 4, 8, 16, 70, 108, 128, 133, 137, 141, 143, 145, 148, 166, 174, 208, 311, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160]

Regardless of whether or not we can calibrate with the different gains, I still want to try to get these spectra again. Just need to figure out when those coordinates will be attainable and also calendar time. BIG oof.)
