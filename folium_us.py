import folium
#from folium import plugins
import math
from datetime import date
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

#IMPORT TODAY'S DAILY REPORT -------------------
today = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
yesterday = datetime.strftime(datetime.now() - timedelta(7), '%m-%d-%Y')

print(today)
print(yesterday)

print('reading...')
test02= 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'+str(today)+'.csv'
test_yesterday= 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'+str(yesterday)+'.csv'

#Daily Report US
#us = pd.read_csv(test02)
#us_yes = pd.read_csv(test_yesterday)

#us.to_csv('today.csv', index = False)
#us_yes.to_csv('yesterday.csv', index = False)

us = pd.read_csv('today.csv')
us_yes = pd.read_csv('yesterday.csv')

print('done')
#----------------------------------------------------
#Dictionary of State Abbreviations
#https://gist.github.com/rogerallen/1583593
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

#remove non-states
def reformat(df):
	us2 = df[df['Province_State'] != 'Grand Princess']
	us2 = us2[us2['Province_State'] != 'Diamond Princess']

	us2.reset_index(drop=True, inplace=True)

	#Use state abb. dictionary to rename state column
	for index, row in us2.iterrows():
		
		state = row['Province_State']

		state_abb = us_state_abbrev[state]

		us2.iloc[index, 0] = state_abb
	return us2

#us_reformat = us.copy(deep=True)
us1 = reformat(us)

#us_reformat_yes = us_yes.copy(deep=True)
us1_yes = reformat(us_yes)

us_diff = us1['Active']-us1_yes['Active']



us1['Diff'] = us_diff

print(us1)
#------------------------------------------------------------------
#States JSON
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'

bins = list(us1['Diff'].quantile([0, 0.25, 0.5, 0.75, 1]))

#Prepared Data
state_data = us1

#Creat Map
m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=state_data,
    columns=['Province_State', 'Diff'],
    key_on='feature.id',
    fill_color='YlOrRd',
    #fill_opacity=0.7,
    #line_opacity=0.2,
    legend_name='Diff'
    ,bins=bins
).add_to(m)

folium.LayerControl().add_to(m)
#----------------
#Add circle to map with size related to %cases
for index, row in us1.iterrows():
	radius1 = row['Diff']/1000
	color1 = "#3db7e3"

	if row['Diff'] < 0:
		print(row['Province_State'])
		radius1 = 20
		color1 = "#31b03b"

	folium.CircleMarker([row['Lat'], row['Long_']],radius=radius1,fill_color=color1,tooltip=str(row['Province_State'])+': '+str(row['Diff']),show=False).add_to(m)


m.save('us_covid.html')
    