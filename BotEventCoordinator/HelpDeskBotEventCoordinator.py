##   Copyright (C) 2012 Bryan King
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.

from JidHandleGroup import JidHandleGroup
from RecipientListModifiers.Filter.HelpDeskRecipientFilter import HelpDeskRecipientFilter
from RecipientChooser import RecipientChooser
from Message import Message
from JidHandle import JidHandle
from BotEventCoordinator.DefaultBotEventCoordinator import DefaultBotEventCoordinator
from PresenceConfirmationManager import PresenceConfirmationManager

class HelpDeskBotEventCoordinator(DefaultBotEventCoordinator):

	def __init__(self, RecipientChooser, MessageBuilder, ItBot, PresenceConfirmationManager, JidHandleGroups, MyConfig):
		DefaultBotEventCoordinator.__init__(self, RecipientChooser, MessageBuilder, ItBot)
		self._PresenceConfManager = PresenceConfirmationManager
		self.__Filter = self._RecipientChooser.getRecipientListModifierByClass(HelpDeskRecipientFilter)
		self.__JidHandleGroups = JidHandleGroups
		self.__emailSender = MyConfig.getUserSupportEmailSender()
		self.__emailReceiver = MyConfig.getUserSupportEmailReceiver()

	@staticmethod
	def factory(MyConfig, ItBot, BotEventCoordinator):
		PresenceConfManager = PresenceConfirmationManager(MyConfig)
		return BotEventCoordinator(
			RecipientChooser(MyConfig),
			MyConfig.getMessageBuilder(),
			ItBot,
			PresenceConfManager,
			MyConfig.getJidHandleGroups(),
			MyConfig
		)

	def handleStatusCheck(self):
		if (self._PresenceConfManager.hasPendingRequest() and self._PresenceConfManager.hasTimedOut()):
			PreviousRequestedRecipient = self.__Filter.getCurrentRequestedRecipient()

			self.__Filter.currentRequestedUserHasTimedOut()

			Result = self.__forwardPendingMessages()
			if (Result.hasJidHandles()):
				NextRequestedRecipient = Result.getJidHandleGroups()[0].getJidHandles()[0]
			else:
				NextRequestedRecipient = None
			self.__notifyPreviousRequestedRecipient(PreviousRequestedRecipient, NextRequestedRecipient)

	def handleMessageReceived(self, sender, receivedMessageBody):
		if self.__senderIsRequestedRecipient(sender, receivedMessageBody):
			if (self.__weShouldForwardPendingMessages(receivedMessageBody)):
				self.__forwardPendingMessagesToAnotherGroup(sender, receivedMessageBody)
			else:
				self.__sendHelpDeskUserConfirmationMessage(sender)
				self.__sendRequestConfirmedMessage(sender)

				self.__confirmPresence()
		else:
			DefaultBotEventCoordinator.handleMessageReceived(self, sender, receivedMessageBody)

			self.__updateConfirmationRequest(sender, receivedMessageBody)

	def _sendConfirmationMessage(self, sender):
		if not self.__Filter.alreadyMessagedRequester(sender):
			DefaultBotEventCoordinator._sendConfirmationMessage(self, sender)

	def _handleNobodyAvailable(self, Result, sender, receivedMessageBody):
		DefaultBotEventCoordinator._handleNobodyAvailable(self, Result, sender, receivedMessageBody)

		if (Result.shouldSendRelayMessage()):
			self.__sendEmail(receivedMessageBody, sender)

		if (self._PresenceConfManager.hasPendingRequest()):
			self._PresenceConfManager.confirmPresence()

	##
	## Private Methods
	##

	def __senderIsRequestedRecipient(self, sender, receivedMessageBody):
		Result = self._RecipientChooser.getJidHandleGroupResult(sender, receivedMessageBody)
		if (Result.hasJidHandles()):
			recipientJid = Result.getJidHandleGroups()[0].getJidHandles()[0].getJid()
			return self._PresenceConfManager.hasPendingRequest() and sender == recipientJid
		else:
			return False

	def __updateConfirmationRequest(self, sender, receivedMessageBody):
		if not self._PresenceConfManager.hasPendingRequest():
			self._PresenceConfManager.startNewRequest()

		self._MessageBuilder.addPendingMessageBody(sender, receivedMessageBody)

		if not (self.__Filter.alreadyMessagedRequester(sender)):
			self.__Filter.addRequester(sender)

	def __sendHelpDeskUserConfirmationMessage(self, sender):
		messageBody = self._MessageBuilder.getHelpdeskUserConfirmationMessageBody()
		SenderJidHandle = [JidHandle('', sender)]
		HelpDeskUserConfirmationMessage = Message([JidHandleGroup(SenderJidHandle)], messageBody)
		self._ItBot.sendMessage(HelpDeskUserConfirmationMessage)

	def __sendHelpDeskUserCouldNotForwardToGroupMessage(self, sender):
		messageBody = self._MessageBuilder.getHelpdeskUserCouldNotForwardToGroupMessageBody()
		SenderJidHandle = [JidHandle('', sender)]
		CouldNotForwardMessage = Message([JidHandleGroup(SenderJidHandle)], messageBody)
		self._ItBot.sendMessage(CouldNotForwardMessage)

	def __sendRequestConfirmedMessage(self, sender):
		messageBody = self._MessageBuilder.getRequestConfirmedMessageBody(self._RecipientChooser.getJidHandleFromJid(sender))
		RequesterHandles = self.__Filter.getRequesterJidHandles()
		RequesterConfirmationMessage = Message([JidHandleGroup(RequesterHandles)], messageBody)
		self._ItBot.sendMessage(RequesterConfirmationMessage)

	def __sendEmail(self, receivedMessageBody, msgSender = None):
		if msgSender:
			receivedMessageBody = msgSender + " : " + receivedMessageBody

		sender = self.__emailSender
		receiver = self.__emailReceiver
		subject = 'Support'
		message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" %(sender, receiver, subject, receivedMessageBody))
		self._ItBot.sendEmail(sender, receiver, message)

	def __forwardPendingMessages(self):
		messageBody = self._MessageBuilder.getPendingMessagesForRequestedRecipient()
		Result = self._RecipientChooser.getJidHandleGroupResult(None, messageBody)

		if (Result.hasJidHandles()):
			RecipientJidHandleGroups = Result.getJidHandleGroups()
			ForwardMessage = Message(RecipientJidHandleGroups, messageBody)
			self._ItBot.sendMessage(ForwardMessage)
			self._PresenceConfManager.startNewRequest()
		elif (Result.nobodyAvailable()):
			messageBody = self._MessageBuilder.getPendingMessagesForEmail()
			self.__sendEmail(messageBody)
			self.__notifyRequestersMessagesHaveBeenEmailed()
			self.__confirmPresence()

		return Result

	def __notifyPreviousRequestedRecipient(self, PreviousRequestedRecipient, NextRequestedRecipient):
		messageBody = self._MessageBuilder.getTimedOutNotificationMessageBody(NextRequestedRecipient)
		NotificationMessage = Message([JidHandleGroup(PreviousRequestedRecipient)], messageBody)

		self._ItBot.sendMessage(NotificationMessage)

	def __confirmPresence(self):
		self._PresenceConfManager.confirmPresence()
		self.__Filter.presenceConfirmed()
		self._MessageBuilder.presenceConfirmed()

	def __notifyRequestersMessagesHaveBeenEmailed(self):
		messageBody = self._MessageBuilder.getNobodyAvailableMessageBody()
		Requesters = self.__Filter.getRequesterJidHandles()

		RequesterMessage = Message([JidHandleGroup(Requesters)], messageBody)

		self._ItBot.sendMessage(RequesterMessage)

	def __weShouldForwardPendingMessages(self, messageBody):
		for JidHandleGroup in self.__JidHandleGroups:
			if JidHandleGroup.getGroupIdentifierString() and JidHandleGroup.getGroupIdentifierString() in messageBody:
				return True

		return False

	def __forwardPendingMessagesToAnotherGroup(self, sender, messageBody):
		successfullySet = self.__Filter.setRequestedRecipientToPassedGroupIdentifier(messageBody, self.__JidHandleGroups)
		if (successfullySet):
			self.__forwardPendingMessages()
			self.__sendForwardedMessageBackToSender(sender)
		else:
			self.__sendRequestConfirmedMessage(sender)
			self.__sendHelpDeskUserCouldNotForwardToGroupMessage(sender)
			self.__confirmPresence()

	def __sendForwardedMessageBackToSender(self, sender):
		messageBody = self._MessageBuilder.getMessageForwardedMessageBody()
		SenderJidHandle = [JidHandle('', sender)]
		MessageForwardedMessage = Message([JidHandleGroup(SenderJidHandle)], messageBody)

		self._ItBot.sendMessage(MessageForwardedMessage)

