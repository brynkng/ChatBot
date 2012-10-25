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

from IsDuringBusinessHours import IsDuringBusinessHours
from RecipientListModifiers.RecipientListModifier import RecipientListModifier
from RecipientListModifiers.Result import Result

class IsDuringBusinessHoursFilter(RecipientListModifier):

	def __init__(self, IsDuringBusinessHours):
		self.__isDuringBusinessHours = IsDuringBusinessHours.isDuringBusinessHours()

	@staticmethod
	def factory(MyConfig, ModifierClass):
		return IsDuringBusinessHoursFilter(IsDuringBusinessHours(MyConfig))

	def getJidHandleGroupResult(self, JidHandleGroups, sender, messageBody):
		if (self.__isDuringBusinessHours):
			return Result(JidHandleGroups)
		else:
			return Result(resultCode=Result.DONT_SEND_RELAY_MESSAGE)
