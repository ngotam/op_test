'''
#######################################################################################################################


Module Name : utils
Purpose     : Provide common functionality needed by other core_tiers.
Role        : Common base utilities for framework.


#######################################################################################################################


'''
__author__ = 'asanghavi'

import sys,os,subprocess,imaplib,email
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PIL import Image

import re,os,sys,glob,time
from pytesseract import image_to_string
from operator import itemgetter

import random


class utils():

    def __init__(self):
        pass

    def read_contents_from_file(self,arg1):
        """

        :rtype : list
        """
        data = []
        with open(arg1, "r") as debug_info:
            data = debug_info.readlines()
        return data



    def captureReport(self,fName,title):
        """
        role: captures current screen of a given application
        :param file name
        :rtype : None
        """

        cmd_rm = 'rm -f *.png'
        cmd_open = 'open %s' %fName
        self.execute_cmd(cmd_rm)
        self.execute_cmd(cmd_open)
        time.sleep(10)
        app_name = 'Safari'
        app_name = '"' + app_name + '"'
        cmd_cap = "screencapture -l$(osascript -e 'tell app %s to id of window 1') testReport.jpg" %app_name
        print(cmd_cap)
        self.execute_cmd(cmd_cap)


    def killChromeWindow(self,app_name):
        """
        :param application name
        :role: Terminates a given application
        :rtype : None
        """

        cmd_rm = 'killall -9 "%s"' %app_name
        self.execute_cmd([cmd_rm])

    def parseContentsFromScreen(self,fName):
        """
        :param : Image file name
        :rtype : list
        role: Opens the input image file and parses text from it
        """
        labels_screen = []
        if(os.path.isfile(fName)):
            image  = Image.open(fName)  # Open image object using PIL
            my_out = image_to_string(image)
            labels_screen = my_out.split('\n')
        return labels_screen

    def copyReportToServer(self,fName):
        """
        :param1 : Html report file
        :param2 : file_name with a given run_id
        :role: Copies generated report to documents directory of local webserver
        :rtype : None
        """
        if(os.path.isfile(fName)):
            cmd_rm = "sudo rm -f /Library/WebServer/Documents/%s" %fName
            self.execute_cmd(cmd_rm)
            cmd_cp = "sudo cp %s /Library/WebServer/Documents/" %fName
            out = os.popen(cmd_cp).read()
            print(cmd_cp)
            #cmd_cp2 = "sudo cp %s /Library/WebServer/Documents/%s" %(fName,fname_with_runid)
            #out = os.popen(cmd_cp2).read()
            #print(out)

    def execute_cmd(self,cmd):
        out = os.popen(cmd).read()
        return out

    def execute_list_of_cmds(self,cmd_list):
        for cmd in cmd_list:
            out = os.popen(str(cmd)).read()


    def append_to_file(self,arg1,arg2):
        """
        :param arg1:handle to file to be written
        :param arg2:message to be written
        """
        with open(arg1, "a") as arg1:
            arg1.write(arg2 + "\n")


    def searchInFile(self,arg1,arg2):
        """
        :role searches for a given field in the file and returns string
        :param arg1:file_name where field has to be searched
        :param arg2:search_field
        :rtype string
        """

        data = self.read_contents_from_file(arg1)
        line_str = ""
        for line in data:
            if arg2 in line:
                line_str = line
                break
        return line_str

    def searchInFileAndReturnBool(self,arg1,arg2):
        """
        :role searches for a given field in the file and returns boolean
        :param arg1:file_name where field has to be searched
        :param arg2:search_field
        :rtype boolean
        """
        data = self.read_contents_from_file(arg1)
        bFound = False
        for line in data:
            if arg2 in line:
                bFound = True
                break
        return bFound

    def searchInFileAndReturnList(self,arg1,arg2):
        """
        :role searches for a given field in the file and returns list
        :param arg1:file_name where field has to be searched
        :param arg2:search_field
        :rtype list
        """
        err_list = []
        with open(arg1,'r') as debug_data:
            data = debug_data.readlines()

        for line in data:
            if(arg2 in data):
                err_list.append(line)

        return err_list


    def write_contents_to_file(self,contents,arg1):
        """
        :type contents: expects a list object
        :type arg1:file with absolute path
         :rtype: None
        """
        fh = open(arg1,'w')
        assert isinstance(contents,list)
        for line in contents:
            fh.write(str(line))
            fh.flush()
        fh.close()



    def redirectDeviceLogs(self,file_path,procName):
        fh = open(file_path,'wb')
        p = subprocess.Popen([procName], stdout=fh, shell=True)


    def generate_unique_ids(self,max_len,type):
        letters_str_mixed   = 'abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letters_num_str     = 'abcdefghijklmnopqrstuvwzyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        nums_str            = '0123456789'

        my_id = ""
        if type == "mixed":
            my_id = [random.choice(letters_num_str) for _ in range(int(max_len))]
        elif type == "num":
            my_id = [random.choice(nums_str) for _ in range(int(max_len))]
        elif type == "letters":
            my_id = [random.choice(letters_str_mixed) for _ in range(int(max_len))]

        return "".join(my_id)


    def getMyName(self):
        return sys._getframe(1).f_code.co_name

    def kill_process_by_name(self,process_name):
        cmd = 'sudo pkill -f %s' %process_name
        self.execute_cmd(['%s'%cmd])


    def does_file_exists_with_name_in_dir(self,filename):
        file_list = glob.glob(filename)
        if(len(file_list) >= 1):
            return True
        else:
            return False

    # Sort given builds list needed for reporting
    # are required for reports and also the same to be uploaded to Browserstack
    def sort_builds(app_builds):
        sorted_list = sorted(app_builds, key=itemgetter(0))
        return sorted_list


