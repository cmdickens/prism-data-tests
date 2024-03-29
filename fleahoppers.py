from setup import get_start_date, get_end_date, get_longitude, get_latitude
import math
import numpy as np
import rasterio
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
		
start_date = get_start_date()
end_date = get_end_date()

longitude = get_longitude()
latitude = get_latitude()

# CONSTANTS
temp_threshold = 14.82
B0 = -25.1941
B1 = 0.0363

accumulated_degree_days = []
dates = []
temp_summation = 0
proportions = []

current_date = start_date
while current_date <= end_date:

	ds = rasterio.open(f"./daily-data/PRISM_tmean_stable_4kmD2_{current_date.year}{current_date.month:02d}{current_date.day:02d}_bil.bil", "r")
	px, py = ds.index(longitude, latitude)
	temp = ds.read(1)[px][py]

	degree_days = temp - temp_threshold
	if degree_days < 0:
		degree_days = 0
	temp_summation += degree_days
	accumulated_degree_days.append(temp_summation)

	numerator = math.exp(B0 + B1*temp_summation)
	proportion = numerator / (1 + numerator)
	proportions.append(proportion)
	
	dates.append(current_date)

	current_date = current_date + dt.timedelta(days=1)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))

plt.plot(dates, proportions)
plt.gcf().autofmt_xdate()

plt.title(f"Proportion of Nymph Emergence\n{start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')}, at ({latitude}, {longitude})")
plt.xlabel("Dates")
plt.ylabel("Proportion of Nymph Emergence")
plt.savefig("fleahoppers.png") 