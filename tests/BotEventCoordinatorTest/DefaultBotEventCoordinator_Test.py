#!/usr/bin/python

import unittest
from JidHandleGroup import JidHandleGroup
from ludibrio.spy import *
from ChatBot import PathAutoloader
from RecipientListModifiers.Result import Result
from BotEventCoordinator import DefaultBotEventCoordinator
import JidHandle
import Message
from ludibrio import *

class DefaultBotEventCoordinatorTestCase(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.__RecipientChooser = None
		self.__ExpectedJidHandleGroups = []

		with Spy() as MessageBuilder:
			pass
		self.__MessageBuilder = MessageBuilder

		with Spy() as ItBot:
			pass
		self.__ItBot = ItBot
		self.__sender = "someSender@someAddress.net"
		self.__ExpectedMessage = Message.Message(None, None)

	def test_handleMessageReceived_sends_confirmation_message_to_sender_and_sends_relay_message(self):
		self.__given_recipient_chooser_returns_a_jid_handle()
		self.__given_message_builder_returns_a_sender_confirmation_and_relay_message_body()

		self.__then_expected_relay_and_confirmation_message_will_be_sent()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__ItBot.validate()

	def test_handleMessageReceived_sends_nobody_available_message_when_no_recipient_jid_handles_are_returned(self):
		self.__given_recipient_chooser_returns_no_jid_handles()
		self.__and_message_builder_returns_a_nobody_available_message()

		self.__then_expected_nobody_available_and_confirmation_message_will_be_sent()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__ItBot.validate()

	def test_does_not_send_any_messages_if_recipient_chooser_returns_dont_send_any_message_result(self):
		self.__given_recipient_chooser_returns_dont_send_any_message_result()
		self.__then_expect_no_messages_to_be_sent()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

	def test_does_not_send_relay_message_when_recipient_chooser_returns_dont_send_relay_message_result(self):
		self.__given_recipient_chooser_returns_dont_send_relay_message_result()
		self.__given_message_builder_returns_a_sender_confirmation_and_relay_message_body()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		verify(self.__ItBot).sendMessage(self.__ExpectedRelayMessage).called(times == 0)

	def __given_message_builder_returns_a_sender_confirmation_and_relay_message_body(self):
		expectedMessageBody = "Successfully forwarded."
		with Spy() as MockedMessageBuilder:
			MockedMessageBuilder.getImmediateSenderConfirmationMessageBody() >> expectedMessageBody
			MockedMessageBuilder.getRelayMessageBody(self.__sender, 'some message') >> 'some message'

		self.__MessageBuilder = MockedMessageBuilder

		self.__ExpectedRelayMessage = Message.Message(self.__ExpectedJidHandleGroups, 'some message')

		self.__ExpectedMessage._Message__RecipientJidHandleGroups = [JidHandleGroup([JidHandle.JidHandle('', self.__sender)])]
		self.__ExpectedMessage._Message__messageBody = expectedMessageBody

	def __getMockedRecipientChooser(self, ExpectedJidHandleGroups):
		with Stub() as MockedRecipientChooser:
			MockedRecipientChooser.getJidHandleGroupResult(any(), any()) >> Result(ExpectedJidHandleGroups)

		self.__RecipientChooser = MockedRecipientChooser

	def __given_recipient_chooser_returns_no_jid_handles(self):
		self.__getMockedRecipientChooser([])

		self.__ExpectedJidHandleGroups = [JidHandleGroup([JidHandle.JidHandle('', self.__sender)])]

	def __given_recipient_chooser_returns_a_jid_handle(self):
		ExpectedRecipientJidHandles = [JidHandle.JidHandle("someUserName", "someJid@someAddress.net")]

		self.__ExpectedJidHandleGroups = [JidHandleGroup(ExpectedRecipientJidHandles)]

		self.__getMockedRecipientChooser(self.__ExpectedJidHandleGroups)



	def __getBotEventCoordinator(self):
		return DefaultBotEventCoordinator.DefaultBotEventCoordinator(
			 self.__RecipientChooser,
			 self.__MessageBuilder,
			 self.__ItBot
		 )

	def __then_expected_nobody_available_and_confirmation_message_will_be_sent(self):
		with Mock() as MockedItBot:
			MockedItBot.sendMessage(self.__ExpectedConfirmationMessage)
			MockedItBot.sendMessage(self.__ExpectedMessage)

		self.__ItBot = MockedItBot

	def __then_expected_relay_and_confirmation_message_will_be_sent(self):
		with Mock() as MockedItBot:
			MockedItBot.sendMessage(self.__ExpectedMessage)
			MockedItBot.sendMessage(self.__ExpectedRelayMessage)

		self.__ItBot = MockedItBot

	def __and_message_builder_returns_a_nobody_available_message(self):
		expectedMessageBody = "There is nobody currently available to receive your message."
		with Spy() as MockedMessageBuilder:
			MockedMessageBuilder.getImmediateSenderConfirmationMessageBody() >> 'Successfully forwarded.'
			MockedMessageBuilder.getNobodyAvailableMessageBody() >> expectedMessageBody

		self.__ExpectedConfirmationMessage = Message.Message(self.__ExpectedJidHandleGroups, 'Successfully forwarded.')

		self.__MessageBuilder = MockedMessageBuilder
		self.__ExpectedMessage._Message__messageBody = expectedMessageBody
		self.__ExpectedMessage._Message__RecipientJidHandleGroups = self.__ExpectedJidHandleGroups

	def __given_recipient_chooser_returns_dont_send_any_message_result(self):
		with Stub() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result(resultCode=Result.DONT_SEND_ANY_MESSAGE)

		self.__RecipientChooser = RecipientChooser

	def __then_expect_no_messages_to_be_sent(self):
		with Mock() as ItBot:
			pass
		self.__ItBot = ItBot

	def __given_recipient_chooser_returns_dont_send_relay_message_result(self):
		with Stub() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result(resultCode=Result.DONT_SEND_RELAY_MESSAGE)

		self.__RecipientChooser = RecipientChooser

if __name__ == '__main__':
	unittest.main()
