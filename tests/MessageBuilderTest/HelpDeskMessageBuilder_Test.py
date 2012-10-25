import unittest
from ludibrio import Stub
from ludibrio.spy import Spy
from MessageBuilder.HelpDeskMessageBuilder import HelpDeskMessageBuilder

class HelpDeskMessageBuilderTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.skipTest("")

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_factory_returns_instance_of_builder(self):
		Builder = self._getBuilder()

		self.assertIsInstance(Builder, HelpDeskMessageBuilder)

	def test_getRelayMessage_adds_sender_to_its_body(self):
		Builder = self._getBuilder()
		sender = 'someSender'

		self.assertIn(sender, Builder.getRelayMessageBody(sender, 'some other message'))

	def test_getPendingMessagesForRequestedRecipient_returns_all_pending_messages(self):
		Builder = self._getBuilder()
		expectedPendedMessage = 'some pended message'
		Builder.addPendingMessageBody('aSender@fake.com', expectedPendedMessage)
		otherExpectedPendedMessage = 'some other pended message'
		Builder.addPendingMessageBody('aSender@fake.com', otherExpectedPendedMessage)

		self.assertIn(expectedPendedMessage, Builder.getPendingMessagesForRequestedRecipient())
		self.assertIn(otherExpectedPendedMessage, Builder.getPendingMessagesForRequestedRecipient())

	def _getBuilder(self):
		Config = self.__getMockedConfig()
		with Spy() as IsDuringBusinessHours:
			pass
		Builder = HelpDeskMessageBuilder(Config, IsDuringBusinessHours)
		return Builder

	def __getMockedConfig(self):
		with Spy() as MyConfig:
			pass
		return MyConfig

if __name__ == '__main__':
	unittest.main()