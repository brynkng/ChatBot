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

class ConfigParser():

	def __init__(self, configFilePath):
		self.__configString = open(configFilePath, 'r').read()

	def findConfigLine(self, idString):
		idString += '='
		idStringStartIndex = self.__configString.find(idString)
		if (idStringStartIndex == -1 or self.__configString[idStringStartIndex - 1] == '#'):
			return ''

		idStringValueStartIndex =  idStringStartIndex + len(idString)
		idStringValueEndIndex = self.__configString.find('\n', idStringValueStartIndex)
		if (idStringValueEndIndex == -1): #if we can't find a new line char that means this is the last line
			idStringValueEndIndex = None

		return self.__configString[idStringValueStartIndex : idStringValueEndIndex].strip('"\'')

	def findConfigLinesBetween(self, startKey = False, endKey = False):
		idStringStartIndex = self.__configString.find(startKey)
		if (idStringStartIndex == -1):
			return []

		if (startKey):
			idStringValueStartIndex =  idStringStartIndex + len(startKey)
		else:
			idStringValueStartIndex = 0

		if (endKey):
			idStringValueEndIndex = self.__configString.find(endKey)
		else:
			idStringValueEndIndex = len(self.__configString)


		return [configLine
				for configLine in self.__configString[idStringValueStartIndex: idStringValueEndIndex].split('\n')
				if not configLine.startswith('#') and configLine.strip()]