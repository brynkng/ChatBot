from random import random
import unittest
from JidHandle import JidHandle

class RecipientListModifierTestBase(unittest.TestCase):

	def _getJidHandle(self):
		return JidHandle('someJid' + str(random()), 'someJid' + str(random()) + '@jid.com')