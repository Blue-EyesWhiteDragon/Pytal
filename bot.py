#
# Vital Bank/Preset/Wavetable downloader
# Scowers the Vital forums for presets, wavetables and banks and downloads them for use in the Vital VSTi
# (c) Blue-EyesWhiteDragon, 2020.
# Blue-EyesWhiteDragon.users.no-reply@github.com
#

import os
import re
import subprocess
import wget
import json
import multiprocessing
from coolname import generate_slug
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path

# We're gonna search for any url that has a upload with the ext .vital or .vitalbank

global VITAL_PATH, SAVE_PATH, PRESET_PATH, BANK_PATH, TABLE_PATH
PREFIX_URL = "https://forum.vital.audio"
BASE_URL = PREFIX_URL + "/c/share"

def console_indent ( amount = 1 ):
	return (" "*(3*amount)+"↳") # feel free to use .encode("utf8") if outputting to file

def pad_url (url):
	return "\""+url+"\""

def check_directories ( _VITAL_PATH, _SAVE_PATH, _PRESET_PATH, _BANK_PATH, _TABLE_PATH ):

	global VITAL_PATH, SAVE_PATH, PRESET_PATH, BANK_PATH, TABLE_PATH

	VITAL_PATH = _VITAL_PATH
	SAVE_PATH = os.path.join(VITAL_PATH, _SAVE_PATH)
	PRESET_PATH = os.path.join(SAVE_PATH, _PRESET_PATH)
	BANK_PATH = os.path.join(SAVE_PATH, _BANK_PATH)
	TABLE_PATH = os.path.join(SAVE_PATH, _TABLE_PATH)

	if ( os.path.isdir(SAVE_PATH) == False ):
		print("Download folder not present.\n> Creating", pad_url(SAVE_PATH))
		os.mkdir(SAVE_PATH)

	if ( os.path.isdir(PRESET_PATH) == False ):
		print("Preset folder not present.\n> Creating", pad_url(PRESET_PATH))
		os.mkdir(PRESET_PATH)

	if ( os.path.isdir(BANK_PATH) == False ):
		print("Bank folder not present.\n> Creating", pad_url(BANK_PATH))
		os.mkdir(BANK_PATH)
	
	if ( os.path.isdir(TABLE_PATH) == False ):
		print("Wavetable folder not present.\n> Creating", pad_url(TABLE_PATH))
		os.mkdir(TABLE_PATH)
	
	return 0

def download_preset ( preset, acquired, additions : int ):
	
	preset = PREFIX_URL + preset
	filename = preset.rsplit("/", 1)[-1]

	if ( filename in acquired ):
		return 0

	print(console_indent(2), "Downloading:", pad_url(preset))
	re_table_or_bank = re.compile("(table|bank)")
	result = re_table_or_bank.search(filename)
	saveto = ""
	funky_filename = generate_slug(2) +".vital"
	if result is not None: 
		bank_or_table = result.group(1)
		saveto = os.path.join(globals()[bank_or_table.upper()+"_PATH"], funky_filename+bank_or_table)
	else:
		saveto = os.path.join(PRESET_PATH, funky_filename)

	print(console_indent(3), "Saving as", pad_url(saveto))

	try:
		print(preset)
		wget.download(preset, saveto)
	except:
		print(console_indent(4), "Couldn't download preset! (Wrong format or a broken URI)\n", console_indent(4), "Continuing...")
		return 0

	acquired[filename] = saveto

	return 1;
	
	#wget.download()

def grab_preset ( url, acquired ):
	additions = 0
	print(console_indent(1), "Crawling:", pad_url(url))
	page = urlopen( url )
	html = page.read().decode("utf-8")
	soup = BeautifulSoup(html,"html.parser")
	for link in soup.find_all("a",href=re.compile(".*\.vital(bank|table)?")):
		additions += download_preset(link["href"], acquired, additions)
	return additions;

def grab_presets ( acquired, acquired_location ):
	additions = 0
	print(multiprocessing.cpu_count, "cores detected!")
	print("Grabbing presets!")
	if ( len(acquired) >= 1 ):
		print(console_indent(0), "Acquired presets (" + str(len(acquired)) + ")")
	else:
		print(console_indent(0), "No previously acquired presets!")
	
	page = urlopen(BASE_URL)
	html = page.read().decode("utf-8")
	soup = BeautifulSoup(html,"html.parser")
	
	print (console_indent(0), "Crawling:", pad_url(BASE_URL))
	for link in soup.find_all("a",href=re.compile("\/t\/.*[0-9]$")):
		additions += grab_preset(link["href"], acquired)
	
	print("Grabbed", additions == 0 and "no" or additions, "new presets!")

	with open(acquired_location, "w") as file:
		json.dump(acquired, file)

	return 0