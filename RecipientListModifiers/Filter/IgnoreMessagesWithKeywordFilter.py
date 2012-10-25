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

from ConfigParser import ConfigParser
from RecipientListModifiers.Result import Result
from RecipientListModifiers.RecipientListModifier import RecipientListModifier

class IgnoreMessagesWithKeywordFilter(RecipientListModifier):
	"""" This filter is intended to be used to ignore messages that have a certain keyword.
		For instance if someone sends a broadcast message that has [BROADCAST] in its message,
		we can prevent that from being relayed on"""

	START_IGNORE_MESSAGES_WITH_KEYWORDS_KEY = '--START_IGNORE_MESSAGES_WITH_KEYWORDS--'
	END_IGNORE_MESSAGES_WITH_KEYWORDS_KEY = '--END_IGNORE_MESSAGES_WITH_KEYWORDS--'

	def __init__(self, ConfigParser):
		self.__ConfigParser = ConfigParser

	@staticmethod
	def factory(MyConfig, ModifierClass):
		return IgnoreMessagesWithKeywordFilter(ConfigParser('config/filter/ignoreMessagesWithKeyword.txt'))

	def getJidHandleGroupResult(self, JidHandleGroups, sender, messageBody):
		keywordsToIgnore = self.__ConfigParser.findConfigLinesBetween(
			self.START_IGNORE_MESSAGES_WITH_KEYWORDS_KEY,
			self.END_IGNORE_MESSAGES_WITH_KEYWORDS_KEY
		)

		for keyword in keywordsToIgnore:
			if messageBody.find(keyword) != -1:
				return Result(resultCode=Result.DONT_SEND_ANY_MESSAGE)

		return Result(JidHandleGroups)