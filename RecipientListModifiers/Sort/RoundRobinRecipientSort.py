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

from datetime import date, datetime
from ConfigParser import ConfigParser
from RecipientListModifiers.RecipientListModifier import RecipientListModifier
from RecipientListModifiers.Result import Result
from RecipientListModifiers.Sort.RoundRobinSettings import RoundRobinSettings

class RoundRobinRecipientSort(RecipientListModifier):

	def __init__(self, RoundRobinSettings):
		self.__RoundRobinSettings = RoundRobinSettings

	@staticmethod
	def factory(MyConfig, ModifierClass):
		return RoundRobinRecipientSort(RoundRobinSettings(ConfigParser('config/sort/roundRobin.txt')))

	def getJidHandleGroupResult(self, JidHandleGroups, sender, messageBody):
		if (len(JidHandleGroups) > 0):
			for JidHandleGroup in JidHandleGroups:
				JidHandles = JidHandleGroup.getJidHandles()
				if (len(JidHandles) > 0):
					timeUnit = self.__RoundRobinSettings.getTimeUnit()
					numSupportAvailable = len(JidHandles)

					sortByIndex = 0
					CurrentDate = date.today()
					if (timeUnit == 'daily'):
						day = datetime.now().timetuple().tm_yday
						sortByIndex = day % numSupportAvailable
					elif(timeUnit == 'weekly'):
						isoWeek = CurrentDate.isocalendar()[1]
						sortByIndex = isoWeek % numSupportAvailable
					elif(timeUnit == 'monthly'):
						month = CurrentDate.month
						sortByIndex = month % numSupportAvailable

					JidHandles = JidHandles[sortByIndex::] + JidHandles[:sortByIndex]
					JidHandleGroup.setJidHandles(JidHandles)

		return Result(JidHandleGroups)