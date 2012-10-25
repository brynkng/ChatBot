import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Filter.AvailableRecipientFilter import AvailableRecipientFilter
from ludibrio import Stub
from ludibrio import *
from JidHandle import JidHandle

class AvailableRecipientFilterTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.__PresenceManager = None
		FirstJidHandle = JidHandle('someUserName', 'someJid@jid.com')
		SecondJidHandle = JidHandle('someOtherUserName', 'someOtherJid@jid.com')
		self.__JidHandles = [FirstJidHandle, SecondJidHandle]

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_returns_no_jid_handles_if_nobody_is_available(self):
		self.__given_nobody_is_available()

		self.__then_no_jid_handles_were_returned()

	def test_returns_first_jid_handle_if_it_is_available_and_second_is_not(self):
		self.__given_first_jid_handle_is_available_and_second_is_not()
		ExpectedJidHandleGroup = [JidHandleGroup([self.__JidHandles[0]])]

		Result = self.__getResult()

		self.assertEquals(ExpectedJidHandleGroup, Result.getJidHandleGroups())

	def test_returns_second_available_jid_handle_when_first_jid_handle_is_unavailable(self):
		self.__given_second_jid_handle_is_available_and_first_is_not()

		Result = self.__getResult()

		self.assertEquals([JidHandleGroup([self.__JidHandles[1]])], Result.getJidHandleGroups())

	def test_returns_all_available_jid_handles(self):
		self.__given_all_jid_handles_are_available()

		Result = self.__getResult()

		self.assertEquals([JidHandleGroup(self.__JidHandles)], Result.getJidHandleGroups())

	def __given_nobody_is_available(self):
		self.__JidHandles = []
		with Stub() as PresenceManager:
			PresenceManager.isJidHandleAvailable() >> False

		self.__PresenceManager = PresenceManager

	def __getFilter(self):
		return AvailableRecipientFilter(self.__PresenceManager)

	def __then_no_jid_handles_were_returned(self):
		Result = self.__getResult()

		self.assertEquals(Result.NOBODY_AVAILABLE, Result.getCode())
		self.assertFalse(Result.hasJidHandles())

	def __given_first_jid_handle_is_available_and_second_is_not(self):
		with Stub() as PresenceManager:
			PresenceManager.isJidHandleAvailable(self.__JidHandles[0]) >> True
			PresenceManager.isJidHandleAvailable(self.__JidHandles[1]) >> False

		self.__PresenceManager = PresenceManager

	def __given_second_jid_handle_is_available_and_first_is_not(self):
		with Stub() as PresenceManager:
			PresenceManager.isJidHandleAvailable(self.__JidHandles[0]) >> False
			PresenceManager.isJidHandleAvailable(self.__JidHandles[1]) >> True

		self.__PresenceManager = PresenceManager

	def __given_all_jid_handles_are_available(self):
		with Stub() as PresenceManager:
			PresenceManager.isJidHandleAvailable(any()) >> True

		self.__PresenceManager = PresenceManager

	def __getResult(self):
		Filter = self.__getFilter()
		Result = Filter.getJidHandleGroupResult([JidHandleGroup(self.__JidHandles)], None, '')

		return Result


if __name__ == '__main__':
	unittest.main()
