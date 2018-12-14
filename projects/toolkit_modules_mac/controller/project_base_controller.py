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

__author__ = 'asanghavi'

from core_framework.config import global_cfg, params
import json,requests,re,os,base64
from projects.toolkit_modules_mac.config import project_params
import time
from core_framework.controller import mac_ui_controller
from Crypto.Cipher import AES


class projects_base_controller:

    curr_feed_url   = None
    feed_info       = None
    macuiConObj     = None

    def __init__(self):
        self.curr_feed_url  = ""
        self.feed_info      = {}
        self.macuiConObj    = mac_ui_controller.mac_ui_controller()

        with open(project_params.ini_file_loc, 'r') as debug_info:
            file_info = debug_info.readlines()
        str_info = "".join(file_info)

        feed_info = json.loads(str_info)
        print(feed_info)

    def setup_build(self):
        self.cleanup_builds()

        if(params.feed_url):
            self.curr_feed_url = params.feed_url
        else:
            try:
                res = requests.get(project_params.index_page_for_builds)
                ret_val = re.findall(r'ini_file_pattern',res.json())
                self.curr_feed_url = ret_val[0]
            except:
                print("Cannot access build info page")
        self.feed_info['ApplicationUpdate'] = self.curr_feed_url
        print(self.feed_info)
        self.update_TestServerForOmni(self.feed_info)
        self.setup_installer()
        time.sleep(5)
        self.install_toolkit()



    def update_TestServerForOmni(self,feed_info):
        fh = open(project_params.ini_file_loc, 'w')
        fh.write(json.dumps(feed_info))
        fh.close()

    def get_sys_password(self):
        encoded = b'nLO+UG1KcsKYI9WEHAKHmIkPElQfwMLAttt+DmjrbBA='

        cipher = AES.new(os.environ.get('CSG_KEY'), AES.MODE_ECB)

        decoded = cipher.decrypt(base64.b64decode(encoded))
        pass_bytes = decoded.strip()
        sys_password = pass_bytes.decode("utf-8")
        return sys_password

    def uninstall_toolkit(self):
        self.macuiConObj.change_current_application_in_test("System Preferences")
        self.macuiConObj.click_on_button_by_text("Toolkit")
        time.sleep(3)
        self.macuiConObj.click_on_button_by_text("Uninstall")
        time.sleep(1)
        self.macuiConObj.click_on_button_by_text("OK")
        time.sleep(2)
        my_password = str(self.get_sys_password())
        time.sleep(2)
        self.macuiConObj.enter_system_password(my_password)





    def cleanup_builds(self):
        self.macuiConObj.quit_application("Toolkit")
        time.sleep(5)
        self.macuiConObj.quit_application("System Preferences")
        self.uninstall_toolkit()
        print("Removing app contents {}".format(project_params.cmd_rm_app))
        out = os.popen(project_params.cmd_rm_app).read()
        print(out)

        out1 = os.popen(project_params.cmd_rm_file).read()
        print(out1)
        if(os.path.isdir(project_params.app_path)):
            project_params.uninstall_status['status'] = False
        else:
            project_params.uninstall_status['status'] = True

        self.format_connected_drive()
        os.popen(global_cfg.disk3_rename).read()
        os.popen(global_cfg.disk2_rename).read()
        self.macuiConObj.click_on_decide_later_alert()




    def setup_installer(self):
        try:

            res = requests.get(self.curr_feed_url)
            info = res.text
            res_info = info.split('\n')
            for line in res_info:
                if(project_params.lacie_toolkit_installer_pattern in line):
                    print(line)
                    url_info = re.search(r'https.*',line)
                    url = url_info.group(0)
                    url = url.rstrip('\r')
                    cmd_dld = "curl {} -o {}".format(url,project_params.toolkit_installer_file)
                    out = os.popen(cmd_dld).read()
                    print(out)
                    if(os.path.isfile(project_params.toolkit_installer_file)):
                        project_params.build_download_status['status'] = True

                    cmd_mv = "mv -f {} {}".format(project_params.toolkit_installer_file,project_params.destn_folder_toolkit_installer)
                    os.popen(cmd_mv)
                    curr_dir = os.getcwd()
                    os.chdir(project_params.destn_folder_toolkit_installer)
                    cmd_unzip = "unzip {}".format(project_params.toolkit_installer_file_Apps)
                    os.popen(cmd_unzip).read()
                    os.chdir(curr_dir)
                    if(os.path.isfile(project_params.build_download_path)):
                        project_params.build_download_status['status'] = True
                    else:
                        project_params.build_download_status['status'] = False


        except:
            print("Cannot access build info page")




    def install_toolkit(self):


        self.macuiConObj.change_current_application_in_test("LaCie Toolkit Installer")
        self.macuiConObj.start_application("LaCie Toolkit Installer")
        time.sleep(10)
        self.macuiConObj.click_on_button_by_index(4)
        time.sleep(10)
        self.macuiConObj.click_on_button_by_text("Continue")

        time.sleep(3)
        if(os.path.isdir(project_params.app_path)):
            project_params.install_status['status'] = True
        else:
            project_params.install_status['status'] = False


    def get_connected_sd_card_name(self):
        sd_card_name = self.get_connected_devices_info(params.sd_card_name)

    def get_connected_drive_name(self):
        return self.get_connected_devices_info(params.drive_name)

    def get_connected_devices_info(self,field):
        device_list = []
        out = os.popen(global_cfg.disk_info_cmd).read()
        disk_info = out.split('\n')
        for line in disk_info:
            if (("(external, physical)" in line)):
                out = re.findall(r'disk\w+', line)
                if(out):
                    name = out[0]
                    device_list.append(name)
        return device_list


    def format_connected_drive(self):
        device_list = self.get_connected_devices_info(params.drive_name)
        for item in device_list:

            format_cmd = global_cfg.format_drive_cmd.format(item)
            print("Formating drive....{} please wait#####".format(item))
            time.sleep(10)
            out = os.popen(format_cmd).read()
            print(out)


    def validate_uninstall_toolkit(self):
        ret_val = True
        out = os.popen("ls /Applications/").read()
        if("Toolkit.app" in out):
           ret_val = False

        return ret_val


    def validate_toolkit_build_download(self):
        return  project_params.build_download_status['status']

    def get_uninstall_toolkit_status(self):
        return True


    def validate_install_toolkit(self):
        return  project_params.install_status['status']






























