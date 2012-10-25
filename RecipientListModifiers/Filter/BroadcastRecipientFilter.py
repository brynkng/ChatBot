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

from RecipientListModifiers.RecipientListModifier import RecipientListModifier
from RecipientListModifiers.Result import Result

class BroadcastRecipientFilter(RecipientListModifier):
	"""" This filter is intended to be used to send a broadcast to all recipients.
		 It will filter out the sender"""

	def __init__(self, MyConfig):
		pass

	def getJidHandleGroupResult(self, JidHandleGroups, sender, messageBody):

		for JidHandleGroup in JidHandleGroups:
			if JidHandleGroup.shouldUseListModifierClass(self.__class__):
				JidHandles = [JidHandle for JidHandle in JidHandleGroup.getJidHandles() if JidHandle.getJid() != sender]
				JidHandleGroup.setJidHandles(JidHandles)

		return Result(JidHandleGroups)