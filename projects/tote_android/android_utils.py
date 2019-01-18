__author__ = 'tammyngo'
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
import datetime as dt
from selenium.common.exceptions import WebDriverException
from core_framework.commons import logger
from core_framework.controller import ui_controller
from projects.tote_android import labels



'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   android_utils
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

class android_utils:
    logger          = None
    uiObject        = None


    def __init__(self):
        self.uiObject = ui_controller.ui_controller()
        pass

    def click_phone_storage(self, driver):
        elm = driver.find_element_by_id(labels.phone_storage)
        phone = elm.find_element_by_id(labels.child_menu_items)
        storages = phone.find_elements_by_xpath("//android.widget.LinearLayout")

        if (len(storages) > 0) :
            device = phone.find_elements_by_xpath("//android.widget.LinearLayout")[1]
            device.click()
        else :
            phone.click()
        print("click device")
        done = True

        time.sleep(2)
        return done

    def click_external_storage(self, driver):
        done = False
        try :
            externalLn = driver.find_element_by_id(labels.external_storage)
            if ( externalLn.is_displayed()):
                externalElm = externalLn.find_element_by_id(labels.child_menu_items)
                if (externalElm.is_displayed()) :
                    externalElm.click()
                    print("click external storage")
                    done = True
                    time.sleep(3)
                else :
                    print("not exist external storaged")
            else:
                print("not existed external link")

        except NoSuchElementException:
            print("Exception on external")
            return False
        return done

    def click_menu_icon(self, driver):
        done = False
        try:
            time.sleep(3)
            menuIcon = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.ImageButton")
            if (menuIcon.is_displayed()):
                menuIcon.click()
                print("click menu icon")
                done = True
                time.sleep(2)
            else:
                print("No menu icon existed")

        except NoSuchElementException:
            print("exception on menu icon")
            return False
        return done

    def navigateToRoot(self, driver):
        done = False
        try :
            tvFolders = driver.find_elements_by_id(labels.tvFolder)
            if ( len(tvFolders) > 0):
                rootFolder = tvFolders[0]

                folderPath = driver.find_element_by_id(labels.folder_path)
                sourceLayout = folderPath.find_element_by_xpath("//android.widget.LinearLayout[@index=0]")

                if ( sourceLayout.is_displayed()) :
                    #sourceLayout = folderPath.find_element_by_xpath("//android.widget.LinearLayout[@index=0]")
                   # folderPath = 'new UiSelector().resourceId(" + labels.folder_path+ ")';
                   # linearLayout = 'new UiSelector().className(\"android.widget.LinearLayout\").index(0)'
                   # sourceLayout = driver.find_element_by_android_uiautomator(folderPath + ".childSelector(" + linearLayout + ")")

                    print("click root link = " + rootFolder.text)
                    sourceLayout.click()
                    done = True
                    time.sleep(3)
                else :
                    print("not exist source layout")
            else:
                print("not exist tvFolder")

        except NoSuchElementException:
            print("Exception on navigate to root")
            return False
        return done

    def click_notification_menu_item(self, driver):
        done = False
        try:
            notifyLn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.TextView[@text='Notifications']/../..")
            if (notifyLn.is_displayed()):
                notifyLn.click()
                print("click Notifications link")
                done = True
                time.sleep(1)
            else:
                print("No Notifications link existed")
        except NoSuchElementException:
            print("exception on Notifications menu")
            return False
        return done

    def verifyNofification(self, driver, action, completed):
        done = False
        try:
            msgList = driver.find_elements_by_id(labels.notify_message)
            timeList = driver.find_elements_by_id(labels.notify_timestamp)
            for i in range(len(msgList)) :
                msg = (msgList[i].text).strip()
                timeS = timeList[i].text
                print("get notification msg = " + msg)
                print("action = " + action + ", completed = " + str(completed))
                if ( action == "Backup" ):
                    if (completed):
                        if ( msg == "Backup Completed!" ) :
                            done = True
                            print("Get correct notification = " + msg + " with timestamp = " + timeS)
                            time.sleep(1)
                        else:
                            print("Get wrong notification = " + msg)
                    else:
                        if ( msg == "Backup failed"):
                            done = True
                            print("Get correct notification = " + msg + " with timestamp = " + timeS)
                            time.sleep(1)
                        else:
                            print("Get wrong notification = " + msg)
                    break

                elif (action == "Restore"):
                    if ( completed ) :
                        if ( msg == "Restore Completed!" ) :
                            done = True
                            print("Get correct notification = " + msg + " with timestamp = " + timeS)
                            time.sleep(1)
                            break
                        else:
                            print("Get wrong notification = " + msg)
                    else:
                        print("msg in restore = " + msg)
                        if ( msg == "Restore failed"):
                            done = True
                            print("Get correct notification = " + msg + " with timestamp = " + timeS)
                            time.sleep(1)
                        else:
                            print("Get wrong notification = " + msg)
                    break

                time.sleep(1)
                self.click_navigate_up(driver)
                time.sleep(1)

        except NoSuchElementException:
            print("exception on verify Notifications")
            return False
        return done

    def click_Settings_menu_item(self, driver):
        done = False
        try:
            time.sleep(1)
            settingOpt = self.uiObject.find_element_by_id(labels.settings_option, driver)
            if ( settingOpt.is_displayed()) :
                settingOpt.click()
                print("click on Settings menu item")
                done = True
            else:
                print("No Settings link existed")

        except NoSuchElementException:
            print("exception on Settings menu")
            return False
        return done

    def click_Report_problem(self, driver, sendTo, confirm):
        done = False
        try:
            time.sleep(1)
            for i in range(2) :
                self.scrollForward(driver, labels.settings_recycler)


            reportLnk = self.uiObject.find_element_by_its_xpath(driver,
                                                               "//android.widget.TextView[@text='Report a problem']/../..")
            if (reportLnk.is_displayed()):
                reportLnk.click()
                print("click on Report a problem")
                time.sleep(3)
                self.scrollBackward(driver, labels.compose)
                time.sleep(1)

                fromElm = self.uiObject.find_element_by_id(labels.from_act_name, driver)
                toElm = self.uiObject.find_element_by_id(labels.to_name, driver)
                print("get email from = " + fromElm.text)
                print("send email to = " + toElm.text)
                subjectElm = self.uiObject.find_element_by_id(labels.subject, driver)
                print("get subject title = " + subjectElm.text)
                if ( toElm.text != sendTo ) :
                    toElm.click()
                    toElm.clear()
                    self.uiObject.input_text_in_element(toElm, sendTo, driver)
                    print("input to new recepient = " + sendTo)
                    time.sleep(1)

                if ( confirm ) :
                    sendTxt = self.uiObject.find_element_by_its_xpath(driver,
                                                                            "//android.widget.TextView[@content-desc='Send']")
                    if (sendTxt.is_displayed()):
                        sendTxt.click()
                        print("Click Send to send email")
                        time.sleep(5)
                        done = True
                    else:
                        print("Send not existed")

                self.click_navigate_up(driver)
                time.sleep(1)
                self.click_navigate_up(driver)
                time.sleep(1)
            else:
                print("No Report a problem link existed")

        except NoSuchElementException:
            print("exception on Report a problem")
            return False
        return done

    def click_restore_menu_item(self, driver):
        done = False
        try:
            time.sleep(1)
            restoreLn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.TextView[@text='Restore']/../..")
            if (restoreLn.is_displayed()):
                restoreLn.click()
                print("click Restore link")
                done = True
                time.sleep(1)
            else:
                print("No Restore link existed")

        except NoSuchElementException:
            print("exception on restore menu")
            return False
        return done

    def click_restore_now(self, driver, deviceName):
        done = False
        try:
            found = False
            selectedDevice = driver.find_element_by_id(labels.selected_folder)
            if ( selectedDevice.is_displayed()) :
                print("selected device = " + selectedDevice.text)

            if ( len(deviceName) == 0 ) :
                restoreNow = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='RESTORE NOW']")
                if ( restoreNow.is_displayed()):
                    restoreNow.click()
                    print("click RESTORE NOW")
                    done = True
                    time.sleep(5)
                    title = driver.find_element_by_id(labels.txt_view_title)
                    msg = driver.find_element_by_id(labels.txt_view_msg)
                    if ( msg.is_displayed()) :
                        print("get title = " + title.text + ", msg = " + msg.text)
                        okBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='OK']")
                        if ( okBtn.is_displayed()):
                            okBtn.click()
                            print("click Ok button")
                            time.sleep(2)

            else:
                folderName = driver.find_element_by_id(labels.folder_name)
                txtDevice = folderName.text
                if ( txtDevice.find(deviceName)) :
                    parent = driver.find_element_by_xpath("//android.widget.TextView[@text='" +
                                txtDevice + "']/..")
                    if ( parent.is_displayed()):
                        parent.click()
                        print("click on device = " + txtDevice)
                        time.sleep(2)
                        viewMsg = driver.find_element_by_xpath("//android.widget.TextView[contains(@resource-id,'" +
                                labels.txt_view_msg + "')]")
                        if ( viewMsg.is_displayed()) :
                            print("get view msg = " + viewMsg.text)
                            yesBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='YES']")
                            if ( yesBtn.is_displayed()):
                                yesBtn.click()
                                print("click Yes to agree")
                                time.sleep(2)
                            else:
                                print("no Yes btn existed")
                        else:
                            print("view msg not existed")
                    else:
                        print("device parent not existed")
                else:
                    print("device name not existed in list")

            self.click_navigate_up(driver)
            time.sleep(1)
            optType = self.uiObject.find_element_by_id(labels.operation_type, driver)
            optAct = self.uiObject.find_element_by_id(labels.operation_action, driver)
            self.uiObject.wait_for_element_from_id(driver, labels.operation_action)
            if ( optAct.is_displayed()) :
                print("get operation type = " + optType.text)
                print("click on operation = " + optAct.text)
                optAct.click()
                time.sleep(2)
            else:
                print("no operation action displayed")

        except NoSuchElementException:
            print("exception in restore now")
            return False

        return done

    def click_backup_menu_item(self, driver):
        done = False
        try:
            backupLn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.TextView[@text='Backup']/../..")
            if (backupLn.is_displayed()):
                backupLn.click()
                print("click backup link")
                done = True
                time.sleep(1)
                allowBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='ALLOW']")
                if ( allowBtn.is_displayed()):
                    allowBtn.click()
                    print("click Allow btn")
                    time.sleep(2)
            else:
                print("No backup link existed")

        except NoSuchElementException:
            print("exception on backup menu")
            return False
        return done

    def click_backup_now(self, driver, listSelected, confirm):
        done = False
        try:
            found = False
            backupNames = driver.find_elements_by_id(labels.backupName)
            checkboxes = driver.find_elements_by_id(labels.checkbox)
            backupNow = self.uiObject.find_element_by_id(labels.backupNow, driver)
            for i in range(len(backupNames)):
                checked = checkboxes[i].get_attribute("checked")
                for j in range(len(listSelected)) :
                    if ( found ) :
                       found = False

                    if ( backupNames[i].text == listSelected[j]) :
                       found = True
                       if ( checked == False ):
                            checkboxes[i].click()
                            time.sleep(1)
                            print("click on selected backup = " + backupNames[i])
                       else:
                            print("get selected backup = " + listSelected[j])
                            break
                    else:

                        if ( (checked) and (not found) ):
                            if ( backupNames[i].text != listSelected[j] ) :
                                if ( backupNames[i].text != "SD Card") :
                                    checkboxes[i].click()
                                    print("click to unselect checkedbox = " + backupNames[i].text)
                                    time.sleep(2)
                            break
                if ( found ) :
                    break

            if ( not found ) :
                print("fail to get selected backup names")
            else:
                if ( confirm ) :
                    if (backupNow.is_displayed() ) :
                        backupNow.click()
                        print ("click backup now")
                        time.sleep(2)

                        while self.uiObject.is_path_not_visible(driver, "//*[@text='Back Up Now']", 2 ):
                            time.sleep(5)
                        done = True
                        self.click_navigate_up(driver)
                        print("click navigate up")
                        time.sleep(2)
                        optType = self.uiObject.find_element_by_id(labels.operation_type, driver)
                        optAct = self.uiObject.find_element_by_id(labels.operation_action, driver)
                        self.uiObject.wait_for_element_from_id(driver, labels.operation_action)

                        if (optAct.is_displayed()):
                            print("click operation action = " + optAct.text)
                            optAct.click()
                            time.sleep(1)
                        else:
                            print("no operation type existed")

                else:
                    cancelBtn = self.uiObject.find_element_by_its_xpath(driver,
                                                                        "//android.widget.TextView[@text='CANCEL']")
                    cancelBtn.click()
                    print("click cancel backup")

        except NoSuchElementException:
            print("exception")
            return False

        return done

    def verifyBackup(self, driver, listSelected):
        done = False
        try:
            firstFolder = ""
            if (self.click_menu_icon(driver)):
                if (self.click_external_storage(driver)):
                    if ( self.openFolder(driver, "Backup")) :
                        if (params.device_name.startswith("SAMSUNG")):
                            deviceName = "samsung " + params.device_name
                        else:
                            deviceName = params.device_name

                        if (self.openFolder(driver, deviceName)):
                            print("open folder in device name = " + deviceName)
                            time.sleep(1)
                            if ( self.openFolder(driver, "Phone")):
                                if ( len(listSelected) > 0 ):
                                    firstFolder = listSelected[0]

                                    if (self.openFolder(driver, firstFolder.upper())):
                                        print("get open folder = " + firstFolder)
                                        time.sleep(3)
                                        done = True
                                    else:
                                        print("fail to open selected backup folder")
                            self.click_navigate_up(driver)
                            self.navigateToRoot(driver)
                        else:
                            print ("fail to open device name")
                    else:
                        print("Fail to open Backup folder")
                else:
                    print("Fail to open external storage")
                time.sleep(2)

        except NoSuchElementException:
            print("exception")
            return False

        return done

    def create_folder(self, driver, folderName, cancel):
        done = False

        createFolder = driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Create New Folder']")
        if ( createFolder.is_displayed()) :
            createFolder.click()
            time.sleep(1)
            newFolderEdit = self.uiObject.find_element_by_its_class_name(driver, "android.widget.EditText")
            if ( newFolderEdit.is_displayed()) :
                self.uiObject.clear_text_from_element(newFolderEdit)
                self.uiObject.input_text_in_element(newFolderEdit, folderName, driver)
                time.sleep(2)

                if ( cancel ) :
                    cancelBtn = driver.find_element_by_xpath("//android.widget.Button[@text='CANCEL']");
                    if ( cancelBtn.is_displayed()) :
                        cancelBtn.click()
                        done = True
                        print ("click cancel btn")
                    else :
                        done = False
                        print("Cancel not existed")
                else :
                    createBtn = driver.find_element_by_xpath("//android.widget.Button[@text='CREATE']");
                    if (createBtn.is_displayed()):
                        createBtn.click()
                        print ("click create btn")
                        time.sleep(1)

                        toolbar = self.uiObject.find_element_by_id(labels.toolbar, driver)
                        if ( toolbar.is_displayed()) :
                            titleElm = toolbar.find_element_by_class_name("android.widget.TextView")
                            if ( titleElm.text == folderName ) :
                                done = True
                                print("get correct folder name")
                            else :
                                print("get wrong folder name")
                        self.click_navigate_up(driver)

        else :
            done = False
            print("create folder not existed")
        return done

    def click_copy_option(self, driver, itemName, destination, confirm):
        done = False

        try:
            if (self.open_folder_option(driver, itemName)):
                time.sleep(1)
                if (self.click_more_option(driver, itemName, "action_copy")):
                    if ( self.openFolder(driver, destination)) :
                        if (confirm):
                            time.sleep(1)
                            copyBtn = self.uiObject.find_element_by_its_xpath(driver,"//android.widget.Button[@text='COPY HERE']")
                            if ( copyBtn.is_displayed()):
                                copyBtn.click()
                                time.sleep(2)
                                print("click copy button")

                                optType = self.uiObject.find_element_by_id(labels.operation_type, driver)
                                optAct = self.uiObject.find_element_by_id(labels.operation_action, driver)
                                self.uiObject.wait_for_element_from_id(driver, labels.operation_action)

                                print("get operation type = " + optType.text)
                                time.sleep(10)
                                if (optAct.is_displayed()):
                                    print("click operation action = " + optAct.text)
                                    optAct.click()
                                    time.sleep(1)
                                    if (self.verify_item_existed(driver, itemName)):
                                        print("verified copy item = " + itemName)
                                        done = True
                                    else:
                                        print ("fail to copy item = " + itemName)
                                else:
                                    print("operation action not existed")

                                time.sleep(3)
                                self.click_navigate_up(driver)
                                time.sleep(2)
                        else:
                            cancelBtn = self.uiObject.find_element_by_its_xpath(driver,
                                                                                "//android.widget.TextView[@text='CANCEL']")
                            if (cancelBtn.is_displayed()):
                                cancelBtn.click()
                                print("click cancel btn")
                                done = True
                                time.sleep(1)
                            else:
                                print("cancel btn not existed")
                time.sleep(2)

        except NoSuchElementException:
            print("exception")
            return False

        return done

    def click_delete_option(self, driver, itemName, cancel):
        done = False

        if ( self.open_folder_option(driver, itemName)) :
            time.sleep(1)
            if ( self.click_more_option(driver, itemName, "action_delete")) :
                txtMsg = self.uiObject.find_element_by_id(labels.txt_message, driver)
                print("get text msg = " + txtMsg.text)
                if (cancel == False) :
                    deleteBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='DELETE']")
                    deleteBtn.click()
                    time.sleep(2)
                    print("click delete button")
                    optType = self.uiObject.find_element_by_id(labels.operation_type, driver)
                    optAct = self.uiObject.find_element_by_id(labels.operation_action, driver)
                    self.uiObject.wait_for_element_from_id(driver, labels.operation_action)
                    print("get operation type = " + optType.text)
                    time.sleep(3)
                    if ( optAct.is_displayed()) :
                        print("click operation action = " + optAct.text)
                        optAct.click()
                        time.sleep(1)
                        if ( self.verify_item_not_existed(driver, itemName) ) :
                            print("verified delete item = " + itemName)
                            done = True
                        else :
                            print ("fail to delete item = " + itemName)
                    else :
                        print("operation action not existed")

                else :
                    cancelBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.TextView[@text='CANCEL']")
                    if ( cancelBtn.is_displayed()) :
                        cancelBtn.click()
                        print("click cancel btn")
                        done = True
                        time.sleep(1)
                    else :
                        print("cancel btn not existed")

            time.sleep(2)
        return done

    def click_rename_option(self, driver, itemName, newName, confirm):
        done = False

        try:
            if ( self.open_folder_option(driver, itemName)) :
                time.sleep(1)
                if ( self.click_more_option(driver, itemName, "action_rename")) :
                    editTxt = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.EditText")
                    if ( editTxt.is_displayed()):
                        editTxt.clear()
                        self.uiObject.input_text_in_element(editTxt, newName, driver)
                        time.sleep(1)
                        print("set new name to = " + newName)
                        if (confirm) :
                            renameBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='RENAME']")
                            if ( renameBtn.is_displayed()):
                                renameBtn.click()
                                time.sleep(2)
                                print("click Rename button")
                                if ( self.verify_item_existed(driver, newName) ) :
                                    print("verified new item = " + newName +  " existed")
                                    done = True
                                else :
                                    print ("fail to rename item = " + newName)
                        else :
                            cancelBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='CANCEL']")
                            if ( cancelBtn.is_displayed()) :
                                cancelBtn.click()
                                print("click cancel btn")
                                done = True
                                time.sleep(1)
                            else :
                                print("cancel btn not existed")
                else:
                    print("fail to get Rename option")
            else:
                print("fail to open folder option = " + itemName)

        except NoSuchElementException:
            print("exception")
            return False

        return done

    def click_more_option(self, driver, itemName, action):
        done = False
        print("selected filename = " + labels.selected_file)
        selectedItem = self.uiObject.find_element_by_id(labels.selected_file, driver)
        print ("selected item = " + selectedItem.text)
        if (selectedItem.text == itemName) :
            print("get correct selected item title")
            if ( action == "action_delete") :
                action = labels.action_delete
            elif (action == "action_move") :
                action = labels.action_move
            elif (action == "action_copy") :
                action = labels.action_copy
            elif (action == "action_rename"):
                action = labels.action_rename
            elif (action == "action_duplicate") :
                action = labels.action_duplicate

            actionOpt = self.uiObject.find_element_by_id(action, driver)
            if ( actionOpt.is_displayed()) :
                actionOpt.click()
                done = True
                print("click action = " + action)
                time.sleep(1)
            else :
                print("action option not existed")
        return done

    def verify_item_not_existed(self, driver, itemName):
        status = False
        found = False
        count = 0
        folderList = self.uiObject.find_element_by_id(labels.folderList, driver)
        txtNames = self.uiObject.find_elements_by_id(labels.txt_name, driver)

        if ( folderList.is_displayed()) :
            while ( not(found)  and count < 1) :
                for  txtName in txtNames :
                    if ( txtName.text == itemName ) :
                        found = True
                        break

                if( not(found)) :
                    self.uiObject.scroll_to_find(driver, itemName)
                    count = count+1

            if (not (found)):
                status = True
                print ("Success not to find item = " + itemName)
                self.uiObject.scroll_up_screen_android(driver)
        else :
            print ("folder list view not existed")

        return status

    def verify_item_existed(self, driver, itemName):
        status = False
        found = False
        count = 0
        folderList = self.uiObject.find_element_by_id(labels.folderList, driver)
        txtNames = self.uiObject.find_elements_by_id(labels.txt_name, driver)

        if (folderList.is_displayed()) :
            while ( not(found)  and count < 3) :
                for  txtName in txtNames :
                    if ( txtName.text == itemName ) :
                        found = True
                        status = True
                        print("found item = " + itemName)
                        break

                if( not(found)) :
                    self.uiObject.scroll_to_find(driver, itemName)
                    count = count+1

            if (not (found)):
                print ("Fail not to find item = " + itemName)

            self.scrollBackward(driver, labels.folderList)

        else :
            print ("folder list view not existed")

        return status

    def click_source_folder(self, driver):
        done = False
        folderPath = self.uiObject.find_element_by_id(labels.folder_path, driver)
        sourceLayout = folderPath.find_element_by_xpath("//android.widget.LinearLayout[0]")

        if (sourceLayout.is_displayed()) :
            sourceLayout.click()
            print( "go back to source folder")
            done = True
            time.sleep(2)
        return done

    def openTab(self, driver, actionID):

        done = False
        id = ""
        if ( actionID == "action_documents"):
            id = labels.action_documents
        elif (actionID == "action_music"):
            id = labels.action_music
        elif (actionID == "action_gallery"):
            id = labels.action_gallery
        elif (actionID == "action_folders"):
            id = labels.action_folders

        tabSel = self.uiObject.find_element_by_id(id, driver)
        if (tabSel.is_displayed()) :
            tabText = tabSel.find_element_by_xpath(".//android.widget.TextView")
            tabSel.click()
            print( "click on tab = " + tabText.text)
            done = True
            time.sleep(5)
        return done

    def openFolder(self, driver, folderName):

        done = False
        try :
            if ( len(folderName) == 0 ) :
                return False

            time.sleep(1)
            count = 0
            found = False;
            folderList = self.uiObject.find_element_by_id(labels.folderList, driver)

            if ( folderList.is_displayed()) :
                roots = driver.find_elements_by_id(labels.root)
                listNames = driver.find_elements_by_id(labels.txt_name)
                while count < 3 and not done :
                    for i in range(len(listNames)):
                        nameElm = listNames[i]
                        if ( nameElm.text == folderName ):
                            root = roots[i]
                            root.click()
                            print("click to open folder = " + folderName)
                            found = True
                            done = True
                            break

                    if ( not found ) :
                        found = self.uiObject.scroll_to_find(driver, folderName)
                    count = count+1

                if ( not found):
                     print("Fail to find folder = " + folderName)
            else:
                print("folderList not displayed")

        except NoSuchElementException:
            print ("Exception")
            return False
        return done

    def openPhotoAtIndex(self, driver, index):

        done = False
        recycler = driver.find_element_by_id(labels.recycler)
        if ( recycler.is_displayed()) :
            frameView = recycler.find_element_by_xpath("//android.widget.FrameLayout[" + index + "]")
            view = frameView.find_element_by_xpath("//android.view.View")
            if (view.is_displayed()) :
                view.click()
                print("click photo at index = " + str(index))
                done = True
                time.sleep(2)
            else :
                print("view not displayed")
        else:
            print("recycler not displayed")

        if ( done ) :
            self.click_navigate_up(driver)

        return done

    def scrollForward(self, driver, listID):
        try:
            selector = "new UiScrollable(new UiSelector()" + ".resourceId(\"" + listID + "\"))." + "scrollForward()"
            elm = driver.find_element_by_android_uiautomator(selector)
            return elem

        except NoSuchElementException:
            return False



    def scrollBackward(self, driver, listID):
        try:
            selector = "new UiScrollable(new UiSelector()" + ".resourceId(\"" + listID + "\"))." + "scrollBackward()"
            elm = driver.find_element_by_android_uiautomator(selector)
            time.sleep(1)
            return elm

        except NoSuchElementException:
            return False

    def sortBy(self, driver, sortByTxt, orderByTxt):

        done = False
        moreOpt = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.ImageView[@content-desc='More options']")
        if ( moreOpt.is_displayed()) :
            moreOpt.click()
            print("click on more option button")
            time.sleep(1)
            sortBy = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.TextView[@text='Sort']")
            sortBy.click()
            print("click Sort")
            time.sleep(1)

            listChecked = driver.find_elements_by_class_name("android.widget.CheckedTextView")
            for  item in listChecked :
                if ( item.text ==  sortByTxt ) :
                    item.click()
                    print("click sort by = " + sortByTxt)
                    time.sleep(2)
                    break

            orderBtn = self.uiObject.find_element_by_its_xpath(driver, "//android.widget.Button[@text='" + orderByTxt + "']")
            if ( orderBtn.is_displayed()) :
                orderBtn.click()
                print("click order by = " + orderByTxt)
                time.sleep(2)
            else:
                print("not display order by btn")

            if (self.verifySortBy(driver, sortByTxt, orderByTxt)) :
                done = True
                print("success verified sort")
            else:
                print("fail verified sort")

        else:
            print("more options not displayed")


        return done

    def verifySortBy(self, driver, sortBy, orderBy):

        done = False
        folderList = self.uiObject.find_element_by_id(labels.folderList, driver)
        if ( folderList.is_displayed()) :
            count = 0
            listDates = []
            listNames = []

            while (count < 6) :

                txtNames = self.uiObject.find_elements_by_id(labels.txt_name, driver)
                txtDates = self.uiObject.find_elements_by_id(labels.txt_date, driver)

                if ( len(txtNames) == len(txtDates) ) :
                    for i in range(len(txtNames)) :
                        txtName = txtNames[i].text
                        txtDate = txtDates[i].text
                        if ( sortBy == "Name") :
                            if (listNames.count(txtName) == 0):
                                listNames.append(txtName)

                        elif (sortBy == "Date Modified") :
                            listDates.append(txtDate)

                self.scrollForward(driver, labels.folderList)
                time.sleep(1)
                count = count+1

            if ( len(listNames) > 0) :
                print(listNames)

            if ( len(listDates) > 0 ):
                for x in range(len(listDates)):
                    print (listDates[x])


            if ( len(listNames) != 0 or len(listDates) != 0 ) :
                if ( sortBy == "Name" ) :
                    if ( orderBy == "ASCENDING") :
                        if ( self.checkAscendingOrder(listNames)) :
                            print("success to get names sort by = " + sortBy + ", order by = " + orderBy)
                            done = True
                        else:
                            print("fail to get names sort by = " + sortBy + ", order by = " + orderBy)
                    else:
                        if ( self.checkDescendingOrder(listNames)):
                            print("success to get names sort by = " + sortBy + ", order by = " + orderBy)
                            done = True
                        else:
                            print("fail to get names sort by = " + sortBy + ", order by = " + orderBy)
                elif ( sortBy == "Date Modified") :
                    if (orderBy == "ASCENDING"):
                        if ( self.checkDateAscendingOrder(listDates)):
                            print("success to get dates sort by = " + sortBy + ", order by = " + orderBy)
                            done = True
                        else:
                            print("fail to get dates sort by = " + sortBy + ", order by = " + orderBy)
                    else:
                        if ( self.checkDateDescendingOrder(listDates)):
                            print("success to get dates sort by = " + sortBy + ", order by = " + orderBy)
                            done = True
                        else:
                            print("fail to get dates sort by = " + sortBy + ", order by = " + orderBy)

            else:
                print("not display names and dates")

            for x in range(6):
                self.scrollBackward(driver, labels.folderList)
                time.sleep(1)

        return done


    def checkAscendingOrder(self, listNames):

        listTmp = listNames[:]
        listTmp.sort()
        print("list ascending using sort")
        print(listTmp)

        if ( listTmp == listNames ):
            return True

    def checkDescendingOrder(self, listNames):

        listTmp = listNames[:]
        listTmp.sort(reverse=True)
        print("list descending using sort")
        print(listTmp)
        if ( listTmp == listNames) :
            return True
        else:
            return False
        """
        i = 1
        while i < len(listNames):
            if (listNames[i] > listNames[i - 1]):
               
                return False
            i += 1
        return True
        """

    def checkDateDescendingOrder(self, listDates):

        try:
            previous = ""
            current = ""
            i = 0
            for dateStr in listDates :
                current = dateStr
                if ( i == 0 ) :
                    previous = current
                    print("previous = " + previous + ", current = " + current)

                datePrev = dt.datetime.strptime(previous, '%m-%d-%Y, %I-%M %p')
                dateCur = dt.datetime.strptime(current, '%m-%d-%Y, %I-%M %p')
                print("date current = " + dateCur)

                if ( dateCur > datePrev ) :
                    return False

                previous = current

        except:
            return False

        return True

    def checkDateAscendingOrder(self, listDates):

        try:
            previous = ""
            current = ""
            i = 0
            for dateStr in listDates :
                current = dateStr
                if ( i == 0 ) :
                    previous = current
                    print("previous = " + previous + ", current = " + current)

                datePrev = dt.datetime.strptime(previous, '%m-%d-%Y, %I-%M %p')
                dateCur = dt.datetime.strptime(current, '%m-%d-%Y, %I-%M %p')
                print("date current = " + dateCur)

                if ( dateCur < datePrev ) :
                    return False

                previous = current

        except:
            return False

        return True

    def open_folder_option(self, driver, itemName):
        done = False
        found = False
        self.uiObject.wait_till_element_is_visible(driver, global_cfg.by_id, labels.folderList)


        count = 0

        while (count < 5) :
            txtNames = self.uiObject.find_elements_by_id(labels.txt_name, driver)
            btnOptions = self.uiObject.find_elements_by_id(labels.options_btn, driver)

            for i in range(len(txtNames)) :
                if (txtNames[i].text == itemName) :
                    btnOption = btnOptions[i]
                    btnOption.click()
                    print("click button option")
                    done = True
                    found = True
                    break

            if ( not found ) :
                self.uiObject.scroll_to_find(driver, itemName)
                time.sleep(3)
                count = count + 1
            else :
                break

        if (not found ):
            print("Fail to find item = " + itemName)

        return done

    def click_navigate_up(self, driver):
        done = False
        navUp = driver.find_element_by_xpath("//android.widget.ImageButton[@content-desc='Navigate up']")
        if ( navUp.is_displayed()) :
            navUp.click()
            done = True
            time.sleep(2)
        else :
            print("navigate up not existed")

        return done