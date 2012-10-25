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

class Message():

	def __init__(self, RecipientJidHandleGroups, messageBody):
		self.__RecipientJidHandleGroups = RecipientJidHandleGroups
		self.__messageBody = messageBody

	def __eq__(self, other):
		return isinstance(other, Message) and  (
			self.getRecipientJidHandleGroups() == other.getRecipientJidHandleGroups()
			and self.getMessageBody() == other.getMessageBody()
		)

	def __repr__(self):
		return str(self.__class__) \
			   + '\n' + ', '.join([repr(jidHandleString) for jidHandleString in self.getRecipientJidHandleGroups()]) \
			   + '\nMessage: ' + self.getMessageBody()

	def getRecipientJidHandleGroups(self):
		return self.__RecipientJidHandleGroups

	def getMessageBody(self):
		return self.__messageBody