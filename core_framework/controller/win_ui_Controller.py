__author__ = 'asanghavi'
import os
from core_framework.config import global_cfg
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotSelectableException
from core_framework.commons import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from appium import webdriver
import win32gui


'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   win_ui_controller
#
# Purpose:      Facilitates driving of UI elements on Windows
# 
# Arguments:    None
#
# Return Value: An instance of this class 
#
#
###################################################################################################################################################################################

####################################################################################################################################################################################

'''

from core_framework import core_win_lib
import time,re

"""
Win UI Controller
"""
class win_ui_controller:
    logger          = None


    #constructor call
    def __init__(self):
        #self.logger = logger.logger(__name__)
        pass



    def start_application(self,app_name):
        """
        Launches application by name found in test suite config
        :return: None

        """
        core_win_lib.start_app(app_name)

    def quit_application(self,app_name):
        """
        stops application by name found in test suite config

        :return: None

        """
        core_win_lib.stop_app(app_name)

    def get_all_buttons_with_path(self):
        return core_win_lib.get_all_buttons_with_path()

    def click_on_x_and_y_coordinates(self,x,y):
        """
        click on x and y position of an element on the screen

        :param : x and y coordinates
        :return: boolean True on success

        """
        return core_win_lib.click_on_x_and_y_coordinates(x,y)

    def enter_text(self,elm,text):
        """
        Finds element and enters text in the field

        :param driver: Appium webdriver instance
        :param elm: element where texts needs to be entered
        :return: boolean (True on success ,False on failure)
        """
        return core_win_lib.enter_text(elm,text)




    def get_all_strings_visible_on_screen(self):
        """
        returns list of all visible texts present in any UIElement on the current screen
        :param : None
        :return: List of all visible texts

        """
        return core_win_lib.get_all_strings_on_screen()

    def click_element_by_text_or_classNN(self,text,window_title):
        """
        clicks matching text present in any UIElement on the current screen
        :param 1: text on the element (like label on the button)
        :param 2: window title of the application
        :return:  boolean

        """
        return core_win_lib.click_element_by_text_or_classNN(text,window_title)


    def find_element_by_name(self, name):
        """
        Finds ui element by its name

        :param driver: winappdriver instance
        :param identifier: Ui element name
        :return: boolean (True on success ,False on failure)

        """

        return core_win_lib.find_element_by_name(name)

    def click_element_by_name(self, name):
        """
        Finds ui element by its name and clicks it

        :param driver: winappdriver instance
        :param identifier: Ui element name
        :return: boolean (True on success ,False on failure)

        """

        return core_win_lib.click_element_by_name(name)


    def capture_screen_shot_of_screen(self,img_name):
        """
        Finds button by content description in an android application and click

        :param driver: Appium webdriver instance
        :param text: Label of the button
        :return: boolean (True on success ,False on failure)

        """

        global_cfg.driver_instance['driver'].screenshot(img_name)


    def find_element_by_automationId(self, driver,identifier):

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


    def wait_for_element_to_be_visible(self,label,wait_time):
        """
        waits till a given time and checks if element with a given label is visible
        :return: returns True if it finds it else False and also returns False if reaches max_timeout

        """

        bmatchFound = False
        i = 0
        if (wait_time > global_cfg.max_timeout):
            wait_time = global_cfg.max_timeout
        while (i <= wait_time):
            time.sleep(1)
            i = i + 1
            if (core_win_lib.find_if_text_is_visible_on_screen(label)):
                bmatchFound = True
                break
            else:
                time.sleep(5)
        return bmatchFound

    def find_if_text_is_visible_on_screen(self,text):
        """
        searches all static text fields and textareas on screen and checks if a given text is visible
        :return: returns True if it finds it else False and also returns False if it does not find it

        """
        return core_win_lib.find_if_text_is_visible_on_screen(text)

    def take_screen_shot(self,fname):
        """
        searches all static text fields and textareas on screen and checks if a given text is visible
        :return: returns True if it finds it else False and also returns False if it does not find it

        """
        return core_win_lib.take_screen_shot(fname)


    def parse_screen_contents(self,fname):
        """
        searches all static text fields and textareas on screen and checks if a given text is visible
        :return: returns True if it finds it else False and also returns False if it does not find it

        """
        return core_win_lib.parse_screen_contents(fname)


    def click_element_by_image_class_with_max_x_pos(self):
        """
        Finds element by Image class with max x position and click


        :return: boolean (True on success ,False on failure)

        """
        return core_win_lib.click_by_x_pos_for_element_by_class_image()

    def click_element_by_image_class_with_max_y_pos(self):
        """
        Finds element by Image class with max x position and click


        :return: boolean (True on success ,False on failure)

        """
        return core_win_lib.click_by_y_pos_for_element_by_class_image()

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # Add functions for win_ui_controller using appium by Tammy
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def find_element_by_text(self, driver, name):
        """
            Finds ui element by its name
            :param driver: winappdriver instance
            :param identifier: Ui element name
            :return: element
        """
        try:
            elm = driver.find_element_by_name(name)
            return elm
        except NoSuchElementException:
            return None

    def find_element_by_classname(self, driver, cname):
        """
            Finds ui element by its classname
            :param driver: winappdriver instance
            :param identifier: Ui element classname
            :return: element
        """
        try:
            elm = driver.find_element_by_class_name(cname)
            return elm
        except NoSuchElementException:
            return None

    def find_elements_by_classname(self, driver, cname):
        """
            Finds ui element by its classname
            :param driver: winappdriver instance
            :param identifier: Ui element classname
            :return:list element
        """
        try:
            elms = driver.find_elements_by_class_name(cname)
            return elms
        except NoSuchElementException:
            return None

    def find_element_by_id(self, driver, identifier):
        """
            Finds ui element by its automationID
            :param driver: winappdriver instance
            :param identifier: automationID
            :return:element
        """
        try:
            elm = driver.find_element_by_accessibility_id(identifier)
            return elm
        except NoSuchElementException:
            return False

    def find_elements_by_id(self, driver, identifier):
        """
            Finds ui element by its automationID
            :param driver: winappdriver instance
            :param identifier: automationID
            :return: list element
        """
        try:
            elm = driver.find_elements_by_accessibility_id(identifier)
            return elm
        except NoSuchElementException:
            return False

    def find_element_by_xpath(self, driver, xpath):
        """
            Finds ui element by its xpath
            :param driver: winappdriver instance
            :param identifier: xpath
            :return:element
        """
        try:
            elm = driver.find_element_by_xpath(xpath)
            return elm
        except NoSuchElementException:
            return False

    def element_id_visible(self, driver, id):
        """
            Check if ui element visible by its automationID
            :param driver: winappdriver instance
            :param identifier: automationID
            :return: True/False
        """
        try:
            if (driver.find_element_by_accessibility_id(id).is_displayed()):
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def element_xpath_visible(self, driver, xpath):
        """
            Check if ui element visible by its automationID
            :param driver: winappdriver instance
            :param identifier: automationID
            :return: True/False
        """
        try:
            if (driver.find_element_by_xpath(xpath).is_displayed()):
                return True
            else:
                return False
        except NoSuchElementException:
            return False
    def element_name_visible(self, driver, name):
        """
            Check if ui element visible by its name
            :param driver: winappdriver instance
            :param identifier: name
            :return: True/False
        """
        try:
            if (driver.find_element_by_name(name).is_displayed()):
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def element_classname_visible(self, driver, classname):
        """
            Check if ui element visible by its classname
            :param driver: winappdriver instance
            :param identifier: classname
            :return: True/False
        """
        try:
            if (driver.find_element_by_class_name(classname).is_displayed()):
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def element_id_selected(self, driver, id):
        """
            Check if ui element selected by its automationID
            :param driver: winappdriver instance
            :param identifier: automationID
            :return: True/False
        """
        checked = False
        try:
            elm = self.find_element_by_id(driver, id)
            if (elm.get_attribute('check')):
                checked = True
            else:
                print("checkbox is unchecked")
                checked = False
            return checked
        except NoSuchElementException:
            return False

    def click_element_by_text(self, driver, name):
        """
           click ui element by its name
           :param driver: winappdriver instance
           :param identifier: name
           :return: True/False
       """
        try:
            driver.find_element_by_name(name).click()
            return True
        except NoSuchElementException:
            return False

    def click_element_by_id(self, driver, id):
        """
           click ui element by its automationID
           :param driver: winappdriver instance
           :param identifier: automationID
           :return: True/False
       """
        try:
            if (self.element_id_visible(driver, id)):
                driver.find_element_by_accessibility_id(id).click()
                time.sleep(1)
                return True
            else:
                print("id not visible = " + id)
                return False
        except NoSuchElementException:
            return False

    def click_element_by_classname(self, driver, classname):
        """
           click ui element by its classname
           :param driver: winappdriver instance
           :param identifier: classname
           :return: True/False
       """
        try:
            if (self.element_classname_visible(driver, classname)):
                driver.find_element_by_class_name(classname).click()
                time.sleep(1)
                return True
            else:
                print("classname not visible = " + classname)
                return False
        except NoSuchElementException:
            return False

    def right_click_element(self, driver, element):
        """
           right click ui element
           :param driver: winappdriver instance
           :param identifier: element
           :return: True/False
       """
        driver.actions().click(element, 2).perform()
        time.sleep(1)

    def wait_visible_by_ID(self, driver, id, timeout):
        """
           wait for ui element visible by automationID
           :param driver: winappdriver instance
           :param identifier: automationID
           :param timeout: time out for waiting
           :return: element
       """
        element = None
        try:
            element_present = EC.visibility_of_element_located((By.ID, id))
            element = WebDriverWait(driver, timeout).until(element_present)
            return element
        except TimeoutException:
            print("time out waiting for item visible")
            return None

    def wait_visible_by_Name(self, driver, name, timeout):
        """
           wait for ui element visible by name
           :param driver: winappdriver instance
           :param identifier: name
           :param timeout: time out for waiting
           :return: element
       """
        status = False
        try:
            element = EC.presence_of_element_located((By.NAME, name))
            WebDriverWait(driver, timeout).until(element)
            status = True
            return status
        except TimeoutException:
            print("time out waiting for item visible")
            return False

    def wait_visible_by_ClassName(self, driver, cname, timeout):
        """
           wait for ui element visible by classname
           :param driver: winappdriver instance
           :param identifier: classname
           :param timeout: time out for waiting
           :return: element
        """
        status = False
        try:
            element = EC.presence_of_element_located((By.CLASS_NAME, cname))
            WebDriverWait(driver, timeout).until(element)
            status = True
            return status
        except TimeoutException:
            print("time out waiting for item visible")
            return False

    def start_winappdriver(self):
        try:
            # start win app driver
            #os.popen(global_cfg.winapp_driver).read()
            
            time.sleep(5)
            driver = None
            desired_caps = {}
            desired_caps["app"] = "C:\Program Files (x86)\Toolkit\Toolkit.exe"
            desired_caps["platformName"] = "Windows"
            desired_caps["deviceName"] = "WindowsPC"
            #print("desire cap = " + str(desired_caps))
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723',
                desired_capabilities=desired_caps)
           # print("winapp driver = " + str(driver))
            time.sleep(8)

            return driver
        except:
            return False

    def launch_winappdriver(self):
        try:
            # start win app driver
            # os.popen(global_cfg.winapp_driver).read()

            time.sleep(5)
            driver = None
            desired_caps = {}
            desired_caps["app"] = "C:\Program Files (x86)\Toolkit\Toolkit.exe"
            desired_caps["platformName"] = "Windows"
            desired_caps["deviceName"] = "WindowsPC"
            desired_caps["noReset"] = True
           # print("desire cap = " + str(desired_caps))
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723',
                desired_capabilities=desired_caps)
            #print("launch app driver = " + str(driver))
            time.sleep(8)

            return driver
        except:
            return False
    def launch_app(self):
        status = False
        try:
            cmd = "C:\Program Files (x86)\Toolkit\Toolkit.exe"
            out = os.popen(cmd).read()
            time.sleep(2)
            status = True
            return status
        except:
            return False

    def get_win_handle(self, title):
        handle = None
        try:
            handle = win32gui.FindWindow(0, title)
            #handle = hex(handle).upper()
            handle = hex(handle)
            handleStr = '0x' + handle[2:].zfill(8)
            #print("new format = " + str(handleStr))
            self.handle = handle
            return handle
        except:
            print("Get exception on get win handle")
            return None

    def launch_appium_topLevel(self, handle):
        try:
            # set up top level session
            desired_caps = {}
            desired_caps["appTopLevelWindow"] = handle
            desired_caps["platformName"] = "Windows"
            desired_caps["deviceName"] = "WindowsPC"
            newDriver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723',
                desired_capabilities=desired_caps)
            time.sleep(10)
            return newDriver
        except:
            return False

    def get_web_driver(self, url):
        try:
            time.sleep(3)
            driver = None
            desired_caps = {}
            driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=desired_caps)
            time.sleep(3)
            return driver
        except:
            print("get exception on get web driver")
            return False


