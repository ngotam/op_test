__author__ = 'asanghavi'
from selenium.common.exceptions import WebDriverException
from core_framework.commons import logger
import os




'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   mac_ui_controller
#
# Purpose:      Facilitates driving of UI elements on MacOSX 
#
# Arguments:    None
#
# Return Value: An instance of this class 
#
#
###################################################################################################################################################################################

####################################################################################################################################################################################

'''
from core_framework.commons import logger

from Crypto.Cipher import AES

from core_framework import core_mac_lib
class mac_ui_controller:
    logger          = None



    def __init__(self):
        #self.logger = logger.logger(__name__)
        pass


    def handle_decide_later_alert(self):
        """
        Handle decide later alert
        :return: None

        """
        core_mac_lib.handle_decide_later_alert()

    def change_current_application_in_test(self,app_name):
        """
        sets the current application in test
        :param app_name: name of the application
        :return: None

        """
        core_mac_lib.change_current_application_in_test(app_name)


    def start_application(self,app_name):
        """
        Launches application by name found in test suite config
        :return: None

        """
        core_mac_lib.start_app(app_name)

    def quit_application(self,app_name):
        """
        stops application by name found in test suite config

        :return: None

        """
        core_mac_lib.stop_app(app_name)


    def get_all_textFields_by_index(self):
        """
        returns list of all visible textFields by index on the current screen
        :param : None
        :return: List of textFields by Index

        """
        return core_mac_lib.get_all_textfields_by_index()

    def get_all_buttons_by_index(self):
        """
        returns list of all visible buttons by index on the current screen
        :param : None
        :return: List of textFields by Index

        """
        return core_mac_lib.get_all_buttons_by_index()

    def get_all_checkboxes_by_index(self):
        """
        returns list of all visible checkboxes by index on the current screen
        :param : None
        :return: List of checkboxes by Index

        """
        return core_mac_lib.get_all_checkboxes_by_index()

    def get_all_comboboxes_by_index(self):
        """
        returns list of all visible comboboxes by index on the current screen
        :param : None
        :return: List of checkboxes by Index

        """
        return core_mac_lib.get_all_comboboxes_by_index()


    def get_all_static_texts_by_name(self):
        """
        returns list of all visible static texts on the current screen
        :param : None
        :return: List of all visible static texts

        """
        pass


    def click_on_button_by_text(self,button_label):
        """
        find a button by it's text and click it
        :param button_label: text on the button
        :return: None

        """
        core_mac_lib.find_and_click_button_by_label(button_label)

    def click_on_button_by_index(self,index):
        """
        find a button by it's index and click it
        :param button_label: text on the button
        :return: None

        """
        core_mac_lib.click_button_by_index(index)


    def click_on_textField_by_name(self,name):
        """
        find a textField by index and click it
        :param name: name of the textField
        :return: None

        """
        core_mac_lib.find_and_click_textField_by_label(name)


    def click_on_checkbox_by_index(self,index):
        """
        find a checkbox by index and click it
        :param index: index of the item
        :return: None

        """
        core_mac_lib.click_checkbox_by_index(index)

    def click_on_checkbox_by_name(self,name):
        """
        find a checkbox by index and click it
        :param index: name of the checkbox
        :return: None

        """
        core_mac_lib.find_and_click_checkbox_by_label(name)


    def click_on_textField_by_index(self,index):
        """
        find a textField by index and click it
        :param index: index of the item
        :return: None

        """
        core_mac_lib.click_textField_by_index(index)


    def enter_text_in_textField_by_index(self,index,text):
        """
        find a textField by index and enter text in it
        :param index: index of the item
        :param text: text to be entered
        :return: None

        """
        core_mac_lib.find_textField_by_index_and_enter_text(index,text)


    def enter_text_in_textField_by_name(self,name,text):
        """
        find a textField by name and enter text in it
        :param name: name of the textField
        :param text: text to be entered
        :return: None

        """
        core_mac_lib.find_textField_by_name_and_enter_text(name,text)


    def enter_system_password(self,password):
        """
        Enters system password required for macOSX apps
        :param password: system password
        :return: None

        """
        core_mac_lib.enter_system_password(password)


    def allow_permission_to_open_new_app(self):
        """
         clicks on open button when permssion is assked for macOSX apps
        :return: None

        """
        core_mac_lib.allow_permission_to_open_app()


    def click_on_decide_later_alert(self):
        """
         clicks on decide later button on drive detection
        :return: None

        """
        core_mac_lib.click_decide_later_message()




