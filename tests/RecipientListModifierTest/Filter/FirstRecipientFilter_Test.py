import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Result import Result
from ChatBot import JidHandle
from ludibrio.spy import Spy
from RecipientListModifiers.Filter.FirstRecipientFilter import FirstRecipientFilter

class FirstRecipientFilterTest(unittest.TestCase):

	def setUp(self):
		self.__MyConfig = None
		unittest.TestCase.setUp(self)

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_returns_first_jid_handle_retrieved_from_config_when_there_are_multiple(self):
		JidHandles = self.__given_multiple_jid_handles_in_configuration()

		Filter = FirstRecipientFilter(self.__MyConfig)
		ActualResult = Filter.getJidHandleGroupResult([JidHandleGroup(JidHandles)], None, '')

		ExpectedJidHandles = [JidHandles[0]]
		self.assertEquals([JidHandleGroup(ExpectedJidHandles)], ActualResult.getJidHandleGroups())

	def test_returns_no_jid_handles_if_none_are_passed(self):
		Filter = FirstRecipientFilter(self.__MyConfig)

		ActualResult = Filter.getJidHandleGroupResult([], None, '')

		self.assertFalse(ActualResult.hasJidHandles())
		self.assertEquals(Result.NOBODY_AVAILABLE, ActualResult.getCode())


	def __given_multiple_jid_handles_in_configuration(self):
		ExpectedJidHandles = []
		ExpectedJidHandles.append(JidHandle.JidHandle('someUserName', 'someCrazyJid'))
		ExpectedJidHandles.append(JidHandle.JidHandle('someOtherUserName', 'someOtherJid'))
		with Spy() as MockedConfig:
			MockedConfig.getJidHandleGroups() >> [JidHandleGroup(ExpectedJidHandles)]

		self.__MyConfig = MockedConfig
		return ExpectedJidHandles

if __name__ == '__main__':
	unittest.main()