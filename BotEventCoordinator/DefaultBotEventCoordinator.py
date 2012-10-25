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

import Message
import JidHandle
from RecipientChooser import RecipientChooser

class DefaultBotEventCoordinator():

	def __init__(self, RecipientChooser, MessageBuilder, ItBot):
		self._RecipientChooser = RecipientChooser
		self._MessageBuilder = MessageBuilder
		self._ItBot = ItBot

	@staticmethod
	def factory(MyConfig, ItBot, BotEventCoordinator):
		return BotEventCoordinator(
			RecipientChooser(MyConfig),
			MyConfig.getMessageBuilder(),
			ItBot
		)

	def handleStatusCheck(self):
		pass

	def handleMessageReceived(self, sender, receivedMessageBody):
		Result = self._RecipientChooser.getJidHandleGroupResult(sender, receivedMessageBody)
		if (Result.shouldSendConfirmationMessage()):
			self._sendConfirmationMessage(sender)

		if (Result.hasJidHandles() and Result.shouldSendRelayMessage):
			self._sendRelayMessage(sender, receivedMessageBody, Result.getJidHandleGroups())
		elif (Result.shouldSendNobodyAvailableMessage()):
			self._handleNobodyAvailable(Result, sender, receivedMessageBody)

	def _sendRelayMessage(self, sender, receivedMessageBody, RecipientJidHandleGroups):
		messageBody = self._MessageBuilder.getRelayMessageBody(sender, receivedMessageBody)
		RelayMessage = Message.Message(RecipientJidHandleGroups, messageBody)

		self._ItBot.sendMessage(RelayMessage)

	def _handleNobodyAvailable(self, Result, sender, receivedMessageBody):
		messageBody = self._MessageBuilder.getNobodyAvailableMessageBody()
		NobodyAvailableMessage = Message.Message([JidHandleGroup([JidHandle.JidHandle('', sender)])], messageBody)

		self._ItBot.sendMessage(NobodyAvailableMessage)

	def _sendConfirmationMessage(self, sender):
		confirmationMessageBody = self._MessageBuilder.getImmediateSenderConfirmationMessageBody()
		ConfirmationMessage = Message.Message([JidHandleGroup([JidHandle.JidHandle('', sender)])], confirmationMessageBody)

		self._ItBot.sendMessage(ConfirmationMessage)