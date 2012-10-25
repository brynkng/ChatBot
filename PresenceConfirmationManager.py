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

from time import time
class PresenceConfirmationManager():

	def __init__(self, MyConfig):
		self.__confirmationRequestSecondThreshold = MyConfig.getConfirmationRequestSecondThreshold()
		self.__requestStartTime = None
		self.__hasPendingRequest = False

	def startNewRequest(self):
		self.__hasPendingRequest = True
		self.__requestStartTime = time()

	def hasTimedOut(self):
		return time() > self.__requestStartTime + int(self.__confirmationRequestSecondThreshold)

	def hasPendingRequest(self):
		return self.__hasPendingRequest

	def confirmPresence(self):
		self.__hasPendingRequest = False
		self.__requestStartTime = None