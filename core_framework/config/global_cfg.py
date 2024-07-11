__author__ = 'asanghavi'

from os.path import expanduser
from core_framework.config import params

from core_framework.commons.testrail import *
#from appium import webdriver

from pathlib import Path
import os

('\n'
 'All the static parameters which all the framework needs update can go here.\n'
 'Params are run time parameteres but these are static.\n'
 '\n'
 )

import os, sys, re, random,bz2,datetime

home                        = ""
home_name                   = home.split('/')
home_folder_name            = "Auto"
file_ext                    = "/*.png"
nums_str                    = '0123456789'
max_len                     = 3
letters_str_sm              = 'abcdefghijklmnopqrstuvwzyz'
letters_str_mixed           ='abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters_num_str             = 'abcdefghijklmnopqrstuvwzyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

file_out_str                = [random.choice(letters_str_sm) for _ in range(int(max_len))]
rand_str_info               = [random.choice(nums_str) for _ in range(int(max_len))]
rand_str                    = "".join(rand_str_info)
tmp_out                     = "".join(file_out_str) + ".txt"

d                           = datetime.date.today()
version                     = "1.0.0"
build                       = ""

i                           = datetime.datetime.now()
file_name                   = ""

log_config_path             = '../../coreFramework/config/log.config'

('\n'
 '########################################################################################################################\n'
 '\n'
 'Section below lists all the TestRail config.\n'
 '\n'
 '########################################################################################################################\n'
 )




client                          = APIClient('https://testrail.blackpearlsystems.com/')

client.email                    = params.testrail_user
client.password                 = params.testrail_pass
smtp_host                       = "mailhost.seagate.com"

sender_email                    = "alpa.sanghavi@seagate.com"
link_url                        = "http://localhost/"
#link_url                        = "http://10.24.67.155/"
status_local                     = ""
test_image_name                  =""
html_file_path                   = "report\\results\\"
html_file_path_dir               = "report\\results\\"

docs_path                        = "docs\\"
logs_path                        = "logs\\"
main_rep_template_file           = "..\\..\\tests\\configs\\templates\\report\\rep_template.html"

test_per   = ""
lin_info                         = "For detailed HTML report, please click on the link below..."

link_info                        = "For detailed HTML report, please click on the link below..."
userId                           = 16
project_id                       = 28
section_id                       = 0
run_all                          = True
test_list                        = []
run_id                           = 0
id                               = 0
status_fail                      = 5
status_pass                      = 1
master_suite_id                  = 0
test_pass_comm                   = "Test Passed"
test_fail_comm                   = "Test Failed"
test_comm                        = ""
testrail_title                   = "'testrail'"
testrun_url                      = "https://.testrail.net/index.php?/runs/view/"
test_info_list                   = []
test_info_dict                   = {}
test_results_list                = []
test_result_dic                  = {"results":test_info_list}
crash_log                       = {"fname" : ""}
def_jira_proj                    = "OPAUTO"
build_in_test                    = {'build' : "latest"}
ids                              = {"test_plan_id" : "", "test_set_id" : "","test_id" : "", "test_exec_id" : "", "test_run_id" : ""}
html_ext                         = ".html"
html_report_ext                  = " Report"
run_name_ext                     ="_" + d.strftime('%Y-%m-%d-')+str(i.hour) + ":"+ str(i.minute) +":"+ str(i.second)
total_tests                      = 0
tests_failed                     = 0
tests_passed                     = 0
suite_id                         = 0
logger_flag                      = False
log_file                         = "logs/auto_test.log"
reporter_flag                    = False
img_file_ext                     = "*.jpg"
all_failed_per                   = "0"
start_server_macosx              = "open /Applications/AppiumForMac.app/"
stop_server_macosx               = "sudo pkill -f 'AppiumForMac'"
start_server_mac_script_path     = "../../coreFramework/platforms/MacOSX/helpers/"
master_report_file               = "mas"
test_details_pattn               = 'TEST_DETAILS'
test_report_pattn                = 'TEST_REPORT'
test_report_name_pattn           = "REPORT_NAME"
rep_template_path                = "..\\..\\tests\\configs\\templates\\report\\rep_template.html"


kwargs                      = {"output": 'results',"report_name": params.suite_name + "", "failfast": False, "report_title" : "Tests for ", "stream":sys.stdout}
path                        = "../suites/"
clean_up                    = "del report\\results\\*.html"
clean_up_logs               = os.popen("rm -f logs/auto_test*").read()

out                         = os.popen(clean_up).read()

setup_done                  = False
setup_info                  = {'status' : False }

curr_suite_name             = {'name' : ''}
current_suite_info          = {'name' : '%s' %curr_suite_name}

driver_info                 = {'obj' : None}

charts_build_info_list      = []
charts_build_info           = {'fname' : '', 'cl_name' : ''}



