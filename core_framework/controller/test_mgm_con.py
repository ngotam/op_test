__author__ = 'asanghavi'
'''
#######################################################################################################################
Module Name : test_mgm
Purpose     : Provide commom functionality needed for test case management
Author      : Alpa Sanghavi.
Vesion      : 1.0
#######################################################################################################################
'''
import sys, os,json
from core_framework.config import global_cfg
import xray_lib


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))




class controller():

    libObj = None
    def __init__(self, jira_server, jira_user,jira_pass):
        self.libObj = xray_lib.xray_lib(jira_server, jira_user,jira_pass)


    def get_test_by_id(self, jira_id):
        res = self.libObj.send_get("def", "issue/" + str(jira_id))
        if(res):
            print(res.json())


    def add_testPlan(self,summary, desc,proj_key):
        ret_val = 0
        try:
            ret_val = self.libObj.create_issue(summary, desc,proj_key,"Test Plan")
        except:
            print("Failed addding Test Plan")
        return ret_val

    def add_testSet(self,summary, desc,proj_key):
        ret_val = 0
        try:
            ret_val = self.libObj.create_issue(summary, desc,proj_key,"Test Set")
        except:
            print("Failed addding Test Plan")
        return ret_val

    def add_test(self, summary, desc,proj_key):
        ret_val = 0
        try:
            ret_val = self.libObj.create_issue(summary, desc,proj_key,"Test")
        except:
            print("Failed addding Test Plan")
        return ret_val

    def add_testExecution(self, summary, desc,proj_key):
        ret_val = 0
        try:
            ret_val = self.libObj.create_issue(summary, desc,proj_key,"Test Execution")
        except:
            print("Failed addding Test Plan")
        return ret_val

    def add_testSteps(self):
        pass


    def link_test_to_product_task(self,src_test_id, dest_test_id):
        ret_val = False
        try:
            ret_val = self.libObj.link_tests(src_test_id,dest_test_id)
        except:
            print("Failed addding Test Plan")
        return ret_val


    def add_relationship_between_tests(self,src_test_id, dest_test_id):
        ret_val = False
        try:
            ret_val = self.libObj.link_two_issues(src_test_id, dest_test_id)
        except:
            print("Failed addding Test Plan")
        return ret_val


    def update_test_execution(self,test_execution_id,os,build):
        ret_val = False
        try:
            ret_val = self.libObj.update_test_execution(test_execution_id,os,build)
        except:
            print("Failed updating execution status")
        return ret_val

    def update_test_run_status(self,test_run_id,status,assignee):
        ret_val = False
        try:
            ret_val = self.libObj.update_test_run_status_for_test(test_run_id,status,assignee)
            print("ret_val = " + str(ret_val))
        except:
            print("Failed updating execution status")
        return ret_val


    def associate_test_to_testPlan(self,test_key,test_plan_key):
        data = {"add" : ["%s" %test_key]}
        try:
            res = self.libObj.send_post("xray","testplan/%s/test" %test_plan_key,data)
            if(res):
                res_val = json.loads(res.text)
                print(res_val)
        except:
            print("Failed adding test to testPlan ...")

    def associate_test_exec_to_testPlan(self,test_exec,test_plan_key):
        data = {"add" : ["%s" %test_exec]}
        try:
            res = self.libObj.send_post("xray","testplan/%s/testexecution" %test_plan_key,data)
            if(res):
                res_val = json.loads(res.text)
                print(res_val)
        except:
            print("Failed adding test execution to testPlan ...")


    def associate_test_to_testSet(self,test_key,test_set_key):
        data = {"add" : ["%s" %test_key]}
        try:
            res = self.libObj.send_post("xray","testset/%s/test" %test_set_key,data)
            if(res):
                res_val = json.loads(res.text)
                print(res_val)
        except:
            print("Failed adding test to testSet ...")


    def associate_test_to_testExecution(self,test_key, test_exec_key):
        data = {"add" : ["%s" %test_key]}
        try:
            res = self.libObj.send_post("xray","testexec/%s/test" %test_exec_key,data)
            if(res):
                res_val = json.loads(res.text)
                print(res_val)

        except:
            print("Failed adding test to testExecution ...")


    def get_test_run_id(self, test_exec_id,test_id):
        try:
            res = self.libObj.send_get("xray","testrun?testExecIssueKey={}&testIssueKey={}".format(test_exec_id,test_id) )
            if(res):
                res_val = json.loads(res.text)
                print(res_val)
                key_val = res_val['id']
                return key_val
        except:
            print("Failed creating issue in Jira")


    def run_query(self, jql):
        import requests
        try:
            jql = requests.utils.quote(jql)
            res = self.libObj.send_get("def", "search/?jql={}".format(jql))
            if (res):
                res_val = res.json()
                return res_val
        except:
            print("Failed creating issue in Jira")


    def check_if_issue_exists(self, name, issue_type):
        ret_val = ""
        try:
            jql = "project=%s AND issuetype='%s'" %(global_cfg.def_jira_proj,issue_type)
          #  print("jql=" + str(jql))
            data = self.run_query(jql)
          #  print("data = " + str(data))
            all_issues = data['issues']
            for issue in all_issues:
                info_dict = {'Id': "", 'Summary': ""}
                info_dict['Id'] = issue['key']
                info_dict['Summary'] = issue['fields']['summary']
                if(name in info_dict['Summary']):
                    ret_val = info_dict['Id']
                    break

        except:
            print("Failed checking issue")
        return ret_val
