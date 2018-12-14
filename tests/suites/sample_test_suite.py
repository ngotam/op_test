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
from core_framework.controller import ui_controller
from core_framework.config import global_cfg,params



import base64

from core_framework import core_mac_lib


class sample_test_suite(unittest.TestCase):

    uiObj = None
    driver = None
    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)
        self.uiObj = ui_controller.ui_controller()
        '''''
        if(not global_cfg.setup_info['status']):
            driver = self.uiObj.get_webdriver_instance(global_cfg.platform_android_wifi)
            global_cfg.driver_instance['driver'] = driver
            self.driver = driver
            global_cfg.setup_info['status'] = True
        else:
            self.driver = global_cfg.driver_instance['driver']
        '''''




    def test_launch_toolkit(self):
        #print(self.driver)
        print("Test passed...")
        core_mac_lib.start_macOSX_application()
        time.sleep(8)
        #core_mac_lib.find_and_click_uielement_by_text("Set Up")
        #time.sleep(1)
        #core_mac_lib.enter_system_password("Shreeji2930")
        #time.sleep(5)











