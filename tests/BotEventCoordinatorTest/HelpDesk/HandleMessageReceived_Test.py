#!/usr/bin/python

import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Result import Result
from tests.ludibrio.spy import *
from ChatBot.BotEventCoordinator.HelpDeskBotEventCoordinator import HelpDeskBotEventCoordinator
import JidHandle
import Message
from tests.ludibrio import *

class BotEventCoordinator_HelpDesk_HandleMessageReceivedTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.__sender = "someSender@someAddress.net"

		JidHandles = [JidHandle.JidHandle('', self.__sender)]
		self.__ExpectedMessage = Message.Message([JidHandleGroup(JidHandles)], "")
		self.__RequesterConfMessage = Message.Message([], "")


		with Spy() as ItBot:
			pass
		self.__ItBot = ItBot

		self.__nobodyAvailableMsg = 'nobody available!'
		self.__immediateSenderConfMsg = 'someone will assist you shortly!'

		with Spy() as MessageBuilder:
			MessageBuilder.getImmediateSenderConfirmationMessageBody() >> self.__immediateSenderConfMsg
			MessageBuilder.getNobodyAvailableMessageBody() >> self.__nobodyAvailableMsg
			MessageBuilder.getRelayMessageBody(any(), any()) >> ""
		self.__MessageBuilder = MessageBuilder

		with Spy() as PresenceConfManager:
			PresenceConfManager.hasPendingRequest() >> True
		self.__PresenceConfirmationManager = PresenceConfManager

		with Spy() as RecipientFilter:
			RecipientFilter.getRequesterJidHandles() >> []
			RecipientFilter.addRequester(any())
			RecipientFilter.alreadyMessagedRequester(any()) >> True
		self.__RecipientFilter = RecipientFilter
		
		with Spy() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result([])
			RecipientChooser.getJidHandleFromJid(any())
			RecipientChooser.getRecipientListModifierByClass(any()) >> self.__RecipientFilter
		self.__RecipientChooser = RecipientChooser

		Spy.__calls__ = [] #hack job to reset spy call recording in between tests

	def test_confirms_presence_when_we_have_a_pending_confirmation_request_and_the_sender_is_current_requested_recipient(self):
		self.__given_sender_is_current_requested_recipient()
		self.__and_we_have_a_pending_confirmation_request()

		self.__then_expect_presence_is_confirmed()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__PresenceConfirmationManager.validate()

	def test_sends_confirmation_message_to_confirmer_when_we_have_a_pending_confirmation_request_and_the_sender_is_current_requested_recipient(self):
		self.__given_sender_is_current_requested_recipient()
		self.__and_we_have_a_pending_confirmation_request()
		self.__and_message_builder_returns_a_helpdesk_user_confirmation_message()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		verify(self.__ItBot).sendMessage(self.__ExpectedMessage).called(times == 1)

	def test_sends_confirmation_message_to_requesters_when_we_have_a_pending_confirmation_request_and_the_sender_is_current_requested_recipient(self):
		self.__given_recipient_filter_returns_requester()
		self.__given_sender_is_current_requested_recipient()
		self.__and_we_have_a_pending_confirmation_request()
		self.__and_message_builder_returns_a_requester_confirmation_message()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		verify(self.__ItBot).sendMessage(self.__ExpectedMessage).called(times == 1)

	def test_starts_new_presence_confirmation_request_when_there_is_no_pending_request(self):
		self.__expect_new_presence_conf_was_started_given_we_do_not_have_a_pending_confirmation_request()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__PresenceConfirmationManager.validate()

	def test_adds_pending_message_body_to_message_builder_when_we_have_a_pending_confirmation_request_but_sender_was_not_requested_user(self):
		self.__given_we_have_a_pending_confirmation_request_but_sender_was_not_requested_user()
		expectedMessageBody = 'some expected message'

		self.__then_expect_message_body_was_added_to_message_builder(expectedMessageBody)

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, expectedMessageBody)

		self.__MessageBuilder.validate()

	def test_adds_requester_to_recipient_chooser_when_we_have_a_pending_confirmation_request_but_sender_was_not_requested_user(self):
		self.__given_sender_is_different_requested_recipient()
		self.__and_we_have_a_pending_confirmation_request()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		verify(self.__RecipientFilter).addRequester(self.__sender).called(times == 1)

	def test_confirms_presence_when_there_is_a_pending_request_and_sender_is_not_confirmer_but_nobody_is_available(self):
		self.__given_nobody_is_available()
		self.__and_we_have_a_pending_confirmation_request()

		self.__then_expect_presence_is_confirmed()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__PresenceConfirmationManager.validate()

	def test_sends_email_when_nobody_available(self):
		self.skipTest("")
		self.__given_nobody_is_available()

		self.__then_expect_email_is_sent()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__ItBot.validate()

	def test_adds_sender_to_email_body_when_nobody_is_available_and_message_was_received(self):
		self.__given_nobody_is_available()

		self.__then_expect_sender_is_added_to_email_body()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		self.__ItBot.validate()

	def test_notifies_recipient_filter_that_presence_has_been_confirmed(self):
		self.__given_presence_will_be_confirmed()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		verify(self.__RecipientFilter).presenceConfirmed().called(times == 1)

	def test_notifies_message_builder_that_presence_has_been_confirmed(self):
		self.__given_presence_will_be_confirmed(mockMessageBuilder=True)

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		verify(self.__MessageBuilder).presenceConfirmed().called(times == 1)

	def test_does_not_send_a_confirmation_message_if_the_requester_has_already_received_one_this_request(self):
		self.__given_requester_has_already_received_confirmation_message()

		BotEventCoordinator = self.__getBotEventCoordinator()
		BotEventCoordinator.handleMessageReceived(self.__sender, 'some message')

		JidHandles = [JidHandle.JidHandle('', self.__sender)]
		ConfirmationMessage = Message.Message([JidHandleGroup(JidHandles)], self.__immediateSenderConfMsg)
		verify(self.__ItBot).sendMessage(ConfirmationMessage).called(times == 0)

	def __getBotEventCoordinator(self):
		with Spy() as Config:
			pass

		return HelpDeskBotEventCoordinator(
		 	self.__RecipientChooser,
		 	self.__MessageBuilder,
		 	self.__ItBot,
			self.__PresenceConfirmationManager,
			[],
			Config
		)

	def __expect_new_presence_conf_was_started_given_we_do_not_have_a_pending_confirmation_request(self):
		with Mock() as MockedPresenceConfirmationManager:
			MockedPresenceConfirmationManager.startNewRequest()

		with Stub(proxy=MockedPresenceConfirmationManager) as StubbedPresenceConfirmationManager:
			StubbedPresenceConfirmationManager.hasPendingRequest() >> False
			StubbedPresenceConfirmationManager.startNewRequest(any())

		self.__PresenceConfirmationManager = StubbedPresenceConfirmationManager

	def __given_sender_is_current_requested_recipient(self):
		with Stub() as RecipientChooser:
			JidHandles = [JidHandle.JidHandle('', self.__sender)]
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result([JidHandleGroup(JidHandles)])
			RecipientChooser.getJidHandleFromJid(any())
			RecipientChooser.getRecipientListModifierByClass(any()) >> self.__RecipientFilter

		self.__RecipientChooser = RecipientChooser

	def __then_expect_presence_is_confirmed(self):
		with Mock() as PresenceConfirmationManager:
			PresenceConfirmationManager.confirmPresence()

		with Stub(proxy=PresenceConfirmationManager) as StubbedConfManager:
			StubbedConfManager.hasPendingRequest() >> True
			StubbedConfManager.confirmPresence(any())

		self.__PresenceConfirmationManager = StubbedConfManager

	def __and_we_have_a_pending_confirmation_request(self):
		with Stub() as PresenceConfirmationManager:
			PresenceConfirmationManager.hasPendingRequest() >> True
			PresenceConfirmationManager.confirmPresence()

		self.__PresenceConfirmationManager = PresenceConfirmationManager

	def __and_message_builder_returns_a_helpdesk_user_confirmation_message(self):
		expectedMessageBody = "Presence confirmed."

		with Spy() as MessageBuilder:
			MessageBuilder.getHelpdeskUserConfirmationMessageBody() >> expectedMessageBody

		self.__MessageBuilder = MessageBuilder

		SenderJidHandle = [JidHandle.JidHandle('', self.__sender)]
		SenderJidHandleGroup = [JidHandleGroup(SenderJidHandle)]
		with Stub() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result(SenderJidHandleGroup)
			RecipientChooser.getJidHandleFromJid(any())
			RecipientChooser.getRecipientListModifierByClass(any()) >> self.__RecipientFilter

		self.__RecipientChooser = RecipientChooser

		self.__ExpectedMessage = Message.Message(SenderJidHandleGroup, expectedMessageBody)

	def __and_message_builder_returns_a_requester_confirmation_message(self):
		expectedMessageBody = "Your message was received and is being looked at by"
		with Spy() as MessageBuilder:
			MessageBuilder.getRequestConfirmedMessageBody(any()) >> expectedMessageBody

		self.__MessageBuilder = MessageBuilder
		self.__ExpectedMessage = Message.Message(self.__ExpectedJidHandleGroups, expectedMessageBody)

	def __given_recipient_filter_returns_requester(self):

		JidHandles = [JidHandle.JidHandle('', 'someRequesterJid@jid.com')]
		self.__ExpectedJidHandleGroups = [JidHandleGroup(JidHandles)]
		with Spy() as RecipientFilter:
			RecipientFilter.getRequesterJidHandles() >> JidHandles

		self.__RecipientFilter = RecipientFilter

	def __given_we_have_a_pending_confirmation_request_but_sender_was_not_requested_user(self):
		self.__and_we_have_a_pending_confirmation_request()
		self.__given_nobody_is_available()

	def __given_nobody_is_available(self):
		with Stub(proxy=self.__RecipientChooser) as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result([])
			RecipientChooser.getRecipientListModifierByClass(any()) >> self.__RecipientFilter

		self.__RecipientChooser = RecipientChooser

	def __given_sender_is_different_requested_recipient(self):
		with Spy() as RecipientFilter:
			RecipientFilter.getRequesterJidHandles() >> []
			RecipientFilter.addRequester(any())
			RecipientFilter.alreadyMessagedRequester(any()) >> False
		self.__RecipientFilter = RecipientFilter

		with Stub(proxy=self.__RecipientChooser) as RecipientChooser:
			JidHandles = [JidHandle.JidHandle('', 'someNonSenderJid@jid.com')]
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result([JidHandleGroup(JidHandles)])
			RecipientChooser.getRecipientListModifierByClass(any()) >> self.__RecipientFilter

		self.__RecipientChooser = RecipientChooser

	def __then_expect_message_body_was_added_to_message_builder(self, expectedMessageBody):
		with Mock() as MockedMessageBuilder:
			MockedMessageBuilder.addPendingMessageBody(self.__sender, expectedMessageBody)

		#you an stub a mock as long as you call the mocked method in the stub with different params
		with Stub(proxy=MockedMessageBuilder) as MessageBuilder:
			MessageBuilder.getImmediateSenderConfirmationMessageBody() >> ""
			MessageBuilder.getNobodyAvailableMessageBody() >> ""
			MessageBuilder.addPendingMessageBody() >> ""

		self.__MessageBuilder = MessageBuilder

	def __then_expect_email_is_sent(self):
		with Mock() as ItBot:
			ItBot.sendEmail(contains('@'), contains('@'), kind_of(basestring))

		with Stub(proxy=ItBot) as StubbedItBot:
			StubbedItBot.sendMessage(any())
			StubbedItBot.sendEmail()

		self.__ItBot = StubbedItBot

	def __then_expect_sender_is_added_to_email_body(self):
		with Mock() as ItBot:
			ItBot.sendEmail(any(), any(), contains(self.__sender))

		with Stub(proxy=ItBot) as StubbedItBot:
			StubbedItBot.sendMessage(any())
			StubbedItBot.sendEmail()

		self.__ItBot = StubbedItBot

	def __given_presence_will_be_confirmed(self, mockMessageBuilder = False):

		if mockMessageBuilder:
			builderMock = Spy()

			with Stub() as RecipientFilter:
				RecipientFilter.presenceConfirmed()
				RecipientFilter.getRequesterJidHandles() >> []
			self.__RecipientFilter = RecipientFilter
		else:
			builderMock = Stub()

		with builderMock as MessageBuilder:
			MessageBuilder.presenceConfirmed()
			MessageBuilder.getRequestConfirmedMessageBody(any()) >> 'something'
			MessageBuilder.getHelpdeskUserConfirmationMessageBody() >> 'something else'

		self.__MessageBuilder = MessageBuilder

		with Spy() as RecipientChooser:
			JidHandles = [JidHandle.JidHandle('', self.__sender)]
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result([JidHandleGroup(JidHandles)])
			RecipientChooser.getJidHandleFromJid(any())
			RecipientChooser.getRecipientListModifierByClass(any()) >> self.__RecipientFilter

		self.__RecipientChooser = RecipientChooser

		self.__and_we_have_a_pending_confirmation_request()

	def __given_requester_has_already_received_confirmation_message(self):
		with Spy() as RecipientFilter:
			RecipientFilter.alreadyMessagedRequester(self.__sender) >> True

		with Spy() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result([])
			RecipientChooser.getRecipientListModifierByClass(any()) >> RecipientFilter

		self.__RecipientChooser = RecipientChooser
if __name__ == '__main__':
	unittest.main()
