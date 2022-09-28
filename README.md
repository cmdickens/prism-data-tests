# PRISM Data Tests
This project is a test messing with PRISM data. The main.py uses a formula given to me by Majari and Tom.
I honestly don't remember the formula. The formula is for cotton flea hopper emergence over time.
In order for their populations to start emerging a certain amount of temperature has to be accumulated.


## Getting PRISM Data
The main.py files expects a directory called `daily-data` to be in the same directory.
daily-data should contain directories in the format of `PRISM_tmean_stable_4kmD2_20200109_bil`.
Where tmean means that the data is for mean temp, 4km is the size of data grid chunks, 2020 is the year, 01 is the month and 09 is the day. 
You can manually download the data from the [PRISM FTP server](https://ftp.prism.oregonstate.edu/daily/tmean/).

I created a helper script to download the data and extract it for you. although I think there was bug when you choose more than one year to download the data for.
> Note: the script is meant to run in a linux environment

## Dependencies
`main.py` depends on
- [rasterio](https://rasterio.readthedocs.io/en/latest/index.html) - used to decode the .bil data format used by PRISM
- - [GDAL](https://gdal.org/) - is what actually decodes the data. rasterio is just a nice wrapper for it
- [matplotlib](https://matplotlib.org/) - used to graph
- [numpy](https://numpy.org/) - used for calculations

The `download-data.sh` needs
- [wget](https://www.gnu.org/software/wget/)

>Note: If you need any help you can reach me at edwinmirandat@gmail.com