##########################LOCALIZATION############################################################
list_of_langs               = ['en','jp']
locales                     = {'jp':'jp_JP', 'en' : 'en_EN'}
en_list                     = []
labels                      = []
glob_loc_dic                = []
msgs                        = []

by_xpath                                = "xpath"
by_id                                   = "id"
by_par_link                             = "parlink"
by_css_selector                         = "css"
by_class_name                           = "class_name"
by_input_name                           = "name"
def_wait_time                           = 3
max_timeout                             = 60
counter                                 = 0
PATH                                    = lambda p: os.path.abspath(os.path.join(os.getcwd(), p))
desired_caps                            = {}
if(params.platform == "Android"):
 desired_caps['automationName']         = 'UiAutomator2'
 desired_caps['platformName']            = params.platform
 desired_caps['platformVersion']         = params.platformVersion
 desired_caps['deviceName']              = params.device_name
 desired_caps['app']                     = PATH(params.app_path)
desired_caps['newCommandTimeout']       = 120
drive_name1                             = "AutoTest"
drive_name2                             = "SDAuto"
format_drive_cmd                        = "diskutil eraseDisk ExFAT DiskName /dev/{}"

disk_info_cmd                           = "diskutil list"
disk2_rename                            = "diskutil rename DiskName  SDAuto"
disk3_rename                            = "diskutil rename DiskName  AutoTest"
setup_info['status']                    = False
curr_drive_path                         = ""
platform_mac                            = "mac"
platform_windows                        = "windows"
platform_android                        = "android"
platform_android_wifi                   = "android_wifi"
mac_elm_type_checkbox                   = "checkboxes"
mac_elm_type_button                     = "buttons"
mac_elm_type_textField                  = "textFields"
mac_elm_type_combobox                   = "comboBoxes"
mac_elm_type_static_text                = "staticTexts"
mac_elm_type_textAreas                  = "textAreas"
mac_elm_type_images                     = "images"
temp_var                                = ""
op_type_add                             = "add"
op_type_subtract                        = "subtract"
clicked_button_label                    = "Clicked on button "
entered_text_label                      = "Entered text "
checked_checkbox_label                  = "Clicked on checkbox "
clicked_on_label                        = "Clicked on "
clicked_on_drive_label                  = "Clicked on the drive with label "
failed_clicking_on_button               = "Failed clicking on the button with label "
failed_clicking_checkbox                = "Failed clicking on the checkbox "
failed_clicking_drive_label             = "Failed clicking on the drive with label "
failed_clicking_on                      = "Failed clicking on label "
failed_entering_text                    = "Failed entering text "
failed_finding_button                   = "Failed finding button with label "
failed_finding_label                    = "Failed finding label "
failed_finding_checkbox                 = "Failed finding checkbox "
failed_finding_screen                   = "Failed finding screen with label "
start_app_msg                           = "Starting application "
found_label                             = "Found match on the screen for label "
################################# WEB DRIVER INSTANCE #################################################
app_path                                = ""
desired_caps                            = {}
driver                                  = None
driver_instance                         = {'driver': driver}
application_in_test                     = {'app_name' : ""}
match_status                            = {'match' : False}
winapp_driver                           = "C:\\Program Files (x86)\\Windows Application Driver\\WinAppDriver.exe"

################################# TELEMETRY #############################
op_dump_file                          = "C:\\Users\\534026\\optimus_win_auto\\tests\\op_dump.txt"
request_type                            = "Optimus"
req_payload                             = None
device_id                               = "0000NL3P00AM"
partition_id                            = "E:"
deet_client_id                          = "63ee9120-e88f-4a5b-a34d-76ce2a636233"
deet_module_version                     = "1.4.0.138"
deet_request_ts                         = 1578349660091
deet_timestamp                          = 1578349558949
deet_request_type                       = "DEET"

############## For IMPORT ######################################
slurpee_dump_file                       = "C:\\Users\\534026\\csg_automation_win\\tests\\dump_slurpee2.txt"
request_type                            = "Slurpee"
request_ts                              = 1579199288864
timestamp                               = 1579199395605
client_id                               = "63ee9120-e88f-4a5b-a34d-76ce2a636233"
module_version                          = "2.1.0.12"
manufacturer                            = "LaCie"
is_incremental                          = False
model                                   = "LaCie Rugged RAID Pro Drive"
serial_number                           = "NL3P00AM"
source_type                             = "SD"
import_status                           = "Success"
files_imported                          = 354
import_id_for_report                    = "c6128168-d7ce-417d-93ab-133c9f8b4828"
import_id                               = "d211fec7-e1a5-4d8c-9413-0f07c4e2d567"
file_type                               = ".jpg"
internal_drive                          = False
is_os_volume                            = False
partition_name                          = "No Name"
ordinal                                 = 1

############################ Localization ##################################

dict_locale                            = {}
dict_omni_locale                       = {}
dict_smartcard_locale                  = {}







