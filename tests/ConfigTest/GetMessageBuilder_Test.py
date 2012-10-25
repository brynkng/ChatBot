import unittest
import ConfigTestBase
from ChatBot.MessageBuilder.DefaultMessageBuilder import DefaultMessageBuilder
import ValidMessageBuilder

class GetMessageBuilderTest(ConfigTestBase.ConfigTestBase):

	def setUp(self):
		super(GetMessageBuilderTest, self).setUp()
		self.__defaultClass = DefaultMessageBuilder
		self.__configKeyString = 'message_builder'
		self.__validClass = ValidMessageBuilder.ValidMessageBuilder
		self.__name = 'MessageBuilder'
		self._clearConfig()

	def test_returns_default_class_when_no_class_exists_in_config(self):
		self._given_production_setup_is_correct()
		self._given_no_class_exists()

		MyConfig = self._getConfig()

		self.assertIsInstance(MyConfig.getMessageBuilder(), self.__defaultClass)

	def test_raises_exception_when_module_and_class_are_invalid(self):
		self._given_production_setup_is_correct()

		self._assert_raises_exception_when_module_and_class_are_invalid(self.__configKeyString, self.__name)

	def test_raises_exception_when_module_is_valid_but_class_is_invalid(self):
		self._assert_raises_exception_when_module_is_valid_but_class_is_invalid(self.__configKeyString, self.__name)

	def test_raises_exception_if_class_does_not_subclass_default_class(self):
		self._assert_raises_exception_if_class_does_not_subclass_default_class(self.__configKeyString, self.__name)

	def test_returns_valid_class_when_one_exists_in_config_and_is_valid(self):
		self._given_production_setup_is_correct()

		self._given_module_and_class_exist_in_config_and_are_valid(self.__configKeyString, self.__name)
		ExpectedConfigLoadedClass = self.__validClass

		MyConfig = self._getConfig()

		ActualConfigLoadedClass = MyConfig.getMessageBuilder()

		self.assertIsInstance(ActualConfigLoadedClass, ExpectedConfigLoadedClass)

if __name__ == '__main__':
	unittest.main()