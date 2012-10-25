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

class JidHandle():
	__userName = ''
	__jid = ''

	def __init__(self, userName, jid):
		self.__userName = userName
		self.__jid = jid

	def __eq__(self, other):
		return isinstance(other, JidHandle) and  (self.getUsername() == other.getUsername() and self.getJid() == other.getJid())

	def __repr__(self):
		return str(self.__class__) + '\n' + 'Username: ' + self.getUsername() + 'Jid: ' + self.getJid()

	def getUsername(self):
		return self.__userName

	def getJid(self):
		return self.__jid
