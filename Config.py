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

from ConfigParser import ConfigParser

import JidHandle
import os.path
import sys
from JidHandleGroup import JidHandleGroup
from MessageBuilder.DefaultMessageBuilder import DefaultMessageBuilder
from BotEventCoordinator.DefaultBotEventCoordinator import DefaultBotEventCoordinator
from ConfigurationError import ConfigurationError

class Config():
	DEFAULT_CONFIRMATION_REQUEST_SECOND_THRESHOLD = 120
	DEFAULT_FORWARDED_MESSAGE_DELAY_SECOND_THRESHOLD = 120

	START_FILTERS_AND_SORTS_KEY = '--START_FILTERS_AND_SORTS--'
	END_FILTERS_AND_SORTS_KEY = '--END_FILTERS_AND_SORTS--'

	START_JID_FILE_LOCATIONS_KEY = '--START_JID_FILE_LOCATIONS--'
	END_JID_FILE_LOCATIONS_KEY = '--END_JID_FILE_LOCATIONS--'

	START_JID_HANDLES_KEY = '--START_JID_HANDLES--'
	END_JID_HANDLES_KEY = '--END_JID_HANDLES--'

	START_IGNORED_LIST_MODIFIERS_KEY = '--START_IGNORED_LIST_MODIFIERS--'
	END_IGNORED_LIST_MODIFIERS_KEY = '--END_IGNORED_LIST_MODIFIERS--'

	def __init__(self, configFilePath, PresenceManager):
		self.__currentDir = os.path.dirname(__file__)
		self.__configFilePath = configFilePath
		self.__PresenceManager = PresenceManager
		self.__ConfigParser = ConfigParser(configFilePath)
		self.__configString = open(configFilePath, 'r').read()

		self.__productionJid = self.__ConfigParser.findConfigLine('production_jid')
		self.__productionPwd = self.__ConfigParser.findConfigLine('production_pwd')
		self.__testJid = self.__ConfigParser.findConfigLine('test_jid')
		self.__testPwd = self.__ConfigParser.findConfigLine('test_pwd')

		self.__jidHandleGroups = self.__getJidHandleGroups()
		self.__testingEnabled = self.__ConfigParser.findConfigLine('testing_enabled').lower() == 'true'
		self.__messageBuilderClassDict = {
			'class' : self.__ConfigParser.findConfigLine('message_builder'),
			'config_key' : 'message_builder'
		}
		self.__botEventCoordinatorClassDict = {
			'class' : self.__ConfigParser.findConfigLine('bot_event_coordinator'),
			'config_key' : 'bot_event_coordinator'
		}

		self.__validateConfiguration()

	def getConfigFilePath(self):
		return self.__configFilePath

	def getJid(self):
		if (self.isTestingEnabled()):
			jid = self.__testJid
		else:
			jid = self.__productionJid

		return jid

	def getPwd(self):
		if (self.isTestingEnabled()):
			pwd = self.__testPwd
		else:
			pwd = self.__productionPwd

		return pwd

	def getJidHandleGroups(self):
		return self.__jidHandleGroups

	def getPresenceManager(self):
		return self.__PresenceManager

	def getMessageBuilder(self, **kwargs):
		return self.__getConfigLoadedClass(
			self.__messageBuilderClassDict['class'],
			DefaultMessageBuilder,
			kwargs
		)

	def getBotEventCoordinator(self, ItBot):
		moduleString = self.__botEventCoordinatorClassDict['class']
		if (moduleString):
			BotEventCoordinator = self.__getClassFromModuleString(moduleString)
			return BotEventCoordinator.factory(self, ItBot, BotEventCoordinator)
		else:
			return DefaultBotEventCoordinator.factory(
				self,
				ItBot,
				DefaultBotEventCoordinator
			)

	def getOrderedRecipientListModifiers(self):

		filterAndSortModuleStrings = self.__ConfigParser.findConfigLinesBetween(
			self.START_FILTERS_AND_SORTS_KEY,
			self.END_FILTERS_AND_SORTS_KEY
		)

		return [
			self.__getClassFromModuleString(moduleString.strip()).factory(self, self.__getClassFromModuleString(moduleString.strip()))
			for moduleString in filterAndSortModuleStrings
			if moduleString.strip()
		]

	def isTestingEnabled(self):
		return self.__testingEnabled

	def getCustomImmediateSenderConfirmationMessage(self):
		return self.__ConfigParser.findConfigLine('custom_immediate_sender_confirmation_message')

	def getCustomNobodyAvailableDuringBusinessHoursMessage(self):
		return self.__ConfigParser.findConfigLine('nobody_available_during_business_hours_message')

	def getCustomNobodyAvailableOutsideBusinessHoursMessage(self):
		return self.__ConfigParser.findConfigLine('nobody_available_outside_business_hours_message')

	def getBusinessHoursSettingString(self):
		return self.__ConfigParser.findConfigLine('business_hours_setting_string')

	def getConfirmationRequestSecondThreshold(self):
		"""Used in HelpDesk module's PresenceConfirmationManager"""

		confirmationRequestSecondThreshold = self.__ConfigParser.findConfigLine('confirmation_request_second_threshold')
		if (confirmationRequestSecondThreshold):
			return confirmationRequestSecondThreshold
		else:
			return self.DEFAULT_CONFIRMATION_REQUEST_SECOND_THRESHOLD

	def getForwardedMessageSecondThreshold(self):
		"""Used in HelpDesk module's PresenceConfirmationManager"""

		forwardedRequestSecondThreshold = self.__ConfigParser.findConfigLine('forwarded_message_second_threshold')
		if (forwardedRequestSecondThreshold):
			return forwardedRequestSecondThreshold
		else:
			return self.DEFAULT_FORWARDED_MESSAGE_DELAY_SECOND_THRESHOLD

	def getUserSupportEmailSender(self):
		return self.__ConfigParser.findConfigLine('user_support_email_sender')

	def getUserSupportEmailReceiver(self):
		return self.__ConfigParser.findConfigLine('user_support_email_receiver')

	def __getConfigLoadedClass(self, moduleString, DefaultClass, kwargs):
		if (moduleString):
			ConfigLoadedClass = self.__getClassFromModuleString(moduleString)
			return ConfigLoadedClass.factory(self, ConfigLoadedClass, kwargs)
		else:
			return DefaultClass.factory(self, DefaultClass, kwargs)

	def __getJidHandleGroups(self):
		JidHandleGroups = []

		idString = 'jid_handle_group_file_location='

		fileLocations = self.__ConfigParser.findConfigLinesBetween(
			self.START_JID_FILE_LOCATIONS_KEY,
			self.END_JID_FILE_LOCATIONS_KEY
		)
		fileLocations = [fileLocation.replace(idString, '') for fileLocation in fileLocations]

		for fileLocation in fileLocations:
			JidHandleConfigParser = ConfigParser(os.path.join(self.__currentDir, fileLocation))

			jidHandleLines = JidHandleConfigParser.findConfigLinesBetween(
				self.START_JID_HANDLES_KEY,
				self.END_JID_HANDLES_KEY
			)
			JidHandles = []
			for jidHandleLine in jidHandleLines:
				jidHandleLine = jidHandleLine.split(':')
				jid = jidHandleLine.pop().strip()
				userName = jidHandleLine.pop().strip()
				JidHandles.append(JidHandle.JidHandle(userName, jid))

			ignoredListModifierLines = JidHandleConfigParser.findConfigLinesBetween(
				self.START_IGNORED_LIST_MODIFIERS_KEY,
				self.END_IGNORED_LIST_MODIFIERS_KEY
			)
			IgnoredListModifiers = [self.__getClassFromModuleString(listModifierLine)
									for listModifierLine in ignoredListModifierLines
									if listModifierLine.strip()]

			groupIdentifierString = JidHandleConfigParser.findConfigLine('group_identifier_string')
			JidHandleGroups.append(JidHandleGroup(JidHandles, IgnoredListModifiers, groupIdentifierString))

		return JidHandleGroups

	def __validateConfiguration(self):
		if (self.isTestingEnabled()):
			if (self.__testJid.strip() == '' or self.__testPwd.strip() == ''):
				raise ConfigurationError('Must have a valid jabber id and password for test account when testing is enabled!')

		elif (self.__productionJid.strip() == '' or self.__productionPwd.strip() == ''):
			raise ConfigurationError('Must enter valid production jid and password in configuration file when testing account is disabled!')

		JidHandleGroups = self.getJidHandleGroups()
		if (not JidHandleGroups or (JidHandleGroups and not JidHandleGroups[0].getJidHandles())):
			raise ConfigurationError('''Must enter at least one jid_handle_group_file_location and have one jid handle set
							Inside main config file:
							jid_handle_group_file_location=config/RecipientLists/defaultSupportList.txt

							Inside defaultSupportList.txt:
							--START_JID_HANDLES--
							John Smith : johnSmith@talk.google.com
							--END_JID_HANDLES--''')

		self.__validateConfigLoadedClass(self.__messageBuilderClassDict)
		self.__validateConfigLoadedClass(self.__botEventCoordinatorClassDict)

	def __validateConfigLoadedClass(self, classDict):
		if classDict['class']:

			configClassKey = classDict['config_key']
			moduleString = classDict['class']

			prettyClassBase = configClassKey.replace('_', ' ')

			try:
				ConfigLoadedClass = self.__getClassFromModuleString(moduleString)
			except AttributeError:
				raise ConfigurationError('Invalid ' + prettyClassBase + ' class. Must be the same name as module')

			PackageName = prettyClassBase.title().replace(' ', '')
			defaultModuleString = PackageName + '.Default' + PackageName
			defaultClassString = 'Default' + PackageName
			DefaultModule = sys.modules[defaultModuleString]
			DefaultModuleClass = getattr(DefaultModule, defaultClassString)
			if (not issubclass(ConfigLoadedClass, DefaultModuleClass) and ConfigLoadedClass.__name__ != DefaultModuleClass.__name__):
				raise ConfigurationError(ConfigLoadedClass.__name__ + ' must subclass ' + DefaultModuleClass.__name__)

	def __getClassFromModuleString(self, moduleString):
		__import__(moduleString)
		Module = sys.modules[moduleString]
		return getattr(Module, moduleString)