import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime
from datetime import date
from datetime import datetime, timedelta

#Import John Hopkins CSSE data
#df = pd.read_csv('time_series_covid19_confirmed_US.csv')
link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
df = pd.read_csv(link)

link_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
df_death = pd.read_csv(link_death)

#make a list of states/territories
states = df['Province_State']
states.drop_duplicates(inplace=True)

#Drop FIPS lookup/Coordinates
df.drop(['Country_Region','Lat','Long_'], axis=1,inplace=True) #positive cases
df1 = df.iloc[:,6:]

#function to form state_df + df_tot
def state_func(state):
    state_len = len(state)
    dc1 = df1.loc[df1['Province_State'] == state]

    dc1.drop(['Province_State'], axis=1,inplace=True)
    dc1 = dc1.T

    new_header = dc1.iloc[0] #grab the first row for the header
    dc = dc1[1:] #take the data less the header row
    dc.columns = new_header

    dc.columns = pd.Index(map(lambda x : str(x)[:-(state_len+6)], dc.columns))
    dc.columns.name = 'Date'

    sum = dc.sum(axis=1)
    dc[state] = sum

    return dc

#Plotting tools

#---------
#function to plot total cases
def fig(state1):
    #plt.figure()
    #-------
    df1 = state_func(state1)
   
    plt.plot(df1.index,df1[state1],ls='-',label=state1)
    
    ax=plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(14))

    plt.title('Total Cases')
    plt.ylabel('Positive Cases')
    plt.xlabel('Date')

    plt.legend() 
    plt.xticks(rotation='0')

    ax.yaxis.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #plt.show()

#plot daily cases
def plot_diff(state):
    #---------------------------------
    #diff_st = state_func(state).diff()

    #plt.figure()

    #diff
    #plt.bar(diff.index,diff[state],ls='-',label='Daily Cases',color='indianred',alpha=0.5)
    plt.plot(rol.index,rol[state],label=str(state)+' '+str(trial_1)+'-day rolling average')  
    
    ax=plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(14))

    plt.title('Daily Cases')
    plt.ylabel('Positive Cases')
    #plt.xlabel('Date')

    plt.legend() 
    plt.xticks(rotation='0')

    ax.yaxis.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #plt.show()

#rolling average
def rol_avg(state):
    #plt.figure()

    #plt.plot(gf.index,gf[state],label='Growth Factor')
    plt.plot(rol_1.index,rol_1[state],label=str(state)+' '+str(trial_1)+'-day rolling average')

    

    ax=plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(14))

    plt.title('Growth Factor')
    plt.ylabel('Growth Factor')

    plt.ylim(0,2)
    plt.axhline(1,ls='--')

    plt.xticks(rotation='0')

    plt.legend()
    ax.yaxis.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #plt.show()

#needs work
def top_states(df_top):
    plt.figure()

    ax = df_top.plot(kind='barh')
    plt.xlabel('Positive Cases')
    ax.invert_yaxis()
    plt.ylabel('')

    plt.xticks(rotation=0)
    plt.show()


#Form matrix [dc_tot] with sum of each state
#-------------------------
dc = state_func('New York')
dates = dc.index
dc_tot = pd.DataFrame(dates)
dc_tot.rename(columns={ dc_tot.columns[0]: "Date" }, inplace = True)

df_test = df
states = df_test.loc[:,'Province_State']
states = states.drop_duplicates()

#Sum counties for each state
for col in states:
    dtest = state_func(col)
    sf = dtest.reset_index()
    dc_tot=pd.concat( [dc_tot, sf[col]],axis=1)

#retrun dc_tot
dc_tot = dc_tot.set_index('Date')

#Calculate metrics
#------
diff = dc_tot.diff()

window = 14
trial_1 = 10

gf = diff.pct_change()+1
rol = (diff.rolling(trial_1).sum()/trial_1)
rol_1 = (gf.rolling(window).sum()/window)

#Fun investigation
#------- 
state = 'Texas'

#fig(state)
#plot_diff(state)
#rol_avg(state)
#-----
#top states
dct = dc_tot.T
dft = diff.T

yest = len(dct.columns)-30
today = len(dct.columns)-1

top10 = dct.sort_values(dct.columns[today], ascending = False)
top_prev = dct.sort_values(dct.columns[yest], ascending = False)

top10_daily = dft.sort_values(dft.columns[today], ascending = False)
top_prev_daily = dft.sort_values(dft.columns[yest], ascending = False)

num = 5
#--
top10 = top10.iloc[:,today].head(num)
top_prev = top_prev.iloc[:,yest].head(num)

top10_daily = top10_daily.iloc[:,today].head(num)
top_prev_daily = top_prev_daily.iloc[:,yest].head(num)
#--

top10_ls = list(top10.T.index)
top_prev_ls = list(top_prev.T.index)

top10_ls_daily = list(top10_daily.T.index)
top_prev_ls_daily = list(top_prev_daily.T.index)
#----
# hotspot = [item for item in top10_ls if item not in top_prev_ls]
# recovery = [item for item in top_prev_ls if item not in top10_ls]
# print(hotspot)
# print(recovery)
#----
test_list = ['Florida','Texas','California','Georgia','Arizona','New York']
test2 = ['New York','Arizona','Texas']

print(top10_ls_daily)

# plt.figure()
# for state in test2:
#     plot_diff(state) #plot_diff, rol_avg, fig
#     #plt.pause(0.05)

# plt.show()

plt.figure()
plot_diff('New York')
plt.show()


