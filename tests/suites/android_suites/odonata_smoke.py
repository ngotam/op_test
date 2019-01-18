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
__author__ = 'tammyngo'

import unittest, time, os
from core_framework.controller import ui_controller
from core_framework.config import global_cfg, params
from projects.tote_android import labels
from projects.tote_android import android_utils

import base64

uiObj = None
driver = None


class odonata_smoke(unittest.TestCase):
    uiObj = None
    driver = None
    utils = None

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)

        self.uiObj = ui_controller.ui_controller()
        self.utils = android_utils.android_utils()

        if (not global_cfg.setup_info['status']):
            driver = self.uiObj.get_webdriver_instance(global_cfg.platform_android_wifi)
            global_cfg.driver_instance['driver'] = driver
            self.driver = driver
            global_cfg.setup_info['status'] = True
        else:
            self.driver = global_cfg.driver_instance['driver']



    # setup your test case here
    def setup(self):
        pass

    def test_odonata(self):
        print("odonata launch")
        time.sleep(10)
        next = self.uiObj.find_elements_by_id("com.seagate.odonata.app:id/welcome_card_next");
        if ( next.is_displayed()) :
            next.click()
            time.sleep(1)
            print("click Next")


    def tear_down(self):
        self.uiObj.close_app(self.driver)
        self.uiObj.stop_appium_server()