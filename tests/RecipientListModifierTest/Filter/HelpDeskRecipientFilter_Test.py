import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Filter.HelpDeskRecipientFilter import HelpDeskRecipientFilter
from ludibrio.spy import Spy
from ChatBot import JidHandle

class HelpDeskRecipientFilterTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.__PassedJidHandleGroups = []
		self.__CurrentRequestedRecipient = [JidHandle.JidHandle('someCurrentlyRequestedJid', 'someCurrentlyRequestedjid@jid.net')]

	def test_returns_first_recipient_passed_if_currently_no_requested_recipient(self):
		self.__given_recipient_is_passed()
		Filter = self.__getFilter()
		self.__and_there_is_no_requested_recipient(Filter)

		ActualJidHandle = self.__getActualJidHandles(Filter)

		self.assertEquals(self.__PassedJidHandleGroups[0].getJidHandles(), ActualJidHandle)

	def test_returns_current_requested_recipient(self):
		self.__given_recipient_is_passed()
		Filter = self.__getFilter()
		self.__and_there_is_a_current_requested_recipient(Filter)

		ActualJidHandle = self.__getActualJidHandles(Filter)

		self.assertEquals(self.__CurrentRequestedRecipient, ActualJidHandle)

	def test_sets_current_requested_recipient_when_is_called(self):
		self.__given_recipient_is_passed()
		Filter = self.__getFilter()
		self.__and_there_is_no_requested_recipient(Filter)

		ActualJidHandle = self.__getActualJidHandles(Filter)

		self.assertEquals(self.__PassedJidHandleGroups[0].getJidHandles(), Filter._HelpDeskRecipientFilter__RequestedRecipient)

	def test_currentRequestedUserHasTimedOut_clears_requested_user_if_no_more_recipients_available(self):
		self.__given_there_are_no_passed_recipients()
		Filter = self.__getFilter()
		self.__and_there_is_a_current_requested_recipient(Filter)

		Filter.currentRequestedUserHasTimedOut()

		self.__then_no_recipients_are_returned(Filter)

	def test_currentRequestedUserHasTimedOut_sets_next_recipient_as_requested_user(self):
		self.__given_recipient_is_passed()
		Filter = self.__getFilter()
		self.__and_there_is_a_current_requested_recipient(Filter)

		Filter.currentRequestedUserHasTimedOut()

		ActualJidHandle = self.__getActualJidHandles(Filter)

		self.assertEquals(self.__PassedJidHandleGroups[0].getJidHandles(), ActualJidHandle)

	def test_currentRequestedUserHasTimedOut_does_not_set_requested_user_to_previously_ignored_recipient(self):
		ExpectedJidHandles = self.__given_multiple_recipients_passed()
		Filter = self.__getFilter()
		self.__and_there_is_a_current_requested_recipient(Filter)
		Filter.currentRequestedUserHasTimedOut()

		Filter.currentRequestedUserHasTimedOut()

		ActualJidHandle = self.__getActualJidHandles(Filter)

		self.assertEquals(ExpectedJidHandles, ActualJidHandle)



	def __getFilter(self):
		with Spy() as MyConfig:
			pass
		Filter = HelpDeskRecipientFilter(MyConfig)
		return Filter

	def __and_there_is_no_requested_recipient(self, Filter):
		Filter._HelpDeskRecipientFilter__RequestedRecipient = None

	def __given_recipient_is_passed(self):
		self.__PassedJidHandleGroups.append(JidHandleGroup([JidHandle.JidHandle('somejid', 'somejid@jid.net')]))

	def __and_there_is_a_current_requested_recipient(self, Filter):
		Filter._HelpDeskRecipientFilter__RequestedRecipient = self.__CurrentRequestedRecipient
		#if there's a current requested recipient that means the jid handles should already be in the filter
		Filter._HelpDeskRecipientFilter__JidHandleGroups = self.__PassedJidHandleGroups

	def __given_there_are_no_passed_recipients(self):
		self.__PassedJidHandleGroups = []

	def __then_no_recipients_are_returned(self, Filter):
		Result = Filter.getJidHandleGroupResult(self.__PassedJidHandleGroups, None, '')
		self.assertFalse(Result.hasJidHandles())
		self.assertEquals(Result.NOBODY_AVAILABLE, Result.getCode())

	def __given_multiple_recipients_passed(self):
		ExpectedJidHandle = [JidHandle.JidHandle('someExpectedjid', 'someExpectedjid@jid.net')]
		self.__PassedJidHandleGroups.append(JidHandleGroup([self.__CurrentRequestedRecipient[0], JidHandle.JidHandle('someOtherjid', 'someOtherjid@jid.net'), ExpectedJidHandle[0]]))

		return ExpectedJidHandle

	def __getActualJidHandles(self, Filter):
		Result = Filter.getJidHandleGroupResult(self.__PassedJidHandleGroups, None, '')
		return Result.getJidHandleGroups()[0].getJidHandles()

if __name__ == '__main__':
	unittest.main()