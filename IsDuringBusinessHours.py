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

from resources.period import in_period, is_holiday

class IsDuringBusinessHours():

	def __init__(self, Config):
		businessHoursSetting = Config.getBusinessHoursSettingString()

		if not businessHoursSetting:
			self.__isDuringBusinessHours = True
		else:
			self.__isDuringBusinessHours = in_period(businessHoursSetting) and not is_holiday(holidays="config/holidays.txt")

	def isDuringBusinessHours(self):
		return self.__isDuringBusinessHours
