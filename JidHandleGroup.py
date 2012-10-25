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


class JidHandleGroup():

	def __init__(self, JidHandles, IgnoredListModifiers=None, groupIdentifierString=None):
		if not IgnoredListModifiers: IgnoredListModifiers = []
		self.__JidHandles = JidHandles
		self.__IgnoredListModifiers = IgnoredListModifiers
		self.__groupIdentifierString = groupIdentifierString


	def getJidHandles(self):
		return self.__JidHandles

	def setJidHandles(self, JidHandles):
		self.__JidHandles = JidHandles

	def getIgnoredListModifierClasses(self):
		return self.__IgnoredListModifiers

	def getGroupIdentifierString(self):
		return self.__groupIdentifierString

	def shouldUseListModifierClass(self, ListModifierClass):
		return ListModifierClass not in self.__IgnoredListModifiers


	def __eq__(self, other):
		return self.__JidHandles == other.getJidHandles() \
			and self.__IgnoredListModifiers == other.getIgnoredListModifierClasses()