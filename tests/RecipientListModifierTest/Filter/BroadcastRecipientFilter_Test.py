import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifierTest.RecipientListModifierTestBase import RecipientListModifierTestBase
from RecipientListModifiers.Filter.BroadcastRecipientFilter import BroadcastRecipientFilter

class BroadcastRecipientFilterTest(RecipientListModifierTestBase):

	def setUp(self):
		unittest.TestCase.setUp(self)

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_returns_all_jid_handles_minus_the_sender(self):
		senderHandle = self._getJidHandle()
		JidHandleGroups = [JidHandleGroup([senderHandle, self._getJidHandle(), self._getJidHandle()])]
		ExpectedJidHandleGroups = JidHandleGroups[::]
		ExpectedJidHandleGroups[0].getJidHandles().pop(0)

		Filter = self.__getFilter()
		Result = Filter.getJidHandleGroupResult(JidHandleGroups, senderHandle.getJid(), '')

		self.assertEquals(ExpectedJidHandleGroups, Result.getJidHandleGroups())


	def test_returns_all_jid_handles_passed_when_sender_is_not_in_list(self):
		JidHandleGroups = [JidHandleGroup([self._getJidHandle(), self._getJidHandle(), self._getJidHandle()])]

		Filter = self.__getFilter()
		Result = Filter.getJidHandleGroupResult(JidHandleGroups, '', '')

		self.assertEquals(JidHandleGroups, Result.getJidHandleGroups())

	def __getFilter(self):
		return BroadcastRecipientFilter(None)

if __name__ == '__main__':
	unittest.main()