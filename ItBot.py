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

import sys
import os
import PathAutoloader
import xmpp
import smtplib
import logging
import time

class ItBot():

	def __init__(self, MyConfig):
		self.__MyConfig = MyConfig

		self.__configFilePath = self.__MyConfig.getConfigFilePath().replace('config/', '')
		logPath = '/var/log/' + self.__configFilePath + 'Log'
		if not (os.path.exists(logPath)):
			open(logPath, 'a').close()

		logging.basicConfig(filename=logPath, level=logging.DEBUG)

		self.__BotEventCoordinator = self.__MyConfig.getBotEventCoordinator(self)

		self.start()

	def start(self):
		jid = self.__MyConfig.getJid()
		pwd = self.__MyConfig.getPwd()

		jid = xmpp.protocol.JID(jid)

		cl = xmpp.Client(jid.getDomain(), debug=[])

		if cl.connect() == "":
			logging.error("Failed to connect to domain.")
			sys.exit(0)

		if cl.auth(jid.getNode(),pwd) == None:
			logging.error("authentication failed")
			sys.exit(0)

		cl.RegisterHandler('presence', self.presenceCB)
		cl.RegisterHandler('message', self.messageCB)

		cl.sendInitPresence()

		logging.info('Started IM bot with configuration - ' + self.__configFilePath + ' - at ('  + time.ctime() + ')')
		if (self.__MyConfig.isTestingEnabled()):
			logging.info("(test mode)\n")
		else:
			logging.info("(production mode)\n")

		self.__conn = cl
		self.GoOn()

	def sendMessage(self, Message):
		recipients = []
		for JidHandleGroup in Message.getRecipientJidHandleGroups():
			recipients += [JidHandle.getJid() for JidHandle in  JidHandleGroup.getJidHandles()]
		if (self.__MyConfig.isTestingEnabled()):
			recipientString = ', '.join(recipients)
			logging.info("######Sending Message: \n\n'" + Message.getMessageBody() + "'\n\n------To: " + recipientString)
#			for recipient in recipients:
#				self.__conn.send(xmpp.protocol.Message(recipient, Message.getMessageBody()))
		else:
			for recipient in recipients:
				self.__conn.send(xmpp.protocol.Message(recipient, Message.getMessageBody()))

	def sendEmail(self, sender, receiver, message):
		if (self.__MyConfig.isTestingEnabled()):
			logging.info("######Sending Support Email: \n\n'" + message)
			#s = smtplib.SMTP('localhost')
			#s.sendmail(sender, [receiver], message)
			#s.quit()
		else:
			s = smtplib.SMTP('localhost')
			s.sendmail(sender, [receiver], message)
			s.quit()

	def StepOn(self):
		try:
			self.__conn.Process(1)
		except KeyboardInterrupt:
			return 0
		return 1

	def GoOn(self):
		while self.StepOn():
			self.__BotEventCoordinator.handleStatusCheck()

	def presenceCB(self, conn, presence):
		self.__MyConfig.getPresenceManager().updatePresence(presence)

	def messageCB(self, conn, msg):
		try:
			body = msg.getBody()
			sender = str(msg.getFrom())
			if body is not None:
				body = body.encode('utf-8')
				self.__BotEventCoordinator.handleMessageReceived(sender, body)
		except Exception, e:
			logging.exception(e)
