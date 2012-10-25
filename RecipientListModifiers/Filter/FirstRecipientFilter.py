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

class FirstRecipientFilter(RecipientListModifier):

	def __init__(self, MyConfig):
		pass

	def getJidHandleGroupResult(self, JidHandleGroups, sender, messageBody):
		if (len(JidHandleGroups) > 0):
			FirstJidHandleGroup = JidHandleGroups[0]
			JidHandles = FirstJidHandleGroup.getJidHandles()
			if (JidHandles):
				FirstJidHandleGroup.setJidHandles([JidHandles[0]])
			return Result([FirstJidHandleGroup])
		else:
			return Result(JidHandleGroups)