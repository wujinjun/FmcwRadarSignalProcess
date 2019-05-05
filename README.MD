#  

# FMCW Radar signal process (Python)

This project is from my master degree work. FMCW signal process was implemented by python script, which can be sum up as:

0. FMCW IF signal pre-process

1. Range-Time-Map construction (RTM)
2. Doppler-Time-Map construction (DTM)
3. Angle-Time-Map construction (ATM)

## 0. FMCW IF signal pre-process

In `pyradar.py`, we built a class `radar_data_reader` . 

1. Read radar data from `.bin` file
2. Define and init varible to save RTM, DTM and ATM

More details about IF-signal pre-process, please refer to `tools.py`

##1. Range-Time-Map construction (RTM)

1. Get a new one frame 
2. Do 1d-fft
3. Compute RTM-bin with the new one frame
4. Accumelate 32 frame to construct a RTM

##2. Doppler-Time-Map construction (DTM)

1. Get a new one frame 
2. Compute RDM
3. Compute pink value from the result of 1d-fft
4. Pick the doppler bin from RDM, which has pink value in range bin
5. Accumelate 32 frame to construct a dam

##3. Angle-Time-Map construction (ATM)

1. Get a new one frame 
2. reshape data to 8 channel (2Tx 4Rx)
3. Apply MUSIC algorithm to compute angle bin
4. Accumelate 32 frame to construct a atm