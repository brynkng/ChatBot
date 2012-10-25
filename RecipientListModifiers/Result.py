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

class Result():

	OK = 0
	NOBODY_AVAILABLE = 1
	DONT_SEND_ANY_MESSAGE = 2
	DONT_SEND_RELAY_MESSAGE = 3

	def __init__(self, JidHandleGroups = False, resultCode = False):
		self.__JidHandleGroups = JidHandleGroups

		if (resultCode == False):
			if (self.__foundJidHandle()):
				resultCode = self.OK
			else:
				resultCode = self.NOBODY_AVAILABLE

		self.__resultCode = resultCode

	def setJidHandleGroups(self, JidHandleGroups):
		self.__JidHandleGroups = JidHandleGroups

	def hasJidHandles(self):
		return self.__resultCode == self.OK

	def nobodyAvailable(self):
		return self.__resultCode == self.NOBODY_AVAILABLE

	def shouldSendConfirmationMessage(self):
		return self.__resultCode != self.DONT_SEND_ANY_MESSAGE

	def shouldSendNobodyAvailableMessage(self):
		return self.__resultCode != self.DONT_SEND_ANY_MESSAGE

	def shouldSendRelayMessage(self):
		return self.__resultCode != self.DONT_SEND_ANY_MESSAGE and self.__resultCode != self.DONT_SEND_RELAY_MESSAGE

	def getJidHandleGroups(self):
		return self.__JidHandleGroups

	def getCode(self):
		return self.__resultCode

	def __foundJidHandle(self):
		for JidHandleGroup in self.__JidHandleGroups:
			if (JidHandleGroup.getJidHandles()):
				return True

		return False