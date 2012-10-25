import unittest
from JidHandleGroup import JidHandleGroup
from RecipientChooser import RecipientChooser
from JidHandle import JidHandle
from RecipientListModifiers.Result import Result
from ludibrio.spy import Spy
from ludibrio import *

class RecipientChooserTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_getJidHandleFromJid_returns_None_if_no_jid_handle_has_jid(self):
		self.__given_multiple_jid_handles_in_configuration_with_no_list_modifiers()

		MyChooser = RecipientChooser(self.	__MyConfig)

		self.assertEquals(None, MyChooser.getJidHandleFromJid('someRandomInvalidJid@jid.com'))

	def test_getJidHandleFromJid_returns_correct_jid_handle(self):
		ExpectedJidHandleGroups = self.__given_multiple_jid_handles_in_configuration_with_no_list_modifiers()
		ExpectedJidHandle = ExpectedJidHandleGroups[0].getJidHandles()[0]

		MyChooser = RecipientChooser(self.__MyConfig)

		ActualJidHandle = MyChooser.getJidHandleFromJid(ExpectedJidHandle.getJid())

		self.assertEquals(ExpectedJidHandle, ActualJidHandle)

	def test_getJidHandleGroupResult_returns_all_jid_handles_if_no_list_modifiers_are_set(self):
		ExpectedJidHandleGroups = self.__given_multiple_jid_handles_in_configuration_with_no_list_modifiers()

		MyChooser = RecipientChooser(self.__MyConfig)
		Result = MyChooser.getJidHandleGroupResult('', '')

		self.assertEquals(ExpectedJidHandleGroups, Result.getJidHandleGroups())

	def test_getJidHandleGroupResult_skips_subsequent_filters_if_first_list_modifier_returns_no_jid_handles(self):
		self.__given_first_list_modifier_returns_no_jid_handles()

		MyChooser = RecipientChooser(self.__MyConfig)
		Result = MyChooser.getJidHandleGroupResult('', '')

		self.assertFalse(Result.hasJidHandles())

	def test_getJidHandleGroupResult_skips_subsequent_filters_if_second_list_modifier_returns_no_jid_handles(self):
		self.__given_second_list_modifier_returns_no_jid_handles()

		MyChooser = RecipientChooser(self.__MyConfig)
		Result = MyChooser.getJidHandleGroupResult('', '')

		self.assertFalse(Result.hasJidHandles())

	def __given_multiple_jid_handles_in_configuration_with_no_list_modifiers(self):
		ExpectedJidHandles = []
		ExpectedJidHandles.append(JidHandle('someUserName', 'someCrazyJid'))
		ExpectedJidHandles.append(JidHandle('someOtherUserName', 'someOtherJid'))
		with Spy() as MockedConfig:
			MockedConfig.getJidHandleGroups() >> [JidHandleGroup(ExpectedJidHandles)]
			MockedConfig.getOrderedRecipientListModifiers() >> []

		self.__MyConfig = MockedConfig
		return [JidHandleGroup(ExpectedJidHandles)]

	def __given_first_list_modifier_returns_no_jid_handles(self):
		with Spy() as FirstFilter:
			FirstFilter.getJidHandleGroupResult(any(), any(), any()) >> Result([])

		UnExpectedJidHandles = []
		UnExpectedJidHandles.append(JidHandle('someUserName', 'someCrazyJid'))
		UnExpectedJidHandles.append(JidHandle('someOtherUserName', 'someOtherJid'))

		with Spy() as SecondFilter:
			SecondFilter.getJidHandleGroupResult(any(), any(), any()) >> Result([JidHandleGroup(UnExpectedJidHandles)])

		with Spy() as MockedConfig:
			MockedConfig.getOrderedRecipientListModifiers() >> [FirstFilter, SecondFilter]
			MockedConfig.getJidHandleGroups() >> [JidHandleGroup(UnExpectedJidHandles)]

		self.__MyConfig = MockedConfig

	def __given_first_list_modifier_returns_dont_send_message_result(self):
		with Spy() as FirstFilter:
			FirstFilter.getJidHandleGroupResult(any(), any(), any()) >> Result(resultCode=Result.DONT_SEND_ANY_MESSAGE)

		UnExpectedJidHandles = []
		UnExpectedJidHandles.append(JidHandle('someUserName', 'someCrazyJid'))
		UnExpectedJidHandles.append(JidHandle('someOtherUserName', 'someOtherJid'))

		with Spy() as SecondFilter:
			SecondFilter.getJidHandleGroupResult(any(), any(), any()) >> Result(UnExpectedJidHandles)

		with Spy() as MockedConfig:
			MockedConfig.getOrderedRecipientListModifiers() >> [FirstFilter, SecondFilter]
			MockedConfig.getJidHandleGroups() >> [JidHandleGroup([]), JidHandleGroup(UnExpectedJidHandles)]

		self.__MyConfig = MockedConfig

	def __given_second_list_modifier_returns_no_jid_handles(self):

		UnExpectedJidHandles = []
		UnExpectedJidHandles.append(JidHandle('someUserName', 'someCrazyJid'))
		UnExpectedJidHandles.append(JidHandle('someOtherUserName', 'someOtherJid'))

		with Spy() as FirstFilter:
			FirstFilter.getJidHandleGroupResult(any(), any(), any()) >> Result([JidHandleGroup(UnExpectedJidHandles)])

		with Spy() as SecondFilter:
			SecondFilter.getJidHandleGroupResult(any(), any(), any()) >> Result([])

		with Spy() as ThirdFilter:
			ThirdFilter.getJidHandleGroupResult(any(), any(), any()) >> Result([JidHandleGroup(UnExpectedJidHandles)])

		with Spy() as MockedConfig:
			MockedConfig.getOrderedRecipientListModifiers() >> [FirstFilter, SecondFilter, ThirdFilter]
			MockedConfig.getJidHandleGroups() >> [JidHandleGroup(UnExpectedJidHandles)]

		self.__MyConfig = MockedConfig


if __name__ == '__main__':
	unittest.main()