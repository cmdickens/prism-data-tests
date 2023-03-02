import os
import rasterio
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import numpy as np

import math


#filename = "./daily-data/PRISM_ppt_provisional_4kmM3_2020_bil.bil"
#ds = rasterio.open("./daily-data/PRISM_ppt_provisional_4kmM3_202202_bil.bil", "r")

files = os.listdir("./daily-data/")
print(len(files))

# The starting and end dates to run the calculations for.
# Depends on what years you have data for
biofix = "20200901" # september 01
endDate = "20210630"

# the temp in C required for it to add to the ADD
tempTreshold = 14.82

date = {
  "year": int(biofix[0:4]),
  "month": int(biofix[4:6]),
  "day": int(biofix[6:])
}

dates =  []

temps = []

add = 0
adds = []

ps = []

# values given to me by Tom and Manjari
b0 = -25.1941
b1 = 0.0363



#print(endDate[0:4], endDate[4:6], endDate[6:])
while(True):
  dirname = f"PRISM_tmean_stable_4kmD2_{date['year']}{date['month']:0>2}{date['day']:0>2}_bil"
  filename = ""

  try:
    files.index(dirname)
  except ValueError:
    print(dirname, "dir does not exist")
    if date["month"] == 13:
      date["year"] += 1
      date["month"] = 1
      date["day"] = 1

    if (date["month"] == 2 and date["day"] >= 28) or (date["day"] >= 30):
      date["month"] += 1
      date["day"] = 1
      continue

    print("something else is wrong man")
  else:
    #print(dirname, "dir good")
    print(f"[{date['year']}/{date['month']:0>2}/{date['day']:0>2}]")

    filename = f"./daily-data/{dirname}/{dirname}.bil"
    ds = rasterio.open(filename, "r")

    # convert from longitude, latitude to the row, col values

    # this variable is what decides which location we are running the calculations for.
    # The PRISM data is data for the entire US, this chooses the specific location.
    pixelCoords = ds.index(-100.7415, 32.2377)
    temp = ds.read(1)[pixelCoords[0]][pixelCoords[1]]
    adjustedTemp = temp - tempTreshold
    #print(temp, "\n")
    temps.append(temp)

    # if temp passes treshold then add it to the add
    if adjustedTemp > 0:
      add += adjustedTemp
    adds.append(add)


    p = 1 / (1 + math.exp( -1 * (b0 + (b1 * add) ) ) )
    ps.append(p)


    dates.append(f"{date['year']}-{date['month']:0>2}-{date['day']:0>2}")

    if date["year"] == int(endDate[0:4]) and date["month"] == int(endDate[4:6]) and date["day"] == int(endDate[6:]):
      break

    date["day"] += 1


posTemp = np.array(temps)
posTemp[posTemp < tempTreshold] = tempTreshold

#plt.plot(temps)
fig = plt.figure()
ax1, ax2, ax3 = fig.subplots(3, 1)

ax1.fill_between(x= np.arange(0, len(temps), 1), y1= posTemp, y2= tempTreshold, interpolate= True, color= "green", alpha= 0.2)
ax1.plot(temps)
ax1.set_xlabel("days")
ax1.set_ylabel("temp")

zt1 = np.arange(0, 100, 100/len(adds)) / 100
ax2.plot(dates, adds)
#ax2.set_xticklabels([dates[0], dates[-1]], rotation = 0)
ax2.set_xticks([dates[0], dates[len(dates)//4], dates[len(dates)//2], dates[len(dates)//4 * 3], dates[-1]], rotation = 0)
ax2.set_xlabel("days")
ax2.set_ylabel("ADD")

ax3.scatter(adds, ps)
ax3.set_xlabel("ADD")
ax3.set_ylabel("P")

plt.show()
