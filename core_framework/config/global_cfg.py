__author__ = 'asanghavi'

from os.path import expanduser
from core_framework.config import params

from core_framework.commons.testrail import *


('\n'
 'All the static parameters which all the framework needs update can go here.\n'
 'Params are run time parameteres but these are static.\n'
 '\n'
 )

import os, sys, re, random,bz2,datetime



home                        = expanduser("~")
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


password_file                  =  home + "/mypass.txt"

client                          = APIClient('https://testrail.blackpearlsystems.com/')

client.email                      = "alpa.sanghavi@seagate.com"
#bfhr                            = bz2.BZ2File(password_file,'rb')
#my_password                     = bfhr.read()
#bfhr.close()
my_password                     = str.encode("Test1234!")
#decompressed                    = bz2.decompress(my_password)
client.password                 = 'Test1234!'
smtp_host                       = "mailhost.seagate.com"

sender_email                    = "alpa.sanghavi@seagate.com"
link_url                        = "http://localhost/"
#link_url                        = "http://10.24.67.155/"
status_local                     = ""
test_image_name                  =""
test_per   = ""
lin_info                        = "For detailed HTML report, please click on the link below..."

link_info                        = "For detailed HTML report, please click on the link below..."
userId                          = 16
project_id                      = 28
section_id                      = 0
run_all                         = True
test_list                       = []
run_id                          = 0
id                              = 0
status_fail                     = 5
status_pass                     = 1
master_suite_id                 = 0
test_pass_comm                  = "Test Passed"
test_fail_comm                  = "Test Failed"
test_comm                       = ""
testrail_title                  = "'testrail'"
testrun_url                     = "https://.testrail.net/index.php?/runs/view/"
test_info_list                  = []
test_result_dic                 = {"results":test_info_list}
html_ext                        = ".html"
html_report_ext                 = " Report"
run_name_ext                    ="_" + d.strftime('%Y-%m-%d-')+str(i.hour) + ":"+ str(i.minute) +":"+ str(i.second)
total_tests                     = 0
tests_failed                    = 0
tests_passed                    = 0
suite_id                        = 0
logger_flag                     = False
log_file                        = "logs/auto_test.log"
reporter_flag                   = False
img_file_ext                    = "*.jpg"
all_failed_per                  = "0"
start_server_macosx             = "open /Applications/AppiumForMac.app/"
stop_server_macosx              = "sudo pkill -f 'AppiumForMac'"
start_server_mac_script_path    = "../../coreFramework/platforms/MacOSX/helpers/"


kwargs                      = {"output": 'results/',"report_name": params.run_name,"failfast": False, "report_title" : "Tests for ","stream":sys.stdout}
path                        = "../suites/"
clean_up                    = "rm -rf reports/results/*.html"
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

by_xpath                                = "xpath"
by_id                                   = "id"
by_par_link                             = "parlink"
by_css_selector                         = "css"
by_class_name                           = "class_name"
by_input_name                           = "name"
def_wait_time                           = 3
max_timeout                             = 60
PATH                                    = lambda p: os.path.abspath(os.path.join(os.getcwd(), p))
desired_caps                            = {}
desired_caps['platformName']            = params.platform
desired_caps['platformVersion']         = params.platformVersion
desired_caps['deviceName']              = params.device_name
desired_caps['app']                     = PATH(params.app_path)
if(params.platform == "Android"):
 desired_caps['automationName']         = 'UiAutomator2'
desired_caps['newCommandTimeout']       = 120
format_drive_cmd                        = "diskutil eraseDisk ExFAT DiskName /dev/{}"
disk_info_cmd                           = "diskutil list"
disk2_rename                            = "diskutil rename DiskName  AutoTest"
disk3_rename                            = "diskutil rename DiskName  SDAuto"
setup_info['status']                    = False
platform_mac                            = "mac"
platform_windows                        = "windows"
platform_android                        = "android"
platform_android_wifi                   = "android_wifi"


######################################################################################################
launch_app                              = ["proc = Application(%s);" %params.app_name, "proc.activate();"]
close_app                               = ["proc = Application(%s);" %params.app_name, "proc.quit();"]


app_base_path                           = "/AXApplication[@AXTitle='%s']/AXWindow[@AXTitle='%s']/" % (params.app_name, params.app_name)

################################# WEB DRIVER INSTANCE #################################################
driver                                  = None
driver_host                             = 'http://localhost:4622/wd/hub'





