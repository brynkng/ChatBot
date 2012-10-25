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

from RecipientListModifiers.Result import Result
from ConfigurationError import ConfigurationError
from copy import deepcopy

class RecipientChooser():

	def __init__(self, MyConfig, JidHandleGroups=None):
		if not (JidHandleGroups):
			JidHandleGroups = MyConfig.getJidHandleGroups()
		self.__JidHandleGroups = JidHandleGroups
		self.__OrderedRecipientListModifiers = MyConfig.getOrderedRecipientListModifiers()


	def getJidHandleGroupResult(self, sender, messageBody):
		if (self.__OrderedRecipientListModifiers):
			ListResult = self.__applyListModifiers(messageBody, sender)
		else:
			ListResult = Result(self.__JidHandleGroups)

		return ListResult


	def getRecipientListModifierByClass(self, Class):
		self.getJidHandleGroupResult(None, '')
		for FilterOrSort in self.__OrderedRecipientListModifiers:
			if self.__isListModifierInstanceOfClass(Class, FilterOrSort):
				return FilterOrSort

		raise ConfigurationError('Required Recipient List Modifier: ' + Class.__name__ + ' was not found!')


	def getJidHandleFromJid(self, jid):
		for JidHandleGroup in self.__JidHandleGroups:
			for MyJidHandle in JidHandleGroup.getJidHandles():
				if MyJidHandle.getJid() == jid:
					return MyJidHandle

		return None


	def __isListModifierInstanceOfClass(self, Class, FilterOrSort):
		"hack job because isinstance() doesn't work here due to some weird namespace issues"
		return FilterOrSort.__class__.__name__ == Class.__name__


	def __applyListModifiers(self, messageBody, sender):
		FirstListModifier = self.__OrderedRecipientListModifiers[0]
		ListResult = FirstListModifier.getJidHandleGroupResult(
			deepcopy(self.__JidHandleGroups),
			sender,
			messageBody
		)

		if (ListResult.hasJidHandles()):
			iterListModifiers = iter(self.__OrderedRecipientListModifiers)
			next(iterListModifiers)

			for ListModifier in iterListModifiers:
				self._clearEmptyGroups(ListResult)
				if (ListResult.hasJidHandles()):
					ListResult = ListModifier.getJidHandleGroupResult(
						ListResult.getJidHandleGroups(),
						sender,
						messageBody
					)

		return ListResult

	def _clearEmptyGroups(self, ListResult):
		JidHandleGroups = ListResult.getJidHandleGroups()
		for key, JidHandleGroup in enumerate(ListResult.getJidHandleGroups()):
			if not (JidHandleGroup.getJidHandles()):
				del JidHandleGroups[key]

		ListResult.setJidHandleGroups(JidHandleGroups)