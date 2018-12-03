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

import unittest, time




class sample_test_suite(unittest.TestCase):

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)


    def test_launch_toolkit(self):
        print("Test passed...")
        #core_mac_lib.start_macOSX_application()
        #time.sleep(5)
        #core_mac_lib.find_and_click_uielement_by_text("Set Up")
