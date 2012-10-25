import unittest
import PathAutoloader
from ConfigTestBase import ConfigTestBase
from ChatBot.BotEventCoordinator.DefaultBotEventCoordinator import DefaultBotEventCoordinator
import ValidBotEventCoordinator

class GetBotEventCoordinatorTest(ConfigTestBase):
    
    __configKeyString = 'bot_event_coordinator'
    
    __name = 'BotEventCoordinator'
    
    def setUp(self):
        ConfigTestBase.setUp(self)
    
    def tearDown(self):
        ConfigTestBase.tearDown(self)
        
    def test_raises_exception_when_module_and_class_are_invalid(self):
        self._given_production_setup_is_correct()
        
        self._assert_raises_exception_when_module_and_class_are_invalid(self.__configKeyString, self.__name)
        
    def test_raises_exception_when_module_is_valid_but_class_is_invalid(self):
        self._assert_raises_exception_when_module_is_valid_but_class_is_invalid(self.__configKeyString, self.__name)
            
    def test_raises_exception_if_class_does_not_subclass_default_class(self):
        self._assert_raises_exception_if_class_does_not_subclass_default_class(self.__configKeyString, self.__name)        
        
    def test_returns_default_class_when_no_class_exists_in_config(self):
        self._given_production_setup_is_correct()
        self._given_no_class_exists()
        
        MyConfig = self._getConfig()
        
        ItBotPlaceholder = None
        self.assertIsInstance(MyConfig.getBotEventCoordinator(ItBotPlaceholder), DefaultBotEventCoordinator)
    
    def test_returns_valid_class_when_one_exists_in_config_and_is_valid(self):
        self._given_production_setup_is_correct()
        
        self._given_module_and_class_exist_in_config_and_are_valid(self.__configKeyString, self.__name)
        ExpectedConfigLoadedClass = ValidBotEventCoordinator.ValidBotEventCoordinator
    
        MyConfig = self._getConfig()
        
        ItBotPlaceholder = None
        ActualConfigLoadedClass = MyConfig.getBotEventCoordinator(ItBotPlaceholder)
        
        self.assertIsInstance(ActualConfigLoadedClass, ExpectedConfigLoadedClass)
            
if __name__ == '__main__':
    unittest.main()