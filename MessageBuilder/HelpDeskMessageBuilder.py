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

from IsDuringBusinessHours import IsDuringBusinessHours
from MessageBuilder.DefaultMessageBuilder import DefaultMessageBuilder

class HelpDeskMessageBuilder(DefaultMessageBuilder):

	def __init__(self, MyConfig, IsDuringBusinessHours):
		DefaultMessageBuilder.__init__(self, MyConfig)
		self.__pendingMessages = {}
		self.__customImmediateSenderConfirmationMessage = self._MyConfig.getCustomImmediateSenderConfirmationMessage()
		self.__isDuringBusinessHours = IsDuringBusinessHours.isDuringBusinessHours()
		self.__customNobodyAvailableDuringBusinessHoursMessage = MyConfig.getCustomNobodyAvailableDuringBusinessHoursMessage()
		self.__customNobodyAvailableOutsideBusinessHoursMessage = MyConfig.getCustomNobodyAvailableOutsideBusinessHoursMessage()
		self.__JidHandleGroups = MyConfig.getJidHandleGroups()

	@staticmethod
	def factory(MyConfig, MessageBuilder, kwargs):
		return MessageBuilder(MyConfig, IsDuringBusinessHours(MyConfig))

	def getRelayMessageBody(self, sender, receivedMsgBody):
		message = self.__getXmppLink(sender) + ": " + receivedMsgBody + " "
		message += self.__getConfirmationRequestMessage()

		return message

	def getPendingMessagesForRequestedRecipient(self):
		messageBody = self.__getPendingMessages()
		messageBody += self.__getConfirmationRequestMessage()

		return messageBody

	def getPendingMessagesForEmail(self):
		return self.__getPendingMessages()

	def getImmediateSenderConfirmationMessageBody(self):
		msgBody = "Someone will be contacting you shortly. \n"
		if (self.__customImmediateSenderConfirmationMessage):
			msgBody += self.__customImmediateSenderConfirmationMessage

		return msgBody

	def getMessageForwardedMessageBody(self):
		return "Message has been forwarded."

	def getTimedOutNotificationMessageBody(self, NextRecipientJidHandle):
		msg = "Confirmation request timed out and message has been forwarded to "
		if (NextRecipientJidHandle):
			msg += NextRecipientJidHandle.getUsername()
		else:
			msg += 'user support email.'

		return msg

	def getNobodyAvailableMessageBody(self):
		if (self.__isDuringBusinessHours):
			if self.__customNobodyAvailableDuringBusinessHoursMessage:
				msg = self.__customNobodyAvailableDuringBusinessHoursMessage
			else:
				msg = "There is nobody currently available to receive your message."
		else:
			if self.__customNobodyAvailableOutsideBusinessHoursMessage:
				msg = self.__customNobodyAvailableOutsideBusinessHoursMessage
			else:
				msg = "There is nobody currently available to receive your message. Please contact us during normal business hours."

		return msg

	def getHelpdeskUserConfirmationMessageBody(self):
		return "Presence confirmed."

	def getHelpdeskUserCouldNotForwardToGroupMessageBody(self):
		return "Nobody in that group is currently available. Your presence has been confirmed."

	def getRequestConfirmedMessageBody(self, ConfirmerJidHandle):
		return "Your request will be handled by " + ConfirmerJidHandle.getUsername()

	def addPendingMessageBody(self, sender, messageBody):
		if not sender in self.__pendingMessages:
			self.__pendingMessages[sender] = []

		self.__pendingMessages[sender].append(messageBody)

	def presenceConfirmed(self):
		self.__pendingMessages = {}

	def __getXmppLink(self, sender):
		return "xmpp:" + sender

	def __getConfirmationRequestMessage(self):
		groupIdString = ", ".join(self.__getAllGroupIdentifierStrings())
		msg = """
---=====---
Please type anything in this window to acknowledge this request!
Forward to another group using a keyword: %s
---=====---
""" % (groupIdString)

		return msg

	def __getAllGroupIdentifierStrings(self):
		idStrings = [
			JidHandleGroup.getGroupIdentifierString()
			for JidHandleGroup in self.__JidHandleGroups
			if JidHandleGroup.getGroupIdentifierString()
		]

		return idStrings

	def __getPendingMessages(self):
		messageBody = ""
		for sender, messages in self.__pendingMessages.items():
			messageBody += self.__getXmppLink(sender) + "\n"
			messageBody += "\n".join(messages) + "\n"
		return messageBody