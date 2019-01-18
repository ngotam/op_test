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
from selenium.common.exceptions import NoSuchElementException

import base64

uiObj = None
driver = None


class tote_smoke(unittest.TestCase):
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

    def test_00_CheckConnectUSB(self):
        time.sleep(3)
        try:
            checkbox = self.uiObj.find_element_by_its_xpath(self.driver, "//android.widget.CheckBox")
            if not ( checkbox.is_displayed()):
                print("check box not existed")
            else :
                checkbox.click()
                elm = self.uiObj.find_button_by_text_android(self.driver, "OK")
                elm.click()
                done = True
                self.assertTrue(done, "Connect this USB device = " + done)
                time.sleep(3)
        except NoSuchElementException:
            return False


    def test_01_AllowAcessMedia(self):
        time.sleep(15)
        done = False
        elm = self.uiObj.find_button_by_text_android(self.driver, "ALLOW")
        elm.click()
        done = True
        if ( done ) :
            self.assertTrue(done, "Allow Access Media pass")
        else:
            self.assertTrue(done, "Allow Access Media fail")
        time.sleep(2)

    def test_02_AcceptConditions(self):

        lineartnc = self.driver.find_element_by_id(labels.switch_tnc)
        linear1 = lineartnc.find_element_by_xpath("//android.widget.LinearLayout")
        switch_tnc = linear1.find_element_by_id(labels.id_check)
        switch_tnc.click()

        time.sleep(1)
        lineareula = self.driver.find_element_by_id(labels.switch_eula)
        linear1 = lineareula.find_element_by_xpath("//android.widget.LinearLayout")
        switch_eula = linear1.find_element_by_id(labels.id_check)
        switch_eula.click()
        time.sleep(1)

        linearprivacy = self.driver.find_element_by_id(labels.switch_privacy)
        linear1 = linearprivacy.find_element_by_xpath("//android.widget.LinearLayout")
        switch_privacy = linear1.find_element_by_id(labels.id_check)
        switch_privacy.click()
        time.sleep(1)

        done = self.uiObj.find_and_click_ui_element_by_id(global_cfg.platform_android, self.driver, labels.continue_btn)

        if ( done ) :
            self.assertTrue(done, "Accept all conditions and click continue pass")
        else:
            self.assertTrue(done, "Accept all conditions and click continue fail")
        time.sleep(1)

    def test_03_LaunchRegistration(self):

        done = False
        first_name = params.first_name
        last_name = params.last_name
        email = params.user_email

        self.uiObj.input_text_in_field(labels.firstNameEdit, first_name, self.driver)
        time.sleep(1)

        self.uiObj.input_text_in_field(labels.lastNameEdit, last_name, self.driver)
        time.sleep(1)
        #self.driver.press_keycode(66)
        self.driver.hide_keyboard()
        time.sleep(1)

        self.uiObj.input_text_in_field(labels.emailEdit, email, self.driver)
        time.sleep(1)
    #    self.driver.hide_keyboard()
        self.uiObj.find_element_by_its_xpath(self.driver, "//android.widget.FrameLayout[@index='7']").click()
        done = True
        if ( done ) :
            self.assertTrue(done, "Register user pass")
        else:
            self.assertTrue(done, "Register user fail")
        time.sleep(10)

    def test_04_GetMoreInfo(self):
        done = self.uiObj.find_and_click_ui_element_by_id(global_cfg.platform_android, self.driver, labels.skip_btn)
        if ( done ) :
            self.assertTrue(done, "Skip more info pass")
        else:
            self.assertTrue(done, "Skip more info fail")
        time.sleep(1)

    def test_05_StartInput(self):

        elm = self.driver.find_element_by_id(labels.getStart_btn)
        elm.click()
        done = True
        time.sleep(1)
        if ( done ):
            self.assertTrue(done, "Click get start button pass")
        else:
            self.assertTrue(done, "Click get start button fail")

    def test_06_AllowAccess(self):
        elm = self.uiObj.find_button_by_text_android(self.driver, "ALLOW")
        elm.click()
        done = True
        if (done):
            self.assertTrue(done, "Allow Access Media pass")
        else:
            self.assertTrue(done, "Allow Access Media fail")
        time.sleep(1)

    def test_07_GetDlgMessage(self):
        title = self.uiObj.find_element_by_id(labels.txt_view_title, self.driver)
        print ("title text = " + title.text)
        msg = self.uiObj.find_element_by_id(labels.txt_view_msg, self.driver)
        print ("title msg = " + msg.text)
        if (msg.is_displayed()):
            done = True
        else:
            done = False
        if ( done ) :
            self.assertTrue(done, "Get dialog enable media sort pass")
        else:
            self.assertTrue(done, "Get dialog enable media sort fail")
        time.sleep(2)

    def test_08_ClickLearnMore(self):
        elm = self.uiObj.find_element_by_its_xpath(self.driver, "//*[@text='LEARN MORE']")
        if (elm.is_displayed()):
            elm.click()
            done = True
        else:
            done = False
        if ( done ) :
            self.assertTrue(done, "Click Learn More pass")
        else:
            self.assertTrue(done, "Click Learn More fail")
        time.sleep(2)

    def test_09_SwitchMediaSort(self):
        elm = self.uiObj.find_element_by_id(labels.switch_media_sort, self.driver)
        if (elm.is_displayed()):
            elm.click()
            done = True
        else:
            done = False

        if ( done ) :
            self.assertTrue(done, "switch media sort pass")
        else:
            self.assertTrue(done, "switch media sort fail")
        time.sleep(1)

    def test_10_EnableMediaSort(self):
        elm = self.uiObj.find_button_by_text_android(self.driver, "SORT")
        if (elm.is_displayed()):
            done = True
            elm.click()
            nav_up = self.uiObj.find_element_by_its_xpath(self.driver,
                                                          "//android.widget.ImageButton[@content-desc='Navigate up']")
            if (nav_up.is_displayed()):
                nav_up.click()
        else:
            done = False
        if ( done ) :
            self.assertTrue(done, "Click SORT pass")
        else:
            self.assertTrue(done, "Click SORT fail")
        time.sleep(2)

    def test_11_ClickMenuIcon(self):
        elm = self.uiObj.find_element_by_its_xpath(self.driver, "//android.widget.ImageButton")
        elm.click()
        done = True
        time.sleep(1)
        if ( done ) :
            self.assertTrue(done, "Click menu icon pass")
        else:
            self.assertTrue(done, "Click menu icon fail")

    def test_12_ClickPhoneStorage(self):
        done = self.utils.click_phone_storage(self.driver)
        time.sleep(2)
        if ( done ) :
            self.assertTrue(done, "Click phone storage pass")
        else:
            self.assertTrue(done, "Click phone storage fail")

    def test_13_CreateFolder(self):
        folder_name = "Folder1"
        cancel = False
        done = self.utils.create_folder(self.driver, folder_name, cancel)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Create folder pass")
        else:
            self.assertTrue(done, "Create folder fail")

    def test_14_RenameFolder(self):
        folder_name = "Folder1"
        new_name = "FolderRename"
        confirm = True
        done = self.utils.click_rename_option(self.driver, folder_name, new_name, confirm)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Rename folder pass")
        else:
            self.assertTrue(done, "Rename folder fail")

    def test_15_CopyFolder(self):
        folder_name = "Alarms"
        destination = "FolderRename"
        confirm = True
        done = self.utils.click_copy_option(self.driver, folder_name, destination, confirm)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Copy folder pass")
        else:
            self.assertTrue(done, "Copy folder fail")

    def test_16_DeleteFolder(self):
        folder_name = "FolderRename"
        cancel = False
        done = self.utils.click_delete_option(self.driver, folder_name, cancel)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Delete folder pass")
        else:
            self.assertTrue(done, "Delete folder fail")

    def test_17_OpenTab_Documents(self):
        action_id = "action_documents"
        done = self.utils.openTab(self.driver, action_id)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Open tab documents pass")
        else:
            self.assertTrue(done, "Open tab documents fail")

    def test_18_OpenTab_Music(self):
        action_id = "action_music"
        done = self.utils.openTab(self.driver, action_id)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Open tab music pass")
        else:
            self.assertTrue(done, "Open tab music fail")

    def test_19_OpenTab_Gallery(self):
        action_id = "action_gallery"
        done = self.utils.openTab(self.driver, action_id)
        time.sleep(10)
        if (done):
            self.assertTrue(done, "Open tab gallery pass")
        else:
            self.assertTrue(done, "Open tab gallery fail")

    def test_20_OpenPhotoAtIndex(self):
        index = 7
        done = self.utils.openPhotoAtIndex(self.driver, index)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Open photo pass")
        else:
            self.assertTrue(done, "Open photo fail")

    def test_21_OpenTab_Folders(self):
        action_id = "action_folders"
        done = self.utils.openTab(self.driver, action_id)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Open tab folders pass")
        else:
            self.assertTrue(done, "Open tab folders fail")

    def test_26_ClickBackup(self):
        if (self.utils.click_menu_icon(self.driver)):
            done = self.utils.click_backup_menu_item(self.driver)
            time.sleep(2)
            self.assertTrue(done, "Click backup link pass")
        else:
            self.assertTrue(False, "Fail to click backup link")

    def test_27_ClickBackupNow(self):
        listSelected = ["Documents"]
        confirm = True
        done = self.utils.click_backup_now(self.driver, listSelected, confirm)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Click backup now pass")
        else:
            self.assertTrue(done, "Click backup now fail")

    def test_28_VerifyBackup(self):
        listSelected = ["Documents"]
        done = self.utils.verifyBackup(self.driver, listSelected)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified backup folder pass")
        else:
            self.assertTrue(done, "Verified backup folder fail")

    def test_29_ClickNofications(self):
        if (self.utils.click_menu_icon(self.driver)):
            done = self.utils.click_notification_menu_item(self.driver)
            time.sleep(2)
            self.assertTrue(done, "Verified click Notifications pass")
        else:
            self.assertTrue(False, "Fail to click Notifications link")

    def test_30_VerifyNotifications(self):
        action = "Backup"
        completed = True
        done = self.utils.verifyNofification(self.driver, action, completed)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified Notification backup pass")
        else:
            self.assertTrue(done, "Verified Notification backup fail")

    def test_31_ClickRestore(self):
        time.sleep(2)
        if (self.utils.click_menu_icon(self.driver)):
            done = self.utils.click_restore_menu_item(self.driver)
            time.sleep(2)
            self.assertTrue(done, "Click Restore link pass")
        else:
            self.assertTrue(False, "Fail to click Restore link")

    def test_32_ClickRestoreNow(self):
        deviceName = ""
        done = self.utils.click_restore_now(self.driver, deviceName)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Click Restore now pass")
        else:
            self.assertTrue(done, "Click Restore now fail")

    def test_33_ClickNofications(self):
        if (self.utils.click_menu_icon(self.driver)):
            done = self.utils.click_notification_menu_item(self.driver)
            time.sleep(2)
            self.assertTrue(done, "Verified click Notifications pass")
        else:
            self.assertTrue(False, "Fail to click Notifications link")

    def test_34_VerifyNotifications(self):
        action = "Restore"
        completed = False
        done = self.utils.verifyNofification(self.driver, action, completed)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified Notification restore pass")
        else:
            self.assertTrue(done, "Verified Notification restore fail")

    def test_35_ClickSettings(self):
        if (self.utils.click_menu_icon(self.driver)):
            done = self.utils.click_Settings_menu_item(self.driver)
            time.sleep(2)
            self.assertTrue(done, "Verified click Settings pass")
        else:
            self.assertTrue(False, "Fail to click Settings link")

    def test_36_ClickReport(self):
        sendTo = params.user_email
        confirm = True
        done = self.utils.click_Report_problem(self.driver, sendTo, confirm)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified report problem pass")
        else:
            self.assertTrue(done, "Verified report problem fail")

    def tear_down(self):
        self.uiObj.close_app(self.driver)
        self.uiObj.stop_appium_server()

