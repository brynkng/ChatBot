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

class DefaultMessageBuilder():
    
    def __init__(self, MyConfig):
        self._MyConfig = MyConfig
    
    @staticmethod
    def factory(MyConfig, MessageBuilder, kwargs):
        return MessageBuilder(MyConfig)
    
    def getRelayMessageBody(self, sender, receivedMsgBody):
        return receivedMsgBody
    
    def getImmediateSenderConfirmationMessageBody(self):
        return "Successfully forwarded."
    
    def getNobodyAvailableMessageBody(self):
        return "There is nobody currently available to receive your message."