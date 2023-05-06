from setup import get_start_date, get_end_date, get_longitude, get_latitude
from math import exp, sqrt, pow, pi
import rasterio
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
		
start_date = get_start_date()
end_date = get_end_date()

longitude = get_longitude()
latitude = get_latitude()

# CONSTANTS
temp_threshold = 10.50
weighting_coefficients = [0.02, 0.07, 0.18, 0.32, 0.41]
sigma_values = [50, 70, 90, 120, 170]
peak = 237			# 237 DD is how many it takes to get from egg to adult for this species

temp_summation = 0
accumulated_degree_days = []
dates = []
thrips_magnitudes = []

current_date = start_date
while current_date <= end_date:

	ds = rasterio.open(f"./daily-data/PRISM_tmean_stable_4kmD2_{current_date.year}{current_date.month:02d}{current_date.day:02d}_bil.bil", "r")
	px, py = ds.index(longitude, latitude)
	temp = ds.read(1)[px][py]

	degree_days = temp - temp_threshold
	if degree_days < 0:
		degree_days = 0
	temp_summation += degree_days

	magnitude = 0
	for i in range(5):
		part_one = weighting_coefficients[i] / sqrt(2 * pi * sigma_values[i])
		part_two = exp(-(pow(temp_summation - peak * (i+1), 2)) / (2 * pow(sigma_values[i], 2)))
		magnitude += part_one * part_two

	accumulated_degree_days.append(temp_summation)
	thrips_magnitudes.append(magnitude)
	
	dates.append(current_date)

	current_date = current_date + dt.timedelta(days=1)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=50))

plt.plot(dates, thrips_magnitudes)
plt.gcf().autofmt_xdate()

plt.title(f"Thrips Mixture Distribution\n{start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')}, at ({latitude}, {longitude})")
plt.xlabel("Dates")
plt.ylabel("Thrips Magnitude")
plt.savefig("thrips.png") 