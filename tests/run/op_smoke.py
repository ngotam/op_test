


class op_smoke():
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



            if ( self.xray ):
                self.baseConObj.update_run_info_in_xray()
            time.sleep(5)
        else:
            self.app = project_params.app_instance
            self.op = self.app.LyveClient
            time.sleep(5)

    '''''
    def test_001_verify_accept_license(self):
        time.sleep(3)
        global_cfg.msgs = []
        bresult = task.verify_accept_license(self.app)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_001_verify_accept_license"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_002_verify_devices_page(self):
        bresult = False
        global_cfg.msgs = []
        if ( task.click_Devices_tab(self.op)):
            bresult = task.verify_devices_page(self.op)

        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_002_verify_devices_page"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_003_verify_get_data_icon_view(self):
        global_cfg.msgs = []
        bresult = False
        listData = task.get_data_icon_view(self.op)
        if ( listData != []):
            bresult = True
        else:
            global_cfg.msgs.append("fail to get list of data icon view")
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_003_verify get data icon view"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_004_verify_click_device_icon_inspect(self):
        deviceName = "LaCie Rugged RAID Pro Drive"
        global_cfg.msgs = []
        bresult = task.click_device_inspect(self.op, deviceName)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if ( bresult ):
            task.click_device_list_link(self.op)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_004_verify_click_device_icon_inspect"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_005_verify_toggle_list_view(self):
        global_cfg.msgs = []
        bresult = task.toggle_view(self.op)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_005_verify_toggle_list_view"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_006_verify_get_data_list_view(self):
        listName = ["LaCie Rugged RAID Pro SD", "LaCie Rugged RAID Pro Drive",
                    "DJI Fly Drive", "DJI Fly SD",
                    "LaCie Rugged SSD"]
        global_cfg.msgs = []
        bresult = task.verify_data_list_view(self.op, listName)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_006_verify_get_data_list_view"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_007_verify_device_inspect(self):
        deviceName = "DJI Fly SD"
        volumeName = "FLY_SD"
        serialNo = "00001612"
        connection = "USB"
        global_cfg.msgs = []
        bresult = False
        time.sleep(1)
        if (task.click_device_inspect(self.op, deviceName)):
            bresult = task.verify_device_detail(self.op, volumeName, serialNo, connection)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (bresult):
            task.click_device_list_link(self.op)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_007_verify_device_inspect"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_008_verify_settings_about_page(self):
        global_cfg.msgs = []
        version = params.file_version
        #print("version got = " + version)
        version = "1.99.17"
        if (task.click_Settings_tab(self.op)):
            bresult = task.verify_Settings_About_version(self.op, version)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_008_verify_settings_about_page"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_009_verify_workflows_page(self):
        bresult = False
        global_cfg.msgs = []
        if ( task.click_Workflows_tab(self.op)):
            bresult = task.verify_workflows_page(self.op)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_009_verify_workflows_page"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_010_verify_create_new_workflow(self):
        bresult = False
        global_cfg.msgs = []
        if ( task.click_add_workflow(self.op)):
            bresult = task.verify_welcome_workflow(self.op)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_010_verify_create_new_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_011_verify_click_copy_option(self):
        global_cfg.msgs = []
        bresult = task.verify_click_copy_option(self.op)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_011_verify_click_copy_option"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_012_verify_edit_workflow_name(self):
        name = "Workflow-Copy1"
        global_cfg.msgs = []
        bresult = task.edit_workflow_name(self.op, name)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_012_verify_edit_workflow_name"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_013_verify_select_source(self):
        source = "DJI Fly SD"
      #  source = "FLY_SD"
        global_cfg.msgs = []
        name = params.workflow_name
        bresult = task.verify_select_sources(self.op, name, source)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_013_verify_select_source"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_014_verify_select_files(self):
        select = "All Files"
        global_cfg.msgs = []
        bresult = task.verify_select_files(self.op, select)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_014_verify_select_files"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_015_verify_select_destination(self):
        destination = "DJI Fly Drive"
       # destination = "Fly Drive"
        global_cfg.msgs = []
        name = params.workflow_name
        bresult = task.verify_select_destination(self.op, name, destination)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_015_verify_select_destination"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_016_verify_select_second_action(self):
        delete = False
        notify = True
        global_cfg.msgs = []
        bresult = task.verify_select_second_action_for_copy(self.op, delete, notify)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_016_verify_select_second_action"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_017_verify_select_trigger(self):
        trigger = "Manual"
        global_cfg.msgs = []
        bresult = task.verify_select_trigger(self.op, trigger)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_017_verify_select_trigger"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_018_verify_click_create_workflow(self):
        trigger = "Manual"
        actions = "Copy, Notify"
        global_cfg.msgs = []
        bresult = task.verify_click_create_workflow(self.op, actions, trigger)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_018_verify_click_create_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_019_verify_workflow_detail(self):
        trigger = "Manual"
        name = params.workflow_name
        type = "Copy"
        global_cfg.msgs = []
        bresult = task.verify_workflow_detail(self.op, name, type, trigger)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_019_verify_workflow_detail"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_020_verify_workflow_copy_created_notification(self):
        bresult = False
        name = "Workflow-Copy1"
        action = "was created"
        global_cfg.msgs = []
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_020_verify_workflow_copy_created_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_021_verify_click_play_copy_workflow(self):
        #name = params.workflow_name
        global_cfg.msgs = []
        name = "Workflow-Copy1"
        task.click_Workflows_tab(self.op)
        bresult = task.verify_click_play_workflow(self.op, name)
        time.sleep(2)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_021_verify_click_play_copy_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, "")
    
    def test_022_verify_click_cancel_workflow(self):
        # name = params.workflow_name
        global_cfg.msgs = []
        name = "Workflow-Copy1"
        time.sleep(1)
        bresult = task.verify_click_cancel_workflow(self.op, name)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_022_verify_click_cancel_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_023_verify_click_play_workflow(self):
        bresult = False
        global_cfg.msgs = []
        #name = params.workflow_name
        name = "Workflow-Copy1"
        if ( task.click_Workflows_tab(self.op)):
            bresult = task.verify_click_play_workflow(self.op, name)
            time.sleep(40)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_023_verify_click_play_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_024_verify_click_inspect_copy_workflow(self):
        #name = params.workflow_name
        name = "Workflow-Copy1"
        global_cfg.msgs = []
        bresult = False
        if ( task.click_Workflows_tab(self.op)):
            bresult = task.verify_click_inspect_workflow(self.op, name)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_024_verify_click_inspect_copy_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_025_verify_inspect_copy_workflow_page(self):
        trigger = "Manual"
        #name = params.workflow_name
        name = "Workflow-Copy1"
        type = "Copy"
        global_cfg.msgs = []
        bresult = task.verify_inspect_workflow_page(self.op, name, type, trigger)
        time.sleep(10)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_025_verify_inspect_copy_workflow_page"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_026_verify_click_inspect_activity(self):
        global_cfg.msgs = []
        bresult = task.verify_click_inspect_activity(self.op)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_026_verify_click_inspect_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_027_verify_inspect_activity_page(self):
        activity = "Completed"
        #name = params.workflow_name
        name = "Workflow-Copy1"
        type = "Copy"
        source = "FLY_SD"
        destination = "Fly Drive"
        global_cfg.msgs = []
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_027_verify_inspect_activity_page"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_028_verify_click_run_workflow_activity(self):
        time.sleep(1)
        title = "Workflow-Copy1 is under way"
        action = "Run Workflow"
        global_cfg.msgs = []
        task.click_Activity_tab(self.op)
        bresult = task.click_action_workflow(self.op, title, action)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_028_verify_click_run_workflow_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
  
    def test_029_verify_click_cancel_all_workflow_activity(self):
        title = "Workflow-Copy1 is under way"
        action = "Cancel All"
        global_cfg.msgs = []
        bresult = task.click_action_workflow(self.op, title, action)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_029_verify_click_cancel_all_workflow_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_030_verify_click_inspect_copy_workflow_activity(self):
        title = "Workflow-Copy1 is under way"
        task.click_Activity_tab(self.op)
        global_cfg.msgs = []
        bresult = task.click_inspect_notification_item(self.op, title)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_030_verify_click_inspect_copy_workflow_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_031_verify_inspect_copy_workflow_activity(self):
        title = "Workflow-Copy1"
        type = "Copy"
        trigger = "Manual"
        global_cfg.msgs = []
        bresult = task.verify_inspect_workflow_notification(self.op, title, type, trigger)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_031_verify_inspect_copy_workflow_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_032_verify_edit_trigger_auto_workflow(self):
        name = "Workflow-Copy1"
        option = "Edit"
        trigger = "Automatic"
        type = "Copy"
        bresult = False
        global_cfg.msgs = []
        task.click_Workflows_tab(self.op)
        if (task.verify_click_dotmenu(self.op, name, option)):
            if (task.verify_edit_trigger_workflow(self.op, trigger)):
                task.verify_click_update_workflow(self.op, type, trigger)
                bresult = task.verify_workflow_detail(self.op, name, type, trigger)
                time.sleep(25)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_032_verify_edit_trigger_auto_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_033_verify_edit_trigger_workflow_notification(self):
        bresult = False
        name = "Workflow-Copy1"
        action = "was edited"
        global_cfg.msgs = []
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_033_verify_edit_trigger_workflow_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_034_verify_copy_data_activity_completed(self):
        activity = "Completed"
        name = "Workflow-Copy1"
        type = "Copy"
        source = "FLY_SD"
        destination = "Fly Drive"
        global_cfg.msgs = []
        time.sleep(25)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_034_verify_copy_data_activity_completed"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_035_verify_add_delete_action(self):
        name = "Workflow-Copy1"
        option = "Edit"
        trigger = "Automatic"
        type = "Copy, Delete, Notify"
        bresult = False
        global_cfg.msgs = []
        task.click_Workflows_tab(self.op)
        if (task.verify_click_dotmenu(self.op, name, option)):
            if (task.verify_add_delete_action(self.op)):
                bresult = task.verify_click_update_workflow(self.op, type, trigger)
                time.sleep(30)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_035_verify_add_delete_action"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_036_verify_copy_automatic_completed(self):
        activity = "Completed"
        name = "Workflow-Copy1"
        type = "Copy"
        source = "FLY_SD"
        destination = "Fly Drive"
        global_cfg.msgs = []
        time.sleep(10)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        time.sleep(60)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_036_verify_copy_automatic_completed"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_037_verify_delete_action_completed(self):
        activity = "Completed"
        name = "Workflow-Copy1"
        type = "Delete"
        source = "FLY_SD"
        global_cfg.msgs = []
        time.sleep(25)
        bresult = task.verify_inspect_delete_action(self.op, name, type, activity, source)

        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_037_verify_delete_action_completed"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_038_verify_create_delete_manual_workflow(self):
        trigger = "Manual"
        name = "Workflow-Delete1"
        action = "Delete, Notify"
        source = "LaCie Rugged RAID Pro Drive"
       # source = "LaCie"
        notify = True
        bresult = False
        global_cfg.msgs = []
        time.sleep(1)
        task.click_Workflows_tab(self.op)
        if (task.click_add_workflow(self.op)):
            task.verify_click_delete_option(self.op)
            task.edit_workflow_name(self.op, name)
            task.verify_select_sources(self.op, name, source)
            task.verify_select_second_action_for_delete(self.op, notify)
            task.verify_select_trigger(self.op, trigger)
            task.verify_summary_workflow(self.op, source, trigger)
            bresult = task.verify_click_create_workflow(self.op, action, trigger)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_038_verify_create_delete_manual_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_039_verify_workflow_delete_created_notification(self):
        bresult = False
        name = "Workflow-Delete1"
        action = "was created"
        global_cfg.msgs = []
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_039_verify_workflow_delete_created_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_040_verify_play_delete_manual_workflow(self):
        name = "Workflow-Delete1"
        global_cfg.msgs = []
        task.click_Workflows_tab(self.op)
        bresult = task.verify_click_play_workflow(self.op, name)
        time.sleep(45)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_040_verify_play_delete_manual_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_041_verify_inspect_delete_manual_workflow(self):
        activity = "Completed"
        name = "Workflow-Delete1"
        type = "Delete"
        source = "LaCie"
        destination = None
        global_cfg.msgs = []
        time.sleep(25)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_activity(self.op)
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_041_verify_inspect_delete_manual_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_042_verify_create_delete_multi_sources_workflow(self):
        trigger = "Automatic"
        name = "Workflow-Delete2"
        action = "Delete, Notify"
        sources = ["LaCie Rugged RAID Pro SD", "DJI Fly SD"]
       # sources = ["LACIE_SD", "FLY_SD"]
        global_cfg.msgs = []
        bresult = False
        notify = True

        task.click_Workflows_tab(self.op)
        if (task.click_add_workflow(self.op)):
            task.verify_click_delete_option(self.op)
            task.edit_workflow_name(self.op, name)
            task.verify_select_multi_sources(self.op, name, sources)
            task.verify_select_second_action_for_delete(self.op, notify)
            task.verify_select_trigger(self.op, trigger)
            bresult = task.verify_click_create_workflow(self.op, action, trigger)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_042_verify_create_delete_multi_sources_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_043_verify_workflow_delete_auto_created_notification(self):
        bresult = False
        name = "Workflow-Delete2"
        action = "was created"
        global_cfg.msgs = []
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_043_verify_workflow_delete_auto_created_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_044_verify_inspect_delete_auto_workflow(self):
        activity = "Completed"
        name = "Workflow-Delete2"
        type = "Delete"
        #source = "SSD"
        sourceList = ["FLY_SD", "LACIE_SD"]
        destination = None
        global_cfg.msgs = []

        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_activity(self.op)
        #bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        bresult = task.verify_inspect_activity_with_multi_sources(self.op, name, type, activity, sourceList, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "044_verify_inspect_delete_auto_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_045_verify_create_copy_auto_newfiles_workflow(self):
        trigger = "Automatic"
        name = "Workflow-Copy2"
        actions = "Copy, Notify"
        destination = "DJI Fly SD"
        source = "LaCie Rugged SSD"
        #source = "Ovo"
        #destination = "FLY_SD"
        delete = False
        notify = True
        select = "New Files"
        global_cfg.msgs = []
        time.sleep(1)

        task.click_Workflows_tab(self.op)
        task.click_add_workflow(self.op)
        task.verify_click_copy_option(self.op)
        task.edit_workflow_name(self.op, name)
        task.verify_select_sources(self.op, name, source)
        task.verify_select_files(self.op, select)
        task.verify_select_destination(self.op, name, destination)
        task.verify_select_second_action_for_copy(self.op, delete, notify)
        task.verify_select_trigger(self.op, trigger)
        bresult = task.verify_click_create_workflow(self.op, actions, trigger)
        time.sleep(60)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_045_verify_create_copy_auto_newfiles_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_046_verify_workflow_copy_created_notification(self):
        bresult = False
        name = "Workflow-Copy2"
        action = "was created"
        global_cfg.msgs = []
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_046_verify_workflow_copy_created_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_048_verify_copy_completed_from_inspect(self):
        activity = "Completed"
        name = "Workflow-Copy2"
        type = "Copy"
        destination = "FLY_SD"
        source = "Ovo"
        global_cfg.msgs = []
        time.sleep(20)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_048_verify_copy_completed_from_inspect"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    

    def test_049_verify_add_source_files(self):
        global_cfg.msgs = []
        source = "C:\\Users\\534026\\Documents\\Photos_Copy\\America"
        destination = "I:\\America"
        time.sleep(2)
        bresult = task.copy_tree(source, destination)
        time.sleep(10)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_049_verify_add_source_files"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_050_verify_click_play_auto_copy_workflow(self):
        bresult = False
        global_cfg.msgs = []
        # name = params.workflow_name
        name = "Workflow-Copy2"
        if (task.click_Workflows_tab(self.op)):
            bresult = task.verify_click_play_workflow(self.op, name)
            time.sleep(10)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_050_verify_click_play_auto_copy_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_051_verify_copy_newfiles_completed_from_inspect(self):
        activity = "Completed"
        name = "Workflow-Copy2"
        type = "Copy"
        destination = "FLY_SD"
        source = "Ovo"
        global_cfg.msgs = []
        time.sleep(2)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        time.sleep(1)
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_051_verify_copy_newfiles_completed_from_inspect"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_052_verify_delete_source_files(self):
        source = "I:\\America"
        global_cfg.msgs = []
        bresult = task.delete_folder(source)
        time.sleep(5)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if ( self.xray ):
            desc = "test_052_verify_delete_source_files"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_053_verify_click_play_auto_copy_workflow(self):
        bresult = False
        global_cfg.msgs = []
        # name = params.workflow_name
        name = "Workflow-Copy2"
        if (task.click_Workflows_tab(self.op)):
            bresult = task.verify_click_play_workflow(self.op, name)
            time.sleep(10)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_053_verify_click_play_auto_copy_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_054_verify_copy_completed_after_update_source(self):
        activity = "Completed"
        name = "Workflow-Copy2"
        type = "Copy"
        destination = "FLY_SD"
        source = "Ovo"
        global_cfg.msgs = []
        time.sleep(3)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        
        if ( self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_054_verify_copy_completed_after_update_source"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_055_verify_set_trigger_manual_from_dropdown(self):
        name = "Workflow-Delete2"
        trigger = "Manual"
        type = "Delete"
        bresult = False
        global_cfg.msgs = []
        time.sleep(5)
        task.click_Workflows_tab(self.op)
        if (task.update_trigger(self.op, name, trigger)):
            bresult = task.verify_workflow_detail(self.op, name, type, trigger)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_055_verify_set_trigger_manual_from_dropdown"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_056_verify_workflow_set_trigger_notification(self):
        bresult = False
        global_cfg.msgs = []
        name = "Workflow-Delete2"
        action = "trigger set to manual"
        time.sleep(1)
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_056_verify_workflow_set_trigger_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_057_verify_edit_workflow_system_notify(self):
        name = "Workflow-Delete1"
        option = "Edit"
        notify = "System"
        trigger = "Manual"
        type = "Delete, Notify"
        notifyMsg = "Workflow-Delete1 was edited"
       
        bresult = False
        global_cfg.msgs = []
        task.click_Workflows_tab(self.op)
        if (task.verify_click_dotmenu(self.op, name, option)):
            if (task.verify_edit_notify(self.op, notify)):
                bresult= task.verify_click_update_workflow(self.op, type, trigger)
                if (notify == 'System'):
                    task.move_to_system_notification(self.op)
                    bresult = task.verify_system_notification(notifyMsg)
            
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_057_verify_edit_workflow_system_notify"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_058_verify_delete_workflow(self):
        name = "Workflow-Delete1"
        option = "Delete"
        global_cfg.msgs = []
        time.sleep(1)
        task.click_Workflows_tab(self.op)
        bresult = task.verify_click_dotmenu(self.op, name, option)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_058_verify_delete_auto_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_059_verify_workflow_delete_notification(self):
        bresult = False
        global_cfg.msgs = []
        name = "Workflow-Delete1"
        action = "was deleted"
        if (task.click_Activity_tab(self.op)):
            bresult = task.verify_workflow_notification(self.op, name, action)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_059_verify_workflow_delete_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_060_verify_click_inspect_showAll_notification(self):
        time.sleep(1)
        titleNot = "Workflow-Copy2 is under way"
        titleWf = "Workflow-Copy2"
        type = "Copy"
        trigger = "Automatic"
        global_cfg.msgs = []
        bresult = False
        task.click_Activity_tab(self.op)
        #if (task.click_inspect_showAll(self.op, titleNot)):
        if (task.click_inspect_notification_item(self.op, titleNot)):
          #  bresult = task.verify_inspect_data_activity_page(self.op)
             bresult = task.verify_inspect_workflow_notification(self.op, titleWf, type,trigger )
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_060_verify_click_inspect_showAll_notification"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    
    def test_061_verify_click_unlock_MrA(self):
        deviceName = "NB26002C"
        global_cfg.msgs = []
        pwd = project_params.mrA_pwd
        trusted = False
        task.click_Devices_tab(self.op)
        task.toggle_view(self.op)
        bresult = task.click_unlock_device_listview(self.op, deviceName, pwd, trusted)
        time.sleep(30)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_061_verify_click_unlock_MrA"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)

    def test_062_verify_device_MrA(self):
        deviceName = "NB26002C"
        volName = "Volume1"
        format = "exFAT"
        firmwareVer = "M100R003"
        global_cfg.msgs = []
        bresult = False
        time.sleep(1)
        task.click_Devices_tab(self.op)
        if (task.click_device_inspect(self.op, deviceName)):
            bresult = task.verify_device_MrA(self.op, volName, format, firmwareVer)
            time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_062_verify_device_MrA"
            jira_link = ""
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_063_verify_create_copy_workflow_with_multi_sources(self):
        trigger = "Manual"
        name = "Workflow-Copy3"
        actions = "Copy, Notify, Delete"
        sourceList = ["LaCie Rugged RAID Pro Drive", "LaCie Rugged RAID Pro SD"]
        destination = "NB26002C"
      #  sourceList = ["LACIE_SD", "LaCie"]
     #   destination = "Volume1"
        delete = True
        notify = True
        select = "All Files"
        global_cfg.msgs = []

        srcFolder = "C:\\Users\\534026\\Documents\\Photos"
        destFolder = "G:\\Photos"
        task.copy_tree(srcFolder, destFolder)
        time.sleep(15)
        
        task.click_Workflows_tab(self.op)
        task.click_add_workflow(self.op)
        task.verify_click_copy_option(self.op)
        task.edit_workflow_name(self.op, name)
    
        task.verify_select_multi_sources(self.op, name, sourceList)
        task.verify_select_files(self.op, select)
        task.verify_select_destination(self.op, name, destination)
        task.verify_select_second_action_for_copy(self.op, delete, notify)
        task.verify_select_trigger(self.op, trigger)
        bresult = task.verify_click_create_workflow(self.op, actions, trigger)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_063_verify_create_copy_workflow_with_multi_sources"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_064_verify_click_play_multi_copies_workflow(self):
        bresult = False
        global_cfg.msgs = []
        # name = params.workflow_name
        name = "Workflow-Copy3"
        if (task.click_Workflows_tab(self.op)):
            bresult = task.verify_click_play_workflow(self.op, name)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_064_verify_click_play_multi_copies_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_065_verify_click_cancel_multi_copies_workflow(self):
        global_cfg.msgs = []
        # name = params.workflow_name
        name = "Workflow-Copy3"
        time.sleep(1)
        bresult = task.verify_click_cancel_workflow(self.op, name)
        time.sleep(10)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_065_verify_click_cancel_multi_copies_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_066_verify_copy_multi_sources_status_aborted(self):
        activity = "Aborted"
        name = "Workflow-Copy3"
        type = "Copy"
        sourceList = ["LACIE_SD", "LaCie"]
        destination = "Volume1"
        global_cfg.msgs = []
        time.sleep(5)

        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_with_multi_sources(self.op, name, type, activity, sourceList,
                                                                  destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_066_verify_copy_multi_sources_status_aborted"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_067_verify_click_play_multi_copies_workflow(self):
        bresult = False
        global_cfg.msgs = []
        # name = params.workflow_name
        name = "Workflow-Copy3"
        if (task.click_Workflows_tab(self.op)):
            bresult = task.verify_click_play_workflow(self.op, name)
            time.sleep(20)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_067_verify_click_play_multi_copies_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_068_verify_copy_multi_sources_status_completed(self):
        activity = "Completed"
        name = "Workflow-Copy3"
        type = "Copy"
        sourceList = ["LACIE_SD", "LaCie"]
        destination = "Volume1"
        global_cfg.msgs = []
        time.sleep(15)

        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_with_multi_sources(self.op, name, type, activity, sourceList,
                                                                  destination)
        time.sleep(60)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_068_verify_copy_multi_sources_status_completed"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_069_verify_delete_multi_sources_completed(self):
        activity = "Completed"
        name = "Workflow-Copy3"
        type = "Delete"
        sourceList = ["LaCie","LACIE_SD"]
        global_cfg.msgs = []
        time.sleep(15)
        
        bresult = task.verify_inspect_delete_multi_sources_action(self.op, name, type, activity, sourceList)
        time.sleep(1)
        task.click_inspect_workflow_panel_link(self.op)
    
        task.click_workflow_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_069_verify_delete_multi_sources_completed"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_070_verify_click_enable_dynamic_spares(self):
        global_cfg.msgs = []
        dynamic = "enabled"
        deviceName = "NB26002C"
        bresult = False
        task.click_Devices_tab(self.op)
        if (task.click_device_inspect(self.op, deviceName)):
            task.click_inspect_disk(self.op)
            if (task.toggle_dynamic_spares(self.op)):
                time.sleep(5)
                bresult = task.verify_enable_dynamic_spare(self.op, dynamic)
    
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_070_verify_click_enable_dynamic_spares"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    
    def test_071_verify_edit_disk_group(self):
        global_cfg.msgs = []
        raid = "RAID 0"
        volume = "Volume1"
        format = "NTFS"
        time.sleep(2)
        bresult = False
        if (task.verify_click_edit_diskgroup(self.op)):
            time.sleep(8)
            task.verify_select_raid(self.op, raid)
            bresult = task.verify_edit_format(self.op, format)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_071_verify_edit_disk_group"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_072_verify_confirm_switch_raid(self):
        global_cfg.msgs = []
        confirm = True
        bresult = task.verify_confirm_data_delete(self.op, confirm)
        time.sleep(100)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_072_verify_confirm_switch_raid"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)


    def test_073_verify_click_disable_dynamic_spares(self):
        global_cfg.msgs = []
        dynamic = "disabled"
        deviceName = "NB26002C"
        bresult = False
        if (task.click_device_inspect(self.op, deviceName)):
            task.click_inspect_disk(self.op)
            if (task.toggle_dynamic_spares(self.op)):
                time.sleep(5)
                bresult = task.verify_disable_dynamic_spare(self.op, dynamic)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_073_verify_click_disable_dynamic_spares"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_074_verify_edit_raid_format(self):
        global_cfg.msgs = []
        raid = "RAID 5"
        format = "exFAT"
        time.sleep(15)
        bresult = False
        if (task.verify_click_edit_diskgroup(self.op)):
            time.sleep(8)
            task.verify_select_raid(self.op, raid)
            bresult = task.verify_edit_format(self.op, format)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_074_verify_edit_raid_format"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_075_verify_confirm_switch_raid(self):
        global_cfg.msgs = []
        confirm = True
        bresult = task.verify_confirm_data_delete(self.op, confirm)
        time.sleep(100)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_075_verify_confirm_switch_raid"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)


    def test_076_verify_disable_security(self):
        global_cfg.msgs = []
        pwd = project_params.mrA_pwd
        title = "Disable Security"
        deviceName = "NB26002C"
        bresult = False
        time.sleep(1)
        task.click_Devices_tab(self.op)
        if (task.click_device_inspect(self.op, deviceName)):
            task.click_button_security(self.op)
            if (task.input_password_for_disable(self.op, title, pwd)):
                task.click_device_inspect(self.op, deviceName)
                bresult = task.verify_disable_security(self.op)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_076_verify_disable_security"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_077_verify_enable_security(self):
        global_cfg.msgs = []
        bresult = False
        if (task.click_enable_security(self.op)):
            bresult = task.confirm_enable_security(self.op)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_077_verify_enable_security"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_078_verify_create_password(self):
        global_cfg.msgs = []
        pwd = project_params.mrA_pwd
        trusted = False
        bresult = False
        if (task.create_password(self.op, pwd, trusted)):
            bresult = task.verify_setup_complete(self.op)
            time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_078_verify_create_password"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_079_verify_diskgroup_info_tooltip(self):
        deviceName = "NB26002C"
        global_cfg.msgs = []
        raid = "5"
        time.sleep(1)
        bresult = False
        if (task.click_device_inspect(self.op, deviceName)):
            bresult = task.verify_diskgroup_info_tooltip(self.op, raid)
        time.sleep(1)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_079_verify_diskgroup_info_tooltip"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_080_verify_click_crypto_erase(self):
        global_cfg.msgs = []
        pwd = project_params.mrA_pwd
        deviceName = "NB26002C"
        bresult = False
        time.sleep(2)

        if (task.click_crypto_erase(self.op)):
            bresult = task.confirm_crypto_erase(self.op, deviceName)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_080_verify_click_crypto_erase"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_081_verify_input_password_for_crypto_erase(self):
        global_cfg.msgs = []
        pwd = project_params.mrA_pwd
        deviceName = "NB26002C"

        bresult = task.input_password_for_crypto(self.op, deviceName, pwd)
        time.sleep(90)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_081_verify_input_password_for_crypto_erase"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_082_verify_certify_crypto_erase(self):
        global_cfg.msgs = []
        deviceName = "NB26002C"
        bresult = task.certify_crypto_erase(self.op, deviceName)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_082_verify_certify_crypto_erase"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
        

    def test_083_verify_save_PDF(self):
        global_cfg.msgs = []
        deviceName = "NB26002C"
        bresult = task.save_certificate_crypto_erase(self.op, deviceName)
       # bresult = task.save_pdf_explorer()
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_083_verify_save_PDF"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_084_verify_click_add_external_endpoint(self):
        global_cfg.msgs = []
        bresult = False
        time.sleep(1)
        task.click_Devices_tab(self.op)
        if (task.verify_click_add_external_endpoint(self.op)):
            bresult = task.verify_click_Next_external_endpoint(self.op)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_084_verify_click_add_external_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_085_verify_enter_bucket_url(self):
        global_cfg.msgs = []
        bucket_url = project_params.bucket_url_sub2
        bresult = task.verify_enter_bucket_url(self.op, bucket_url)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_085_verify_enter_bucket_url"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    
    def test_086_verify_enter_new_endpoint(self):
        global_cfg.msgs = []
        bucket_url = project_params.bucket_url_sub2
        accessKey = project_params.access_key
        secretKey = project_params.secret_access_key
        epName = project_params.ep_name_sub2
        bresult = task.verify_enter_new_endpoint(self.op, bucket_url, epName, accessKey, secretKey)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_086_verify_enter_new_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    
    def test_087_verify_add_new_folder(self):
        global_cfg.msgs = []
        bresult = False
        folder = "Sub22"
        if (task.verify_click_new_folder_endpoint(self.op)):
            bresult = task.verify_click_create_new_folder(self.op, folder)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_087_verify_add_new_folder"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_088_verify_save_endpoint(self):
        global_cfg.msgs = []
        folder = "Sub22"
        time.sleep(2)
        bresult = task.verify_click_save_endpoint(self.op, folder)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_088_verify_save_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_089_verify_create_copy_workflow_endpoint(self):
        trigger = "Automatic"
        name = "Workflow-Copy-Endpoint"
        actions = "Copy, Notify, Verify"
        destination = "NB26002C"
       # destination = "LaCie Rugged SSD"
        source = project_params.ep_name_sub2
        delete = False
        notify = True
        verify = True
        select = "All Files"
        global_cfg.msgs = []
        time.sleep(1)
        
        task.click_Workflows_tab(self.op)
        task.click_add_workflow(self.op)
        task.verify_click_copy_option(self.op)
        task.edit_workflow_name(self.op, name)
        task.verify_select_source_endpoint(self.op, name, source)
        task.verify_select_files(self.op, select)
        task.verify_select_destination(self.op, name, destination)
        task.verify_select_action_for_copy_endpoint(self.op, delete, notify, verify)
        task.verify_select_trigger(self.op, trigger)
        bresult = task.verify_click_create_workflow(self.op, actions, trigger)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_089_verify_create_copy_workflow_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_090_verify_copy_with_endpoint_completed(self):
        activity = "Completed"
        name = "Workflow-Copy-Endpoint"
        type = "Copy"
        source = project_params.ep_name_sub2
        destination = "Volume1"
        #destination = "LaCie"
        global_cfg.msgs = []
        time.sleep(25)
        task.click_Workflows_tab(self.op)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        #bresult = task.verify_inspect_activity_with_multi_sources(self.op, name, type, activity, sourceList,
           #                                                       destination)
        bresult = task.verify_inspect_activity_data_with_verify(self.op, name, type, activity, source, destination)

        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()),
                                                 bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_090_verify_copy_with_endpoint_completed"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_091_verify_add_endpoint_from_settings(self):
        global_cfg.msgs = []

        bucket_url = project_params.bucket_url_sub3
        accessKey = project_params.access_key
        secretKey = project_params.secret_access_key
        epName = project_params.ep_name_sub3
        folder = ""
        task.click_Settings_tab(self.op)
        if (task.verify_click_add_endpoint_from_settings(self.op)):
            task.verify_click_Next_external_endpoint(self.op)
            task.verify_enter_bucket_url(self.op, bucket_url)
            task.verify_enter_new_endpoint(self.op, bucket_url, epName, accessKey, secretKey)
            bresult = task.verify_click_save_endpoint(self.op, folder)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_091_verify_add_endpoint_from_settings"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    

    def test_092_verify_edit_source_endpoint_workflow(self):
        name = "Workflow-Copy-Endpoint"
        option = "Edit"
        trigger = "Automatic"
        type = "Copy, Notify, Verify"
        source = project_params.ep_name_sub3
        bresult = False
        global_cfg.msgs = []
        task.click_Workflows_tab(self.op)
        if (task.verify_click_dotmenu(self.op, name, option)):
            if (task.verify_edit_source_workflow(self.op, source)):
                task.verify_select_source_endpoint(self.op, name, source)
                bresult = task.verify_click_update_workflow(self.op, type, trigger)
               
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_092_verify_edit_source_endpoint_workflow"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_093_verify_click_cancel_workflow_endpoint(self):
        # name = params.workflow_name
        global_cfg.msgs = []
        name = "Workflow-Copy-Endpoint"
        bresult = task.verify_click_cancel_workflow(self.op, name)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_093_verify_click_cancel_workflow_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_094_verify_copy_aborted_from_inspect(self):
        activity = "Aborted"
        name = "Workflow-Copy-Endpoint"
        type = "Copy"
        destination = "Volume1"
        source = project_params.ep_name_sub3
        global_cfg.msgs = []

        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data_with_verify(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_094_verify_copy_aborted_from_inspect"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    '''''
    def test_095_verify_edit_name_endpoint(self):
        global_cfg.msgs = []
        bucket_url = project_params.bucket_url_sub1
        epName = project_params.ep_name_sub3
        epNewName = project_params.ep_name_sub1
        accessKey = project_params.access_key
        secretKey = project_params.secret_access_key
        folder = ""
        task.click_Devices_tab(self.op)
       # task.toggle_view(self.op)
        if ( task.verify_click_edit_endpoint(self.op, epName)):
            task.verify_edit_endpoint_with_keys(self.op, bucket_url, epNewName, accessKey, secretKey)
            bresult = task.verify_click_save_endpoint(self.op, folder)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_095_verify_edit_name_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_096_verify_click_delete_endpoint(self):
        global_cfg.msgs = []
        name = project_params.ep_name_sub1
        bresult = task.verify_click_delete_endpoint(self.op, name)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_096_verify_click_delete_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_097_verify_delete_endpoint(self):
        global_cfg.msgs = []
        name = project_params.ep_name_sub1
        confirm = True
        bresult = task.verify_delete_endpoint(self.op, name, confirm)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_097_verify_delete_endpoint"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    """""
    def test_098_verify_terms_and_conditions(self):
        global_cfg.msgs = []

        task.click_Settings_tab(self.op)
        bresult = task.click_Terms_and_Conditions(self.op)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_098_verify_terms_and_conditions"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_072_verify_click_create_diskgroup(self):
        deviceName = "NB26002C"
        global_cfg.msgs = []
        bresult = False
        time.sleep(5)

        if (task.click_device_inspect(self.op, deviceName)):
            bresult = task.verify_click_create_diskgroup(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_072_verify_click_create_diskgroup"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)

    def test_073_verify_select_available(self):
        global_cfg.msgs = []
        availSelect = "Disk 2"
        bresult = task.verify_select_available(self.op, availSelect)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_073_verify_select_available"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)

    def test_074_verify_create_raid_volume_format(self):
        global_cfg.msgs = []
        raid = "RAID 0"
        volume = "Volume1"
        format = "NTFS"
        if (task.verify_select_raid(self.op, raid)):
            bresult = task.verify_create_volume_format(self.op, raid, volume, format)
            time.sleep(75)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_074_verify_create_raid_volume_format"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_075_verify_device_MrA_after_select_available(self):
        deviceName = "NB26002C"
        volName = "Volume1"
        format = "NTFS"
        numavail = "1"
        raid = "RAID 0"
        global_cfg.msgs = []
        bresult = False
        time.sleep(1)
        task.click_Devices_tab(self.op)
        if (task.click_device_inspect(self.op, deviceName)):
            bresult = task.verify_disk_available_MrA(self.op, volName, format, numavail, raid)
            time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_075_verify_device_MrA_after_select_available"
            jira_link = ""
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_076_verify_inspect_disk_available(self):
        global_cfg.msgs = []
        diskNo = "Disk 2"
        arrayDisk = "Unassigned"
        bresult = False
        if (task.click_inspect_disk(self.op)):
            bresult = task.verify_inspect_disk_available(self.op, diskNo, arrayDisk)
            task.click_Device_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_076_verify_inspect_disk_available"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_078_verify_edit_select_spare_disk(self):
        global_cfg.msgs = []
        spareSelect = "Disk 2"
        raid = "RAID 5"
        volume = "Volume1"
        format = "exFAT"
        time.sleep(5)
        bresult = False
        if (task.verify_click_edit_diskgroup(self.op)):
            time.sleep(10)
            task.verify_select_raid_spare(self.op, raid, spareSelect)
            bresult = task.verify_edit_volume_format(self.op, raid, volume, format)
             
        time.sleep(2)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_078_verify_edit_select_spare_disk"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
        
    def test_079_verify_confirm_switch_raid(self):
        global_cfg.msgs = []
        confirm = True
        bresult = task.verify_confirm_data_delete(self.op, confirm)
        
        time.sleep(100)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_079_verify_confirm_switch_raid"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_080_verify_inspect_disk_spare(self):
        global_cfg.msgs = []
        deviceName = "NB26002C"
        diskNo = "Disk 2"
        spare = "Dedicated"
        bresult = False
        time.sleep(10)
        if (task.click_device_inspect(self.op, deviceName)):
            task.click_inspect_disk(self.op)
            bresult = task.verify_inspect_disk_spare(self.op, diskNo, spare)
            task.click_Device_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_080_verify_inspect_disk_spare"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_083_verify_create_disk_available(self):
        deviceName = "NB26002C"
        global_cfg.msgs = []
        raid = "RAID 5"
        availSelect = "Disk 2"
        volume = "Volume1"
        format = "NTFS"
        time.sleep(1)

        if (task.click_device_inspect(self.op, deviceName)):
            task.verify_click_create_diskgroup(self.op)
            task.verify_select_available(self.op, availSelect)
            task.verify_select_raid(self.op, raid)
            bresult = task.verify_create_volume_format(self.op, raid, volume, format)
            time.sleep(95)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_083_verify_create_disk_available"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_084_verify_device_after_select_available(self):
        deviceName = "NB26002C"
        volName = "Volume1"
        format = "NTFS"
        numavail = "1"
        raid = "RAID 5"
        global_cfg.msgs = []
        bresult = False
        time.sleep(1)

        if (task.click_device_inspect(self.op, deviceName)):
            bresult = task.verify_disk_available_MrA(self.op, volName, format, numavail, raid)
            time.sleep(1)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_084_verify_device_after_select_available"
            jira_link = ""
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
    
    def test_085_verify_select_global_spare(self):
       global_cfg.msgs = []
       diskSelect = "Disk 2"
       numglobal = "1 global spare"
       bresult = False
       time.sleep(2)
       if (task.click_inspect_disk(self.op)):
           task.verify_click_global_spare(self.op, diskSelect)
           time.sleep(1)
           task.click_Device_link(self.op)
           bresult = task.verify_disk_global_spare(self.op, numglobal)
       if (self.testrail):
           self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
       if (self.xray):
           desc = "test_085_verify_select_global_spare"
           self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
           jira_link = ""
           self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

       self.assertTrue(bresult, global_cfg.msgs)
    
    def test_086_verify_remove_global_spare(self):
       diskSelect = "Disk 2"
       numavail = "1 available"
       global_cfg.msgs = []
       bresult = False
       if (task.click_inspect_disk(self.op)):
           task.verify_remove_global_spare(self.op, diskSelect)
           time.sleep(1)
           task.click_Device_link(self.op)
           time.sleep(1)
           bresult = task.verify_disk_available(self.op, numavail)
       if (self.testrail):
           self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
       if (self.xray):
           desc = "test_086_verify_remove_global_spare"
           jira_link = ""
           self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
           self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

       self.assertTrue(bresult, global_cfg.msgs)
    
     
    def test_091_verify_click_create_diskgroup_all_selected(self):
        deviceName = "NB26002C"
        global_cfg.msgs = []
        raid = "RAID 5"
        volume = "Volume1"
        format = "exFAT"
        bresult = False
        time.sleep(5)
        task.click_Devices_tab(self.op)
        if (task.click_device_inspect(self.op, deviceName)):
            task.verify_click_create_diskgroup(self.op)
            task.verify_select_raid(self.op, raid)
            bresult = task.verify_create_volume_format(self.op, raid, volume, format)
            time.sleep(95)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        if (self.xray):
            desc = "test_091_verify_click_create_diskgroup_all_selected"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

        self.assertTrue(bresult, global_cfg.msgs)
      
    def test_086_verify_Verify_aborted_from_inspect(self):
        activity = "Aborted"
        name = "Workflow-Copy-Endpoint"
        type = "Verify"
        destination = "LaCie"
        source = project_params.ep_name_sub2
        global_cfg.msgs = []
        time.sleep(2)
        task.verify_click_inspect_workflow(self.op, name)
        task.verify_click_inspect_copy_activity(self.op)
        bresult = task.verify_inspect_activity_data_with_verify(self.op, name, type, activity, source, destination)
        task.click_inspect_workflow_panel_link(self.op)
        task.click_workflow_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_086_verify_Verify_aborted_from_inspect"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)

    def test_088_verify_click_inspect_copy_workflow_activity(self):
        title = "Workflow-Copy-Endpoint is under way"
        global_cfg.msgs = []
        bresult = task.click_inspect_notification_item(self.op, title)
        time.sleep(1)
        task.click_Activity_link(self.op)
        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_088_verify_click_inspect_copy_workflow_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    
    def test_094_verify_edit_endpoint_from_activity(self):
        global_cfg.msgs = []
        bucket_url = project_params.bucket_url_sub1
        new_bucket_url = project_params.bucket_url_sub1 + "/Sub11"
        epName = "AWS work, online"
        epNewName = project_params.ep_name_sub1

        if (task.verify_click_edit_endpoint_from_activity(self.op, epName)):
            bresult = task.verify_edit_endpoint(self.op, bucket_url, epNewName)

        if (self.testrail):
            self.testmgmObj.updateTestResultInfo(self.testmgmObj.getCaseIdFromName(self.utils.getMyName()), bresult)
        self.assertTrue(bresult, global_cfg.msgs)
        if (self.xray):
            desc = "test_094_verify_edit_endpoint_from_activity"
            self.baseConObj.update_test_in_xray(desc, desc, bresult, "")
            jira_link = ""
            self.baseConObj.update_test_info(desc, bresult, global_cfg.msgs, False, jira_link)
    """""



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(op_smoke)
    unittest.TextTestRunner(verbosity=2).run(suite)
    




