import unittest
from ConfigTestBase import ConfigTestBase
from ConfigParser import ConfigParser

class ConfigParserTest(ConfigTestBase):

	def setUp(self):
		ConfigTestBase.setUp(self)

	def tearDown(self):
		ConfigTestBase.tearDown(self)

	def test_findConfigLine_correctly_reads_last_line_of_config_file(self):
		expectedValue = 'fullSentence'
		with open(self.configFilePath, 'w') as fh:
			fh.write('test=' + expectedValue)

		Parser = ConfigParser(self.configFilePath)

		self.assertEquals(expectedValue, Parser.findConfigLine('test'))

	def test_findConfigLine_ignores_lines_with_pound_symbol_in_front(self):
		self._appendLineToConfigString('#test=someValue')

		Parser = ConfigParser(self.configFilePath)

		self.assertEquals('', Parser.findConfigLine('test'))

	def test_findConfigLinesBetween_ignores_lines_with_pound_symbol_in_front(self):
		self._appendLineToConfigString('startKey')
		self._appendLineToConfigString('#someValue')
		self._appendLineToConfigString('endKey')

		Parser = ConfigParser(self.configFilePath)

		self.assertEquals([], Parser.findConfigLinesBetween('startKey', 'endKey'))

if __name__ == '__main__':
	unittest.main()