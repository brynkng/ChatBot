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

import logging

class PresenceManager():

	def __init__(self):
		self.__presenceRoster = {}

	def updatePresence(self, presence):
		jid = presence.getFrom()
		status = presence.getShow()
		statusMsg = presence.getStatus()
		type = presence.getType()

		self.__presenceRoster[jid] = {'status' : status, 'status_msg' : statusMsg, 'type' : type}

	def isJidHandleAvailable(self, JidHandle):
		jid = JidHandle.getJid()

		if jid in self.__presenceRoster:
			presence = self.__presenceRoster.get(jid)
		else:
#			logging.info("jid: " + jid + " is not logged on - skipping. ")
			return False

		isOnAvailableStatus = presence.get('status') is None or presence.get('status') == 'chat'
		markedAsOffline = presence.get('type') == 'unavailable'

		return isOnAvailableStatus and not markedAsOffline

	def getStatusMsg(self, JidHandle):
		jid = JidHandle.getJid()
		presence = self.__presenceRoster.get(jid)
		return presence.get('status_msg')