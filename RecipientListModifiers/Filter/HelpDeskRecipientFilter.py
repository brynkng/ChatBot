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
from JidHandle import JidHandle
from JidHandleGroup import JidHandleGroup
from RecipientChooser import RecipientChooser
from RecipientListModifiers.RecipientListModifier import RecipientListModifier
from RecipientListModifiers.Result import Result
from copy import deepcopy

class HelpDeskRecipientFilter(RecipientListModifier):

	def __init__(self, MyConfig):
		self.__MyConfig = MyConfig
		self.__JidHandleGroups = []
		self.__IgnoredRecipients = []
		self.__requesters = []
		self.__RequestedRecipient = []
		self.__RequestedJidHandleGroup = None
		self.__LastConfirmedRecipient = []
		self.__lastConfirmedTime = None
		self.__noAvailableUsers = False
		self.__forwardedMessageSecondThreshold = MyConfig.getForwardedMessageSecondThreshold()

	def getJidHandleGroupResult(self, JidHandleGroups, sender, messageBody):
		self.__JidHandleGroups = JidHandleGroups

		if (self.__noAvailableUsers):
			return Result(resultCode=Result.NOBODY_AVAILABLE)
		else:
			if (self.__LastConfirmedRecipient and not self.__lastConfirmedRecipientTimedOut()):
				self.__RequestedRecipient = self.__LastConfirmedRecipient
			else:
				if not (self.__RequestedRecipient and self.__JidHandleGroups):
					self.__RequestedRecipient = self.__firstRecipientFromFirstGroup()

			return Result([JidHandleGroup(self.__RequestedRecipient)])

	def addRequester(self, requester):
		self.__requesters.append(requester)

	def getRequesterJidHandles(self):
		return [JidHandle(requester, requester) for requester in self.__requesters]

	def alreadyMessagedRequester(self, requester):
		return requester in self.__requesters

	def presenceConfirmed(self):
		self.__IgnoredRecipients = []
		self.__requesters = []
		self.__LastConfirmedRecipient = self.__RequestedRecipient
		self.__lastConfirmedTime = time()
		self.__RequestedRecipient = []
		self.__RequestedJidHandleGroup = None
		self.__noAvailableUsers = False

	def getCurrentRequestedRecipient(self):
		return self.__RequestedRecipient

	def setRequestedRecipientToPassedGroupIdentifier(self, messageBody, JidHandleGroups):
		for JidHandleGroup in JidHandleGroups:
			if (JidHandleGroup.getGroupIdentifierString() in messageBody):
				MyRecipientChooser = RecipientChooser(self.__MyConfig, [JidHandleGroup])
				Result = MyRecipientChooser.getJidHandleGroupResult(None, messageBody)
				if Result.hasJidHandles():
					for JidHandle in Result.getJidHandleGroups()[0].getJidHandles():
						if JidHandle not in self.__IgnoredRecipients:
							self.__RequestedRecipient = Result.getJidHandleGroups()[0].getJidHandles()
							self.__RequestedJidHandleGroup = JidHandleGroup
							self.__timeOutLastConfirmedRecipient()
							return True

		return False

	def currentRequestedUserHasTimedOut(self):
		if not (self.__noAvailableUsers):
			if (self.__RequestedRecipient):
				self.__IgnoredRecipients.append(self.__RequestedRecipient[0])

			self.__timeOutLastConfirmedRecipient()

			JidHandleGroups = self.__getOrderedJidHandleGroups()

			for JidHandleGroup in JidHandleGroups:
				for JidHandle in JidHandleGroup.getJidHandles():
					if (JidHandle not in self.__IgnoredRecipients):
						self.__RequestedRecipient = [JidHandle]
						return

			self.__RequestedRecipient = []
			self.__RequestedJidHandleGroup = None
			self.__noAvailableUsers = True

	def __firstRecipientFromFirstGroup(self):
		return [self.__JidHandleGroups[0].getJidHandles()[0]]

	def __lastConfirmedRecipientTimedOut(self):
		return time() > self.__lastConfirmedTime + int(self.__forwardedMessageSecondThreshold)

	def __timeOutLastConfirmedRecipient(self):
		self.__lastConfirmedTime = None
		self.__LastConfirmedRecipient = []

	def __getOrderedJidHandleGroups(self):
		JidHandleGroups = deepcopy(self.__JidHandleGroups)
		if (self.__RequestedJidHandleGroup):
			for key, JidHandleGroup in enumerate(JidHandleGroups):
				if JidHandleGroup == self.__RequestedJidHandleGroup:
					del JidHandleGroups[key]
					JidHandleGroups.insert(0, self.__RequestedJidHandleGroup)

		return JidHandleGroups
