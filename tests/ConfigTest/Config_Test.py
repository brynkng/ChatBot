import unittest
from JidHandleGroup import JidHandleGroup
from Config import Config
import ConfigTestBase
import random
from ChatBot import JidHandle
import os
from RecipientListModifiers.RecipientListModifier import RecipientListModifier

class ConfigTest(ConfigTestBase.ConfigTestBase):

	def test_raises_exception_if_testing_is_not_enabled_and_no_production_jid_found(self):
		self._given_testing_is_not_enabled()

		self._assertRaisesExceptionWithMessageContainingString('production')

	def test_raises_exception_if_testing_is_not_enabled_and_no_production_password_found(self):
		self._given_testing_is_not_enabled()
		self._given_production_jid_exists()

		self._assertRaisesExceptionWithMessageContainingString('production')

	def test_raises_exception_if_testing_is_enabled_and_no_testing_password_is_found(self):
		self.__given_testing_is_enabled()

		self._assertRaisesExceptionWithMessageContainingString('test ')

	def test_raises_exception_if_testing_is_enabled_and_no_testing_jid_is_found(self):
		self.__given_testing_is_enabled()
		self.__given_testing_password_exists()

		self._assertRaisesExceptionWithMessageContainingString('test ')

	def test_raises_exception_if_no_jid_handle_group_file_location_is_found(self):
		self._given_testing_is_not_enabled()
		self._given_production_jid_and_pwd_exist()
		self._assertRaisesExceptionWithMessageContainingString('at least one jid_handle_group_file_location')

	def test_returns_expected_production_jid(self):
		self._given_production_setup_is_correct()
		expected = 'someJid'

		MyConfig = self._getConfig()
		actual = MyConfig.getJid()

		self.assertEquals(expected, actual)

	def test_returns_expected_production_password(self):
		self._given_production_setup_is_correct()
		expected = 'somePwd'

		MyConfig = self._getConfig()
		actual = MyConfig.getPwd()

		self.assertEquals(expected, actual)

	def test_returns_expected_test_jid(self):
		self.__given_test_setup_is_correct()
		expected = 'someJid'

		MyConfig = self._getConfig()
		actual = MyConfig.getJid()

		self.assertEquals(expected, actual)

	def test_returns_expected_test_password(self):
		self.__given_test_setup_is_correct()
		expected = 'somePassword'

		MyConfig = self._getConfig()
		actual = MyConfig.getPwd()

		self.assertEquals(expected, actual)

	def test_isTestingEnabled_returns_false_if_testing_is_not_enabled(self):
		self._given_production_setup_is_correct()

		MyConfig = self._getConfig()

		self.assertFalse(MyConfig.isTestingEnabled())

	def test_isTestingEnabled_returns_true_if_testing_is_not_enabled(self):
		self.__given_test_setup_is_correct()

		MyConfig = self._getConfig()

		self.assertTrue(MyConfig.isTestingEnabled())


	def test_getJidHandleGroups_returns_expected_multiple_jid_handle_groups_from_multiple_files(self):
		ExpectedJidHandleGroups = []
		ExpectedJidHandleGroups.append(JidHandleGroup([self.__given_test_setup_is_correct()]))
		ExpectedJidHandleGroups.append(JidHandleGroup([self._given_jid_handle_group_file_location_exists()]))
		ExpectedJidHandleGroups.append(JidHandleGroup([self._given_jid_handle_group_file_location_exists()]))

		MyConfig = self._getConfig()
		ActualJidHandleGroups = MyConfig.getJidHandleGroups()

		self.assertEquals(ExpectedJidHandleGroups, ActualJidHandleGroups)


	def test_getJidHandleGroups_returns_expected_jid_handles_from_same_file(self):
		ExpectedJidHandleGroups = []
		ExpectedJidHandleGroups.append(JidHandleGroup([self.__given_test_setup_is_correct()]))
		ExpectedJidHandleGroups.append(JidHandleGroup(self.__given_jid_handle_group_file_location_exists_with_multiple_handles()))

		MyConfig = self._getConfig()
		ActualJidHandleGroups = MyConfig.getJidHandleGroups()

		self.assertEquals(ExpectedJidHandleGroups, ActualJidHandleGroups)

	def test_getJidHandleGroups_returns_expected_jid_handles_in_order_written_in_config(self):
		ExpectedJidHandleGroups = []
		ExpectedJidHandleGroups.append(JidHandleGroup([self.__given_test_setup_is_correct()]))
		ExpectedJidHandleGroups.append(JidHandleGroup(self.__given_jid_handle_group_file_location_exists_with_multiple_handles()))

		MyConfig = self._getConfig()
		ActualJidHandleGroups = MyConfig.getJidHandleGroups()

		self.assertSequenceEqual(ExpectedJidHandleGroups, ActualJidHandleGroups)

	def test_getCustomImmediateSenderConfirmationMessage_returns_empty_string_if_nothing_exists(self):
		self.__given_test_setup_is_correct()
		self._appendLineToConfigString('custom_immediate_sender_confirmation_message=')

		MyConfig = self._getConfig()

		self.assertEquals('', MyConfig.getCustomImmediateSenderConfirmationMessage())

	def test_getCustomImmediateSenderConfirmationMessage_returns_contact_phone_number_string_that_exists(self):
		self.__given_test_setup_is_correct()
		expectedString = 'If you need to reach us at 555-5555 or ext 409'
		self._appendLineToConfigString('custom_immediate_sender_confirmation_message=' + expectedString)

		MyConfig = self._getConfig()

		self.assertEquals(expectedString, MyConfig.getCustomImmediateSenderConfirmationMessage())

	def test_getConfirmationRequestSecondThreshold_returns_default_if_nothing_exists(self):
		self.__given_test_setup_is_correct()

		self._appendLineToConfigString('confirmation_request_second_threshold=')

		MyConfig = self._getConfig()

		self.assertEquals(MyConfig.DEFAULT_CONFIRMATION_REQUEST_SECOND_THRESHOLD, MyConfig.getConfirmationRequestSecondThreshold())


	def test_getConfirmationRequestSecondThreshold_returns_confirmation_request_threshhold_that_exists(self):
		self.__given_test_setup_is_correct()
		confirmationRequestSecondThreshhold = '300'
		self._appendLineToConfigString('confirmation_request_second_threshold=' + confirmationRequestSecondThreshhold)

		MyConfig = self._getConfig()

		self.assertEquals(confirmationRequestSecondThreshhold, MyConfig.getConfirmationRequestSecondThreshold())

	def test_getForwardedMessageSecondThreshold_returns_default_if_nothing_exists(self):
		self.__given_test_setup_is_correct()

		self._appendLineToConfigString('forwarded_message_second_threshold=')

		MyConfig = self._getConfig()

		self.assertEquals(MyConfig.DEFAULT_FORWARDED_MESSAGE_DELAY_SECOND_THRESHOLD, MyConfig.getForwardedMessageSecondThreshold())

	def test_getForwardedMessageSecondThreshold_returns_forwarded_message_second_threshhold_that_exists(self):
		self.__given_test_setup_is_correct()
		forwardedMessageSecondThreshhold = '120'
		self._appendLineToConfigString('forwarded_message_second_threshold=' + forwardedMessageSecondThreshhold)

		MyConfig = self._getConfig()

		self.assertEquals(forwardedMessageSecondThreshhold, MyConfig.getForwardedMessageSecondThreshold())

	def test_getOrderedRecipientListModifiers_returns_empty_list_if_none_exist(self):
		self.__given_test_setup_is_correct()

		MyConfig = self._getConfig()

		self.assertEquals([], MyConfig.getOrderedRecipientListModifiers())

	def test_getOrderedRecipientListModifiers_returns_modifier_that_exists_in_config(self):
		self.__given_test_setup_is_correct()
		self._appendLineToConfigString(
			Config.START_FILTERS_AND_SORTS_KEY
			+ '\n ValidTestFilter'
			+ Config.END_FILTERS_AND_SORTS_KEY
		)

		MyConfig = self._getConfig()

		self.assertTrue(isinstance(MyConfig.getOrderedRecipientListModifiers()[0], RecipientListModifier))

	def test_getOrderedRecipientListModifiers_returns_multiple_modifiers_that_exists_in_config(self):
		self.__given_test_setup_is_correct()
		self._appendLineToConfigString(
			Config.START_FILTERS_AND_SORTS_KEY
			+ '\n ValidTestFilter'
			+ '\n SecondValidTestFilter'
			+ Config.END_FILTERS_AND_SORTS_KEY
		)

		MyConfig = self._getConfig()

		for Modifier in MyConfig.getOrderedRecipientListModifiers():
			self.assertTrue(isinstance(Modifier, RecipientListModifier))

	def test_getOrderedRecipientListModifiers_does_not_blow_up_if_there_is_an_empty_line(self):
		self.__given_test_setup_is_correct()
		self._appendLineToConfigString(
			Config.START_FILTERS_AND_SORTS_KEY
			+ '''

			'''
			+ Config.END_FILTERS_AND_SORTS_KEY
		)

		MyConfig = self._getConfig()

		MyConfig.getOrderedRecipientListModifiers()

	#
	# Test Helpers
	#

	def __given_testing_jid_exists(self):
		self._appendLineToConfigString('test_jid=someJid')

	def __given_test_setup_is_correct(self):
		self.__given_testing_is_enabled()
		self.__given_testing_password_exists()
		self.__given_testing_jid_exists()
		return self._given_jid_handle_group_file_location_exists()

	def __given_testing_is_enabled(self):
		self._appendLineToConfigString('testing_enabled=True')

	def __given_testing_password_exists(self):
		self._appendLineToConfigString('test_pwd=somePassword')

	def __given_jid_handle_group_file_location_exists_with_multiple_handles(self):
		fileName = str(random.random()) + 'someFileLocation.txt'
		userName = 'Bob Smith'
		secondUserName = 'Luke Skywalker'
		jid = str(random.random()) + 'someJabberId@someAddress.net'
		secondJid = str(random.random()) + 'someJabberId@someAddress.net'
		#Some fun path magic to find the relative path that the current file is in to write the test files
		filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fileName)
		with open(filePath, 'a') as fh:
			fh.write(Config.START_JID_HANDLES_KEY)
			fh.write(userName + ' : ' + jid + '\n')
			fh.write(secondUserName + ' : ' + secondJid + '\n')
			fh.write(Config.END_JID_HANDLES_KEY)

		self._jidHandleFileLocationLines.append('jid_handle_group_file_location=' + filePath)

		return [JidHandle.JidHandle(userName, jid), JidHandle.JidHandle(secondUserName, secondJid)]

if __name__ == '__main__':
	unittest.main()