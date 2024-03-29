# Optical Profilometry Feature Detection
A suite of feature detection tools for optical profilometry data


# Features
 -   Crack Detection and Aalysis
 
#  Setup
1. Installation
```bash
$ pip install optical_profilometry_feature_detection
```
2.	Import it in python
```python
from optical_profilometry_feature_detection import *
``` 
#  A quick example
```python
# separate the individual lines from the raw sample2
lines = g_separate_lines("", "sample2.txt")

# analyze line 1 of sample2, excluding first 2% and last 2% of data, using a span of 0.02 
# in the loewss surface profile model
g_model_cracking("", lines[0], "sample2.txt", 1, first_surf= 0.02, last_surf= 0.98, span = 0.02)

# analyze the first 5 lines in sample1
batch_cracking("", "", "sample1.txt", 5)
``` 
***Output will be series of png and csv files***
