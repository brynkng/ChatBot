import unittest
from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Result import Result
from JidHandle import JidHandle
from ludibrio import *
from ludibrio.spy import *
from BotEventCoordinator.HelpDeskBotEventCoordinator import HelpDeskBotEventCoordinator
from Message import Message


class HandleStatusCheckTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.__RecipientChooser = None
		self.__MessageBuilder = None
		self.__ItBot = None
		self.__PresenceConfirmationManager = None

		with Spy() as RecipientChooser:
			pass
		self.__RecipientChooser = RecipientChooser

		Spy.__calls__ = [] #hack job to reset spy call recording in between tests

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_does_nothing_when_pending_request_does_not_exist(self):
		self.__given_pending_request_does_not_exist()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		verify(self.__RecipientChooser).currentRequestedUserHasTimedOut().called(times == 0)

	def test_does_nothing_if_pending_request_has_not_timed_out(self):
		self.__given_pending_request_exists_and_has_not_timed_out()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		self.__then_assert_no_changes_were_made()

	def test_notifies_recipient_chooser_when_pending_request_has_timed_out(self):
		self.__given_pending_request_exists_and_has_timed_out()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		self.__then_assert_recipient_chooser_was_notified()

	def test_forwards_message_to_next_recipient_when_pending_request_has_timed_out(self):
		self.__given_pending_request_exists_and_has_timed_out()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		verify(self.__ItBot).sendMessage(self.__ExpectedForwardedMessage).called(times == 1)

	def test_sends_message_to_previous_requested_recipient_notifying_them_that_message_has_been_forwarded(self):
		self.__given_pending_request_exists_and_has_timed_out()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		verify(self.__ItBot).sendMessage(self.__ExpectedNotificationMessage).called(times == 1)

	def	test_starts_new_presence_confirmation_request_when_pending_request_has_timed_out(self):
		self.__given_pending_request_exists_and_has_timed_out()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		verify(self.__PresenceConfirmationManager).startNewRequest().called(times == 1)

	def test_notifies_requesters_if_message_timed_out_and_was_emailed(self):
		self.__given_pending_request_exists_and_has_timed_out_and_nobody_is_available()

		HelpDeskCoordinator = self.__getHelpDeskCoordinator()

		HelpDeskCoordinator.handleStatusCheck()

		verify(self.__ItBot).sendMessage(self.__ExpectedRequesterNotificationMessage).called(times == 1)

	def __given_pending_request_does_not_exist(self):
		with Stub() as PresenceConfirmationManager:
			PresenceConfirmationManager.hasPendingRequest() >> False

		self.__PresenceConfirmationManager = PresenceConfirmationManager

	def __getHelpDeskCoordinator(self):

		with Spy() as Config:
			pass

		HelpdeskCoordinator = HelpDeskBotEventCoordinator(
			self.__RecipientChooser,
			self.__MessageBuilder,
			self.__ItBot,
			self.__PresenceConfirmationManager,
			[],
			Config
		)
		return HelpdeskCoordinator

	def __given_pending_request_exists_and_has_not_timed_out(self):
		with Stub() as PresenceConfirmationManager:
			PresenceConfirmationManager.hasPendingRequest() >> True
			PresenceConfirmationManager.hasTimedOut() >> False

		self.__PresenceConfirmationManager = PresenceConfirmationManager


	def __then_assert_no_changes_were_made(self):
		verify(self.__RecipientChooser).currentRequestedUserHasTimedOut().called(times == 0)

	def __given_pending_request_exists_and_has_timed_out(self):
		with Spy() as PresenceConfirmationManager:
			PresenceConfirmationManager.hasPendingRequest() >> True
			PresenceConfirmationManager.hasTimedOut() >> True
			PresenceConfirmationManager.startNewRequest()

		self.__PresenceConfirmationManager = PresenceConfirmationManager

		PreviousRequestedRecipient = [JidHandle('somePreviousJid', 'somePreviousJid@jid.net')]
		JidHandles = [JidHandle('someJid', 'someJid@jid.net')]
		JidHandleGroups = [JidHandleGroup(JidHandles)]
		with Spy() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result(JidHandleGroups)
			RecipientChooser.getCurrentRequestedRecipient() >> PreviousRequestedRecipient

		self.__RecipientChooser = RecipientChooser

		relayMessageBody = 'Some Message Body'
		notificationMessageBody = 'Hey snoozer your message has been forwarded'
		with Stub() as MessageBuilder:
			MessageBuilder.getTimedOutNotificationMessageBody(any()) >> notificationMessageBody
			MessageBuilder.getPendingMessagesForRequestedRecipient() >> relayMessageBody

		self.__MessageBuilder = MessageBuilder

		self.__ExpectedForwardedMessage = Message(JidHandleGroups, relayMessageBody)
		self.__ExpectedNotificationMessage = Message([JidHandleGroup(PreviousRequestedRecipient)], notificationMessageBody)
		self.__ExpectedRequesterNotificationMessage = Message([JidHandleGroup(PreviousRequestedRecipient)], notificationMessageBody)

		with Spy() as ItBot:
			pass
		self.__ItBot = ItBot


	def __given_pending_request_exists_and_has_timed_out_and_nobody_is_available(self):
		with Spy() as PresenceConfirmationManager:
			PresenceConfirmationManager.hasPendingRequest() >> True
			PresenceConfirmationManager.hasTimedOut() >> True

		self.__PresenceConfirmationManager = PresenceConfirmationManager

		PreviousRequestedRecipient = [JidHandle('somePreviousJid', 'somePreviousJid@jid.net')]
		RequesterJidHandles = [JidHandle('someRequesterJid', 'someRequesterJid@jid.net')]
		with Spy() as Filter:
			Filter.getRequesterJidHandles() >> RequesterJidHandles
			Filter.getCurrentRequestedRecipient() >> PreviousRequestedRecipient

		JidHandles = [JidHandle('someJid', 'someJid@jid.net')]
		JidHandleGroups = [JidHandleGroup(JidHandles)]
		with Spy() as RecipientChooser:
			RecipientChooser.getJidHandleGroupResult(any(), any()) >> Result(resultCode=Result.NOBODY_AVAILABLE)
			RecipientChooser.getRecipientListModifierByClass(any()) >> Filter

		self.__RecipientChooser = RecipientChooser

		nobodyAvailableMessageBody = 'Nobody here son!'
		with Spy() as MessageBuilder:
			MessageBuilder.getNobodyAvailableMessageBody() >> nobodyAvailableMessageBody

		self.__MessageBuilder = MessageBuilder

		self.__ExpectedRequesterNotificationMessage = Message([JidHandleGroup(RequesterJidHandles)], nobodyAvailableMessageBody)

		with Spy() as ItBot:
			pass
		self.__ItBot = ItBot

	def __then_assert_recipient_chooser_was_notified(self):
		verify(self.__RecipientChooser).currentRequestedUserHasTimedOut().called(times == 1)

if __name__ == '__main__':
	unittest.main()