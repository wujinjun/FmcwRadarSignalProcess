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

##1. Range-Time-Map construction

In `pyradar.py`, we built a class `radar_data_reader` . 

