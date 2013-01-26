#!/usr/bin/python

##   Copyright (C) 2012 Bryan King
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.


import Config
import ItBot
import sys
from PresenceManager import PresenceManager

if __name__ == '__main__':
	configFilePath = sys.argv.pop()
	MyConfig = Config.Config(configFilePath, PresenceManager())

	ItBot.ItBot(MyConfig)