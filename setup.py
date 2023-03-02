from pyPRISMClimate import get_prism_monthlys, get_prism_monthly_single, get_prism_dailys, get_prism_daily_single, get_prism_normals
import os, shutil
import datetime as dt

def get_start_date():
	return dt.datetime.strptime("01-09-2019", "%d-%m-%Y").date()		#DDMMYYYY

def get_end_date():
	return dt.datetime.strptime("01-04-2020", "%d-%m-%Y").date()

def get_folder_name():
	return "./daily-data"

def get_longitude():
	return -96.499281

def get_latitude():
	return 30.115312

def clean_data_folder(folder):
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
	# clean daily data folder
	folder = get_folder_name()
	clean_data_folder(folder)
			
	start_date = get_start_date()
	end_date = get_end_date()

	# Get daily mean temperature for start_date to end_date
	get_prism_dailys("tmean", 
					min_date = start_date.isoformat(), 
					max_date = end_date.isoformat(), 
					dest_path = folder)