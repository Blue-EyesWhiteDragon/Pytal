#
# Vital Bank/Preset/Wavetable downloader
# Scowers the Vital forums for presets, wavetables and banks and downloads them for use in the Vital VSTi
# (c) Blue-EyesWhiteDragon, 2020.
# Blue-EyesWhiteDragon.users.no-reply@github.com
#

import os
import sys
import json
from pathlib import Path
from modules import m_grab_presets

_vM, _vm, _vp = (0, 0, 1)
_version = ( str(_vM) + "." + str(_vm) + "." + str(_vp) )
_g_config = {}
_g_config_location = os.path.abspath(os.path.join(__file__, "../config.json"))
_g_acquired = {}
_g_acquired_location = os.path.abspath(os.path.join(__file__, "../acquired.json"))
_g_vital_path = os.path.join(str(Path.home()), "Documents", "Vital")

def read_config ( config ) :
	global _g_vital_path, _g_config, _g_config_location

	print ("Loading config...")

	with open(_g_config_location, "r+") as file:
		config = json.load(file)
	
	_g_config = config

	return 0

def check_vital_installation ( vital_path ) :
	if ( os.path.isdir(vital_path) == False ):
		sys.exit("Vital is not installed correctly, please check config.json or your installation!")
	else:
		print("Vital is installed correctly @", m_grab_presets.pad_url(vital_path), "\n", m_grab_presets.console_indent(0), "Continuing...")

def set_acquired ( acquired, config ):
	global _g_vital_path, _g_acquired, _g_acquired_location

	print ("Checking for previous downloads...")

	_assume_acquired = _g_acquired_location

	if ( "acquiredJSON" in config and  config["acquiredJSON"] != "" ):
		_assume_acquired = config["acquiredJSON"]
	else:
		_assume_acquired = os.path.join(_g_vital_path, config["SAVE_PATH"], "acquired.json")
	
	if ( os.path.isfile(_assume_acquired) == True ):
		print(m_grab_presets.console_indent(0),"Previous downloads detected, ommiting them!")
		with open(_assume_acquired, "r+") as file:
			acquired = json.load(file)
		_g_acquired_location = _assume_acquired
	else:
		print(m_grab_presets.console_indent(0),"No previous downloads detected! Let's get cracking!")

	with open(_assume_acquired, "w+") as file:
		json.dump(acquired, file)
	
	config["acquiredJSON"] = _assume_acquired

	with open(_g_config_location, "w+") as file:
		json.dump(config, file)

	_g_acquired = acquired
	_g_config = config
	
	return 0

def main ():
	# use: sys.stdout = open(os.path.join(__file__, "../output.txt"), "w"), if outputting to file
	read_config(_g_config)
	check_vital_installation(_g_vital_path)
	m_grab_presets.check_directories(_g_vital_path, _g_config["SAVE_PATH"], _g_config["PRESET_PATH"], _g_config["BANK_PATH"], _g_config["TABLE_PATH"])
	set_acquired(_g_acquired, _g_config)
	m_grab_presets.grab_presets(_g_acquired, _g_acquired_location)
	sys.stdout.close()
	return 0

if __name__ == "__main__":
	main()