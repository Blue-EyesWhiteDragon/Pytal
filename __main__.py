#
# Vital Bank/Preset/Wavetable downloader
# Scowers the Vital forums for presets, wavetables and banks and downloads them for use in the Vital VSTi
# (c) Blue-EyesWhiteDragon, 2020.
# Blue-EyesWhiteDragon.users.no-reply@github.com
#

import os
import sys
import json
import bot
from pathlib import Path

_version = "0.1"
_config = {}
_config_location = os.path.abspath(os.path.join(__file__, "../config.json"))
_acquired = {}
_acquired_location = os.path.abspath(os.path.join(__file__, "../acquired.json"))
_vital_path = os.path.join(str(Path.home()), "Documents", "Vital")

def read_config ( config ) :
	global _vital_path, _config

	with open(_config_location, "r") as file:
		config = json.load(file)

	if ( "VITAL_PATH" in config and config["VITAL_PATH"] != "" ) :
		_vital_path = config["VITAL_PATH"]
	else :
		config["VITAL_PATH"] = _vital_path
	
	with open(_config_location, "w") as file:
		json.dump(config, file)
	
	_config = config

	return 0

def check_vital_installation ( vital_path ) :
	if ( os.path.isdir(vital_path) == False ):
		sys.exit("Vital is not installed correctly, please check config.json or your installation!")
	else:
		print("Vital is installed correctly @", bot.pad_url(vital_path), "\n", bot.console_indent(0), "Continuing...")

def set_acquired ( acquired ):
	global _vital_path, _acquired, _acquired_location

	print ("Checking for previous downloads...")

	_assume_acquired = os.path.join(_vital_path, _config["SAVE_PATH"], "acquired.json")

	if ( "acquiredJSON" in _config ):
		_assume_acquired = os.path.join(_config["acquiredJSON"])
	
	if ( os.path.isfile(_assume_acquired) == True ):
		print(bot.console_indent(0),"Previous downloads detected, ommiting them!")
		_acquired_location = _assume_acquired

	with open(_acquired_location, "r") as file:
		acquired = json.load(file)
	
	_acquired_location = _assume_acquired

	with open(_acquired_location, "w") as file:
		json.dump(acquired, file)
	
	_acquired = acquired

	return 0

def main ():
	# use: sys.stdout = open(os.path.join(__file__, "../output.txt"), "w"), if outputting to file
	read_config(_config)
	check_vital_installation(_vital_path)
	set_acquired(_acquired)
	bot.check_directories(_vital_path, _config["SAVE_PATH"], _config["PRESET_PATH"], _config["BANK_PATH"], _config["TABLE_PATH"])
	bot.grab_presets(_acquired, _acquired_location)
	sys.stdout.close()
	return 0

if __name__ == "__main__":
	main()