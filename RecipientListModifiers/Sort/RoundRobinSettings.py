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

from ConfigurationError import ConfigurationError

class RoundRobinSettings():

	def __init__(self, ConfigParser):
		self.__timeUnit = ConfigParser.findConfigLine('time_unit')
		self.__validateSettings()

	def getTimeUnit(self):
		return self.__timeUnit

	def __validateSettings(self):
		validUnits = ['monthly', 'weekly', 'daily']
		if not (self.__timeUnit in validUnits):
			message = 'Invalid time unit for round robin recipient sort settings. Must be one of the following: \n'
			message += '\n'.join(validUnits)
			message += '\n but got: ' + self.__timeUnit
			raise ConfigurationError(message)