__author__ = 'asanghavi'
'''
#######################################################################################################################
Module Name : test_mgm
Purpose     : Provide commom functionality needed for test case management
Author      : Alpa Sanghavi.
Vesion      : 1.0
#######################################################################################################################
'''

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from core_framework.config import global_cfg
from core_framework.commons import utils
import inspect


class controller():


    def __init__(self):
        self.comobj     = utils.utils()

    def getRunIdFromName(self,name):
        run_id = 0
        runs = global_cfg.client.send_get('get_runs/%d' % global_cfg.project_id)
        for run in runs:
            if(name == run['name']):
                run_id = run['id']
                break
        return run_id

    def addRun(self,name):
        data = {"suite_id": global_cfg.master_suite_id, "name": '%s' % name,
                "assignedto_id": global_cfg.userId, "include_all": global_cfg.run_all, "case_ids": global_cfg.test_list}
        headers = {'content-type': 'application/json'}
        res_dic = global_cfg.client.send_post('add_run/%d' % global_cfg.project_id, data)
        global_cfg.run_id = res_dic['id']

    def addRun_with_selected_tests(self,name,suite_id,case_list):
        cases = global_cfg.client.send_get('get_cases/%d&suite_id=%d' % (global_cfg.project_id, suite_id))
       # print("cases = " + str(cases))
        if(case_list):
            for case in case_list:
                if(not case in cases):
                    case_list = global_cfg.test_list
                    break


        data = {"suite_id": suite_id, "name": '%s'%name,
                "assignedto_id": global_cfg.userId, "include_all": global_cfg.run_all, "case_ids": case_list}

        headers = {'content-type': 'application/json'}
        res_dic = global_cfg.client.send_post('add_run/%d' % global_cfg.project_id, data)
      #  print("res_dic = " + str(res_dic))
        global_cfg.run_id = res_dic['id']
       # print("run_id = " + str(global_cfg.run_id))

    def getCaseIdFromName(self,name):
        case_id = 0
        suite_id = 0
        bNameFound = False
        frm = inspect.stack()[1]
        calling_module_name = inspect.getmodule(frm[0]).__name__
        suite_id = self.getSuiteIdFromName(calling_module_name)
        section_id = self.getSectionIdFromName(calling_module_name,suite_id)
        cases = global_cfg.client.send_get('get_cases/%d&suite_id=%d&section_id=%s' % (global_cfg.project_id, int(suite_id), section_id))
        for case in cases:
            if(name == case['title']):
                case_id = case['id']
                bNameFound = True

        if(not bNameFound):
            case_id = self.addTestCase(name)

        return case_id

    def addTestCase(self,name):
        data = {"title":'%s'%name,"type_id": 1,"priority_id": 4,"estimate": "3m","description" :"Automated test case for localization" }
        case = global_cfg.client.send_post('add_case/%d' % global_cfg.section_id, data)
        return case['id']

    def getSectionIdFromName(self,name,suite_id):
        sec_id = 0
#        sections = global_cfg.client.send_get('get_sections/%d&suite_id=%d' %(config.project_id,config.master_suite_id))
        sections = global_cfg.client.send_get('get_sections/%d&suite_id=%d' % (global_cfg.project_id, int(suite_id)))
        for section in sections:
            if(name == section['name']):
                sec_id = section['id']
                break

        return sec_id

    def getSuiteIdFromName(self,name):
        suite_id = 0
        suites = global_cfg.client.send_get('get_suites/%d' % (global_cfg.project_id))
        for suite in suites:
            #print("suite = " + str(suite))

            if(name == suite['name']):
                suite_id = suite['id']
                break
        return suite_id

    def getUserIdFromEmail(self,email):
        user_id = global_cfg.client.send_get('get_user_by_email/&email={}'.format(email))
        return user_id


    def addSection(self,name):

        data = {"suite_id": '%d' % global_cfg.master_suite_id, "name": '%s' % name}
        sec_id = global_cfg.client.send_post('add_section/%d' % global_cfg.project_id, data)
        global_cfg.section_id = sec_id['id']

    def addSection_for_suite(self,name,suite_id):

        data = {"suite_id": '%d'%suite_id,"name":'%s' %name}
        sec_id = global_cfg.client.send_post('add_section/%d' % global_cfg.project_id, data)
        global_cfg.section_id = sec_id['id']
        return int(sec_id['id'])

    def addSuite(self,name,desc):
        data = {"name":'%s' %name,"description":'%s'%desc}
        suite_id = global_cfg.client.send_post('add_suite/%d' % global_cfg.project_id, data)
        global_cfg.suite_id = suite_id['id']
      #  print(global_cfg.suite_id)
        return int(suite_id['id'])

    def update_result_with_steps(self,caseId, result, comment):
        dic_name = "dic" + str(caseId)
        dic_name = {}
        dic_name['case_id'] = caseId
        if (result):
            dic_name['comment'] = comment
            dic_name['status_id'] = global_cfg.status_pass

        else:
            dic_name['comment'] = comment
            dic_name['status_id'] = global_cfg.status_fail

        global_cfg.test_info_list = []
        global_cfg.test_info_list.append(dic_name)
        global_cfg.test_result_dic["results"] = {}
        global_cfg.test_result_dic["results"] = global_cfg.test_info_list
        global_cfg.client.send_post('add_results_for_cases/%s' % global_cfg.run_id, global_cfg.test_result_dic)
        if(result):
            global_cfg.tests_passed = global_cfg.tests_passed + 1
        else:
            global_cfg.tests_failed = global_cfg.tests_failed + 1
        global_cfg.total_tests      = global_cfg.total_tests + 1


    def updateTestResultInfo(self, caseId, result):

        dic_name = "dic" + str(caseId)
        dic_name = {}
        dic_name['case_id'] = caseId
        if (result):
            dic_name['comment'] = global_cfg.test_pass_comm
            dic_name['status_id'] = global_cfg.status_pass

        else:
            dic_name['comment'] = global_cfg.test_pass_comm
            dic_name['status_id'] = global_cfg.status_fail

        global_cfg.test_info_list = []
        global_cfg.test_info_list.append(dic_name)
        global_cfg.test_result_dic["results"] = {}
        global_cfg.test_result_dic["results"] = global_cfg.test_info_list
        global_cfg.client.send_post('add_results_for_cases/%s' % global_cfg.run_id, global_cfg.test_result_dic)
        if(result):
            global_cfg.tests_passed = global_cfg.tests_passed + 1
        else:
            global_cfg.tests_failed = global_cfg.tests_failed + 1
        global_cfg.total_tests      = global_cfg.total_tests + 1


    def validate_contents_list(self,list_exp,list_actual):
        bItemFound = True

        for item in list_exp:
            if(item not in list_actual):
                  print("item not found %s" %item)
                  bItemFound = False
                  break

        return bItemFound


    def killChromeWindow(self):
        cmd_rm = 'killall -9 "Google Chrome"'
        os.popen(cmd_rm).read()
