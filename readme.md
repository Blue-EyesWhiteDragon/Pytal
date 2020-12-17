# Pytal #

A Vital preset downloader.

And no it doesn't scroll down, yet.

And no it's not for MacOS or Linux users, yet.

## Installation ##

Requires: Python 3, Windows (for now)

There is a `ez_install` batch file that uses Powershell and Chocolately package manager (also will be installed) to install Python 3

After you have Python installed or if you already have it installed:

Run install_requirements in the `scripts` folder to install the required python modules! or run `python -m pip install -r requirements.txt` on your shell of choice inside the directory.

You can now either run `python {folder of this project}` outside the directory or `python __main__.py` inside the directory!

## Using presets ##

#### Navigate to your download folder that what was set up in `config.json`, this should be `__pydownload__` by default also this is set to change in the future ####

![](https://i.imgur.com/Qs0opPD.png)

## Issues ##

#### It's saying Vital is not installed correctly ####
Please make sure Vital is installed and its data folder is at `C:/Users/%USERNAME%/Documents/Vital`, if it is **NOT** then you should specify where it is inside the `config.json` under "VITAL_PATH". You can open this file with any text editor like `notepad.exe` and save it. If it is still happening after doing this, please report an issue!

#### It fails on launch with some long error message about utf-8 or encoding ###
If you're running this from a bash shell the code may fail based on an Unicode error. There is a function inside `bot.py` at `line 26` with a comment about `.encode()`, you can add `.encode()` function there with `notepad.exe` to look like this:
```python
return (" "*(3*amount)+"↳").encode("utf8")
```
Save it and you error should be resolved

#### My error isn't listed ####
Create an issue here on GitHub so all the public can see how it came up and how we resolved it! Open source, baby!

Have fun,

BEWD.
