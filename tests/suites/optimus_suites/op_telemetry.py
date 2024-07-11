import unittest, time
from pywinauto.application import Application
from pywinauto import timings
#from core_framework.controller import win_ui_Controller
from core_framework.commons import utils
from core_framework.config import global_cfg
from core_framework.config import params as global_params
from projects.optimus_win.ui_screens import op_tasks as task
from projects.optimus_win.config import op_params as params
from projects.optimus_win.config import project_params
from projects.optimus_win.controller import project_base_controller
from core_framework.controller import test_mgm
#from core_framework import core_tele_lib

import core_lib


class op_telemetry(unittest.TestCase):
    app = None
    op = None
    utils = None

    baseConObj = None
    curr_tests = []
    testrail = project_params.testrail_report
    xray     = project_params.xray_report

    def __init__(self, name=''):
        unittest.TestCase.__init__(self, name)

        self.testmgmObj = test_mgm.controller()

        self.utils = utils.utils()
        self.baseConObj = project_base_controller.projects_base_controller()

        #self.app = None

        #self.app = Application(backend='uia').connect(path=app_file)
        if (not project_params.setup_info['status']):
            '''''
            self.baseConObj.uninstall_optimus()
            self.baseConObj.download_op()
            time.sleep(1)
            self.baseConObj.install_op()
            time.sleep(8)
            self.baseConObj.quit_app()
            
            time.sleep(1)
            
            if (self.baseConObj.edit_preferences(project_params.app_mode)):
                time.sleep(5)
                self.baseConObj.launch_app_from_path()
                time.sleep(5)
            '''''
            #app_file = params.appdata_path
            #self.app = Application(backend='uia').start(app_file)

            project_params.setup_info['status'] = True

            suite_id = self.testmgmObj.getSuiteIdFromName(__name__)
            global_cfg.curr_suite_name['name'] = str(__name__)
            if (suite_id):
                global_cfg.suite_id = suite_id
                print("global suite_id = " + str(suite_id))
            else:
                suite_id = self.testmgmObj.addSuite(__name__, "Test Suite for Optimus smoke")
                print("suite_id = " + str(suite_id))
            sec_id = self.testmgmObj.getSectionIdFromName(__name__, int(suite_id))
            if (sec_id):
                global_cfg.section_id = int(sec_id)
                print("global section = " + str(global_cfg.section_id))
            else:
                section_new_id = int(self.testmgmObj.addSection_for_suite(__name__, int(suite_id)))
                print("new id = " + str(section_new_id))

            self.testmgmObj.addRun_with_selected_tests(__name__ + global_cfg.run_name_ext, suite_id, self.curr_tests)

            time.sleep(10)
            timings.Timings.fast()

            if ( project_params.app_mode == "stage"):
                """""
                email = project_params.email_LyveHub
                pwd = project_params.lyve_pwd
                self.baseConObj.signin_LyveHub(email, pwd)
                time.sleep(3)
                code = project_params.recovery_code
                print("code = " + code)
                self.baseConObj.click_recovery_code()
                self.baseConObj.second_auth_LyveHub(code)
                self.baseConObj.get_recovery_code()
                """""
                self.app = Application(backend='uia').connect(title=params.app_name, top_level_only=True, found_index=0)
                self.op = self.app.LyveClient
                project_params.app_instance = self.app
                project_params.op_instance = self.op


            elif ( project_params.app_mode == "standalone"):
                self.app = Application(backend='uia').connect(title=params.app_name, top_level_only=True, found_index=0)
                self.op = self.app.LyveClient
                project_params.app_instance = self.app
                project_params.op_instance = self.op

            ######Telemetry
            '''''
            if (not core_tele_lib.is_proxy_enabled()):
                # enable proxy on the system
                core_tele_lib.enable_proxy()
            time.sleep(5)
            '''''

            self.baseConObj.start_proxy_server()
            print("start proxy server ")
            # Give few minutes for proxy server to start
            time.sleep(10)

            if ( self.xray ):
                self.baseConObj.update_run_info_in_xray()
            time.sleep(5)
        else:
            self.app = project_params.app_instance
            self.op = self.app.LyveClient
            time.sleep(5)

    def test_001_validate_request_type(self):
        bresult = False
        fname = global_cfg.op_dump_file
        request_type = global_cfg.request_type
        req_info = self.baseConObj.get_request_info(fname)
        print(req_info)
        time.sleep(2)
        global_cfg.req_payload = req_info

        for line in req_info:
            print(line)
            for k, v in line.items():
                if (k == "header"):
                    for key, value in v.items():
                        if (key == "request_type"):
                            if (value == request_type):
                                print("get correct request type = " + str(value))
                                bresult = True
                                break
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_001_validate_request_type"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_002_validate_request_ts(self):
        bresult = False
        fname = global_cfg.op_dump_file
        request_ts = global_cfg.request_ts
        req_info = self.baseConObj.get_request_info(fname)
        print(req_info)
        time.sleep(2)
        global_cfg.req_payload = req_info

        for line in req_info:
            print(line)
            for k, v in line.items():
                if (k == "header"):
                    for key, value in v.items():
                        if (key == "request_ts"):
                            if (value == request_ts):
                                print("get correct request ts = " + str(value))
                                bresult = True
                                break
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_002_validate_request_ts"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_003_validate_client_id(self):
        bresult = False
        fname = global_cfg.op_dump_file
        client_id = global_cfg.client_id
        req_info = self.baseConObj.get_request_info(fname)
        print(req_info)
        time.sleep(2)
        global_cfg.req_payload = req_info

        for line in req_info:
            print(line)
            for k, v in line.items():
                if (k == "header"):
                    for key, value in v.items():
                        if (key == "client_id"):
                            if (value == client_id):
                                print("get correct client_id = " + str(value))
                                bresult = True
                                break
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_003_validate_client_id"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_004_validate_module_version(self):
        bresult = False
        fname = global_cfg.op_dump_file
        module_version = global_cfg.module_version
        req_info = self.baseConObj.get_request_info(fname)
        print(req_info)
        time.sleep(2)
        global_cfg.req_payload = req_info

        for line in req_info:
            print(line)
            for k, v in line.items():
                if (k == "header"):
                    for key, value in v.items():
                        if (key == "module_version"):
                            if (value == module_version):
                                print("get correct module version = " + str(value))
                                bresult = True
                                break
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_004_validate_module_version"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_005_validate_activity_id_for_DeviceInfo(self):
        bresult = False
        fname = global_cfg.op_dump_file

        # req_info = core_tele_lib.get_request_info(fname)
        req_info = self.baseConObj.get_request_info(fname)
        print(req_info)
        time.sleep(2)
        global_cfg.req_payload = req_info

        for line in req_info:
            print(line)
            if (task.is_request_type(line, "Optimus")):
                for k, v in line.items():
                    if (k == "payload"):
                        for info in v:
                            print(info)
                            if (info['activity_id'] == 1):
                                bresult = True
                                print("get correct activity_id = 1 for DeviceInfo")
                                break
                            else:
                                print("get wrong activity_id = " + str(info['activity_id']))
            else:
                print("get different request type")
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_005_validate_activity_id_for_DeviceInfo"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_006_validate_format_type(self):
        time.sleep(5)
        bresult = False
        fname = global_cfg.op_dump_file

        req_info = self.baseConObj.get_request_info(fname)
        global_cfg.req_payload = req_info
        for line in req_info:
            if (task.is_request_type(line, "Optimus")):
                for k, v in line.items():
                    if (k == "payload"):
                        for info in v:
                            print(info)
                            if (info['activity_id'] == 1):
                                print("get activity id = 1 ")
                                if (info['format_type'] == 'exFAT'):
                                    bresult = True
                                    print("get correct format type = exFAT")
                                    break
                                else:
                                    print("get format type = " + str(info['format_type']))
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_006_validate_format_type"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_007_validate_device_status(self):
        bresult = False
        fname = global_cfg.op_dump_file

        req_info = self.baseConObj.get_request_info(fname)
        time.sleep(2)
        global_cfg.req_payload = req_info
        for line in req_info:
            if (task.is_request_type(line, "Optimus")):
                for k, v in line.items():
                    if (k == "payload"):
                        for info in v:
                            print(info)
                            if (info['activity_id'] == 1):
                                print("get activity id = 1 ")
                                if (info['device_status'] == 'discovered'):
                                    bresult = True
                                    print("get correct device status = 'discovered")
                                    break
                                else:
                                    print("get device status = " + str(info['device_status']))
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_007_validate_device_status"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_008_validate_manufacturer(self):
        bresult = False
        fname = global_cfg.op_dump_file
        manufacturer = global_cfg.manufacturer
        req_info = self.baseConObj.get_request_info(fname)
        time.sleep(2)
        global_cfg.req_payload = req_info

        for line in req_info:
            if (task.is_request_type(line, "Optimus")):
                for k, v in line.items():
                    if (k == "payload"):
                        for info in v:
                            print(info)
                            if (info['activity_id'] == 1):
                                print("get activity id = 1 ")
                                if (info['manufacturer'] == manufacturer):
                                    bresult = True
                                    print("get correct manufacturer = " + manufacturer)
                                    break
                                else:
                                    print("get manufacturer = " + str(info['manufacturer']))
            if (bresult):
                break
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_008_validate_manufacturer"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(op_telemetry)
    unittest.TextTestRunner(verbosity=2).run(suite)
    




