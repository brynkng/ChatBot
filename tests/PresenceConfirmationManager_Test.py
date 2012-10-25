import unittest
from time import time
from ludibrio import Stub
from PresenceConfirmationManager import PresenceConfirmationManager

class PresenceConfirmationManagerTest(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)

	def tearDown(self):
		unittest.TestCase.tearDown(self)

	def test_hasTimedOut_returns_false_if_the_confirmation_request_threshold_has_not_been_reached(self):
		self.__given_that_the_confirmation_request_threshold_in_seconds_is(120)
		Manager = self.__getPresenceConfirmationManager()
		self.__and_it_has_been_this_many_seconds_since_request_started(60, Manager)

		self.assertFalse(Manager.hasTimedOut())

	def test_hasTimedOut_returns_true_if_the_confirmation_request_threshold_has_been_passed(self):
		self.__given_that_the_confirmation_request_threshold_in_seconds_is(120)
		Manager = self.__getPresenceConfirmationManager()
		self.__and_it_has_been_this_many_seconds_since_request_started(121, Manager)

		self.assertTrue(Manager.hasTimedOut())

	def __getPresenceConfirmationManager(self):
		return PresenceConfirmationManager(self.__MyConfig)

	def __and_it_has_been_this_many_seconds_since_request_started(self, seconds, Manager):
		Manager.startNewRequest()
		Manager._PresenceConfirmationManager__requestStartTime = float(time() - seconds)

	def __given_that_the_confirmation_request_threshold_in_seconds_is(self, seconds):
		with Stub() as MyConfig:
			MyConfig.getConfirmationRequestSecondThreshold() >> str(seconds)
		self.__MyConfig = MyConfig


if __name__ == '__main__':
	unittest.main()