import PathAutoloader
import unittest
from ludibrio import Stub
from JidHandle import JidHandle
from PresenceManager import PresenceManager

class PresenceManagerTest(unittest.TestCase):

	def setUp(self):
		self.__PresenceManager = PresenceManager()
		unittest.TestCase.setUp(self)
		self.__PresenceManager._PresenceManager__presenceRoster = {}

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_isJidHandleAvailable_returns_false_if_jid_handle_is_currently_away(self):
		SomeJidHandle = JidHandle('someUserName', 'someUnAvailableJid@success.net')
		self.__given_jid_handle_status_is_currently(SomeJidHandle, 'away')

		self.assertFalse(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_isJidHandleAvailable_returns_false_if_jid_handle_is_currently_marked_as_offline(self):
		""" This is the option where you can select to appear as offline """

		SomeJidHandle = JidHandle('someUserName', 'someUnAvailableJid@success.net')
		self.__given_jid_handle_is_currently_marked_as_offline(SomeJidHandle)

		self.assertFalse(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_isJidHandleAvailable_returns_false_if_jid_handle_is_do_not_disturb_status(self):
		SomeJidHandle = JidHandle('someUserName', 'someUnAvailableJid@success.net')
		self.__given_jid_handle_status_is_currently(SomeJidHandle, 'dnd')

		self.assertFalse(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_isJidHandleAvailable_returns_false_if_jid_handle_is_extended_away_status(self):
		""" This is the option where you can select to appear as offline """

		SomeJidHandle = JidHandle('someUserName', 'someUnAvailableJid@success.net')
		self.__given_jid_handle_status_is_currently(SomeJidHandle, 'xa')

		self.assertFalse(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_isJidHandleAvailable_returns_true_if_jid_handle_status_is_available(self):
		SomeJidHandle = JidHandle('someUserName', 'someAvailableJid@success.net')
		self.__given_jid_handle_status_is_currently(SomeJidHandle, None)

		self.assertTrue(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_isJidHandleAvailable_returns_true_if_jid_handle_status_is_chatty(self):
		SomeJidHandle = JidHandle('someUserName', 'someAvailableJid@success.net')
		self.__given_jid_handle_status_is_currently(SomeJidHandle, 'chat')

		self.assertTrue(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_isJidHandleAvailable_returns_false_if_jid_handle_is_not_found(self):
		'''This can happen if a JidHandle is invalid or if the person is currently logged off'''
		SomeJidHandle = JidHandle('someUserName', 'someAvailableJid@success.net')

		self.assertFalse(self.__PresenceManager.isJidHandleAvailable(SomeJidHandle))

	def test_getStatusMsg_returns_correct_status_msg(self):
		SomeJidHandle = JidHandle('someUserName', 'someAvailableJid@success.net')
		expectedMsg = 'On vacation!'
		self.__given_jid_handle_status_msg_is_currently(SomeJidHandle, expectedMsg)

		self.assertEquals(expectedMsg, self.__PresenceManager.getStatusMsg(SomeJidHandle))

	def __given_jid_handle_status_is_currently(self, AJidHandle, status):
		with Stub() as presence:
			presence.getFrom() >> AJidHandle.getJid()
			presence.getShow() >> status
			presence.getType() >> None
			presence.getStatus() >> None

		self.__PresenceManager.updatePresence(presence)

	def __given_jid_handle_is_currently_marked_as_offline(self, AJidHandle):
		with Stub() as presence:
			presence.getFrom() >> AJidHandle.getJid()
			presence.getShow() >> None
			presence.getType() >> 'unavailable'
			presence.getStatus() >> None

		self.__PresenceManager.updatePresence(presence)

	def __given_jid_handle_status_msg_is_currently(self, AJidHandle, statusMsg):
		with Stub() as presence:
			presence.getFrom() >> AJidHandle.getJid()
			presence.getShow() >> None
			presence.getType() >> 'unavailable'
			presence.getStatus() >> statusMsg

		self.__PresenceManager.updatePresence(presence)


if __name__ == '__main__':
	unittest.main()