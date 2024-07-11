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

import re,os,sys,glob,time
from operator import itemgetter

import random
import PIL
from PIL import ImageFont
from pytesseract import image_to_string
from PIL import Image
from PIL import ImageDraw, ImageFilter

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

    def search_field_in_string(self,field,search_str):
        bresult = False
        volume_str_info = re.search(r'%s'%field, search_str)
        if (volume_str_info):
            ser_str = volume_str_info.group(0)
            if(ser_str == field):
                bresult = True
        return bresult

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
    # are required for report and also the same to be uploaded to Browserstack
    def sort_builds(app_builds):
        sorted_list = sorted(app_builds, key=itemgetter(0))
        return sorted_list

    def formulate_err_msg(self,test_name,exp_screen):
        return test_name + " failed expected screen with label " + exp_screen + " not found"

    def generate_new_image_file(self, file_name):
        nouns = ["Peacock", "Crow", "Rabbit", "Bear", "Pig", "Wolf", "Tiger", "Lion", "Elephant", "Bobcat", "Racoon",
                 "Hummingbird", "Sparrow", "Pigeon", "Eagle", "Vulture", "Ostrich"]
        verbs = ["Jumps", "Runs", "Blows", "Laughs", "Humps", "Hits", "Dumps", "Glides", "Drags", "Leaps", "Fumbels",
                 "Digs", "Sits", "Pumps", "Slacks", "Falls", "Speeds", "Nags", "Growls", "Whines", "Enjoys"]
        Adverbs = ["Slowly", "Merrily", "Lovingly", "Gracefully", "TactFully", "Carefully", "Blissfully", "Slowly",
                   "Hastily", "Timely", "Awfully", "Playfully", "Cutely", "Momentarily", "Sadly", "Abnoxiously"]
        sentence = random.choice(nouns) + " " + random.choice(verbs) + " " + random.choice(Adverbs)
        font = ImageFont.truetype("/Library/Fonts/Apple Chancery.ttf", 350)

        img = Image.new("RGBA", (600, 600), (random.choice((0, 255)), random.choice((0, 255)), random.choice((0, 255))))
        draw = ImageDraw.Draw(img)
        draw.text((10, 100), '%s' % sentence,
                  (random.choice((0, 255)), random.choice((0, 255)), random.choice((0, 255))), font=font)
        draw.chord((100, 75, 125, 100), 0, 360, fill='green')
        draw.chord((75, 100, 100, 125), 0, 360, fill='blue')
        draw.chord((125, 125, 150, 150), 0, 360, fill='yellow')
        draw.chord((125, 125, 150, 150), 0, 360, fill='yellow')
        draw = ImageDraw.Draw(img)
        img.save(file_name)
        time.sleep(2)

    def modify_file_filter(self,file_name):
        im = Image.open(file_name)
        im_sharp = im.filter(ImageFilter.SHARPEN)
        im_sharp.save(file_name)
        time.sleep(2)


    def modify_file_size(self, file_name,width, height):
        im = Image.open(file_name)
        im_sharp = im.resize(1025,1280)
        im_sharp.save(file_name)
        time.sleep(2)

    def fork_process(self, cmd, fname):
        try:
            fh = open(fname, 'wb')
            subprocess.Popen(str(cmd).split(' '), stdout=fh)
            fh.close()
        except:
            print("Failed forking process...")
