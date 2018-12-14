'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   TEST SUITE TEMPLATE FOR TOOLKIT MODULES
#
# Purpose:      Facilitates methods to execute and validate tests related to TOOLKIT modules
#
# Arguments:    None
#
# Return Value: An instance of this class
#
#
###################################################################################################################################################################################

####################################################################################################################################################################################


'''
__author__ = 'asanghavi'

import unittest, time,os
from core_framework.config import global_cfg,params
from projects.toolkit_modules_mac.config import project_labels



import base64

from core_framework.controller import mac_ui_controller
from projects.toolkit_modules_mac.controller import project_base_controller


class deet_smoke(unittest.TestCase):

    uiObj = None
    baseConObj = None

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)
        self.uiObj = mac_ui_controller.mac_ui_controller()
        self.baseConObj = project_base_controller.projects_base_controller()
        self.baseConObj.setup_build()


    def test_setup_raid(self):
        self.uiObj.change_current_application_in_test("Toolkit")
        time.sleep(20)
        self.uiObj.start_application("Toolkit")
        self.uiObj.click_on_button_by_text(project_labels.got_it_button)

        time.sleep(1)
        self.uiObj.click_on_button_by_text(project_labels.setup_button)
        time.sleep(1)

        self.uiObj.click_on_button_by_text(project_labels.continue_button)
        time.sleep(1)
        self.uiObj.click_on_button_by_text(project_labels.continue_button)

        time.sleep(1)
        self.uiObj.click_on_button_by_text(project_labels.done_button)




    '''''

    def test_setup_raid_drive(self):
        self.uiObj.click_on_button_by_text(project_labels.got_it_button)
        time.sleep(1)
        self.uiObj.click_on_button_by_text(project_labels.setup_button)
        time.sleep(1)

        self.uiObj.click_on_button_by_text(project_labels.continue_button)
        time.sleep(1)
        self.uiObj.click_on_button_by_text(project_labels.continue_button)

        time.sleep(1)
        self.uiObj.click_on_button_by_text(project_labels.done_button)


    def test_launch_toolkit(self):
        #print(self.driver)
        print("Test passed...")
        #core_mac_lib.find_and_click_uielement_by_text("Set Up")
        #time.sleep(1)
        #core_mac_lib.enter_system_password("Shreeji2930")
        #time.sleep(5)

    '''''