"""
    
"""



"""""
     def test_22_VerifySortingNameDescending(self):
        sortBy = "Name"
        orderBy = "DESCENDING"
        done = self.utils.sortBy(self.driver, sortBy, orderBy)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified Sort Name Descending pass")
        else:
            self.assertTrue(done, "Verified Sort Name Descending fail")

    def test_23_VerifySortingDatesDescending(self):
        sortBy = "Date Modified"
        orderBy = "DESCENDING"
        done = self.utils.sortBy(self.driver, sortBy, orderBy)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified Sort Date Descending pass")
        else:
            self.assertTrue(done, "Verified Sort Date Descending fail")

    def test_24_VerifySortingDateAscending(self):
        sortBy = "Date Modified"
        orderBy = "ASCENDING"
        done = self.utils.sortBy(self.driver, sortBy, orderBy)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified Sort Date Ascending pass")
        else:
            self.assertTrue(done, "Verified Sort Date Ascending fail")

    def test_25_VerifySortingNameAscending(self):
        sortBy = "Name"
        orderBy = "ASCENDING"
        done = self.utils.sortBy(self.driver, sortBy, orderBy)
        time.sleep(2)
        if (done):
            self.assertTrue(done, "Verified Sort Name Ascending pass")
        else:
            self.assertTrue(done, "Verified Sort Name Ascending fail")

    

    

        
"""""



'''''
        

'''''
        
        

