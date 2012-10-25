import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifierTest.RecipientListModifierTestBase import RecipientListModifierTestBase
from RecipientListModifiers.Filter.IgnoreMessagesWithKeywordFilter import IgnoreMessagesWithKeywordFilter
from ludibrio.stub import Stub

class IgnoreMessagesWithKeywordFilterTest(RecipientListModifierTestBase):

	def setUp(self):
		unittest.TestCase.setUp(self)

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_returns_dont_send_message_result_when_message_body_contains_an_ignored_keyword(self):
		ignoredKeyword = '[BROADCAST]'
		self.__givenFilterConfigContainsKeywords(ignoredKeyword)
		Recipients = [self._getJidHandle(), self._getJidHandle()]
		Filter = self.__getFilter()

		Result = Filter.getJidHandleGroupResult(Recipients, '', ignoredKeyword + ' some message')

		self.assertEquals(Result.DONT_SEND_ANY_MESSAGE, Result.getCode())
		self.assertFalse(Result.hasJidHandles())

	def test_returns_jid_handles_when_message_body_does_not_contain_ignored_keyword(self):
		ignoredKeyword = '[BROADCAST]'
		self.__givenFilterConfigContainsKeywords([ignoredKeyword])
		ExpectedJideHandleGroups = [JidHandleGroup([self._getJidHandle(), self._getJidHandle()])]
		Filter = self.__getFilter()

		Result = Filter.getJidHandleGroupResult(ExpectedJideHandleGroups, '', 'some message')

		self.assertEquals(ExpectedJideHandleGroups, Result.getJidHandleGroups())

	def test_returns_dont_send_message_result_when_message_body_contains_second_ignored_keyword(self):
		ignoredKeywords = ['[BROADCAST]', 'FREE STUFF']
		self.__givenFilterConfigContainsKeywords(ignoredKeywords)
		ExpectedJideHandleGroups = [self._getJidHandle(), self._getJidHandle()]
		Filter = self.__getFilter()

		Result = Filter.getJidHandleGroupResult(ExpectedJideHandleGroups, '', ignoredKeywords[1] + 'some message')

		self.assertEquals(Result.DONT_SEND_ANY_MESSAGE, Result.getCode())

	def __getFilter(self):
		return IgnoreMessagesWithKeywordFilter(self.__ConfigParser)

	def __givenFilterConfigContainsKeywords(self, ignoredKeywords):
		with Stub() as ConfigParser:
			ConfigParser.findConfigLinesBetween(
				IgnoreMessagesWithKeywordFilter.START_IGNORE_MESSAGES_WITH_KEYWORDS_KEY,
				IgnoreMessagesWithKeywordFilter.END_IGNORE_MESSAGES_WITH_KEYWORDS_KEY
			) >> ignoredKeywords

		self.__ConfigParser = ConfigParser

if __name__ == '__main__':
	unittest.main()