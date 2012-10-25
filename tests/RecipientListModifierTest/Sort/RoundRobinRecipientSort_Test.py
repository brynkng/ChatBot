import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Sort.RoundRobinRecipientSort import RoundRobinRecipientSort

from ludibrio import *
from datetime import date, datetime

class RoundRobinRecipientSortTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)

		self.__JidHandleGroups = [JidHandleGroup(['first', 'second', 'third'])]


	def tearDown(self):
		unittest.TestCase.tearDown(self)

		if isinstance(date, Stub):
			date.restoure_import()
		if isinstance(datetime, Stub):
			datetime.restoure_import()

	def test_returns_no_jid_handles_if_none_passed(self):
		Setting = self.__givenDailySettingWithTodaysDateNumberBeing(1)
		self.__JidHandleGroups = [JidHandleGroup([])]

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertEquals([], SortedJidHandles)

	#
	# Daily setting
	#

	def test_sorts_with_daily_setting_on_first_day_of_month(self):
		Setting = self.__givenDailySettingWithTodaysDateNumberBeing(1)

		ExpectedJidHandles = ['second', 'third', 'first']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_daily_setting_on_second_day_of_month(self):
		Setting = self.__givenDailySettingWithTodaysDateNumberBeing(2)
		ExpectedJidHandles = ['third', 'first', 'second']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_daily_setting_on_third_day_of_month(self):
		Setting = self.__givenDailySettingWithTodaysDateNumberBeing(3)
		ExpectedJidHandles = ['first', 'second', 'third']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_daily_setting_on_fourth_day_of_month(self):
		Setting = self.__givenDailySettingWithTodaysDateNumberBeing(4)
		ExpectedJidHandles = ['second', 'third', 'first', ]

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)

	#
	# Monthly setting
	#

	def test_sorts_with_monthly_setting_on_first_month(self):
		Setting = self.__givenMonthlySettingWithMonthNumberBeing(1)
		ExpectedJidHandles = ['second', 'third', 'first', ]

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_monthly_setting_on_second_month(self):
		Setting = self.__givenMonthlySettingWithMonthNumberBeing(2)
		ExpectedJidHandles = ['third', 'first', 'second']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_monthly_setting_on_third_month(self):
		Setting = self.__givenMonthlySettingWithMonthNumberBeing(3)
		ExpectedJidHandles = ['first', 'second', 'third']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)

	#
	# Weekly setting
	#

	def test_sorts_with_weekly_setting_on_first_week_of_year(self):
		Setting = self.__givenWeeklySettingWithWeekNumberBeing(1)
		ExpectedJidHandles = ['second', 'third', 'first', ]

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_weekly_setting_on_second_week_of_year(self):
		Setting = self.__givenWeeklySettingWithWeekNumberBeing(2)
		ExpectedJidHandles = ['third', 'first', 'second']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)


	def test_sorts_with_weekly_setting_on_third_week_of_year(self):
		Setting = self.__givenWeeklySettingWithWeekNumberBeing(3)
		ExpectedJidHandles = ['first', 'second', 'third']

		SortedJidHandles = self._getSortedJidHandles(Setting)

		self.assertSequenceEqual(ExpectedJidHandles, SortedJidHandles)

	def __givenDailySettingWithTodaysDateNumberBeing(self, dateNum):
		with Stub() as date:
			from datetime import datetime
			datetime.now().timetuple().tm_yday >> dateNum

		with Stub() as Settings:
			Settings.getTimeUnit() >> 'daily'

		return Settings

	def __givenMonthlySettingWithMonthNumberBeing(self, monthNum):

		with Stub() as date:
			from datetime import date
			date.today().month >> monthNum

		with Stub() as Settings:
			Settings.getTimeUnit() >> 'monthly'

		return Settings

	def __givenWeeklySettingWithWeekNumberBeing(self, weekNum):

		with Stub() as date:
			from datetime import date
			date.today().isocalendar()[1] >> weekNum

		with Stub() as Settings:
			Settings.getTimeUnit() >> 'weekly'

		return Settings

	def _getSortedJidHandles(self, Setting):
		Sort = RoundRobinRecipientSort(Setting)
		Result = Sort.getJidHandleGroupResult(self.__JidHandleGroups, None, '')
		return Result.getJidHandleGroups()[0].getJidHandles()

if __name__ == '__main__':
	unittest.main()