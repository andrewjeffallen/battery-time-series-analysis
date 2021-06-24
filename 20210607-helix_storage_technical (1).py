'''
Hello, here is the technical problem for the SunPower's Helix
Storage Software team. Please solve this problem using
Python 3.X and the libraries imported below. If you would
like to import additional libraries to bring in additional
functionality that's OK too.

Please reach out to me if you would like clarification
or more information about the background or problems.

Thank you for your time,
Gregory Kimball
'''

import pandas as pd
import numpy as np
# from scipy import XYZ
import io
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt


'''
What is the best way to handle gaps in time series data?

Deliverable:
1. Python code needed to answer the technical questions 
in a .py file.
2. Data visualizations and descriptions as necessary 
in a docx/pptx/googledoc/pdf file.

Background:
For this problem, we have a 2-sec time series data from a 
customer site running SunPower's Helix Storage. The data are 
power and energy data from a PV meter (photovoltaic or 'pv'), an ESS 
meter (energy storage system or 'ba'), and a net load meter (load
at the point of common coupling or 'ut'). Due to communication issues, 
there are several gaps in the data.

Each meter has a '_p_kw' field representing power,
a '_pos_ltea_kwh' representing positive lifetime energy, 
and a '_neg_ltea_kwh' field representing negative lifetime
energy. Please note that the PV and ESS power data use a 'generator' 
convention in which positive values represent generated or discharged 
power and negative values represent consumed or charging power. 
LTE (lifetime energy) values are always positive.

Tip: the 'gross load' data, or the site's consumption data my be
estimated as follows:
'gross load' = 'net load' + 'PV' + 'ESS'

The file 'time_series.csv' contains data with 2-sec interval 
from about 3 hours of site operations. The data is UTC-indexed
and the site is located in Santa Rosa, California.

Backfilling problems:
* How many >60 second gaps are there and how long is each gap?
* For the PV meter, backfill the power and energy data, 
prove that dEnergy/dt matches power, and justify that 
your approach is physically reasonable.
* For the ESS meter, backfill the power and energy data, 
prove that dEnergy/dt matches power, and justify your choice 
of backfill method.
* Backfill the net load data power data, and estimate the mean 
15-min net load data during the period provided.

Demand charge problems:
* If this data represents the highest consumption period of the month,
and the customer pays 20 $/kW all-hours demand charges, what is the 
expected demand charge for this billing period?
* Without the contributions of PV and ESS hardware, what would the 
expected demand charge have been?
* What impact does data backfill method have on estimated demand 
charges for this site?  

'''


