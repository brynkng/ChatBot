import PathAutoloader
import os
import glob
import unittest
from ChatBot import Config
import random
from ChatBot import JidHandle
from ChatBot.ConfigurationError import ConfigurationError

class ConfigTestBase(unittest.TestCase):

	configFilePath = 'testConfig.txt'

	def setUp(self):
		self._jidHandleFileLocationLines = []
		if not (os.path.exists(self.configFilePath)):
			open(self.configFilePath, 'w').close()

	def tearDown(self):
		os.remove(self.configFilePath)
		for filename in glob.glob(os.path.join(os.path.dirname(__file__), '*.txt')):
				os.remove(filename)

	def _getConfig(self):
		self._finalizeJidHandleConfigLines()
		return Config.Config(self.configFilePath, None)

	def _given_production_setup_is_correct(self):
		self._given_testing_is_not_enabled()
		self._given_production_jid_and_pwd_exist()
		self._given_jid_handle_group_file_location_exists()

	def _given_testing_is_not_enabled(self):
		self._appendLineToConfigString('testing_enabled=False')

	def _given_production_jid_and_pwd_exist(self):
		self._given_production_jid_exists()
		self._given_production_pwd_exists()

	def _assertRaisesExceptionWithMessageContainingString(self, expectedString):
			with self.assertRaises(ConfigurationError) as exception:
				self._getConfig()

			self.assertIn(expectedString, exception.exception.message)

	def _given_production_jid_exists(self):
		self._appendLineToConfigString('production_jid=someJid')

	def _given_production_pwd_exists(self):
		self._appendLineToConfigString('production_pwd=somePwd')

	def _appendLineToConfigString(self, string):
		with open('testConfig.txt', 'a') as fh:
			fh.write(string + '\n')

	def _given_jid_handle_group_file_location_exists(self):
		fileName = str(random.random()) + 'someFileLocation.txt'
		userName = 'Bob Smith'
		jid = str(random.random()) + 'someJabberId@someAddress.net'
		#Some fun path magic to find the relative path that the current file is in to write the test files
		filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fileName)
		with open(filePath, 'a') as fh:
			fh.write(Config.Config.START_JID_HANDLES_KEY)
			fh.write(userName + ' : ' + jid)
			fh.write(Config.Config.END_JID_HANDLES_KEY)

		self._jidHandleFileLocationLines.append('jid_handle_group_file_location=' + filePath)

		return JidHandle.JidHandle(userName, jid)

	def _assert_raises_exception_when_module_and_class_are_invalid(self, configKeyString, name):
		self._given_config_file_has_invalid_custom_module(configKeyString, name)

		with self.assertRaises(ImportError) as exception:
			self._getConfig()

		self.assertIsInstance(exception.exception, ImportError)

	def _assert_raises_exception_when_module_is_valid_but_class_is_invalid(self, configKey, name):
		self._given_production_setup_is_correct()
		self._given_module_is_valid_and_class_is_invalid(configKey, name)
		className = configKey.replace('_', ' ')
		self._assertRaisesExceptionWithMessageContainingString('Invalid ' + className + ' class')

		self._clearConfig()

	def _assert_raises_exception_if_class_does_not_subclass_default_class(self, configKey, name):
		self._given_production_setup_is_correct()
		self._given_class_does_not_subclass_default_class(configKey, name)

		className = configKey.replace('_', ' ').title()
		self._assertRaisesExceptionWithMessageContainingString(' must subclass Default' + className.replace(' ', ''))

		self._clearConfig()

	def _given_no_class_exists(self):
		pass

	def _given_config_file_has_invalid_custom_module(self, configKeyString, name):
		self._appendLineToConfigString(configKeyString + '=Invalid' + name )

	def _given_module_and_class_exist_in_config_and_are_valid(self, configKeyString, name):
		self._appendLineToConfigString(configKeyString + '=Valid' + name)

	def _given_class_does_not_subclass_default_class(self, configKeyString, name):
		self._appendLineToConfigString(configKeyString + '=' + name + 'WithInvalidParentClass')

	def _given_module_is_valid_and_class_is_invalid(self, configKeyString, name):
		self._appendLineToConfigString(configKeyString + '=' + name +'WithInvalidClass')

	def _clearConfig(self):
		with open('testConfig.txt', 'w') as fh:
			fh.write('')

	def _finalizeJidHandleConfigLines(self):
		self._appendLineToConfigString(Config.Config.START_JID_FILE_LOCATIONS_KEY)
		for line in self._jidHandleFileLocationLines:
			with open('testConfig.txt', 'a') as fh:
				fh.write(line + '\n')
		self._appendLineToConfigString(Config.Config.END_JID_FILE_LOCATIONS_KEY)