__author__ = 'asanghavi'
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import TimeoutException
from core_framework.commons import logger
from appium.common.exceptions import NoSuchContextException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core_framework.config import params,global_cfg
from appium import webdriver
import time
from selenium.common.exceptions import WebDriverException
from core_framework.commons import logger
from core_framework.commons import utils
import os

'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   ui_controller
#
# Purpose:      Facilitates driving of UI elements using Appium/Selenium
#
# Arguments:    None
#
# Return Value: An instance of this class 
#
#
###################################################################################################################################################################################

####################################################################################################################################################################################

'''


from Crypto.Cipher import AES

class ui_controller:
    logger          = None
    utilsObj        = None


    def __init__(self):
        self.utilsObj = utils.utils()

    def start_appium_server(self):
        """
        starts running instance of appium on port 4723

        :return: boolean (True on success ,False on failure)

        """
        self.utilsObj.fork_process(global_cfg.start_appium_server,global_cfg.appium_log_file)


    def stop_appium_server(self):
        """
        Web driver Instance

        :param platform: Platform
        :return: boolean (True on success ,False on failure)

        """
        os.popen(global_cfg.stop_appium_server).read()


    def get_webdriver_instance(self, platform):

        """
        Web driver Instance

        :param platform: Platform
        :return: boolean (True on success ,False on failure)

        """

        driver = None
        desired_cap = {}

        if (platform == global_cfg.platform_android):

            if (not global_cfg.server_state['status']):
                self.start_appium_server()
                time.sleep(30)
                global_cfg.server_state['status'] = True
                desired_cap = {'platform': params.platform, 'platformVersion': params.platformVersion,
                               'app': params.app_path, 'deviceName': params.device_name,
                               'automationName': 'UiAutomator2'}


        elif(platform == global_cfg.platform_android_wifi):

            desired_cap = {'platformName': 'Android', 'platformVersion': params.platformVersion,
                           'app': params.app_path,
                           'deviceName': params.device_name, 'automationName': 'UiAutomator2',
                           'newCommandTimeout': 120,
                           'appActivity' : params.app_activity,
                           'appWaitActivity': "*",
                           'deviceId': params.ip_address}

        try:
            driver = webdriver.Remote(command_executor=global_cfg.driver_host, desired_capabilities=desired_cap)
        except WebDriverException:
            print("Failed create web driver instance")

        return driver


    def wait_for_element(self,driver,element):
        """
        waits up to 2 mins for the element to be visible

        :param driver: appium webdriver instance
        :param element: element on which call is waiting to be visible
        :return: boolean (True on success ,False on failure)

        """

        try:
            WebDriverWait(driver, global_cfg.max_timeout).until(EC.presence_of_element_located((By.XPATH,element )))
            return True
        except NoSuchElementException:
            return False

    def get_localized_strings(self,driver,locale):
        """
        Get localized strings in a given locale

        :param driver: Appium webdriver instance
        :param locale: Locale (eg: en, es,fr....)
        :return: Returns localized strings

        """

        try:
            return driver.app_strings(language='%s' %locale)
        except NoSuchContextException:
            return False



    def capture_screen_shot_of_screen(self,driver,img_name):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """

        driver.screenshot(img_name)


    def find_element_by_accessibility(self, driver,identifier):

        """
        Finds ui element by its accessibility identifier

        :param driver: Appium webdriver instance
        :param identifier: Ui element accessibility identifier
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_accessibilty_id(identifier)
            return elm
        except NoSuchElementException:
            return False


    def find_element_by_its_xpath(self,driver,element_xpath):
        """
        Finds ui element

        :param driver: Appium webdriver instanceby it's xpath
        :param element_xpath: Ui element xpath
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_xpath(element_xpath)
            return elm
        except NoSuchElementException:
            return False


    def find_element_by_its_class_name(self,driver,class_name):
        """
        Finds ui element by it's class name

        :param driver: Webdriver instance
        :param class_name: Class name of the ui element
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_class_name(class_name)
            return elm
        except NoSuchElementException:
            return False


    def click_element(self,element):
        """
        Click an ui element

        :param element: Webdriver element object
        :return: boolean (True on success ,False on failure)

        """
        try:
            element.click()
            return True
        except ElementNotSelectableException:
            return False

    def input_text_in_field(self,elm_id,text,driver):
        """
        Finds button by content description in an android application and click

        :param driver: Webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """

        try:
            elm = driver.find_element_by_id(elm_id).send_keys(text)
        except NoSuchElementException:
            return False

    def clear_text_from_field(self, elm,driver):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_id(elm).clear()
        except NoSuchElementException:
            return False


    def wait_till_element_is_visible(self,driver,by,field):
        """
        Keeps searching for element's visibility till it reaches max time out limit

        :param driver: Appium webdriver instance
        :param by: By method (eg xpath , id or class name)
        :param field: By label
        :return: boolean (True on success ,False on failure)

        """

        elm = None
        bIsVisible = False
        for i in range(global_cfg.max_timeout):
            try:
                if(by==global_cfg.by_xpath):
                    elm = driver.find_element_by_xpath(field)
                if(by==global_cfg.by_id):
                    elm = driver.find_element_by_id(field)
                if(by==global_cfg.by_input_name):
                    elm = driver.find_element_by_name(field)
                if(by==global_cfg.by_par_link):
                    elm = driver.find_element_by_partial_link_text(field)
                if(by==global_cfg.by_css_selector):
                    elm = driver.find_element_by_css_selector(field)
                if(by==global_cfg.by_class_name):
                    elm = driver.find_element_by_class_name(field)
                if(elm):
                    bIsVisible = True
                    break
            except NoSuchElementException:
                self.logger.logDebug("Element not visible after waiting for max timeout....Please check")
                if(i > global_cfg.max_timeout):
                    self.logger.logDebug("Element not visible after waiting for max timeout....Please check")
        return bIsVisible

    def is_element_visible(self,elm,driver):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        return driver.find_element_by_id(elm).is_displayed()


    def launch_app(self,driver):
        """
        Launches application in test

        :param driver: Appium webdriver instance
        :return: Returns none

        """
        try:
            driver.launch_app()
            time.sleep(3)
        except NoSuchContextException:
            return False

    def close_app(self,driver):
        """
        Closes application in test

        :param driver: Appium webdriver instance
        :return: Returns none

        """
        try:
            driver.close_app()
        except NoSuchContextException:
            return False


    ##############Android related calls#########################################


    def find_and_click_button_by_text_android(self, driver, text):
        """
        Finds button by it's label and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm_path  = self.get_element_path_by_text_android(text)
            self.find_element_by_its_xpath(elm_path, driver).click()
            return True
        except NoSuchElementException:
            return False



    def is_apk_installed_android(self,driver,bundle_id):
        """
        checks if given android application is installed
        :param driver: Appium webdriver instance
        :param text: Application package name
        :return: boolean (True on success ,False on failure)

        """
        try:
            driver.is_app_installed(bundle_id)
        except NoSuchContextException:
            return False



    def scroll_down_screen_android(self,driver):
        """
        scrolls down screen

        :param driver: Appium webdriver instance
        :return: boolean (True on success ,False on failure)

        """
        win_han = driver.current_window_handle()
        size = driver.get_window_size(win_han)
        driver.swipe(size.Width - 10, size.Height * 6 / 8, size.Width - 10, size.Height / 8, 500)
        return True

    def click_back_button_android(self,driver):
        """
        Simulate clicking of back button

        :param driver: Appium webdriver instance
        :return: boolean (True on success ,False on failure)

        """
        try:
            driver.back()
            return True
        except NoSuchContextException:
            return False



    def get_element_path_by_text_android(self,label):
        """
        Finds button by it's label and

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        elm_path = "//*[@text='" + label + "']"
        return elm_path

    def get_element_path_by_desc_android(self,desc):
        """
        Finds ui elemenet by it's content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        elm_path = "//*[@content-desc='" + desc + "']"
        return elm_path


    def find_ui_element_in_android_by_content_desc(self,desc):
        """
        Finds ui element by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        elm = None
        try:
            elm = self.get_element_path_by_desc_android(desc)
            return True
        except NoSuchElementException:
            return False

    def find_and_click_element_by_name_android(self,elm_name,driver):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_name(elm_name)
            return elm
        except NoSuchElementException:
            return False



    def find_and_click_ui_element_by_id(self,platform,driver,id):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        elm = None
        try:
            if(platform == global_cfg.platform_mac):
                elm_path = self.find_element_by_accessibility(id,driver)
                elm = self.find_element_by_its_xpath(elm_path,driver)
            elif(platform == global_cfg.platform_android):
                elm = self.find_element_by_id(id,driver)
            elif(platform == global_cfg.platform_windows):
                elm = self.winObj.find_element_by_automation_id(id,driver)

            elm.click()
            return True
        except NoSuchElementException:
            return False


    def enter_input_in_textfield(self):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """

        pass


    ###########################
        #    Added by tammy
        ##########################

    def find_element_by_android_uiautomator(self, uia_string, driver):

        """
        Finds ui element by its accessibility identifier

        :param driver: Appium webdriver instance
        :param identifier: Ui element accessibility identifier
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_android_uiautomator(uia_string)
            return elm
        except NoSuchElementException:
            return False

    def find_element_by_id(self, identifier, driver):

        """
        Finds ui element by its accessibility identifier

        :param driver: Appium webdriver instance
        :param identifier: Ui element accessibility identifier
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_element_by_id(identifier)
            return elm

        except NoSuchElementException:
            return False

    def find_elements_by_id(self, identifier, driver):

        """
        Finds ui element by its accessibility identifier

        :param driver: Appium webdriver instance
        :param identifier: Ui element accessibility identifier
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm = driver.find_elements_by_id(identifier)
            return elm
        except NoSuchElementException:
            return False

    def find_button_by_text_android(self, driver, text):
        """
        Finds button by it's label and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm_path  = self.get_button_path_by_text_android(text)

            elm = self.find_element_by_its_xpath(driver, elm_path)
            return elm
        except NoSuchElementException:
            return False

    def find_button_elm_path_by_text(self,text):
        """
        Finds button element path by it's text in MacOSX application main window

        :param text: Label of the button
        :return: Button element path in application

        """
        base_path = self.get_base_application_path_macOSX()
        return base_path + "AXButton[@AXTitle='%s']" %text

    def get_button_path_by_text_android(self,label):
        """
        Finds button by it's label and

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        elm_path = "//android.widget.Button[@text='" + label + "']"
        print ("button path = " + elm_path)
        return elm_path

    def scroll_up_screen_android(self, driver):
        """
        scrolls up screen

        :param driver: Appium webdriver instance
        :return: boolean (True on success ,False on failure)

        """
        try:
            size = driver.get_window_size()
            startX = size['width'] / 2
            startY = size['height'] * 0.8
            endX = size['width'] / 2
            endY = size['height'] * 0.2

            #   touchAction = TouchAction(driver)
            #   touchAction.long_press(startX, endY).move_to(startY)
            driver.swipe(startX, startY, endX, endY, 400)

            time.sleep(5)

        except NoSuchContextException:
            return False
        return True

    def scroll_to_find(self, driver, item):
        """
        scrolls to find element by uiautomator

        :param driver: Appium webdriver instance
        :return: boolean (True on success ,False on failure)

        """
        selector = "new UiScrollable(new UiSelector().className(\"android.support.v7.widget.RecyclerView\"))." \
                   + "scrollIntoView(new UiSelector().textContains(\"" + item + "\"))"
        done = self.find_element_by_android_uiautomator(selector, driver)

        return done

    def input_text_in_element(self, elm, text, driver):
        """
        Finds button by content description in an android application and click

        :param driver: Webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """

        try:
            elm.click()
            elm.send_keys(text)

        #   elm = driver.find_element_by_id(elm_id).send_keys(text)
        except NoSuchElementException:
            return False

    def clear_text_from_element(self, elm):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """
        try:
            elm.clear()
        except NoSuchElementException:
            return False

    def is_displayed(self, elm):
        """
        :param elm: element of ui
        :return: boolean (True on success ,False on failure)

        """
        return elm.is_displayed()

    def wait_for_element_from_id(self,driver, identifier):
        """
        waits up to 2 mins for the element to be visible

        :param driver: appium webdriver instance
        :param element: element on which call is waiting to be visible
        :return: boolean (True on success ,False on failure)

        """

        try:
            WebDriverWait(driver, global_cfg.max_timeout).until(EC.presence_of_element_located((By.ID, identifier)))
            return True
        except NoSuchElementException:
            return False

    def is_path_visible(self, driver, xpath, timeout):
        done = False
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            done = True

        except TimeoutException:
            return False
        return done

    def is_path_not_visible(self, driver, xpath, timeout):
        done = False
        try:
            WebDriverWait(driver, timeout).until_not(EC.presence_of_element_located((By.XPATH, xpath)))
            done = True

        except TimeoutException:
            return False
        return done