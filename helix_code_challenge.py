import pandas as pd
import numpy as np
from scipy import interpolate
import scipy

import io
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt


# Backfilling problems:
# 1.1 How many >60 second gaps are there and how long is each gap?


df= pd.read_csv("time_series.csv" ) 
df.index = pd.to_datetime(df.utc_dt_naive)
df.utc_dt_naive = pd.to_datetime(df.utc_dt_naive)

number_of_gaps = len(df[df.utc_dt_naive.diff() >= timedelta(seconds=60)])
print(f"There are {number_of_gaps} time gaps greater than 60 seconds in the dataset based on the utc_dt_naive timestamps:")
s = pd.Series(df.utc_dt_naive.diff())
print("")
print(f"Gap 1: {s[s>=timedelta(seconds=60)][0]}")
print(f"Gap 2: {s[s>=timedelta(seconds=60)][1]}")


# Fill timestamps with freq's of every 1s so that no timestamps are missed
dates = pd.date_range(start=df.utc_dt_naive.min(), end = df.utc_dt_naive.max(), freq='1s')
df_reindexed = df.reindex(dates)



# 1.2 For the PV meter, backfill the power and energy data,  prove that dEnergy/dt matches power, 
#and justify that your approach is physically reasonable.


df_backfill = df_reindexed.interpolate(method='time',inplace=False)


df_backfill['d_pv_energy_dt'] = df_backfill.pv_pos_ltea_kwh.diff()*3600
df_backfill['d_pv_energy_dt_ma'] = df_backfill.d_pv_energy_dt.rolling(window=30).mean()


plt.plot(df_backfill.d_pv_energy_dt_ma,label='dEnergy/dt',alpha=.5,linewidth=3)
plt.plot(df_backfill.pv_p_kw,label='Backfilled PV Power')
plt.title("PV Power over time")
plt.legend(loc='upper right')
plt.show()





# 1.3 For the ESS meter, backfill the power and energy data,  prove that dEnergy/dt matches power, 
#and justify your choice  of backfill method.


df_backfill = df_reindexed.interpolate(method='time',inplace=False)
df_backfill['d_ba_energy_dt']= np.where(
    df_backfill['ba_p_kw'] < 0, df_backfill['ba_neg_ltea_kwh'].diff()*-3600, 
    df_backfill['ba_pos_ltea_kwh'].diff()*3600
)


plt.plot(df_backfill.d_ba_energy_dt, label = 'dEnergy/dt', alpha=0.5) 
plt.plot(df_backfill.ba_p_kw,label = 'Backfilled ESS power') 
plt.xlabel("Time")
plt.ylabel("ESS Power (kwh)")
plt.title("ESS Power over Time")
plt.legend(loc='upper right',bbox_to_anchor=(1.5,1))
plt.show()



# * Backfill the net load data power data, and estimate the mean  15-min net load data during the period provided.

df_backfill = df_reindexed.iloc[:,1:].apply(lambda x: x.interpolate(method='time', inplace=False))


df_backfill['d_ut_energy_dt'] = (df_backfill.ut_pos_ltea_kwh.diff())*3600
df_backfill['d_ut_energy_dt_ma_15'] = df_backfill.d_ut_energy_dt.rolling(window=15*60).mean()
df_backfill['ut_p_kw_ma_15'] = df_backfill.ut_p_kw.rolling(window=15*60).mean()

print(f" The mean 15-min net load data during the period provided is {np.round(df_backfill['d_ut_energy_dt_ma_15'].mean(),3)} kw")
print(" ")

fig1 = plt.plot(df_backfill.d_ut_energy_dt,alpha=0.5,label="dEnergy/dt")
fig2 = plt.plot(df_backfill.ut_p_kw,label='Net Load Power')
fig3 = plt.plot(df_backfill.d_ut_energy_dt_ma_15, label='mean 15-min Net Load')
fig4 = plt.plot(df_backfill.ut_p_kw_ma_15, label='mean 15-min Net Load using dEnergy/dt')
plt.xlabel("Time")
plt.ylabel("Net Load (kwh)")
plt.legend(loc='upper right', bbox_to_anchor=(1.75,1))
plt.show()




# Demand charge problems:

# 2.1 If this data represents the highest consumption period of the month, and the customer 
#pays 20 $/kW all-hours demand charges, what is the expected demand charge for this billing period?

df_backfill = df_reindexed.interpolate(method='time',inplace=False)



df_backfill['bill_rate'] = (df_backfill.ut_p_kw/3600)*20

ess_pv_value = np.round(df_backfill['bill_rate'].cumsum().max(),2)

print(f"""The expected demand charge for this billing period is ${ess_pv_value:,} 

""")



plt.plot(df_backfill.ut_p_kw, label='Backfilled Net Load Power')
plt.xlabel("Time")
plt.ylabel("Net Load (kwh)")
plt.title("Site Energy Consumption with PV & ESS Hardware")
plt.legend(loc='upper right', )
plt.show()



# 2.2 Without the contributions of PV and ESS hardware, what would the  expected demand charge have been?

df_backfill = df_reindexed.interpolate(method='time',inplace=False)

df_backfill['gross_load'] = (df_backfill.ut_p_kw) + (df_backfill.pv_p_kw) + (df_backfill.ba_p_kw)
df_backfill['bill_rate'] = (df_backfill.gross_load/3600)*20

df_reindexed['gross_load'] =  (df_reindexed.ut_p_kw) + (df_reindexed.pv_p_kw) + (df_reindexed.ba_p_kw)

no_ess_pv_value = np.round(df_backfill['bill_rate'].cumsum().max(),2)
print(f"""

The expected demand charge for this billing period, 
without the contributions of  PV and ESS hardware is ${no_ess_pv_value:,} 

which is ${np.round(no_ess_pv_value-ess_pv_value,2):,} more expensive with PV and ESS hardware installed


""")


plt.plot(df_backfill.gross_load,label='Backfilled Gross Load')
plt.plot(df_reindexed.gross_load,label='Raw Gross Load')
plt.title("Site Energy Consumption without PV & ESS Hardware")
plt.xlabel("Time")
plt.ylabel("Gross Load (kwh)")
plt.legend(loc='upper right')
plt.show()



# 2.3 What impact does data backfill method have on estimated demand  charges for this site?  

"""

The data backfill method can affect the bias of the predicted values. A reliable backfilling method is needed to reduce risk of long unmonitored gaps in the data, and could help make decisions on assessing performance of the system.. 

In the ideal scenario, if adequate data supporting the equation `gross load` = `net load` + `PV` + `ESS` were known, then a good backfill
method would be to apply the equation across missing values. However, ideal scenarios never happen.


A common way to handle missing values is dropping values, in this context,
dropping values would lower the actual cost of estimated demand charge as those
data points would not be considered in the calculation. Some sort of backfill is required. 

The time backfill method was selected because because the whole table  was interpolated as a two-dimensional plane instead of as separate single-dimensional series. If the time index was evenly spaced, then linear interpolation would also be appropriate, but this was not the case.

In the context of this data, a more simple backfill method (linear/time interpolation) would give more conservative predictions, than 
a more complex backfill (deep neural nets, KNN, etc.) method. One downside of simple backfill methods is the case of extreme values. This could lead to very high or low estimated demand charges for the site. One upside of a complex backfill method is possible accuracy gain in the case extreme values. 

"""
