'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   modules_base_controller
#
# Purpose:      Facilitates methods common for all modules tests
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

from cryptography.fernet import Fernet
from appium import webdriver
from core_framework.config import global_cfg, params
import json,requests,re,os,base64
from projects.optimus_win.config import project_params, msgs
import time,glob, subprocess, sys, shutil
#from core_framework.controller import win_ui_Controller
from core_framework.commons import utils
from core_framework import core_lib
import pywinauto, win32gui
from subprocess import run
import ctypes
import time, warnings
import zipfile, hashlib, json, pprint
import pyautogui
import pytesseract
from PIL import Image
from pytesseract import Output
from ahk import AHK
from ahk.window import Window
from pywinauto.application import Application
from pywinauto import timings
from xml.etree import cElementTree as ET
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from projects.optimus_win.config import op_params as op_params
from core_framework.controller import test_mgm_con
from core_framework.config import params



class projects_base_controller:
    testmgmObj      = None

    def __init__(self):

        self.testmgmObj = test_mgm_con.controller(params.jiraServer, params.jiraUserName, params.jiraPassword)

    def download_op(self):
        try:
            url = ""
            if (op_params.build_version == ""):
                url = op_params.latest_loc
            else:
                url = op_params.op_loc + op_params.build_version
            # print("url = " + str(url))
                op_params.op_url_version = url
            self.get_app_exe(url)

        except:
            print("get exception on download op")

    def get_app_exe(self, url):
        status = False
        try:
            homedir = os.path.expanduser("~")
            app_install_folder = homedir + "\\Downloads\\"
            resp = requests.get(url)
            http_encode = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
            html_encode = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
            encode = html_encode or http_encode
            soup = BeautifulSoup(resp.content, from_encoding=encode, features="html.parser")
            exe_file = ""
            for link in soup.find_all('a', href=True):
                if (link.get('href').find("Optimus") != -1 or
                    link.get('href').find("Lyve_Pilot_SC") != -1):
                    exe_file = link.get('href')
                    break
            url = url + exe_file
            print("exe file = " + exe_file)
            version = exe_file.split('-')[1]
            version = version[0:7]

            op_params.file_version = version
            print("version = " + op_params.file_version)
            op_params.op_installer_file = app_install_folder + exe_file
            # print("install file = " + params.op_installer_file)
            # print("url = " + str(url))
            if (not os.path.isfile(op_params.op_installer_file)):
                cmd_dld = "curl.exe {} -o {}".format(url, app_install_folder +
                                                     exe_file)
                print(cmd_dld)
                out = os.popen(cmd_dld).read()
                print(out)
                print("Please wait downloading exe file.......")
                time.sleep(5)
                if (os.path.isfile(op_params.op_installer_file)):
                    # print("installer file existed = " + params.op_installer_file)
                    status = True
            else:
                print("install file already existed = " + op_params.op_installer_file)
                status = True
            return status
        except:
            raise ValueError("cannot get app exe")

    def install_op(self):
        try:
            if ( op_params.op_installer_file == ""):
                op_params.op_installer_file = op_params.app_file
            if (os.path.isfile(op_params.op_installer_file)):
                warnings.simplefilter('ignore', category=UserWarning)
                appInstall = Application().start(op_params.op_installer_file)

                dlg = appInstall.window(title_re="Lyve Pilot SC Setup", class_name="#32770")
                # appInstall.dlg.print_control_identifiers()
                time.sleep(2)
                appInstall.dlg.Next.click_input()
                print("click Next on Install")
                time.sleep(1)
                appInstall.dlg.Install.click_input()
                print("click Install")
                time.sleep(40)
                #chbox = appInstall.dlg.CheckBox
                #chbox.click_input()
                #appInstall.dlg.print_control_identifiers()
                appInstall.dlg.Finish.click_input()
                #print("click Finish")
                time.sleep(10)
            else:
                print("fail to get install file = " + op_params.op_installer_file)

        except:
            print("get exception on install op")

    def uninstall_optimus(self):
        try:
            found = False
            warnings.simplefilter('ignore', category=UserWarning)
            Application(backend='uia').start('explorer')
            time.sleep(1)
            timings.Timings.slow()
            explorer = Application().connect(path='explorer.exe')
            time.sleep(1)
            NewWindow = explorer.window(top_level_only=True, active_only=True,
                                        class_name='CabinetWClass')
            time.sleep(3)
            NewWindow.AddressBandRoot.click_input()
            NewWindow.type_keys(r'Control Panel\Programs\Programs and Features{ENTER}', with_spaces=True,
                                set_foreground=False)
            timings.Timings.slow()
            time.sleep(10)
            ProgramsAndFeatures = explorer.window(top_level_only=True, active_only=True, title='Programs and Features',
                                                  class_name='CabinetWClass')
            timings.Timings.slow()
            time.sleep(8)
            appInstall = ProgramsAndFeatures.FolderView.texts()[1:]
            programs_list = ','.join(appInstall)
            listApp = programs_list.split(',')

            app_name = ""
            for el in listApp:
                if (el.find("Optimus") != -1 or
                    el.find("Lyve Pilot SC") != -1):
                    app_name = el
                    found = True
                    break
            if (found):
                item_op = ProgramsAndFeatures.FolderView.get_item(app_name)
                item_op.ensure_visible()
                item_op.click_input(button='right', where='icon')
                time.sleep(3)
                explorer.PopupMenu.wait('ready').menu().get_menu_path('Uninstall')[0].click_input()

                time.sleep(6)
                app = Application(backend='uia').connect(title='Lyve Pilot SC Uninstall')
                time.sleep(5)
                app.LyvePilotSC.Next.click_input()
                print("click Next on Uninstall")
                time.sleep(15)
                app.LyvePilotSC.Finish.click_input()
                print("click Finish uninstall")
                time.sleep(2)
            else:
                print("cannot find app = " + app_name)

            ProgramsAndFeatures.close()
            appPath = r"C:\Users\534026\AppData\Roaming\Lyve Pilot SC"
            if (os.path.isdir(appPath)):
                print("path is dir = " + appPath)
                shutil.rmtree(appPath, ignore_errors=True)
            time.sleep(3)
        except:
            print("get exception on uninstall Op")


    def update_test_info(self,testName, bresult, msgs, b_crashed, jira_feature):
        status_info = {}
        status = "Fail"
        if(bresult):
            status = "Pass"
        if(b_crashed):
            crash_log = "http://10.239.189.161/" + global_cfg.crash_log["fname"]
            status_info["crash_log"] = crash_log

        status_info["status"] = status
        status_info["msgs"] = msgs
        test_info_dict = {"TestName": testName, "%s" % str(params.device_list) : status_info, "Product Feature" : "%s" %jira_feature}
        global_cfg.test_results_list.append(test_info_dict)

    def update_run_info_in_xray(self):
        try:
            test_plan_id = self.testmgmObj.check_if_issue_exists(params.test_plan_name, "Test Plan")
            print("test plan id = " + str(test_plan_id))
            if(test_plan_id):
                global_cfg.ids["test_plan_id"] = test_plan_id
            else:
                global_cfg.ids["test_plan_id"] = self.testmgmObj.add_testPlan(params.test_plan_name, params.test_plan_name,global_cfg.def_jira_proj)

            test_set_id = self.testmgmObj.check_if_issue_exists(params.test_set_name, "Test Set")
            print("test set id = " + str(test_set_id))
            if(test_set_id):
                global_cfg.ids["test_set_id"] = test_set_id
            else:
                global_cfg.ids["test_set_id"] = self.testmgmObj.add_testSet(params.test_set_name, params.test_set_name, global_cfg.def_jira_proj)

            set_name = params.test_set_name + str(global_cfg.build_in_test['build'])
            test_exec_id = self.testmgmObj.check_if_issue_exists(params.test_set_name, "Test Execution")
            print("test exec id = " + str(test_exec_id))
            if(test_exec_id):
                global_cfg.ids["test_exec_id"] = test_exec_id
            else:
                global_cfg.ids["test_exec_id"] = self.testmgmObj.add_testExecution(params.test_exec_name, params.test_exec_name, global_cfg.def_jira_proj)
            return True
        except:
            print("Failed updating test plan , test set or test execution info...")
            return False

    def update_test_in_xray(self,summary,desc, bresult,dest_link_id):
        try:
            status = ""
            if(bresult):
                status = "PASS"
            else:
                status = "FAIL"

            test_id = self.testmgmObj.check_if_issue_exists(summary, "Test")
            print("test_id = " + str(test_id))
            if(not test_id):
                global_cfg.ids["test_id"] = self.testmgmObj.add_test(summary,desc, global_cfg.def_jira_proj)
                print("Test added with ID {}".format(global_cfg.ids["test_id"]))
            else:
                global_cfg.ids["test_id"] = test_id
                print("Test with ID {} exists".format(global_cfg.ids["test_id"]))

            self.testmgmObj.associate_test_to_testSet(global_cfg.ids["test_id"],global_cfg.ids["test_set_id"])
            self.testmgmObj.associate_test_to_testPlan(global_cfg.ids["test_id"],global_cfg.ids["test_plan_id"])

            self.testmgmObj.associate_test_to_testExecution(global_cfg.ids["test_id"],global_cfg.ids["test_exec_id"])
            self.testmgmObj.update_test_execution(global_cfg.ids["test_exec_id"],params.OS,global_cfg.build_in_test['build'])
            self.testmgmObj.associate_test_exec_to_testPlan(global_cfg.ids["test_exec_id"],global_cfg.ids["test_plan_id"])
            run_id = self.testmgmObj.get_test_run_id(global_cfg.ids["test_exec_id"], global_cfg.ids["test_id"])
            print("Current Test Run ID is {}".format(run_id))
            print(self.testmgmObj.update_test_run_status(run_id,status,params.jiraUserName))
            if(dest_link_id):
                self.testmgmObj.link_test_to_product_task(global_cfg.ids["test_id"],dest_link_id)

            return True
        except:
            print("Failed updating test info...")
            return False










































