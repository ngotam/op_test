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
import pyuac
from pyuac import runAsAdmin, isUserAdmin
import pytesseract
from PIL import Image
from pytesseract import Output
from ahk import AHK
from ahk.window import Window
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto import timings
from pywinauto import mouse, keyboard
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
                    link.get('href').find("Lyve_Client") != -1):
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
            print("op installer file = " + str(op_params.op_installer_file))
            time.sleep(1)
            if (os.path.isfile(op_params.op_installer_file)):
                warnings.simplefilter('ignore', category=UserWarning)
                appInstall = Application().start(op_params.op_installer_file)
                time.sleep(2)
                dlg = appInstall.window(title_re="Lyve Client Setup", class_name="#32770")
                time.sleep(3)
                appInstall.dlg.Install.click_input()
                print("click Install")
                time.sleep(20)
                appInstall.dlg.Finish.click_input()
                print("click Finish")
                time.sleep(5)
            else:
                print("fail to get install file = " + op_params.op_installer_file)

        except Exception as ex:
                print(str(ex))
                print("get exception on install op")
    '''''
    def uninstall_optimus(self):
        try:
            found = False
            warnings.simplefilter('ignore', category=UserWarning)
            Application(backend='uia').start('explorer.exe')
            time.sleep(3)

            explorer = Application().connect(path='explorer.exe')
            explorer.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            newWindow = explorer.window(top_level_only=True, active_only=True,
                                        class_name='CabinetWClass')
            time.sleep(5)

            newWindow.AddressBandRoot.click_input()
            print("click address")
            newWindow.type_keys(r'Control Panel\Programs\Programs and Features{ENTER}', with_spaces=True,
                                set_foreground=False)
            #timings.Timings.slow()
            #time.sleep(8)
            explorer.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)

           # ProgramsAndFeatures = explorer.window(top_level_only=True, active_only=True, title='Programs and Features',
             #                                     class_name='CabinetWClass')
          #  ProgramsAndFeatures = explorer.window(top_level_only=True, active_only=True,
           #                          class_name='CabinetWClass')
         #   print("Program Feature = " + ProgramsAndFeatures.window_text())
            time.sleep(3)
            #timings.Timings.slow()

            newWindow.type_keys(r'Lyve Client {ENTER}', with_spaces=True, set_foreground=False)
            print("get launch")
            time.sleep(10)

           # time.sleep(8)
            """""
            folderView = ProgramsAndFeatures.FolderView
            print("folder view")

            
            appInstall = ProgFeat.child_window(title='Folder View', control_type="List")
            print("get folder view")

            listTxt = appInstall.texts()
            print("get listTxt")
        
            # explorer.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            appInstall = ProgramsAndFeatures.FolderView.texts()[1:]

            print("get app install")

            programs_list = ','.join(appInstall)
            listApp = programs_list.split(',')

            app_name = ""
            for el in listApp:
                if (el.find("Lyve Client") != -1):
                    app_name = el
                    found = True
                    break
            if (found):
                item_op = ProgramsAndFeatures.FolderView.get_item(app_name)
                item_op.ensure_visible()
                item_op.click_input(button='right', where='icon')
                time.sleep(3)
                explorer.PopupMenu.wait('ready').menu().get_menu_path('Uninstall')[0].click_input()

                time.sleep(8)
                app = Application(backend='uia').connect(title='Lyve Client Uninstall')
                print("get uninstall dlg")
                time.sleep(10)
                app.LyveClient.Next.click_input()
                print("click Next on Uninstall")
                time.sleep(12)
                app.LyveClient.Finish.click_input()
                print("click Finish uninstall")
                time.sleep(2)
            else:
                print("cannot find app = " + app_name)

            ProgramsAndFeatures.close()
        """""

        except Exception as ex:
            print(str(ex))
            print("get exception on uninstall Op")

    '''''
    def uninstall_optimus(self):
        try:
            '''''
            if pyuac.isUserAdmin():
                print("user is admin")
            else:
                pyuac.runAsAdmin()
                print("run as admin")
            '''''
            warnings.simplefilter('ignore', category=UserWarning)
            Application().start('control.exe')
            time.sleep(2)
            app = Application(backend='uia').connect(path='explorer.exe', title='Control Panel')
            time.sleep(1)
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            app.window(title='Control Panel').ProgramsHyperlink.invoke()
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            app.window(title='Programs').child_window(title='Uninstall a program',
                                                      control_type='Hyperlink').invoke()
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)

            newWindow = app.window(top_level_only=True, active_only=True,
                                   class_name='CabinetWClass')
            time.sleep(1)
            newWindow.type_keys(r'Lyve Client {ENTER}', with_spaces=True, set_foreground=False)
            time.sleep(10)

            app = Application().connect(title='Lyve Client Uninstall', visible_only=True)
            time.sleep(1)
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            dlg = app.window(title="Lyve Client Uninstall")
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            time.sleep(1)
            if dlg.exists():
                btn = dlg.child_window(title="&Uninstall", class_name='Button')
                btn.click()
                time.sleep(8)
            else:
                print("dlg Uninstall not existed")

            dlg = app.window(title_re="Lyve Client Setup", class_name="#32770")
            time.sleep(3)
            app.dlg.Finish.click_input()
            print("click Finish")
            time.sleep(10)
            newWindow.close()

        except Exception as ex:
            print(str(ex))
            #print("get exception on uninstall Optimus")

    def edit_preferences(self, mode):
        try:
            warnings.simplefilter('ignore', category=UserWarning)
            Application(backend='uia').start('notepad.exe')
            time.sleep(2)
            timings.Timings.slow()
            app = Application().connect(path='notepad.exe')
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            app.Notepad.menu_select('File->Open')
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            app.Open.Edit.set_edit_text(r"C:\Users\534026\AppData\Roaming\Lyve Client\preferences.json")
            time.sleep(1)
            print("open preferences")
            app.Open.Open.click_input()
            print("click Open")
            time.sleep(2)
            app.Notepad.menu_select('Edit->Replace')
            time.sleep(1)
            print("click Edit")
            app.Replace.FindwhatEdit.set_edit_text('"lyveEnv": "prod"')
            txtEdit = '"lyveEnv"' + ': "' + mode + '"'
            app.Replace.ReplacewithEdit.set_edit_text(txtEdit)
            time.sleep(0.5)
            app.Replace.Replace.click_input()
            app.Replace.Replace.click_input()
            time.sleep(1)
            app.Nodepad.OK.click_input()
            app.Replace.Cancel.click_input()
            app.Notepad.menu_select('File->Save')
            app.Notepad.menu_select('File->Exit')

            return True

        except Exception as ex:
            print(str(ex))

    def quit_app(self):
        try:
            app = Application(backend="uia").connect(path="explorer.exe")
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            st = app.window(class_name="Shell_TrayWnd")
            t = st.child_window(title="Notification Chevron", control_type='Button')
            app.wait_cpu_usage_lower(threshold=0.5, timeout=30, usage_interval=1.0)
            print(t.window_text())
            t.click_input()
            time.sleep(1)

            list_box = Application(backend="uia").connect(class_name="NotifyIconOverflowWindow")
            list_box_win = list_box.window(class_name="NotifyIconOverflowWindow")
            time.sleep(1)
            list_button = list_box_win.descendants(control_type='Button')

            lyveBut = list_button[len(list_button)-2]
            lyveBut.click_input(button='right')
            desklist = Desktop(backend='uia').windows()
            found = False
            for desk in desklist:
                menu_items = desk.descendants(control_type="MenuItem")
                for it in menu_items:
                    if ( it.window_text() == "Exit"):
                        it.click_input()
                        found = True
                        break
                if ( found ):
                    break
        except Exception as ex:
            print(str(ex))

    def signin_LyveHub(self, email, pwd):
        status = False
        try:
            time.sleep(2)
            app = Application(backend='uia').connect(title="Sign In with Auth0", top_level_only=True, found_index=0)
            op = app.window(title="Sign In with Auth0", control_type='Pane')
            # op.dump_tree()
            email_edit = op.child_window(auto_id="email-lyvehub", control_type="Edit")
            if (email_edit.is_visible()):
                email_edit.set_edit_text(email)
                print("type email = " + email)
                pwd_edit = op.child_window(auto_id="password-lyvehub", control_type="Edit")
                if (pwd_edit.is_visible()):
                    pwd_edit.type_keys(pwd)
                    print("type pwd = " + pwd)
                else:
                    global_cfg.msgs("pwd edit not visible")
            else:
                global_cfg.msgs("email edit not visible")

            login = op.child_window(auto_id="btn-login-lyvehub", control_type="Button")
            if (login.is_visible()):
                login.click_input()
                print("click login")
                time.sleep(5)
                status = True
            else:
                global_cfg.msgs("login not visible")

            return status
        except:
            global_cfg.msgs.append("exception on sign in LyveHub")
            raise ValueError("exception on input sign n LyveHub")

    def click_recovery_code(self):
        status = False
        try:
            time.sleep(2)
            app = Application(backend='uia').connect(title="2nd Factor Authentication", top_level_only=True, found_index=0)
            op = app.window(title="2nd Factor Authentication", control_type='Pane')
            #p.dump_tree()
            codeLink = op.child_window(title="Use the recovery code")
            if ( codeLink.is_visible()):
                codeLink.click_input()
                time.sleep(2)
                status = True

            return status
        except:
            global_cfg.msgs.append("exception on 2nd factor authentication")
            raise ValueError("exception on 2nd factor authentication")

    def second_auth_LyveHub(self, recovery_code):
        status = False
        try:
            time.sleep(2)
            app = Application(backend='uia').connect(title="2nd Factor Authentication", top_level_only=True, found_index=0)
            op = app.window(title="2nd Factor Authentication", control_type='Pane')
           # op.dump_tree()
            edit = op.child_window(title="Enter your code here", control_type="Edit")
            edit.type_keys(recovery_code)
            print("enter code = " + recovery_code)
            time.sleep(1)
            op.Button1.click_input()
            print("click Submit")
            status = True
            time.sleep(1)
            return status
        except:
            global_cfg.msgs.append("exception on 2nd factor authentication")
            raise ValueError("exception on 2nd factor authentication")

    def get_recovery_code(self):
        status = False
        try:
            time.sleep(3)
            app = Application(backend='uia').connect(title="2nd Factor Authentication", top_level_only=True, found_index=0)
            op = app.window(title="2nd Factor Authentication", control_type='Pane', visible_only=False)
            time.sleep(2)
            #table = op.Table
            table = op.child_window(auto_id="lyveCloudWidget", visible_only=False)
            table.print_control_identifiers()
            list_txt = table.descendants(control_type="Text")
            for li in list_txt:
                print(li.window_text())
            edit = table.child_window(control_type="Edit")
            print("edit txt= " + edit.window_text())
            time.sleep(1)
            new_code = edit.window_text()
            project_params.recovery_code = new_code

            time.sleep(1)
            chbox = op.child_window(control_type="CheckBox")
            if ( chbox.is_visible()):
                chbox.click_input()
                print("click checkbox")
                #op.Button1.click_input()
                #print("click Submit")
                status = True
            time.sleep(1)
            return status
        except:
            global_cfg.msgs.append("exception on 2nd factor authentication")
            raise ValueError("exception on 2nd factor authentication")

    def launch_app_from_path(self):
        status = False
        try:
            time.sleep(2)
            pathApp = r"C:\Program Files\Lyve Client\Lyve Client.exe"
            Application().start(pathApp)
            time.sleep(2)
            status = True
            return status
        except:
            print("get exception on launch app from path")

    def launch_app(self):
        status = False
        try:
            pyautogui.hotkey('win', 's')
            time.sleep(1)
            pyautogui.typewrite("Toolkit")
            time.sleep(1)
            #area1 = (0, 400, 400, 700)
            area1 = (0, 450, 400, 650)
            strImg1 = "toolkitApp.png"
            self.take_screen_shot_of_page(strImg1, area1)
            time.sleep(2)
            pyautogui.locateOnScreen(strImg1)
            keys1 = ['App']
            dict1 = self.convert_image_to_position(strImg1, area1, keys1)
            loc1 = dict1.get('App')
            pyautogui.moveTo(loc1[0], loc1[1])
            time.sleep(1)
            pyautogui.click(button='right')
            time.sleep(1)
            #pyautogui.click(loc1[0]+40, loc1[1]+70)
            pyautogui.click(loc1[0] + 40, loc1[1] + 50)
            time.sleep(2)
            strImg2 = "runas.png"
            #area2 = (722, 380, 460, 380)
            area2 = (722, 380, 460, 500)
            self.take_screen_shot_of_page(strImg2, area2)
            time.sleep(1)


            status = True
            if ( not status ):
                global_cfg.msgs.append("fail to launch app")
            return status
        except:
            raise ValueError("fail to launch app")

    def enable_proxy(self):
        cmd_enable = "networksetup -setsocksfirewallproxystate Ethernet on"
        out = os.popen(cmd_enable).read()
        time.sleep(5)

    def disable_proxy(self):
        cmd_enable = "networksetup -setsocksfirewallproxystate Ethernet off"
        out = os.popen(cmd_enable).read()
        time.sleep(5)

    def parse_server_reqs(self,fname):
        cmd_route = "mitmdump -p 5465 --mode socks5 -w {}".format(fname)
        self.utilsObj.fork_process(cmd_route,"test_out2.txt")
        print("Starting socks proxy , routing all traffic ...")
        time.sleep(5)

    def is_proxy_enabled(self):
        cmd_check = "networksetup -getsocksfirewallproxy Ethernet"
        out = os.popen(cmd_check).read()
        if (("Enabled: Yes" in out) and ("Port: 5465" in out)):
            print("Proxy is enabled" and ("Port: 5465" in out))
            return True
        elif ("Enabled: No" in out):
            print("Proxy is not enabled")
            return False

    def clean_out(self,fname):
        cmd_clean = "cat /dev/null > {}".format(fname)
        out = os.popen(cmd_clean).read()

    def start_proxy_server(self):
        try:
            cmd = "netsh winhttp set proxy localhost:5465"
            out = os.popen(cmd).read()
            print("start proxy server " + str(out))
            time.sleep(10)
            return True
        except:
            return False

    def get_request_info(self, fname):
        payload_info = []

        with open(fname, 'r', encoding="ISO-8859-1") as debug_data:
            file_info = debug_data.readlines()
            search_str1 = re.findall(r'{\"\w+\":{.*}\]}', str(file_info))
            list_str = search_str1[0].split(r'{"header":', 10)
            for it in list_str:
                it = r'{"header":' + it
                hd = re.sub(r'-----BEGIN CERTIFICATE-----.*-----END CERTIFICATE-----', "", it)
                info_str1 = re.sub(r',\d+:headers.+\d+:', "", hd)
                line = re.sub("'", "", info_str1)
                mod_line = re.sub(r',$', "", str(line))
                new_info = str(mod_line)
                hdList = new_info.split("]}")
                for i in range(len(hdList)):
                    if (i < len(hdList) - 1):
                        header = hdList[i] + "]}"
                        payload_info_dic = json.loads(header)
                        payload_info.append(payload_info_dic)

        return payload_info

    def update_test_info(self,testName, bresult, msgs, b_crashed, jira_feature):
        status_info = {}
        status = "Fail"
        if(bresult):
            status = "Pass"
        else:
            status = "Fail"
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
           # print("test plan id = " + str(test_plan_id))
            if(test_plan_id):
                global_cfg.ids["test_plan_id"] = test_plan_id
            else:
                global_cfg.ids["test_plan_id"] = self.testmgmObj.add_testPlan(params.test_plan_name, params.test_plan_name,global_cfg.def_jira_proj)

            test_set_id = self.testmgmObj.check_if_issue_exists(params.test_set_name, "Test Set")
          #  print("test set id = " + str(test_set_id))
            if(test_set_id):
                global_cfg.ids["test_set_id"] = test_set_id
            else:
                global_cfg.ids["test_set_id"] = self.testmgmObj.add_testSet(params.test_set_name, params.test_set_name, global_cfg.def_jira_proj)

            set_name = params.test_set_name + str(global_cfg.build_in_test['build'])
            test_exec_id = self.testmgmObj.check_if_issue_exists(params.test_set_name, "Test Execution")
          #  print("test exec id = " + str(test_exec_id))
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
           # print("test_id = " + str(test_id))
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










































