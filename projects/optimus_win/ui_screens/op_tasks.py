import time, os, shutil
import requests, warnings
import glob, os.path, filecmp
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto import timings, mouse, keyboard
from pywinauto.keyboard import send_keys
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.controls.uia_controls import ButtonWrapper
from pywinauto.controls.uia_controls import TooltipWrapper
from projects.optimus_win.config import op_params as params
from projects.optimus_win.config import project_params as project_params
from selenium.common.exceptions import NoSuchElementException
from core_framework.config import global_cfg
from pywinauto.controls.uia_controls import EditWrapper
from datetime import datetime
from zipfile import ZipFile
#import win32file


def verify_dashboard(op):
    status = False
    try:
        dashboard = op.DashboardCustom
        list = get_list_notificatiions(op)
        if ( list != []):
            status = True
        else:
            global_cfg.msgs.append("fail to get list of notifications")
        return status
    except:
        raise ValueError("get exception on verify dashboard")

def click_Exit_app(op):
    status = False
    try:
        click_Lyve_menu(op)
        op.child_window(title="Lyve Client", control_type="MenuItem").click_input()
        exit = op.child_window(title="Exit", control_type="MenuItem")
        if ( exit.is_visible()):
            exit.click_input()
            status = True
        if ( not status ):
            global_cfg.msgs.append("fail to Exit app")
        return status
    except:
        raise ValueError("get exception on click Exit")

def click_Lyve_menu(op):
    hyperlink = op.HyperLink1
    rect = hyperlink.rectangle()
    mouse.move(coords=(rect.left, rect.top))

def click_About(op):
    status = False
    try:
        click_Lyve_menu(op)
        op.child_window(title="Lyve Client", control_type="MenuItem").click_input()
        about = op.child_window(title="About", control_type="MenuItem")
        if ( about.is_visible()):
            about.click_input()
            status = True
            version = op.child_window(auto_id="ContentText")
            print("version = " + version.window_text())
            time.sleep(2)
            op.child_window(title="Close", control_type="Button", found_index=1).click_input()

        if ( not status ):
            global_cfg.msgs.append("fail to click About")
        return status
    except:
        raise ValueError("get exception on click About")

def click_Terms_and_Conditions(op):
    status = False
    try:
        op.Documents.dump_tree()
        term = op.child_window(title="Terms and Conditions", control_type="Hyperlink")
        if ( term.is_visible()):
            term.click_input()
            status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click Terms and Conditions")
        return status
    except:
        raise ValueError("get exception on click Terms and Conditions")

def verify_workflow_notification(op, name, action):
    status = False
    try:
        time.sleep(3)
        down = False
       # op.Document.dump_tree()
        titleNotfiy = name + " " + action
        print("title = " + titleNotfiy)
        notifyWd = op.child_window(title=titleNotfiy, control_type='Text', found_index=0)
        visible = op.child_window(title=titleNotfiy, control_type='Text', found_index=0, visible_only=False).is_visible()
        if (not visible):
            scroll_half_down(op)
            down = True
        if ( notifyWd.is_visible()):
            print("get correct workflow notification")
            status = True
        else:
            msg = "Title notification {} not visible".format(titleNotfiy)
            global_cfg.msgs.append(msg)
        if ( not status ):
            msg = "fail to verify workflow notification {}".format(titleNotfiy)
            global_cfg.msgs.append(msg)
        if ( down ):
            scroll_up(op)
        return status
    except:
        raise ValueError("get exception on verify workflow notification")

def move_to_system_notification(op):
    time.sleep(2)
    listWd = Desktop(backend='uia').windows()

    for w in listWd:
        print(w.window_text())
        if ( w.window_text() == "Lyve Client"):

            rect = w.rectangle()
            #mouse.move(coords=(rect.left+30, rect.top+50))
            mouse.move(coords=(rect.right-100, rect.bottom -50))
            print("mouse move to system notification")
            mouse.press(button='left', coords=(rect.right - 100, rect.bottom - 50))

        if ( w.window_text() == "New notification"):
            print("get notification")
            break

    '''''
    rect = op.Document.rectangle()
    mouse.move(coords=(rect.right-60, rect.bottom-30))
    print("mouse move to system notification")
    time.sleep(10)
    '''''

def verify_workflows_page(op):
    status = False
    try:
        time.sleep(1)
        dbTable = op.NameTable
        showMsg = op.Document.child_window(title_re='Showing', control_type='Text')
        if ( showMsg.is_visible()):
            print("show message = " + showMsg.window_text())
            status = True
        else:
            global_cfg.msgs.append("Not have message showing")
        listTxt = dbTable.descendants(control_type='Text')
        for li in listTxt:
            print (li.window_text())

        '''''
       
        title = op.child_window(title_re='Workflows', found_index=1)
        titleTxt = title.window_text()
        if ( titleTxt.__contains__("Workflows")):
            print("get correct title = " + titleTxt)
            status = True
        else:
            msg = "get wrong title {}".format(titleTxt)
            global_cfg.msgs.append(msg)
        listTitle = titleTxt.split('(')
        index = int(listTitle[1][0:1])
        wfTable = op.child_window(auto_id="WorkflowsTable", control_type='Table')

        for i in range(index):
            autoId = "rowID" + str(i)
            print("get dataItem in row = " + autoId)
            row = wfTable.child_window(auto_id=autoId, control_type='Custom')
            dataList = row.descendants(control_type='DataItem')
            for li in dataList:
                print(li.window_text())
        '''''

        return status
    except:
        raise ValueError("exception on verify workflows page")

def click_add_workflow(op):
    status = False
    try:
        time.sleep(2)
        if ( project_params.app_mode == "stage"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table

        rect = table.rectangle()
        print(rect)
       # mouse.click(button='left', coords=(rect.left + 20, rect.top-40))
        mouse.click(button='left', coords=(rect.left + 20, rect.top + 30))
        print("click Add workflow")
        time.sleep(1)
        status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click add workflow")
        return status
    except:
        raise ValueError("exception on click add workflow")

def click_create_workflow_from_activity(op):
    status = False
    try:
        time.sleep(1)
        create_wf = op.child_window(title="Create a workflow")
        if ( create_wf.is_visible()):
            create_wf.click_input()
        print("click Add workflow")
        time.sleep(1)
        status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click add workflow")
        return status
    except:
        raise ValueError("exception on click create workflow from activity")

def verify_welcome_workflow(op):
    status = False
    try:
        time.sleep(1)
      #  wfTitle = dbTable.WelcometoWorkflows
        wfTable = op.DevicesTable
       # wfTable.dump_tree()
        if ( wfTable.is_visible()):
            status = True
            print("title = " + wfTable.window_text())
        else:
            global_cfg.msgs.append("welcome workflow title not visible")

        listTxt = wfTable.descendants(control_type='Text')
        for li in listTxt:
            print(li.window_text())
        return status
    except:
        raise ValueError("exception on verify welcome workflow")

def click_do_not_show(op):
    status = False
    try:
        wfCustom = op.WelcometoWorkflowsCustom
        chbox = wfCustom.Edit
        chbox.click_input()
        print("click checkbox")
        status = True
        return status
    except:
        raise ValueError("exception on click do now show")

def verify_click_copy_option(op):
    status = False
    try:
      #  dlg = op.DashboardTable2
        dlg = op.DevicesTable

        copy = dlg.descendants(control_type="Image")[0]
        if ( copy.is_visible()):
            copy.click_input()
            print("click copy action")

            status = True
        else:
            global_cfg.msgs.append("Copy not visible")

        return status
    except:
        raise ValueError("exception on verify click copy option")

def verify_click_delete_option(op):
    status = False
    try:
        dlg = op.DevicesTable
        #op.dump_tree()
        delete = dlg.descendants(control_type="Image")[1]
        if ( delete.is_visible()):
            delete.click_input()
            print("click delete action")
            status = True
        else:
            global_cfg.msgs.append("Delete not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to click delete option")
        return status
    except:
        raise ValueError("exception on verify click delete option")

def verify_delete_workflow_preview(op):
    status = False
    try:
        status1 = status2 = False
       # table = op.DashboardTable2
        table = op.DevicesTable
        listTxt = table.descendants(control_type='Text')
        for li in listTxt:
            print(li.window_text())
        nextCus = table.child_window(title='Next', control_type='Text')
        backCus = table.child_window(title='Back', control_type='Text')
        if ( nextCus.is_visible()):
            print("get correct Next button")
            status1 = True
        else:
            global_cfg.msgs.append("Next is not visible")
        if ( backCus.is_visible()):
            print("get correct Back button")
            status2 = True
        else:
            global_cfg.msgs.append("Back not visible")
        if ( status1 and status2 ):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify delete workflow preview")
        return status
    except:
        raise ValueError("exception on verify delete workflow preview")

def verify_connected_devices(op, listDev):
    status = False
    try:
       # op.Document.dump_tree()
        cusDevice = op.DevicesTable
        listTxt = cusDevice.descendants(control_type='Text')
        listStr = []
        for li in listTxt:
            listStr.append(li.window_text())
        print("list device shown = " + str(listStr))
        setList =  set(listStr)
        setDev = set(listDev)
        setCommon = setList.intersection(setDev)
        if ( setCommon == setDev ):
            print("get correct all devices = " + str(listDev))
            status = True
        else:
            print("get wrong connected devices = " + str(listDev))
        return status
    except:
        raise ValueError("exception on verify connected devices")

def edit_workflow_name(op, name):
    status = False
    try:
        #table = op.DashboardTable2
        table = op.DevicesTable2
        title = table.Static0
        print("title = " + title.window_text())
        size = len(title.window_text())
        rect = title.rectangle()
        mouse.click(button='left', coords=(rect.right+15, rect.top))
        print("click Edit")
        time.sleep(1)
        title.type_keys("{BACKSPACE}" * size, with_spaces=True, set_foreground=False)
        title.type_keys(name, with_spaces=True, set_foreground=False)

        if ( table.Static0.window_text() == name):
            status = True
        else:
            msg = "fail to edit workflow name {]".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on edit workflow name")

def verify_select_sources(op, name, device):
    status = False
    try:
        #dbTable = op.DashboardTable2
        dbTable = op.DevicesTable2
        if (click_select_device(op, device)):
            listTxt = dbTable.descendants(control_type='Text')
            for li in listTxt:
                txt = li.window_text()
                #print(txt)
                if (txt == name):
                    print("get correct workflow = " + name)
            status = True
        if ( status ):
            dbTable.Next.click_input()
        else:
            msg = "fail to select source {]".format(device)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify select sources")

def verify_select_source_endpoint(op, name, device):
    status = False
    try:
       # op.Document.dump_tree()
        dbTable = op.DevicesTable2
        epTab = dbTable.child_window(title="External endpoint", control_type="Text")
        epTab.click_input()
        time.sleep(1)
        if (click_select_endpoint(op, device)):
            listTxt = dbTable.descendants(control_type='Text')
            for li in listTxt:
                txt = li.window_text()
                print(txt)
                if (txt == name):
                    print("get correct workflow = " + name)
            status = True
        if ( status ):
            dbTable.Next.click_input()
        else:
            msg = "fail to select source {]".format(device)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify select sources")

def verify_select_multi_sources(op, name, sourceList):
    status = False
    try:
        time.sleep(1)
        dbTable = op.DevicesTable2
        if (click_select_devices(op, sourceList)):
            listTxt = dbTable.descendants(control_type='Text')
            for li in listTxt:
                txt = li.window_text()
                print(txt)
                if (txt == name):
                    print("get correct workflow = " + name)
            status = True
        if ( status ):
            dbTable.Next.click_input()
        else:
            msg = "fail to select source"
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify select sources")

def click_select_devices(op, deviceList):
    status = False
    try:
        time.sleep(1)
        dbTable = op.DevicesTable2
       # dbTable.dump_tree()
        for src in deviceList:
            source = dbTable.child_window(title=src, control_type='Text')
            if ( source.is_visible()):
                rect = source.rectangle()
                mouse.click(button='left', coords=(rect.left + 10, rect.top + 40))
                print("select device = " + src)
                status = True
            else:
                msg = "source {} not visible".format(src)
                global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click select devices")

def click_select_endpoint(op, endpoint):
    status = False
    try:
        time.sleep(1)
        #dbTable = op.DashboardTable2
        dbTable = op.DevicesTable2

        source = dbTable.child_window(title="AWS S3", control_type='Text', found_index=0)
        if ( source.is_visible()):
            print("get source = " + source.window_text())
            rect = source.rectangle()
            #mouse.move(coords=(rect.left+15, rect.top+45))
            preview = dbTable.child_window(title="AWS S3", control_type='Text', found_index=1).exists(timeout=10)
            if ( preview ):
                mouse.click(button='left', coords=(rect.left+15, rect.top+85))
            else:
                mouse.click(button='left', coords=(rect.left + 15, rect.top + 45))

            print("select endpoint = " + endpoint)
            status = True
        else:
            msg = "source {} not visible".format(endpoint)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click select endpoint")

def click_select_device(op, device):
    status = False
    try:
        time.sleep(2)
        dbTable = op.DevicesTable2
        source = dbTable.child_window(title=device, control_type='Text', found_index=0)
        if ( source.is_visible()):
            print("get source = " + source.window_text())
            rect = source.rectangle()
            mouse.move(coords=(rect.left+15, rect.bottom+25))
            #dbTable.dump_tree()
            if ( device == "LaCie Rugged SSD"):

                visible = dbTable.child_window(title="Disconnected", control_type='Text').exists(timeout=10)
                print("visible = " + str(visible))
                if ( not visible ):
                    print("get device disconnected")
                    mouse.click(button='left', coords=(rect.left + 10, rect.bottom + 35))
                else:
                    mouse.click(button='left', coords=(rect.left + 10, rect.bottom + 70))
            else:
                mouse.click(button='left', coords=(rect.left + 10, rect.bottom + 35))

            print("select device = " + device)
            status = True
        else:
            msg = "source {} not visible".format(device)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click select device")
"""""
def click_select_endpoint(op, device):
    status = False
    try:
        time.sleep(1)
        dbTable = op.DevicesTable2
       # dbTable.dump_tree()
        source = dbTable.child_window(title=device, control_type='Text')
        if ( source.is_visible()):
            print("get source = " + source.window_text())
            rect = source.rectangle()
            print(rect)
            #mouse.move(coords=(rect.left+10, rect.top+50))
            mouse.click(button='left', coords=(rect.left - 50, rect.top))
            print("select device = " + device)
            status = True
        else:
            msg = "source {} not visible".format(device)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click select endpoint")
"""""
def verify_select_destination(op, name, device):
    status = False
    try:
        dbTable = op.DevicesTable2
        if (click_select_device(op, device)):
            listTxt = dbTable.descendants(control_type='Text')
            for li in listTxt:
                txt = li.window_text()
            #    print(txt)
                if (txt == name):
                    print("get correct workflow = " + name)
                    break
            status = True
        if (status):
            dbTable.Next.click_input()
        else:
            msg = "fail to select destination {}".format(device)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify select destination")

def verify_select_files(op, select):
    status = False
    try:
        dbTable = op.DevicesTable2
        #dbTable.dump_tree()
        if ( select == "All Files" ):
            allFiles = dbTable.RadioButton1
            if ( allFiles.is_visible()):
                if ( not allFiles.is_selected()):
                    allFiles.click_input()
                    print("select option = " + select)
                else:
                    print("already select = " + select)
                status = True
            else:
                print(select + " not visible")
                msg = "{} not visible".format(select)
                global_cfg.msgs.append(msg)
        elif ( select == "New Files" ):
            newFiles = dbTable.RadioButton2
            if (newFiles.is_visible()):
                if ( not newFiles.is_selected()):
                    newFiles.click_input()
                    print("click option = " + select)
                else:
                    print("already select = " + select)
                status = True
            else:
                print(select + " not visible")
                msg = "{} not visible".format(select)
                global_cfg.msgs.append(msg)
        listTxt = dbTable.descendants(control_type='Text')
        for li in listTxt:
            txt = li.window_text()
            print(txt)
        if ( status ):
            dbTable.Next.click_input()
        else:
            msg = "fail to select files {}".format(select)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify select files")

def verify_select_second_action_for_copy(op, delete, notify):
    status = False
    try:
        status1 = status2 = False
        dbTable = op.DevicesTable2
        if ( delete ):
            deleteCb = dbTable.child_window(title_re="Delete all", control_type='Text')
            if ( deleteCb.is_visible()):
                rect = deleteCb.rectangle()
                print(rect)
                mouse.click(button='left', coords=(rect.left-20, rect.top-20))
                print("click checkbox Delete")
                status1 = True
            else:
                global_cfg.msgs.append("Delete checkbox not visible")
        if ( notify ):
            chboxNoti = dbTable.child_window(title_re="Override default", control_type="Text")
            if ( chboxNoti.is_visible()):
                rect = chboxNoti.rectangle()
                mouse.click(button='left', coords=(rect.left - 20, rect.top - 20))
                print("click checkbox Notify")
                status1 = True
            else:
                global_cfg.msgs.append("Notify checkbox not visible")
        listTxt = dbTable.descendants(control_type='Text')
        for li in listTxt:
            txt = li.window_text()
            print(txt)
        status = True
        if (dbTable.Next.is_visible()):
            dbTable.Next.click_input()
            status2 = True
        else:
            global_cfg.msgs.append("Next is not visible")
        if ( status1 and status2  ):
            status = True
        else:
            global_cfg.msgs.append("fail to select second action")
        return status
    except:
        raise ValueError("exception on verify select second action")

def verify_select_action_for_copy_endpoint(op, delete, notify, verify):
    status = False
    try:
        status1 = status2 = False
        dbTable = op.DevicesTable2
        #dbTable.dump_tree()
        if ( delete ):
            deleteCb = dbTable.child_window(title_re="Delete all", control_type="Text")
            if ( deleteCb.is_visible()):
                rect = deleteCb.rectangle()
                mouse.click(button='left', coords=(rect.left-20, rect.top-5))
                print("click checkbox Delete")
                status1 = True
            else:
                global_cfg.msgs.append("Delete checkbox not visible")
        if ( notify ):
            chboxNoti = dbTable.child_window(title_re="Override default", control_type="Text")
            if (chboxNoti.is_visible()):
                rect = chboxNoti.rectangle()
                mouse.click(button='left', coords=(rect.left - 20, rect.top - 20))
                print("click checkbox Notify")
                status1 = True
            else:
                global_cfg.msgs.append("Notify checkbox not visible")
        if ( verify ):
            chboxVeri = dbTable.child_window(title_re="Verify that all", control_type="Text")
            if ( chboxVeri.is_visible()):
                rect = chboxVeri.rectangle()
                mouse.click(button='left', coords=(rect.left - 20, rect.top - 20))
                print("click checkbox Verify")
                status1 = True
            else:
                global_cfg.msgs.append("Notify checkbox not visible")
        listTxt = dbTable.descendants(control_type='Text')
        for li in listTxt:
            txt = li.window_text()
            print(txt)
        status = True
        if (dbTable.Next.is_visible()):
            dbTable.Next.click_input()
            status2 = True
        else:
            global_cfg.msgs.append("Next is not visible")
        if ( status1 and status2  ):
            status = True
        else:
            global_cfg.msgs.append("fail to select second action")
        return status
    except:
        raise ValueError("exception on verify select actions for copy endpoint")

def verify_select_second_action_for_delete(op, notify):
    status = False
    try:
        time.sleep(1)
        dbTable = op.DevicesTable2
        if ( notify ):
            #chboxNoti = dbTable.NotifyStatic
            chboxNoti = dbTable.child_window(title_re="Override default", control_type="Text")
            if (chboxNoti.is_visible()):
                rect = chboxNoti.rectangle()
                mouse.click(button='left', coords=(rect.left - 20, rect.top - 20))
                print("click checkbox Notify")
        listTxt = dbTable.descendants(control_type='Text')
        for li in listTxt:
            txt = li.window_text()
            print(txt)
        if ( dbTable.Next.is_visible()):
            dbTable.Next.click_input()
            status = True
        else:
            global_cfg.msgs.append("Next not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to select second action for delete")
        return status
    except:
        raise ValueError("exception on verify select second action for delete")

def verify_select_trigger(op, trigger):
    status = False
    try:
        dbTable = op.DevicesTable2
        triggerBtn = dbTable.child_window(control_type='Button')
        if ( triggerBtn.window_text() != trigger ):
            triggerBtn.click_input()
            dbTable.child_window(title=trigger, control_type='Text').click_input()
            print("select trigger = " + trigger)
        else:
            print("already select = " + trigger)
        if ( dbTable.Next.is_visible()):
            dbTable.Next.click_input()
            status = True
        else:
            global_cfg.msgs.append("Next not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to select trigger")
        return status
    except:
        raise ValueError("exception on verify select trigger")

def verify_add_tag(op, tagName):
    status = False
    try:
        dbTable = op.DevicesTable
        tagChb = dbTable.child_window(title='Tag', control_type='Text')
        if ( tagChb.is_visible()):
            tagChb.click_input()
            editTag = dbTable.child_window(auto_id='input')
            editTag.type_keys(tagName)
            print("enter tag name = " + tagName)
            next = dbTable.child_window(title='Next', control_type='Text')
            if ( next.is_visible()):
                next.click_input()
                status = True
            else:
                global_cfg.msgs.append("Next not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to add tag")
        return status
    except:
        raise ValueError("exception on verify add tag")

def verify_click_create_workflow(op, actions, trigger):
    status = False
    try:
        status1 = status2 = status3 = False
        descTable = op.DevicesTable2
      #  descTable.dump_tree()
        txtList = descTable.descendants(control_type='Text')
        title = txtList[0].window_text()
        print("title = " + title)
        params.workflow_name = title
        for li in txtList:
            txt = li.window_text()
            if ( txt == actions ):
                print("get correct actions = " + actions)
                status1 = True
            elif ( txt == trigger ):
                print("get correct trigger = " + trigger)
                status2 = True
        if ( not status1 ):
            msg = "get wrong actions {}".format(actions)
            global_cfg.msgs.append(msg)
        if ( not status2 ):
            msg = "get wrong trigger {}".format(trigger)
            global_cfg.msgs.append(msg)
      #  descTable.dump_tree()
        createCus = descTable.Create
        if ( createCus.is_visible()):
            createCus.click_input()
            print("click Create")
            status3 = True
        else:
            global_cfg.msgs.append("Create button not visible")
        if ( status1 and status2 and status3):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to click create workflow")
        return status
    except:
        raise ValueError("exception on verify click create workflow")

def verify_click_update_workflow(op, type, trigger):
    status = False
    try:
        status1 = status2 = status3 = False
        dashTable = op.DevicesTable2
        txtList = dashTable.descendants(control_type='Text')
        title = txtList[0].window_text()
        print("title = " + title)
        params.workflow_name = title
        for li in txtList:
            txt = li.window_text()
            if ( txt == type ):
                print("get correct type = " + type)
                status1 = True
            elif ( txt == trigger ):
                print("get correct trigger = " + trigger)
                status2 = True
        if ( not status1 ):
            msg = "get wrong type {}".format(type)
            global_cfg.msgs.append(msg)
        if ( not status2 ):
            msg = "get wrong trigger {}".format(trigger)
            global_cfg.msgs.append(msg)

        update = dashTable.child_window(title='Update')
        if ( update.is_visible()):
            update.click_input()
            status3 = True
        else:
            global_cfg.msgs.append("Update not visible")
        if ( status1 and status2 and status3):
            status = True
        else:
            global_cfg.msgs.append("fail to click update workflow")
        return status
    except:
        raise ValueError("exception on verify click update workflow")

def verify_update_workflow(op, name, description, source, destination, action, trigger):
    status = False
    try:
        dashTable = op.DevicesTable
        txtList = dashTable.descendants(control_type='Text')
        title = txtList[0].window_text()
        print("title = " + title)
        if ( title != name ):
            print("click Edit name = " + name)
            params.workflow_name = name

        if ( trigger != None ):
            optImage = dashTable.WorkflowOptionsImage
            rect = optImage.rectangle()
            mouse.move(coords=(rect.left, rect.top))
            txtList = dashTable.descendants(control_type='Text')
            opt = ""
            for i in range(len(txtList)):
                txt = txtList[i].window_text()
                if ( txt == "Trigger"):
                    opt = txtList[i+1].window_text()
                    opt = opt[2:]
                    print("opt = " + opt)
                    break
            if ( opt != trigger):
                mouse.move(coords=(0,0))
                optImage.click_input()
                optImage.click_input()
                if (verify_select_trigger(op, trigger)):
                    status = True

        if ( source != None and destination != None and
            trigger != None and action != None):
            update = dashTable.child_window(title='Update')
            update.click_input()
            status = True
        return status
    except:
        raise ValueError("exception on verify update workflow")

def verify_edit_actions(op, name, type, action):
    status = False
    try:
        dashTable = op.DevicesTable
        if ( action != None):
            update = dashTable.child_window(title='Update')
            update.click_input()
            status = True
        return status
    except:
        raise ValueError("exception on verify edit action workflow")

def verify_edit_notify(op, notify):
    status = False
    try:
        time.sleep(2)
        dashTable = op.DevicesTable2
        actionImg = dashTable.ActionsImage
        rect = actionImg.rectangle()
        mouse.move(coords=(rect.left, rect.top))
        time.sleep(1)
        mouse.double_click(button='left', coords=(rect.left+5, rect.top+5))
        time.sleep(1)
        op.dump_tree()
        chboxNoti = dashTable.child_window(title_re="Override default", control_type="Text")
        if (chboxNoti.is_visible()):
            rect = chboxNoti.rectangle()
            print(rect)
            mouse.double_click(button='left', coords=(rect.left - 20, rect.top - 20))

            if ( notify == "System"):
                dashTable.child_window(title="System", control_type="Button").click_input()
                dashTable.child_window(title=notify, control_type="Text").click_input()
        nextBtn = dashTable.child_window(auto_id="previewApplyButton", control_type="Group")
        if ( nextBtn.is_visible()):
            nextBtn.click_input()
            status = True
        else:
            global_cfg.msgs.append("Next not visible")

        return status
    except:
        raise ValueError("exception on verify edit notify")

def verify_edit_source_workflow(op, source):
    status = False
    try:
        time.sleep(1)
        deviceTable = op.DevicesTable2
        #deviceTable.dump_tree()
        sourceImg = deviceTable.SourcesImage
        rect = sourceImg.rectangle()
        print(rect)
        mouse.move(coords=(rect.left, rect.top))
        time.sleep(1)
        mouse.click(button="left", coords=(rect.left+4, rect.top+10))
        status = True
        return status
    except:
        raise ValueError("exception on verify edit source workflow")


def verify_add_delete_action(op):
    status = False
    try:
        time.sleep(2)
        dashTable = op.DevicesTable2
        actionImg = dashTable.ActionsImage
        rect = actionImg.rectangle()
        mouse.move(coords=(rect.left, rect.top))
        mouse.double_click(button='left', coords=(rect.left + 5, rect.top + 5))
        time.sleep(1)
        delete = dashTable.child_window(title_re="Delete all files", control_type="Text")
        rectDelete = delete.rectangle()
        mouse.click(button='left', coords=(rectDelete.left-20, rectDelete.top-20))
        print("select Delete")
        if ( dashTable.Next.is_visible()):
            dashTable.Next.click_input()
            status = True
        else:
            global_cfg.msgs.append("Next not visible")

        return status
    except:
        raise ValueError("exception on verify add delete action")

def verify_add_verify_action(op):
    status = False
    try:
        time.sleep(2)
        dashTable = op.DevicesTable2
        actionImg = dashTable.ActionsImage
        rect = actionImg.rectangle()
        mouse.move(coords=(rect.left, rect.top))
        time.sleep(1)
        mouse.double_click(button='left', coords=(rect.left + 5, rect.top + 5))
        time.sleep(1)
        dashTable.child_window(title='Delete', control_type='Text').click_input()
        print("select Delete")
        if ( dashTable.Next.is_visible()):
            dashTable.Next.click_input()
            status = True
        else:
            global_cfg.msgs.append("Next not visible")

        return status
    except:
        raise ValueError("exception on verify add verify action")

def verify_edit_trigger_workflow(op, trigger):
    status = False
    try:
        dashTable = op.DevicesTable2
        if ( trigger != None ):
            optImage = dashTable.WorkflowOptionsImage
            rect = optImage.rectangle()
            mouse.move(coords=(rect.left, rect.top))
            txtList = dashTable.descendants(control_type='Text')
           # mouse.move(coords=(rect.left-50, rect.top+50))
           # time.sleep(1)
            opt = ""
            for i in range(len(txtList)):
                txt = txtList[i].window_text()
                if ( txt == "Trigger"):
                    opt = txtList[i+1].window_text()
                    opt = opt[2:]
                    print("opt = " + opt)
                    break
            if ( opt != trigger):
                mouse.click(button='left', coords=(rect.left+5,rect.top+5))
                print("click trigger")
                time.sleep(1)
                if (verify_select_trigger(op, trigger)):
                    status = True
            else:
                print("already got same trigger = " + trigger)
                status = True
        if ( not status ):
            msg = "fail to edit trigger {}".format(trigger)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify edit trigger workflow")

def verify_edit_tag_workflow(op, tag, tagName):
    status = False
    try:
        time.sleep(3)
        dashTable = op.DevicesTable2
        if ( tag ):
            optImage = dashTable.WorkflowOptionsImage
            rect = optImage.rectangle()
            mouse.move(coords=(rect.left, rect.top))
            time.sleep(1)
            mouse.double_click(button='left', coords=(rect.left+10, rect.top+10))
            if ( verify_add_tag(op, tagName)):
                update = dashTable.child_window(title='Update')
                if (update.is_visible()):
                    update.click_input()
                    status = True
                else:
                    global_cfg.msgs.append("Update not visible")
        if ( not status ):
            msg = "fail to edit tag"
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify edit tag workflow")

def verify_workflow_detail(op, name, type, trigger):
    status = False
    try:
        time.sleep(1)
        status1 = status2 = True
        rowSelect = get_workflow_select(op, name)
        time.sleep(1)
        dataList = rowSelect.descendants(control_type='DataItem')
        for li in dataList:
            itemTxt = li.window_text()
            print(itemTxt)
            if ( itemTxt == type ):
                print("get correct type = " + type)
                status1 = True
            elif ( itemTxt == trigger ):
                print("get correct trigger = " + trigger)
                status2 = True
        if ( not status1 ):
            msg = "get wrong type {}".format(type)
            global_cfg.msgs.append(msg)
        if (not status2):
            msg = "get wrong trigger {}".format(trigger)
            global_cfg.msgs.append(msg)
        if ( status1 and status2 ):
            status = True
        if ( not status ):
            global_cfg.msgs.append("fail to verify workflow detail")
        return status
    except:
        raise ValueError("exception on verify workflow detail")

def update_trigger(op, name, trigger):
    status = False
    try:
        time.sleep(2)
        rowSelect = get_workflow_select(op, name)
        print("rowSelect = " + str(rowSelect))
        dataList = rowSelect.descendants(control_type='DataItem')

        for i in range(len(dataList)):
            if ( i == 3 ):
                triggerVal = dataList[i].window_text()
                print("triggerVal = " + triggerVal)
                if ( triggerVal != trigger ):
                    table = dataList[i].descendants(control_type='Table')[0]
                    triggerUpdate = table.descendants(title=triggerVal, control_type='Group')[0]
                    if ( triggerUpdate.is_visible()):
                        triggerUpdate.click_input()
                        time.sleep(1)
                        triggerSelect = triggerUpdate.descendants(title=trigger)[0]
                        if ( triggerSelect.is_visible()):
                            triggerSelect.click_input()
                            print("selec trigger = " + trigger)
                            status = True
                        else:
                            msg = "option trigger {} not visible".format(trigger)
                            global_cfg.msgs.append(msg)
                    else:
                        msg = "Trigger {} not visible".format(triggerVal)
                        global_cfg.msgs.append(msg)
                else:
                    print("already got trigger = " + trigger)
                    status = True
                break
        if ( not status ):
            msg = "fail to update trigger {}".format(trigger)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on update trigger")

def verify_click_dotmenu(op, name, option):
    status = False
    try:
        time.sleep(1)
        rowSelect = get_workflow_select(op, name)
        dataList = rowSelect.descendants(control_type='DataItem')
        for j in range(len(dataList)):
            if ( j == len(dataList) -1):
                dotItem = dataList[j]
                rowTable = dotItem.children(control_type='Table')[0]
                rectTable = rowTable.rectangle()
                mouse.move(coords=(rectTable.left, rectTable.top))
                time.sleep(1)
                dotMenu = rowTable.children(control_type='Image')[0]
                if ( dotMenu.is_visible()):
                    dotMenu.click_input()
                    print("dot menu")
                    time.sleep(1)
                    if ( option == 'Delete'):
                        delete = rowTable.children(title='Delete', control_type='Text')[0]
                        if ( delete.is_visible()):
                            delete.click_input()
                            print("click delete workflow")
                            status = True
                        else:
                            global_cfg.msgs.append("Delete not visible")
                    elif ( option == 'Edit'):
                        edit = rowTable.children(title='Edit', control_type='Text')[0]
                        if ( edit.is_visible()):
                            edit.click_input()
                            print("click edit workflow")
                            status = True
                        else:
                            global_cfg.msgs.append("Edit not visible")
                else:
                    global_cfg.msgs.append("dotmenu not visible")
        if (not status):
            msg = "fail to click {} of name {}".format(option, name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify click dotmenu")

def get_workflow_select(op, name):
    row = None
    try:
        timings.Timings.fast()
        time.sleep(2)
        wfTable = op.child_window(auto_id="WorkflowsTable")
        dataItems = wfTable.descendants(control_type='DataItem')
        for i in range(len(dataItems)):
            itemTxt = dataItems[i].window_text()
            if (itemTxt == name):
                print("get name = " + itemTxt)
                row = dataItems[i].parent()
                break
        if ( row == None ):
            msg = "Workflow {} not found".format(name)
            global_cfg.msgs.append(msg)
        return row
    except:
        raise ValueError("exception on get row select")

def verify_click_play_workflow(op, name):
    status = False
    try:
        time.sleep(2)
        rowSelect = get_workflow_select(op, name)
        dataList = rowSelect.descendants(control_type='DataItem')
        for j in range(len(dataList)):
            if ( j == len(dataList) -1):
                dotItem = dataList[j]
                rowTable = dotItem.children(control_type='Table')[0]
                rectTable = rowTable.rectangle()
                mouse.move(coords=(rectTable.left, rectTable.top))
                time.sleep(1)
                dotMenu = rowTable.children(control_type='Image')[0]
                rect = dotMenu.rectangle()
                mouse.move(coords=(rect.left - 45, rect.top+10))
                mouse.click(button='left', coords=(rect.left-45, rect.top+10))
                print("click icon play")
                mouse.move(coords=(rectTable.left, rectTable.top))
                status = True
        if (not status):
            msg = "fail to click play workflow {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify click play workflow")

def verify_click_cancel_workflow(op, name):
    status = False
    try:
        rowSelect = get_workflow_select(op, name)
        dataList = rowSelect.descendants(control_type='DataItem')
        for j in range(len(dataList)):
            if ( j == len(dataList) -1):
                dotItem = dataList[j]
                rowTable = dotItem.children(control_type='Table')[0]
                rectTable = rowTable.rectangle()
                mouse.move(coords=(rectTable.left, rectTable.top))
                time.sleep(1)
                dotMenu = rowTable.children(control_type='Image')[0]
                rect = dotMenu.rectangle()
              #  mouse.move(coords=(rect.left - 45, rect.top+10))
                mouse.click(button='left', coords=(rect.left-45, rect.top+10))
                print("click cancel")
                time.sleep(1)
                status = True
                mouse.move(coords=(rectTable.left, rectTable.top))
        if (not status):
            msg = "fail to click cancel workflow {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify click cancel workflow")

def verify_click_inspect_workflow(op, name):
    status = False
    try:
        time.sleep(1)
        rowSelect = get_workflow_select(op, name)
        if ( rowSelect != None):
            rowSelect.click_input()
            print("click inspect workflow")
            status = True
        else:
            msg = "fail to click inspect workflow {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify click inspect workflow")

def verify_inspect_workflow_page(op, name, type, trigger):
    status = False
    try:
        timings.Timings.fast()
        title = op.child_window(title_re='Workflow-', control_type='Text')
        print("title = " + title.window_text())
        desc = op['Description\xa0']
        print("desc = " + desc.window_text())
        '''''
        wfList = dbCustom.WorkflowCustom4.descendants(control_type='Text')
        for li in wfList:
            itemTxt = li.window_text()
            print(itemTxt)
            if (itemTxt == name):
                print("get correct name = " + name)
            elif (itemTxt.strip() == type):
                print("get correct type = " + type)
            elif (itemTxt == trigger):
                print("get correct trigger = " + trigger)
        activeList = dbCustom.ActivityCustom0.descendants(control_type='Text')
        for i in range(len(activeList)):
            print("act="+ activeList[i].window_text())

        sourceList = dbCustom.SettingsCustom3.descendants(control_type='Text')
        for li in sourceList:
            print("src=" + li.window_text())
        optCustom = dbCustom.WorkflowOptionCustom.child_window(control_type='Text')
        print("opt=" + optCustom.window_text())
        optStatic = dbCustom.ManualStatic2
        print("opt static = " + optStatic.window_text())
        '''''
        status = True
        return status
    except:
        raise ValueError("exception on verify inspect workflow page")

def verify_inspect_workflow_notification(op, name, type, trigger):
    status = False
    try:
        timings.Timings.fast()
        time.sleep(2)
        status1 = status2 = False
      #  op.Document.print_control_identifiers()
        title = op.child_window(title_re=name, control_type='Text')
        if ( title.window_text() == name):
            print("get correct workflow name = " + title.window_text())
        wfList = op.descendants(control_type='Text')
        for li in wfList:
            itemTxt = li.window_text()
            print(itemTxt)
            if (itemTxt.strip() == type):
                print("get correct type = " + type)
                status1 = True
            elif (itemTxt == trigger):
                print("get correct trigger = " + trigger)
                status2 = True
        if ( not status1 ):
            msg = "get wrong type {}".format(type)
            global_cfg.msgs.append(msg)
        if (not status2):
            msg = "get wrong trigger {}".format(trigger)
            global_cfg.msgs.append(msg)

        if ( status1 == status2 ):
            status = True
        if (not status):
            msg = "fail to verify inspect workflow notification {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify inspect workflow notification")

def click_workflow_link(op):
    status = False
    try:
        time.sleep(1)
     #   wfLink = op.child_window(title='Workflows', control_type='Hyperlink')
        wfLink = op.child_window(control_type='Hyperlink', found_index=2)
        if (wfLink.is_visible()):
            wfLink.click_input()
            print("click workflow link")
            status = True
        else:
            msg = "not visible workflow link"
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click workflow link")

def click_inspect_workflow_panel_link(op):
    status = False
    try:
      #  wfLink = op.child_window(title_re='Inspect Workflow Panel', control_type='Hyperlink')
        wfLink = op.child_window(control_type='Hyperlink', found_index=2)
        if (wfLink.is_visible()):
            wfLink.click_input()
            print("click Inpect workflow panel link")
        else:
            msg = "not visible inspect workflow link"
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click inspect workflow link")

def verify_click_inspect_activity(op):
    status = False
    try:
        time.sleep(2)
       # op.Document.dump_tree()
       # activity = op.child_window(title='Activity', control_type='Text')
        activity = op.Activity2
        rect = activity.rectangle()
        mouse.move(coords=(rect.left+100, rect.top))
        actionImg = op.ActionImage
        rect1 = actionImg.rectangle()
        mouse.double_click(button='left', coords=(rect1.left+2, rect.top+8))
        time.sleep(1)
        print("click Inspect activity")
        #op.Document.dump_tree()
        wfLink = op.child_window(title='Inspect Workflow Panel', control_type='Hyperlink')
        if (wfLink.is_visible()):
            status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click inspect activity")
        return status
    except:
        raise ValueError("exception on verify click inspect activity")

def verify_click_inspect_copy_activity(op):
    status = False
    try:
        time.sleep(1)

        activity = op.Activity2
        rect = activity.rectangle()
        print(rect)
        mouse.move(coords=(rect.right, rect.top))
        time.sleep(1)
        destImg = op.DestinationsImage
        rect1 = destImg.rectangle()
        print(rect1)
        mouse.double_click(button='left', coords=(rect1.left, rect.top-5))
        print("click Inspect activity")
        time.sleep(1)
        status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click inspect copy activity")
        return status
    except:
        raise ValueError("exception on verify click inspect copy activity")

def verify_inspect_activity_page(op, name, type, trigger, source, destination):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = status3 = status4 = False
        title = op.child_window(title=name, control_type='Text')
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
       # table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table

        rowCustom = table.child_window(auto_id='rowID0', control_type='Custom')
        dataList = rowCustom.descendants(control_type='DataItem')
        for i in range(len(dataList)):
            item = dataList[i].window_text()
            print("dataItem = " + item)
            if ( i < len(dataList)-1 ):
                if ( item == type ):
                    print("get correct type = " + type)
                    status1 = True
                elif ( item == trigger ):
                    print("get correct trigger = " + trigger)
                    status2 = True
                elif ( item == source ):
                    print("get correct source = " + source)
                    status3 = True
                elif ( item == destination ):
                    print("get correct destination = " + destination)
                    status4 = True
            elif ( i == len(dataList)-1 ):
                childTable = dataList[i].children(control_type='Table')[0]
                actList = childTable.descendants(control_type='Text')
                for li in actList:
                    print("activity status = " + li.window_text())
        if ( not status1 ):
            msg = "get wrong type {}".format(type)
            global_cfg.msgs.append(msg)
        if ( not status2 ):
            msg = "get wrong trigger {}".format(trigger)
            global_cfg.msgs.append(msg)
        if ( not status3 ):
            msg = "get wrong source {}".format(source)
            global_cfg.msgs.append(msg)
        if ( not status4 ):
            msg = "get wrong destination {}".format(destination)
            global_cfg.msgs.append(msg)
        if ( status1 and status2 and status3 and status4):
            status = True
        if ( not status ):
            global_cfg.msgs.append("fail to verify inspect activity page")
        return status
    except:
        raise ValueError("exception on verify inspect activity page")

def verify_inspect_activity_data(op, name, type, activity,
                                 source, destination):
    status = False
    try:
        time.sleep(4)
        status1 = status2 = status3 = status4 = False
      #  op.dump_tree()
        title = op.child_window(title=name, control_type='Text')
        print("title = " + title.window_text())
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        else:
            msg = "get wrong tile {}".format(title.window_text())
            global_cfg.msgs.append(msg)

        #table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        #op.dump_tree()
        #i = get_row_inspect(op, type)
        #rowId  = "rowID" + str(i-1)
        if ( activity == "Completed"):
            i = get_latest_row_completed(op, type)
            rowId = "rowID" + str(i)
        else:
            rowId = "rowID0"
        print("rowId = " + str(rowId))

        rowCus = table.child_window(auto_id=rowId, control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        typeVal = dataList[0].window_text()

        if ( typeVal == type ):
            print("get correct type = " + typeVal)
            status1 = True
        else:
            msg = "get wrong type {}".format(typeVal)
            global_cfg.msgs.append(msg)
        sourceVal = dataList[1].window_text()
        if ( sourceVal == source ):
            print("get correct source = " + sourceVal)
            status2 = True
        else:
            msg = "get wrong source {}".format(sourceVal)
            global_cfg.msgs.append(msg)
        actVal = dataList[3].window_text()
        if (actVal.__contains__(activity)):
            print("get correct activity = " + actVal)
            status3 = True
        else:
            msg = "get wrong activity {}".format(actVal)
            global_cfg.msgs.append(msg)
        if ( type == "Copy"):
            destVal = dataList[2].window_text()
            if ( destVal == destination ):
                print("get correct destination = " + destVal)
                status4 = True
            else:
                msg = "get wrong destination {}".format(destVal)
                global_cfg.msgs.append(msg)

            if ( status1 and status2 and status3 and status4):
                status = True
            else:
                global_cfg.msgs.append("fail to verify inspect activity data")
        elif ( type == "Delete"):
            if ( status1 and status2 and status3):
                status = True
            else:
                global_cfg.msgs.append("fail to verify inspect activity data")

        return status
    except:
        raise ValueError("exception on verify inspect activity data")

def verify_inspect_activity_data_with_verify(op, name, type, activity,
                                 source, destination):
    status = False
    try:
        time.sleep(3)
        status1 = status2 = status3 = status4 = False
        title = op.child_window(title=name, control_type='Text')
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        else:
            msg = "get wrong tile {}".format(title.window_text())
            global_cfg.msgs.append(msg)

        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
      #  table.dump_tree()
        if ( activity == "Completed"):
            i = get_latest_row_completed(op, type)
            rowId = "rowID" + str(i)
        else:
          #  i = get_last_row_inspect(op, type)
            i = 1;
            if( type == "Verify"):
                rowId = "rowID" + str(i)
            elif (type == "Copy"):
                rowId = "rowID" + str(i-1)

        rowCus = table.child_window(auto_id=rowId, control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        typeVal = dataList[0].window_text()

        if ( typeVal == type ):
            print("get correct type = " + typeVal)
            status1 = True
        else:
            msg = "get wrong type {}".format(typeVal)
            global_cfg.msgs.append(msg)
        sourceVal = dataList[1].window_text()
        if ( sourceVal == source ):
            print("get correct source = " + sourceVal)
            status2 = True
        else:
            msg = "get wrong source {}".format(sourceVal)
            global_cfg.msgs.append(msg)
        actVal = dataList[3].window_text()
        if (actVal.__contains__(activity)):
            print("get correct activity = " + actVal)
            status3 = True
        else:
            msg = "get wrong activity {}".format(actVal)
            global_cfg.msgs.append(msg)
        if (( type == "Copy" ) or ( type == "Verify")):
            destVal = dataList[2].window_text()
            if ( destVal == destination ):
                print("get correct destination = " + destVal)
                status4 = True
            else:
                msg = "get wrong destination {}".format(destVal)
                global_cfg.msgs.append(msg)

            if ( status1 and status2 and status3 and status4):
                status = True
            else:
                global_cfg.msgs.append("fail to verify inspect activity data")
        elif ( type == "Delete"):
            if ( status1 and status2 and status3):
                status = True
            else:
                global_cfg.msgs.append("fail to verify inspect activity data")

        return status
    except:
        raise ValueError("exception on verify inspect activity data with verify")

def verify_inspect_activity_with_multi_sources(op, name, type, activity,
                                 sourceList, destination):
    status = False
    try:
        time.sleep(3)
        status1 = status2 = status3 = status4 = False
        title = op.child_window(title=name, control_type='Text')
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        else:
            msg = "get wrong tile {}".format(title.window_text())
            global_cfg.msgs.append(msg)

        #table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)-1
        lenSource = len(sourceList)

        for i in range(lenRow-1):
            rowId = "rowID" + str(i)
            rowCus = table.child_window(auto_id=rowId, control_type='Custom')
            dataList = rowCus.descendants(control_type='DataItem')
            typeVal = dataList[0].window_text()

            if ( typeVal == type ):
                print("get correct type = " + typeVal)
                status1 = True
            else:
                msg = "get wrong type {}".format(typeVal)
                global_cfg.msgs.append(msg)
            sourceVal = dataList[1].window_text()
            foundSrc = False
            for j in range(lenSource):
                if ( sourceVal == sourceList[j] ):
                    print("get correct source = " + sourceVal)
                    status2 = True
                    foundSrc = True
                    break
            if (not foundSrc):
                msg = "get wrong source {}".format(sourceVal)
                global_cfg.msgs.append(msg)
            actVal = dataList[3].window_text()
            if (actVal.__contains__(activity)):
                print("get correct activity = " + actVal)
                status3 = True
            else:
                msg = "get wrong activity {}".format(actVal)
                global_cfg.msgs.append(msg)
            if ( type == "Copy"):
                destVal = dataList[2].window_text()

                if ( destVal == destination ):
                    print("get correct destination = " + destVal)
                    status4 = True
                else:
                    msg = "get wrong destination {}".format(destVal)
                    global_cfg.msgs.append(msg)

                if ( status1 and status2 and status3 and status4):
                    status = True
                else:
                    global_cfg.msgs.append("fail to verify inspect activity with multi sources")
            elif ( type == "Delete"):
                if ( status1 and status2 and status3):
                    status = True
                else:
                    global_cfg.msgs.append("fail to verify inspect activity with multi sources")

        return status
    except:
        raise ValueError("exception on verify inspect activity with multi sources")

def verify_inspect_delete_action(op, name, type, activity, source):
    status = False
    try:
        time.sleep(5)
        status1 = status2 = status3 = False
        title = op.child_window(title=name, control_type='Text')
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        else:
            msg = "get wrong tile {}".format(title.window_text())
            global_cfg.msgs.append(msg)

        #table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        #table.dump_tree()
        if ( type == "Delete"):
            i = get_row_delete(op)
            rowId = "rowID" + str(i)
        else:
            i = get_row_inspect(op, type)
            rowId  = "rowID" + str(i-1)
        print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=rowId, control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        typeVal = dataList[0].window_text()
        print("typeVal = " + typeVal)
        if ( typeVal == type ):
            print("get correct type = " + typeVal)
            status1 = True
        else:
            msg = "get wrong type {}".format(typeVal)
            global_cfg.msgs.append(msg)
        sourceVal = dataList[1].window_text()
        if ( sourceVal == source ):
            print("get correct source = " + sourceVal)
            status2 = True
        else:
            msg = "get wrong source {}".format(sourceVal)
            global_cfg.msgs.append(msg)
        actVal = dataList[3].window_text()
        if (actVal.__contains__(activity)):
            print("get correct activity = " + actVal)
            status3 = True
        else:
            msg = "get wrong activity {}".format(actVal)
            global_cfg.msgs.append(msg)

        if ( status1 and status2 and status3):
            status = True
        else:
            global_cfg.msgs.append("fail to verify inspect activity data")

        return status
    except:
        raise ValueError("exception on verify inspect delete action")

def verify_inspect_delete_multi_sources_action(op, name, type, activity, sourceList):
    status = False
    try:
        time.sleep(5)
        status1 = status2 = status3 = False
        title = op.child_window(title=name, control_type='Text')
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        else:
            msg = "get wrong tile {}".format(title.window_text())
            global_cfg.msgs.append(msg)

        #table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        #table.dump_tree()
        if ( type == "Delete"):
            i = get_row_delete(op)
            rowId = "rowID" + str(i)
        else:
            i = get_row_inspect(op, type)
            rowId  = "rowID" + str(i-1)
        print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=rowId, control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        typeVal = dataList[0].window_text()
        lenSource = len(sourceList)
        if ( typeVal == type ):
            print("get correct type = " + typeVal)
            status1 = True
        else:
            msg = "get wrong type {}".format(typeVal)
            global_cfg.msgs.append(msg)
        sourceVal = dataList[1].window_text()
        for j in range(lenSource):
            if (sourceVal == sourceList[j]):
                print("get correct source = " + sourceVal)
                status2 = True
                foundSrc = True

        if (not foundSrc):
            msg = "get wrong source {}".format(sourceVal)
            global_cfg.msgs.append(msg)

        actVal = dataList[3].window_text()
        if (actVal.__contains__(activity)):
            print("get correct activity = " + actVal)
            status3 = True
        else:
            msg = "get wrong activity {}".format(actVal)
            global_cfg.msgs.append(msg)

        if ( status1 and status2 and status3):
            status = True
        else:
            global_cfg.msgs.append("fail to verify inspect activity data")

        return status
    except:
        raise ValueError("exception on verify inspect delete multi sources action")

def get_disk_inspect(op, diskNo, arrayVal):
    rowId = 0
    try:
        table = op.Table
        #table.dump_tree()
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        for j in range(lenRow-1):
            row = str(j+1)
            rowCus = table.child_window(auto_id=row, control_type='Custom')
            if (rowCus.is_visible()):
                itemList = rowCus.descendants(control_type='DataItem')
                disk = itemList[0].window_text()
                array = itemList[3].window_text()
                if (disk == diskNo and array == arrayVal):
                    print("get disk " + diskNo + ", array = " + arrayVal)
                    rowId = j+1
                    break

        return rowId
    except:
        raise ValueError("get exception on get disk inspect")

def get_disk_global(op, diskNo):
    rowId = 0
    try:
        #table = op.Table
        table = op.child_window(auto_id="deviceDisks", control_type='Table')
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        for j in range(lenRow-1):
            row = str(j+1)
            rowCus = table.child_window(auto_id=row, control_type='Custom')
            if (rowCus.is_visible()):
                itemList = rowCus.descendants(control_type='DataItem')
                disk = itemList[0].window_text()
                if (disk == diskNo):
                    print("get disk " + diskNo)
                    rowId = j+1
                    break

        return rowId
    except:
        raise ValueError("get exception on get disk global")

def get_disk_spare(op, diskNo, spare):
    rowId = 0
    try:
        #table = op.Table
        table = op.child_window(auto_id="deviceDisks", control_type="Table")
        #table.dump_tree()
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        for j in range(lenRow-1):
            row = str(j+1)
           # print("auto id row = " + str(row))
            rowCus = table.child_window(auto_id=row, control_type='Custom')
            if (rowCus.is_visible()):
                itemList = rowCus.descendants(control_type='DataItem')
                disk = itemList[0].window_text()
                spareVal = itemList[4].window_text()
                if (disk == diskNo and spare == spareVal):
                    print("get disk " + diskNo + ", spare = " + spareVal)
                    rowId = j+1
                    break

        return rowId
    except:
        raise ValueError("get exception on get disk spare")

def get_row_inspect(op, type):
    rowId = 0
    try:
        #table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        i = lenRow - 1
        row = "rowID" + str(i - 1)
        print("row = " + str(row))
        rowCus = table.child_window(auto_id=row, control_type='Custom')
        itemList = rowCus.descendants(control_type='DataItem')
        typeVal = itemList[0].window_text()
        print("typeVal = " + str(typeVal))
        if (type == typeVal):
           rowId = i
        else:
            rowId = i-1
        return rowId
    except:
        raise ValueError("get exception on get row inspect")

def get_last_row_inspect(op, type):

    try:

        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        i = lenRow - 1
        row = "rowID" + str(i - 1)
        print("row = " + str(row))
        rowCus = table.child_window(auto_id=row, control_type='Custom')
        itemList = rowCus.descendants(control_type='DataItem')
        typeVal = itemList[0].window_text()
        rowId = i-1

        return rowId
    except:
        raise ValueError("get exception on get row inspect")

def get_latest_row_completed(op, type):
    rowId = 0
    try:
        time.sleep(2)
        table = None
        #table = op.Table
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
       # table.dump_tree()
        time.sleep(2)
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        for j in range(lenRow-1):
            row = "rowID" + str(j)
           # print("row = " + row)
            rowCus = table.child_window(auto_id=row, control_type='Custom')
            if (rowCus.is_visible()):
                itemList = rowCus.descendants(control_type='DataItem')
                typeVal = itemList[0].window_text()
                activity = itemList[3].window_text()
                if (typeVal == type and "Completed" in activity):
                    rowId = j
                    break
        return rowId
    except:
        raise ValueError("get exception on get latest row completed")

def get_row_delete(op):
    rowId = 0
    try:
        time.sleep(5)
        table = op.Table
        #table.dump_tree()
        if (project_params.app_mode == "staging"):
            table = op.Table4
        elif (project_params.app_mode == "standalone"):
            table = op.Table
        time.sleep(1)
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)
        for j in range(lenRow-1):
            row = "rowID" + str(j)
            rowCus = table.child_window(auto_id=row, control_type='Custom')
            itemList = rowCus.descendants(control_type='DataItem')
            typeVal = itemList[0].window_text()
            print("typeVal = " + typeVal)
            activity = itemList[3].window_text()
            print("activity = " + activity)
            if (typeVal == "Delete" and "Completed" in activity):
                rowId = j
                print("rowId = " + str(rowId))
                break
        #print("return row = " + str(rowId))
        return rowId
    except:
        raise ValueError("get exception on get row delete")

def verify_edit_workflow_option(op):
    status = False
    try:
        dbCustom = op.DashboardCustom9
        optImage = dbCustom.WorkflowOptionImage1
        optImage.click_input()
       # op.dump_tree()
        status = True
        return status
    except:
        raise ValueError("exception on verify edit workflow option")


def verify_summary_workflow(op, device, trigger):
    status = False
    try:
        dbTable = op.DevicesTable
        listTxt = dbTable.descendants(control_type='Text')
        for li in listTxt:
            print(li.window_text())
        status = True
        return status
    except:
        raise ValueError("exception on verify summary workflow")

def click_back(op):
    status = False
    try:
        backCustom = op.BackCustom
        backBtn = backCustom.child_window(control_type='Text')
        if ( backBtn.is_visible()):
            backBtn.click_input()
            print("click Back")
            time.sleep(1)
            status = True
        else:
            global_cfg.msgs.append("Back not visible")
        return status
    except:
        raise ValueError("exception on verify click Back")

def get_list_notificatiions(op):
    listNoti = []
    try:
        listTxt = op.descendants(control_type='Text')
        print("list Notifications:")
        for li in listTxt:
            listNoti.append(li.window_text())
        print(listNoti)
        return listNoti
    except:
        raise ValueError("exception on get list notifications")

def get_item_notification(op, name):
    listItem = []
    try:
        notifyCus = op.Document
        listTxt = notifyCus.descendants(control_type='Text')
        print("get item Notification:")
        for li in listTxt:
            if ( li.window_text() == name ):
                control = notifyCus.child_window(title=name, control_type='Text')
                listItem.append(li.window_text())
                parent = control.parent()
                custom = parent.descendants(control_type='Text')
                for el in custom:
                    listItem.append(el.window_text())
                break
        print(listItem)
        return listItem
    except:
        raise ValueError("exception on get list notifications")

def click_show_tags(op, show):
    status = False
    try:
        customTag = op.DashboardCustom12
       # customTag.dump_tree()
        chbox = customTag.children(control_type='CheckBox')[0]
        state = chbox.get_toggle_state()
        print("get state = " + str(state))
        if ( show ):
            if (state == 0):
                chbox.click()
                status = True
        else:
            if ( state == 1 ):
                chbox.click()
                status = True
        return status
    except:
        raise ValueError("exception on click show tags")

def verify_all_files(op, space):
    listItem = []
    try:
        allFilesCus = op.Document
        listTxt = allFilesCus.descendants(control_type='Text')
        for li in listTxt:
            if (li.window_text() == space):
                print("get correct disk space = " + space)
                listItem.append(li.window_text())
        print(listItem)
        return listItem
    except:
        raise ValueError("exception on get list notifications")

def click_inspect_notification_item(op, name):
    status = False
    try:
        time.sleep(1)
        visible = op.child_window(title=name, control_type='Text', found_index=0, visible_only=False).is_visible()
        notifyCus = op.child_window(title=name, control_type='Text', found_index=0)
        if ( not visible):
            op.Document.wheel_mouse_input(wheel_dist=-10)
            time.sleep(1)
        if ( notifyCus.is_visible()):
            notifyCus.click_input()
            print("click inspect notification name = " + name)
            status = True
           # time.sleep(2)

        else:
            msg = "Notification workflow {} not visible".format(name)
            global_cfg.msgs.append(msg)
        if (not status):
            msg = "fail to click inspect notification {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click inspect notification item")

def click_inspect_copy_files(op, name):
    status = False
    try:
        time.sleep(1)
        listTxt = op.Document.descendants(control_type='Text')
        copyTxt = ""
        for i in range(len(listTxt)):
            txt = listTxt[i].window_text()
            print(txt)
            if ( txt == name ):
                copyTxt = listTxt[i+5].window_text()
                print("copy txt = " + copyTxt)
                copyFiles = op.child_window(title=copyTxt, control_type='Text', found_index=0)
                rect = copyFiles.rectangle()
                mouse.move(coords=(rect.right+100, rect.top))
                dotMenu = op.child_window(title='dots-menu', control_type="Image")

                rect1 = dotMenu.rectangle()
                mouse.click(button='left', coords=(rect1.left+20, rect1.top + 100))
                print("click inspect = " + copyTxt)
                status = True
                break
        if ( not status ):
            msg = "fail to click inspect copy file {}".format(copyTxt)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click inspect copy files")

def click_inspect_showAll(op, name):
    status = False
    try:
        time.sleep(1)
        listTxt = op.Document.descendants(control_type='Text')
        copyTxt = ""
        #op.Document.dump_tree()
        for i in range(len(listTxt)):
            txt = listTxt[i].window_text()
            print(txt)
            if ( txt == name ):
                print("txt item = " + listTxt[i+5].window_text())
                if ( listTxt[i+5].window_text() == "Show All"):
                    copyTxt = listTxt[i+5].window_text()
                elif ( listTxt[i+8].window_text() == "Show All"):
                    copyTxt = listTxt[i + 8].window_text()
                print("copy txt = " + copyTxt)
                copyFiles = op.child_window(title=copyTxt, control_type='Text', found_index=0)
                copyFiles.click_input()
                time.sleep(1)
                '''''
                rect = copyFiles.rectangle()
                mouse.move(coords=(rect.right+100, rect.top))
                dotMenu = op.child_window(title='dots-menu', control_type="Image")

                rect1 = dotMenu.rectangle()
                mouse.click(button='left', coords=(rect1.left+20, rect1.top + 100))
                print("click inspect = " + copyTxt)
                '''''
                status = True
                break
        if ( not status ):
            msg = "fail to click inspect copy file {}".format(copyTxt)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click inspect showAll")

def click_action_workflow(op, name, action):
    status = False
    try:
        time.sleep(1)
        visible = op.child_window(title=name, control_type='Text', found_index=0, visible_only=False).is_visible()
        if ( not visible ):
            scroll_down(op)
        notifyCus = op.child_window(title=name, control_type='Text', found_index=0)
        if (notifyCus.is_visible()):
            print("found workflow = " + name)
            rect = notifyCus.rectangle()
            mouse.move(coords=(rect.right, rect.top))
            time.sleep(1)
          #  op.dump_tree()
            dotMenu = op.child_window(title='dots-menu', control_type='Image')
            if ( dotMenu.is_visible()):
                dotMenu.click_input()
                runWf = op.child_window(title=action, control_type='Text')
                if ( runWf.is_visible()):
                    runWf.click_input()
                    print("click " + action)
                    status = True
                else:
                    msg = "{} not visible".format(action)
                    global_cfg.msgs.append(msg)
            else:
                global_cfg.msgs.append("dotmenu not visible")
        else:
            msg = "Workflow {} not visible".format(name)
            global_cfg.msgs.append(msg)
        if ( not status):
            msg = "fail to click {}".format(action)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click action workflow")

def click_unlock_device_dashboard(op, name, pwd, trusted):
    status = False
    try:
        time.sleep(2)
        visible = op.child_window(title=name, control_type='Text', found_index=0, visible_only=False).is_visible()
        if ( not visible ):
            scroll_down(op)
        notifyCus = op.child_window(title=name, control_type='Text', found_index=0)
        if (notifyCus.is_visible()):
            print("found device = " + name)
            rect = notifyCus.rectangle()
            mouse.click(button='left', coords=(rect.right + 220, rect.top+20))
            time.sleep(1)
            dlg = op.DevicesTable
            title = dlg.child_window(title='Unlock Uninitilized Name', control_type='Text')
            listTxt = dlg.descendants(control_type='Text')
            for li in listTxt:
                print(li.window_text())
            edit = dlg.PasswordEdit
            if (edit.is_visible()):
                edit.set_edit_text(pwd)
                if ( trusted ):
                    chbox = dlg.child_window(title='Trust this computer', control_type='Text')
                    chbox.click_input()
                    time.sleep(1)
                applyBtn = dlg.child_window(title='Unlock', control_type='Custom')
                if ( applyBtn.is_visible()):
                    applyBtn.click_input()
                    print("click unlock device...")
                    time.sleep(20)
                    status = True
                else:
                    global_cfg.msgs.append("Unlock button not visible")
            else:
                global_cfg.msgs.append("edit password fails to display")
        else:
            msg = "Workflow {} not visible".format(name)
            global_cfg.msgs.append(msg)
        if ( not status):
            msg = "fail to unlock {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click unlock device dashboard")

def click_unlock_device(op, name, pwd, trusted):
    status = False
    try:
        time.sleep(1)
       # op.Document.dump_tree()
        deviceObj = op.child_window(title=name, control_type='Text', found_index=0)
        if (deviceObj.is_visible()):
            print("found device = " + name)
            rect = deviceObj.rectangle()
            mouse.move(coords=(rect.right, rect.top))
            mouse.click(button='left', coords=(rect.right + 75, rect.top-40))
            time.sleep(1)
            namelocked = "Unlock " + name
            status = input_password_with_trust(op, namelocked, pwd, trusted)
        else:
            msg = "Workflow {} not visible".format(name)
            global_cfg.msgs.append(msg)
        if ( not status):
            msg = "fail to unlock {}".format(name)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click unlock device")

def click_inspect_disk(op):
    status = False
    try:
        time.sleep(1)
        diskspare = op.child_window(title="Disks and Spares", control_type='Text')
        pwdText = op.child_window(title_re="Password protection", control_type='Text')
        #available = op.child_window(title='Available', control_type='Text')
        if ( diskspare.is_visible()):
            rectDisk = diskspare.rectangle()
            print(rectDisk)
           # rectAv = available.rectangle()
            rectPwd = pwdText.rectangle()
            mouse.move(coords=(rectPwd.right, rectDisk.top+10))
            mouse.double_click(button='left', coords=(rectPwd.right-5, rectDisk.top+10))
            time.sleep(1)
            status = True
        return status
    except:
        raise ValueError("exception on click inspect disk")

def toggle_dynamic_spares(op):
    status = False
    try:
        time.sleep(1)
        chbox = op.CheckBox
        if ( chbox.is_visible()):
            chbox.click_input()
            print("click checkbox dynamic spare")
            status = True
            time.sleep(1)
        click_Device_link(op)
        return status
    except:
        raise ValueError("exception on toggle dynamic spares")

def click_Device_link(op):
    status = False
    try:
        deviceLink = op.child_window(title="Device", control_type='Hyperlink')
        if (deviceLink.is_visible()):
            deviceLink.click_input()
            print("click Device link")
            status = True
        return status
    except:
        raise ValueError("exception on click Device link")

def click_Activity_link(op):
    status = False
    try:
        actLink = op.child_window(title="Activity", control_type='Hyperlink')
        if (actLink.is_visible()):
            actLink.click_input()
            print("click Activity link")
            status = True
        return status
    except:
        raise ValueError("exception on click Activity link")

def click_button_security(op):
    status = False
    try:
        time.sleep(1)
        deviceSet = op.child_window(title="Device Security", control_type="Text")
        rectDevice = deviceSet.rectangle()
        mouse.move(coords=(rectDevice.left+100, rectDevice.top))
        pwdText = op.child_window(title_re="Password protection", control_type="Text")
        rectPwd = pwdText.rectangle()
       # available = op.child_window(title='Available', control_type='Text')
       # rectAv = available.rectangle()
        mouse.click(coords=(rectPwd.right+5, rectDevice.top))
        time.sleep(1)
        status = True
        return status
    except:
        raise ValueError("exception on click disable secured")

def click_enable_security(op):
    status = False
    try:
        time.sleep(1)
        deviceSet = op.child_window(title="Device Security", control_type="Text")
        rectDevice = deviceSet.rectangle()
        mouse.move(coords=(rectDevice.left+100, rectDevice.top))
        pwdText = op.child_window(title_re="Password protection", control_type="Text")
        rectPwd = pwdText.rectangle()

        mouse.click(coords=(rectPwd.right+100, rectDevice.top))
        time.sleep(1)
        status = True
        return status
    except:
        raise ValueError("exception on click disable security")

def click_crypto_erase(op):
    status = False
    try:
        time.sleep(1)
        op.dump_tree()
        deviceSet = op.child_window(title="Device Security", control_type="Text")
        rectDevice = deviceSet.rectangle()
        mouse.move(coords=(rectDevice.left + 100, rectDevice.top))
        pwdText = op.child_window(title_re="Password protection", control_type="Text")
        rectPwd = pwdText.rectangle()
        mouse.click(coords=(rectPwd.right -35, rectDevice.top))
        status = True

        return status
    except:
        raise ValueError("exception on click crypto erase")
        global_cfg.msgs.append("exception on click crypto erase")

def input_password_for_disable(op, title, pwd):
    status = False
    try:
        dlg = op.DevicesTable
        titleObj = dlg.child_window(title_re=title, control_type='Text', found_index=0)
        if ( titleObj.is_visible()):
            print("get correct title = " + titleObj.window_text())
        if ( input_password(op, pwd) ):
            time.sleep(5)
            status = True
        else:
            global_cfg.msgs.append("fail to input password")
        return status
    except:
        global_cfg.msgs.append("exception on input password for disable")
        raise ValueError("exception on input password for disable")

def verify_disable_security(op):
    status = False
    try:
        secureStatus = op.child_window(title_re='Password protection is disabled', control_type='Text')
        if (secureStatus.is_visible()):
            print("get correct msg = " + secureStatus.window_text())
            status = True
        else:
            global_cfg.msg.append("get wrong status {}", secureStatus.window_text())
        return status

    except:
        global_cfg.msgs.append("exception on verify disable security")
        raise ValueError("exception on verify disable security")

def signin_LyveHub(email, pwd):
    status = False
    try:
        time.sleep(2)
        app = Application(backend='uia').connect(title="Sign In with Auth0", top_level_only=True, found_index=0)
        op = app.window(title="Sign In with Auth0", control_type='Pane')
        #op.dump_tree()
        email_edit = op.child_window(auto_id="email-lyvehub", control_type="Edit")
        if ( email_edit.is_visible()):
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
        if ( login.is_visible()):
            login.click_input()
            print("click login")
            time.sleep(5)
            status = True
        else:
            global_cfg.msgs("login not visible")

        return status
    except:
        global_cfg.msgs.append("exception on input login LyveHub")
        raise ValueError("exception on input login LyveHub")

def input_password_for_crypto(op, name, pwd):
    status = False
    try:
        time.sleep(2)
        dlg = op.DevicesTable
        title = dlg.child_window(title_re='Crypto-erase', control_type='Text', found_index=0)
        if ( name in title.window_text()):
            print("get correct title = " + str(title.window_text()))

        status = input_password(op, pwd)
        return status
    except:
        global_cfg.msgs.append("exception on input password for crypto")
        raise ValueError("exception on input password for crypto")

def input_password(op, pwd):
    status = False
    try:
        dlg = op.DevicesTable
        edit = dlg.PasswordEdit
        if (edit.is_visible()):
            edit.type_keys(pwd)
            print("set pwd = " + str(pwd))
            time.sleep(1)
            applyBtn = dlg.child_window(auto_id="applyButton", control_type='Group')
            if (applyBtn.is_visible()):
                applyBtn.click_input()
                time.sleep(40)
                status = True
            else:
                global_cfg.msgs.append("button not visible")
        else:
            global_cfg.msgs.append("edit password fails to display")
        return status
    except:
        global_cfg.msgs.append("exception on input password")
        raise ValueError("exception on input password")

def input_password_with_trust(op, name, pwd, trusted):
    status = False
    try:
       # op.dump_tree()
        dlg = op.DevicesTable
        title = dlg.child_window(title_re=name, control_type='Text', found_index=0)
        if (name in title.window_text()):
            print("get correct title = " + str(title.window_text()))

        edit = dlg.PasswordEdit
        if (edit.is_visible()):
            edit.type_keys(pwd)
            print("set pwd = " + str(pwd))
            time.sleep(1)
            if ( trusted):
                trustTxt = dlg.child_window(title='Trust this computer', control_type='Text')
                trustTxt.click_input()
                print("click chbox trust")
            applyBtn = dlg.child_window(auto_id="applyButton", control_type='Group')
            if (applyBtn.is_visible()):
                applyBtn.click_input()
                time.sleep(30)
                status = True
            else:
                global_cfg.msgs.append("button not visible")
        else:
            global_cfg.msgs.append("edit password fails to display")
        return status
    except:
        global_cfg.msgs.append("exception on input password")
        raise ValueError("exception on input password")

def verify_setup_complete(op):
    status = False
    try:
        dlg = op.DevicesTable
        title = dlg.child_window(title="Setup Complete", control_type="Text")
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        doneBtn = dlg.child_window(title="Done")
        if ( doneBtn.is_visible()):
            doneBtn.click_input()
            time.sleep(1)
            secureStatus = op.child_window(title_re='Password protection is enabled', control_type='Text')
            if (secureStatus.is_visible()):
                print("get correct msg = " + secureStatus.window_text())
                status = True
            else:
                global_cfg.msg.append("get wrong status disable")

        else:
            global_cfg.msgs.append("Done not visible")
        return status
    except:
        global_cfg.msgs.append("exception on verify setup complete")
        raise ValueError("exception on verify setup complete")

def confirm_enable_security(op):
    status = False
    try:
        time.sleep(2)
        dlg = op.DevicesTable
        dlg.dump_tree()
        title = dlg.child_window(title="Lyve Client", control_type="Text")
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        msg = dlg.child_window(title_re="Keep your password", control_type="Text")
       # cbTxt = dlg.child_window(title_re="I understand the password I create cannot be recovered, not even by Seagate.", control_type="Text")
        if ( msg.is_visible()):
            #cbTxt.click_input()
            rect = msg.rectangle()
            print(rect)
            mouse.click(button='left', coords=(rect.left+5, rect.bottom+30))
            print("click checkbox")
            time.sleep(1)
            dlg.child_window(auto_id="applyButton", control_type="Group").click_input()
            time.sleep(1)
            status = True
        else:
            global_cfg.msgs.append("checkbox not visible")
        return status
    except:
        global_cfg.msgs.append("exception on confirm enable security")
        raise ValueError("exception on confirm enable security")

def confirm_crypto_erase(op, deviceName):
    status = False
    try:
        time.sleep(2)
        dlg = op.DevicesTable
        titleStr = "Crypto-erase " + deviceName
        title = dlg.child_window(title=titleStr, control_type="Text")
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        confirmTxt = dlg.child_window(title_re="Crypto-erase permanently deletes all data", control_type="Text")
        if ( confirmTxt.is_visible()):
            print("confirm msg = " + confirmTxt.window_text())
            confirmBtn = dlg.child_window(auto_id="applyButton", control_type="Group")
            if ( confirmBtn.is_visible()):
                confirmBtn.click_input()
                print("click Confirm")
                time.sleep(1)
                status = True
            else:
                global_cfg.msgs.append("confirm massage not visible")
        return status
    except:
        global_cfg.msgs.append("exception on confirm crypto erase")
        raise ValueError("exception on confirm crypto erase")

def certify_crypto_erase(op, deviceName):
    status = False
    try:
        time.sleep(2)
        dlg = op.DevicesTable
        titleStr = "Crypto-erase " + deviceName
        msg = "All data on " + deviceName + " has been crypto-erased"
        title = dlg.child_window(title=titleStr, control_type="Text")
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        confirmTxt = dlg.child_window(title_re=msg, control_type="Text")
        if ( confirmTxt.is_visible()):
            print("certify msg = " + confirmTxt.window_text())
            certifyBtn = dlg.child_window(auto_id="applyButton", control_type="Group")
            if ( certifyBtn.is_visible()):
                certifyBtn.click_input()
                print("click Certify")
                time.sleep(1)
                status = True
            else:
                global_cfg.msgs.append("certify massage not visible")
        return status
    except:
        global_cfg.msgs.append("exception on certify crypto erase")
        raise ValueError("exception on certify crypto erase")

def save_certificate_crypto_erase(op, deviceName):
    status = False
    try:
        dlg = op.DevicesTable
        titleStr = "Crypto-erase " + deviceName
        title = dlg.child_window(title=titleStr, control_type="Text")
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        listTxt = dlg.descendants(control_type="Text")
        for li in listTxt:
            print(li.window_text())

        saveBtn = dlg.child_window(auto_id="applyButton", control_type="Group")
        if ( saveBtn.is_visible()):
            saveBtn.click_input()
            print("click Save PDF")
            time.sleep(1)
            status = True
        else:
            global_cfg.msgs.append("Save PDF not visible")
        return status
    except:
        global_cfg.msgs.append("exception on save certificate crypto erase")
        raise ValueError("exception on save certificate crypto erase")

def save_pdf_explorer():
    status = False
    try:
        time.sleep(1)
        #warnings.simplefilter('ignore', category=UserWarning)
        #timings.Timings.slow()
        app = Application(backend='uia').connect(path='explorer.exe')
        saveAs = app.window(title='Save As', class_name="#32770")

        #saveAs = app.SaveAs
        print("get dlg")
        app.saveAs.SavePDF.click_input()
       # editTxt = saveDlg.child_window(title="File name", control_type="Edit")
       # print("edit text = " + editTxt.window_text())
        #saveBtn = lyve.child_window(title="Save PDF", control_type="Button")
        saveBtn = saveAs.SavePDF

        print("get save btn")
       # saveBtn.click_input()
        status = True
        return status
    except:
        print("get exception on save pdf explorer")

def create_password(op, pwd, trusted):
    status = False
    try:
        dlg = op.DevicesTable
        title = dlg.child_window(title='Create password', control_type='Text')
        if ( title.is_visible()):
            print("get correct title = " + title.window_text())
        pwdEdit = dlg.child_window(auto_id="password1", control_type="Edit")
        confPwd = dlg.child_window(auto_id="confirmPassword", control_type="Edit")
        if ( pwdEdit.is_visible()):
            pwdEdit.type_keys(pwd)
            if ( confPwd.is_visible() ):
                confPwd.type_keys(pwd)
                if ( trusted ):
                    trustCb = dlg.child_window(title='Trust this computer', control_type='Text')
                    if ( trustCb.is_visible()):
                        trustCb.click_input()
                    else:
                        global_cfg.msgs.append("Trust checkbox not visible")
                dlg.Next.click_input()
                status = True
                time.sleep(20)
            else:
                global_cfg.msgs.append("confirm pwd not visible")
        else:
            global_cfg.msgs.append("pwd edit not visible")
        return status
    except:
        global_cfg.msgs.append("exception on create password")
        raise ValueError("exception on create password")

def scroll_half_down(op):
    op.Document.wheel_mouse_input(wheel_dist=-5)
    print("scroll half down")
    time.sleep(2)

def scroll_down(op):
    op.Document.wheel_mouse_input(wheel_dist=-15)
    print("scroll down")
    time.sleep(2)

def scroll_up(op):
    op.Document.wheel_mouse_input(wheel_dist=15)
    print("scroll up")
    time.sleep(2)

def traverse_all_notifications(op):
    status = False
    try:
        notifyCus = op.NotificationsCustom
        listTxt = notifyCus.descendants(control_type='Text')
        for li in listTxt:
            if ( li.window_text() != ""):
                print("click txt = " + li.window_text())
                li.click_input()
                time.sleep(1)
        status = True
        return status
    except:
        raise ValueError("exception on click notification item")

def click_Custom_tab(title, rect):
    status = False
    try:
        left = rect.right
        top = rect.top
        mouse.click(button='left', coords=(left, top))
        print("click tab of title = " + title)
        status = True
        return status
    except:
        raise ValueError("exception on click custom tab")

def verify_accept_license(app):
    status = False
    try:
        time.sleep(2)
        #app.window(title='Lyve Pilot SC', visible_only=False).restore()
        app.window(title='Lyve Client').wait('visible', timeout=20, retry_interval=1)
        op = app.LyveClient

        listTxt = op.descendants(control_type='Text')
        for txt in listTxt:
            if ( txt.window_text().strip() == "End User License Agreement for Seagate Software"):
                print("get correct title = " + txt.window_text())
            else:
                print(txt.window_text())
        time.sleep(2)
        if (click_accept_checkbox(op)):
            if (click_Next(op)):
                status = True
            else:
                global_cfg.msgs.append("fail to verify accept license")
        return status
    except:
        raise ValueError("get exception on verify accept license")

def click_accept_checkbox(op):
    status = False
    try:
        time.sleep(3)
        op.Document.dump_tree()
        cbox = op.child_window(title_re='If you accept the terms', control_type="Text")
        rec = cbox.rectangle()
        mouse.move(coords=(rec.left+7, rec.top+40))
        mouse.click(button='left', coords=(rec.left+7, rec.top+40))
        print("click checkbox")
        status = True
        '''''
        chbox = op.child_window(title='I accept the terms of the License Agreement and Privacy Policy', control_type='Text')
        time.sleep(1)
        if ( chbox.is_visible()):
            chbox.click_input()
            print("click checkbox")
            time.sleep(1)
            status = True
        else:
            global_cfg.msgs.append("checkbox not visible")
        '''''

        return status
    except:
        raise ValueError("exception on click accept checkbox")

def click_Next(op):
    status = False
    try:
       # op.dump_tree()
        nextBtn = op.child_window(auto_id='acceptButton', control_type='Group')
        if ( nextBtn.is_visible()):
            nextBtn.click_input()
            status = True
        else:
            global_cfg.msgs.append("Next button not visible")
        return status
    except:
        raise ValueError("exception on click Next")

def click_Data_tab(op):
    status = False
    try:
        dataCus = op.DataStatic
        if ( dataCus.is_visible()):
            dataCus.click_input()
            print("click Data tab")
            status = True
        else:
            global_cfg.msgs.append("Data tab not visible")
        if (not status):
            global_cfg.msgs.append("fail to click Data tab")
        return status
    except:
        raise ValueError("exception on click Data tab")

def click_Settings_link(op):
    status = False
    try:
        settings = op.SettingsHyperlink
        if ( settings.is_visible()):
            settings.click_input()
            print("click Settings")
            status = True
        else:
            global_cfg.msgs.append("Settings link not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to click Settings")
        return status
    except:
        raise ValueError("exception on click Settings link")

def click_Settings_tab(op):
    status = False
    try:
        settings = op.child_window(title='Settings', control_type='Text')
        if ( settings.is_visible()):
            settings.click_input()
            print("click Settings tab")
            status = True
        else:
            global_cfg.msgs.append("Settings tab not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to click Settings tab")
        return status
    except:
        raise ValueError("exception on click Settings tab")

def verify_Settings_About_version(op, version):
    status = False
    try:
        about = op.child_window(title_re='Lyve Client version', control_type='Text')
        if ( about.is_visible()):
            print("version txt = " + about.window_text())
            verTxt = about.window_text()[20:]
            print("version = " + verTxt)
            print("version download = " + version)
            if ( verTxt.strip() == version.strip() ):
                print("get correct version = " + version)
                status = True
            else:
                msg = "get wrong version {}".format(verTxt)
                global_cfg.msgs.append(msg)
        else:
            global_cfg.msgs.append("About not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to verify About version")
        return status
    except:
        raise ValueError("exception on verfiy About version")

def click_Workflows_tab(op):
    status = False
    try:
        workflow = op.WorkflowsStatic
        if ( workflow.is_visible()):
            workflow.click_input()
            print("click Workflows tab")
            status = True
        else:
            global_cfg.msgs.append("Workflow tab not visible")
        return status
    except:
        raise ValueError("exception on click Workflows tab")

def click_Devices_tab(op):
    status = False
    try:
        devicesCus = op.DevicesStatic
        if ( devicesCus.is_visible()):
            devicesCus.click_input()
            status=True
            print("click Devices tab")
        else:
            global_cfg.msgs.append("Devices tab not visible")
        return status
    except:
        raise ValueError("exception on click Devices tab")

def click_Activity_tab(op):
    status = False
    try:
        activity = op.Activity
       # activity.dump_tree()
        if ( activity.is_visible()):
            activity.click_input()
            print("click Activity tab")
            time.sleep(1)
            status = True
        else:
            global_cfg.msgs.append("Activity not visible")
        return status
    except:
        raise ValueError("exception on click Activity tab")

def verify_data_activity_page(op):
    status = False
    try:
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
       # actTable.dump_tree()
        titleTxt = op.child_window(title_re='Data activity', control_type='Text', found_index=0)
        title = titleTxt.window_text()
        print("title = " + title)
        dataList = actTable.descendants(control_type='DataItem')
        for li in dataList:
            print(li.window_text())
        status = True
        return status
    except:
        raise ValueError("get exception on verify data activity page")

def verify_inspect_data_activity_page(op):
    status = False
    try:
        time.sleep(2)
       # op.dump_tree()
        listBox = op.ListBox
        if ( listBox.is_visible()):
            itemList = listBox.descendants(class_name='ListItem')
            for li in itemList:
                print("item = " + li.window_text())
            listTxt = op.Document.descendants(control_type='Text')
            for i in range(len(listTxt)):
                txt = listTxt[i].window_text()
                print(txt)
                if ( txt == "Throughput"):
                    thruput = listTxt[i+1].window_text()
                    print("Throughput = " + thruput)
                elif ( txt == "Bundle ID"):
                    bundleId = listTxt[i+1].window_text()
                    print("Bundle ID = " + bundleId)
            status = True
        else:
            global_cfg.msgs.append("listBox is not visible")
        if ( not status ):
            global_cfg.msgs.append("fail to verify inspecct data activity page")
        return status
    except:
        raise ValueError("get exception on verify inspect data activity page")

def verify_click_data_activity_link(op):
    status = False
    try:
        datalink = op.child_window(title='Data activity list', control_type='Hyperlink')
        datalink.click_input()
        status = True
        return status
    except:
        raise ValueError("get exception on verify click data activity link")

def verify_click_data_activity_latest_action(op, action):
    status = False
    try:
        time.sleep(3)
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        latest = actTable.child_window(auto_id='rowID0')
        dataList = latest.descendants(control_type='DataItem')
        statusCol = dataList[len(dataList)-1]
        rect = statusCol.rectangle()
        if ( statusCol.window_text().__contains__("Completed")):
            if ( action == "Inspect"):
                mouse.double_click(button='left', coords=(rect.right-50, rect.top+40))
            elif ( action == "Delete"):
                mouse.move( coords=(rect.right - 90, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right-90, rect.top+45))
            elif ( action == "Copy"):
                mouse.double_click(button='left', coords=(rect.right-110, rect.top+45))
            print("click action = " + action)
            time.sleep(1)
            status = True
        elif ( statusCol.window_text().__contains__("Aborted")):
            if (action == "Inspect"):
                mouse.move(coords=(rect.right - 50, rect.top + 40))
                mouse.click(button='left', coords=(rect.right - 50, rect.top + 40))
            elif (action == "Delete"):
                mouse.move(coords=(rect.right - 90, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right - 90, rect.top + 45))
            print("click action = " + action)
            status = True
        else:
            print("status = " + statusCol.window_text())
            if (action == "Inspect"):
                mouse.move(coords=(rect.right - 50, rect.top + 40))
                mouse.double_click(button='left', coords=(rect.right - 50, rect.top + 40))
            elif (action == "Abort"):
                mouse.move(coords=(rect.right - 90, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right - 90, rect.top + 45))
            print("click action = " + action)
            status = True
        if ( not status ):
            msg = "fail to click action {} on latest data activity".format(action)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("get exception on verify click data activity latest action")

def verify_click_data_activity_action(op, action):
    status = False
    try:
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        latest = actTable.child_window(auto_id='rowID1')
        dataList = latest.descendants(control_type='DataItem')
        statusCol = dataList[len(dataList)-1]
        rect = statusCol.rectangle()
        if ( statusCol.window_text().__contains__("Completed")):
            if ( action == "Inspect"):
                mouse.double_click(button='left', coords=(rect.right-50, rect.top+40))
            elif ( action == "Delete"):
                mouse.move( coords=(rect.right - 90, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right-88, rect.top+45))
            elif ( action == "Copy"):
                mouse.double_click(button='left', coords=(rect.right-110, rect.top+45))
            print("click action = " + action)
            status = True
        elif ( statusCol.window_text().__contains__("Aborted")):
            if (action == "Inspect"):
                mouse.move(coords=(rect.right - 50, rect.top + 40))
                mouse.double_click(button='left', coords=(rect.right - 50, rect.top + 40))
            elif (action == "Delete"):
                mouse.move(coords=(rect.right - 87, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right - 90, rect.top + 45))
            print("click action = " + action)
            status = True
        else:
            if (action == "Inspect"):
                mouse.move(coords=(rect.right - 50, rect.top + 40))
                mouse.click(button='left', coords=(rect.right - 50, rect.top + 40))
            elif (action == "Abort"):
                mouse.move(coords=(rect.right - 87, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right - 90, rect.top + 45))
            print("click action = " + action)
            status = True
        if (not status):
            msg = "fail to click action {} on data activity".format(action)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("get exception on verify click data activity action")

def get_row_data_activity(table, type, source ):
    rowId = 0
    try:
        found = False
        dataCus = table.descendants(control_type='Custom')
        for j in range(len(dataCus)):
            dataList = dataCus[j].descendants(control_type='DataItem')
            for i in range(len(dataList)):
                dtype = dataList[1].window_text()
                dsource = dataList[2].window_text()
                if (dtype == type and dsource == source):
                    print("dtype=" + dtype)
                    print("dsource =" + dsource)
                    rowId = j
                    print("rowId = " + str(rowId))
                    found = True
                    break
            if (found):
                print("found row")
                break


        return rowId
    except:
        raise ValueError("get exception on get row data activity")

def verify_click_data_activity_action_type_source(op, action, type, source):
    status = False
    try:
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        rowId = get_row_data_activity(actTable, type, source)
        strId = "rowID" + str(rowId-1)
        selectedRow = actTable.child_window(auto_id=strId)
        dataList = selectedRow.descendants(control_type='DataItem')
        statusCol = dataList[len(dataList)-1]
        rect = statusCol.rectangle()
        if ( statusCol.window_text().__contains__("Completed")):
            if ( action == "Inspect"):
                mouse.double_click(button='left', coords=(rect.right-50, rect.top+40))
            elif ( action == "Delete"):
                mouse.move( coords=(rect.right - 90, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right-88, rect.top+45))
            elif ( action == "Copy"):
                mouse.double_click(button='left', coords=(rect.right-110, rect.top+45))
            print("click action = " + action)
            status = True
        elif ( statusCol.window_text().__contains__("Aborted")):
            if (action == "Inspect"):
                mouse.move(coords=(rect.right - 50, rect.top + 40))
                mouse.double_click(button='left', coords=(rect.right - 50, rect.top + 40))
            elif (action == "Delete"):
                mouse.move(coords=(rect.right - 87, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right - 90, rect.top + 45))
            print("click action = " + action)
            status = True
        else:
            if (action == "Inspect"):
                mouse.move(coords=(rect.right - 50, rect.top + 40))
                mouse.click(button='left', coords=(rect.right - 50, rect.top + 40))
            elif (action == "Abort"):
                mouse.move(coords=(rect.right - 87, rect.top + 45))
                mouse.double_click(button='left', coords=(rect.right - 90, rect.top + 45))
            print("click action = " + action)
            status = True
        if (not status):
            msg = "fail to click action {} on data activity".format(action)
            global_cfg.msgs.append(msg)

        return status
    except:
        raise ValueError("get exception on verify click data activity action type source")

def verify_confirm_delete_destination_data(op, confirm):
    status = False
    try:
        time.sleep(4)
        dashTable = op.DevicesTable
        titleStr = "Delete destination data"
        if ( dashTable.is_visible()):
            title = dashTable.child_window(title=titleStr, control_type='Text')
            if ( title.is_visible()):
                print("get correct title table = " + title.window_text())
            else:
                msg = "Title not visible {}".format(titleStr)
                global_cfg.msgs.append(msg)
            if ( confirm ):
                deleteBtn = dashTable.child_window(title='Delete')
                if (deleteBtn.is_visible()):
                    deleteBtn.click_input()
                    print("click Delete btn")
                    status = True
                else:
                    global_cfg.msgs.append("Delete button not visible")
            else:
                unDelete = dashTable.child_window(title='Do not delete')
                if ( unDelete.is_visible()):
                    unDelete.click_input()
                    print("click Do not delete btn")
                    status = True
                else:
                    global_cfg.msgs.append("Do not delete button not visible")
        else:
            global_cfg.msgs.append("dialog not visible")
        if (not status):
            global_cfg.msgs.append("fail to confirm delete data destination")
        return status
    except:
        raise ValueError("get exception on verify confirm delete data destination")

def verify_confirm_abort_activity(op, confirm):
    status = False
    try:
        time.sleep(3)
        dashTable = op.DevicesTable
        titleStr = "Abort activity"
        title = dashTable.child_window(title=titleStr, control_type='Text')
        if ( title.is_visible()):
            print("get correct title table = " + title.window_text())
        else:
            msg = "Title not visible {}".format(titleStr)
            global_cfg.msgs.append(msg)
        if ( confirm ):
            abortBtn = dashTable.child_window(title='Abort')
            if (abortBtn.is_visible()):
                abortBtn.click_input()
                print("click Abort btn")
                status = True
            else:
                global_cfg.msgs.append("Abory button not visible")
        else:
            cancel = dashTable.child_window(title='Cancel abort')
            if ( cancel.is_visible()):
                cancel.click_input()
                print("click Cancel abort btn")
                status = True
            else:
                global_cfg.msgs.append("Do not delete button not visible")

        if (not status):
            global_cfg.msgs.append("fail to confirm abort activity")
        return status
    except:
        raise ValueError("get exception on verify confirm abort activity")


def get_latest_row_data_activity(op, type):
    rowId = 0
    try:
        time.sleep(2)
        table = op.child_window(auto_id='DataActivityTable', control_type='Table')
        rowCus = None
        if ( type == 'Copy' or type == 'Delete'):
            rowId = 0
            rowCus = table.child_window(auto_id='rowID0', control_type='Custom')

        itemList = rowCus.descendants(control_type='DataItem')
        typeVal = itemList[0].window_text()
        print("type val = " + typeVal)

        return rowId
    except:
        raise ValueError("get exception on get latest row data activity")


def get_first_row_data_activity(op, type):
    rowId = 0
    try:
        time.sleep(2)
        table = op.child_window(auto_id='DataActivityTable', control_type='Table')
        #table.dump_tree()
        rowList = table.descendants(control_type='Custom')
        lenRow = len(rowList)

        i = lenRow - 1
        row = "rowID" + str(i - 1)
        rowCus = table.child_window(auto_id=row, control_type='Custom')

        itemList = rowCus.descendants(control_type='DataItem')
        typeVal = itemList[0].window_text()
        print("type val = " + typeVal)
        if (type == typeVal):
           rowId = i
        else:
            rowId = i-1
        print("rowId = " + str(rowId))
        return rowId
    except:
        raise ValueError("get exception on get row data activity")

def verify_data_activity_latest_status(op, type, statusRun):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = False
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')

        latest =  actTable.child_window(auto_id='rowID0')
        dataList = latest.descendants(control_type='DataItem')
        typeCol = dataList[1].window_text()
        if (typeCol == type):
            print("get correct type = " + type)
            status1 = True
        else:
            msg = "get wrong type {}".format(typeCol)
            global_cfg.msgs.append(msg)
        statusCol = dataList[len(dataList)-1].window_text()
        print("statusCol = " + statusCol)
        if ( statusCol.__contains__(statusRun)):
            print("get correct status = " + statusCol)
            status2 = True
        else:
            msg = "get wrong status {}".format(statusCol)
            global_cfg.msgs.append(msg)
        if (status1 and status2):
            status = True
        if ( not status):
            global_cfg.msgs.append("fail to verify data activity latest status")
        return status
    except:
        raise ValueError("get exception on verify data activity latest status")

def verify_data_activity_status(op, type, statusRun):
    status = False
    try:
        time.sleep(3)
        status1 = status2 = False
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
       # actTable.dump_tree()
        secondRow = actTable.child_window(auto_id='rowID1')
        if ( secondRow.is_visible()):
            dataList = secondRow.descendants(control_type='DataItem')
            typeCol = dataList[1].window_text()
            print("typeCol = " + typeCol)
            if ( typeCol == type ):
                print("get correct type = " + typeCol)
                status1 = True
            else:
                msg = "get wrong type {}".format(typeCol)
                global_cfg.msgs.append(msg)
            statusCol = dataList[len(dataList)-1].window_text()
            if ( statusCol.__contains__(statusRun)):
                print("get correct status = " + statusCol)
                status2 = True
            else:
                msg = "get wrong status {}".format(statusCol)
                global_cfg.msgs.append(msg)
        else:
            global_cfg.msgs.append("second row not visible")
        if ( status1 and status2):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify data activity status")
        return status
    except:
        raise ValueError("get exception on verify data activity status")

def verify_data_activity_source_destination(op, type, source, destination):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = status3 = False
        op.dump_tree()
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        rowId = 'rowID0'
        latest = actTable.child_window(auto_id=rowId)
        dataList = latest.descendants(control_type='DataItem')
        typeCol = dataList[1].window_text()
        print("typeCol = " + typeCol)
        if (typeCol == type):
            status1 = True
        else:
            msg = "get wrong type {}".format(typeCol)
            global_cfg.msgs.append(msg)
        sourceCol = dataList[2].window_text()
        if (sourceCol == source):
            print("get correct source = " + sourceCol)
            status2 = True
        else:
            msg = "get wrong source {}".format(sourceCol)
            global_cfg.msgs.append(msg)

        if ( type == "Copy"):
            destCol = dataList[3].window_text()
            if (destCol == destination):
                print("get correct destination = " + destCol)
                status3 = True
            else:
                msg = "get wrong destination {}".format(destCol)
                global_cfg.msgs.append(msg)
        else:
            status3 = True

        if (status1 and status2 and status3):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify data activity source destination")
        return status
    except:
        raise ValueError("get exception on verify data activity source destination")

def verify_data_activity_latest_source_destination(op, type, source, destination):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = False
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        rowId = 'rowID0'
        latest = actTable.child_window(auto_id=rowId)
        dataList = latest.descendants(control_type='DataItem')
        typeCol = dataList[1].window_text()
        print("typeCol = " + typeCol)
        if (typeCol == type):
            status1 = True
        else:
            msg = "get wrong type {}".format(typeCol)
            global_cfg.msgs.append(msg)

        sourceCol = dataList[2].window_text()
        if (sourceCol == source):
            print("get correct source = " + sourceCol)
            status2 = True
        else:
            msg = "get wrong source {}".format(sourceCol)
            global_cfg.msgs.append(msg)

        if (status1 and status2):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify data activity latest source destination")
        return status
    except:
        raise ValueError("get exception on verify data activity latest source destination")


def verify_data_activity_latest_source(op, source):
    status = False
    try:
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        latest = actTable.child_window(auto_id='rowID0')
        dataList = latest.descendants(control_type='DataItem')
        sourceVal = dataList[len(dataList) - 3].window_text()
        if ( sourceVal == source ):
            print("get correct source = " + source)
            status = True
        else:
            print("get wrong source = " + sourceVal)
        return status
    except:
        raise ValueError("get exception on verify data activity latest source")

def verify_data_activity_latest_destination(op, destination):
    status = False
    try:
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        latest = actTable.child_window(auto_id='rowID0')
        dataList = latest.descendants(control_type='DataItem')
        destVal = dataList[len(dataList) - 2].window_text()
        if ( destVal == destination ):
            print("get correct destination = " + destination)
            status = True
        else:
            print("get wrong destination = " + destVal)
        return status
    except:
        raise ValueError("get exception on verify data activity latest destination")

def verify_data_activity_latest_type(op, type):
    status = False
    try:
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        latest = actTable.child_window(auto_id='rowID0')
        dataList = latest.descendants(control_type='DataItem')
        typeVal = dataList[len(dataList) - 4].window_text()
        if ( typeVal == type ):
            print("get correct type = " + type)
            status = True
        else:
            print("get wrong type = " + typeVal)
        return status
    except:
        raise ValueError("get exception on verify data activity latest type")

def verify_data_activity_latest(op, type, source, destination, statusRun):
    status = False
    try:
        status1 = status2 = status3 = status4 = False
        actTable = op.child_window(auto_id='DataActivityTable', control_type='Table')
        latest = actTable.child_window(auto_id='rowID0')
        dataList = latest.descendants(control_type='DataItem')
        for li in dataList:
            value = li.window_text()
            print(value)
            if ( value == type ):
                print("get correct type = " + type)
                status1 = True
            elif ( value == source ):
                print("get correct source = " + source)
                status2 = True
            elif ( value == destination ):
                print("get correct destination = " + destination)
                status3 = True
            elif ( value.__contains__(statusRun)):
                print("get correct status = " + statusRun)
                status4 = True
        if ( status1 and status2 and status3 and status4):
            status = True
        if ( not status1):
            print("get wrong value of type")
        if ( not status2):
            print("get wrong value of source")
        if ( not status3):
            print("get wrong value of destination")
        elif ( not status4):
            print("get wrong value of status")

        return status
    except:
        raise ValueError("get exception on verify data activity latest")

def verify_devices_page(op):
    status = False
    try:
        time.sleep(1)
        titleTxt = op.child_window(title_re='Devices', control_type='Text', found_index=0)
        title = titleTxt.window_text()
        print("title = " + title)
        if ( title[:8] == "Devices"):
            print("get title = " + title)
            status = True
        else:
            global_cfg.msgs.append("get wrong title")
        time.sleep(1)
        return status
    except:
        raise ValueError("get exception on verify devices page")

def verify_click_add_external_endpoint(op):
    status = False
    try:

        dbImage = op.child_window(title="add-menu", control_type="Image")
        if (dbImage.is_visible()):
            dbImage.click_input()
            addEp = op.child_window(title="Add External Endpoint", control_type="Text")
            if ( addEp.is_visible()):
                addEp.click_input()
                print("click Add external endpoint")
                status = True
                time.sleep(1)
            else:
                global_cfg.msgs.append("Add external endpoint not visible")
        else:
            global_cfg.msgs.append("Add menu not visible")

        return status
    except:
        raise ValueError("get exception on verify click add external endpoint")

def verify_click_add_endpoint_from_settings(op):
    status = False
    try:
        endpoint = op.child_window(title="External endpoints", control_type="Text")
        if ( endpoint.is_visible()):
            rect = endpoint.rectangle()
            print(rect)
            mouse.move(coords=(rect.right +600, rect.top))
            mouse.click(button='left', coords=(rect.right+600, rect.top))
            addImage = op.ExternalendpointsImage
            if ( addImage.is_visible()):
                addImage.click_input()
                status = True
                time.sleep(1)
            else:
                global_cfg.msgs.append(("no add image visible"))
        else:
            global_cfg.msgs.append("external endpoints not visible")

        return status
    except:
        raise ValueError("get exception on verify click add external endpoint")
def verify_click_Next_external_endpoint(op):
    status = False
    try:
        table = op.DevicesTable
        listText = table.descendants(control_type="Text")
        for it in listText:
            print(it.window_text())
        next = op.child_window(title="Next", auto_id="applyButton")
        if (next.is_visible()):
            next.click_input()
            print("click Next")
            status = True
        else:
            global_cfg.msgs.append("Next not visible")

        return status
    except:
        raise ValueError("get exception on verify click Next external endpoint")

def verify_enter_bucket_url(op, url):
    status = False
    try:
        status1 = status2 = False
        table = op.DevicesTable

        listTxt = table.descendants(control_type="Text")
        print("title = " + listTxt[0].window_text())
        if ( listTxt[0].window_text() == "New Endpoint"):
            status1 = True
        editUrl = table.BucketURLEdit

        if ( editUrl.is_visible()):
            editUrl.set_text(url)
            editUrl.type_keys("{ENTER}")
            time.sleep(1)
            print("type url = " + url)
            status2 = True
        if (status1 and status2):
            status = True

        return status
    except:
        raise ValueError("get exception on verify enter bucket url")

def verify_enter_new_endpoint(op, url, name, accessKey, secretKey):
    status = False
    try:
        status1 = status2 = status3 = status4 = status5 = False
        table = op.DevicesTable
        listTxt = table.descendants(control_type="Text")
        print("title = " + listTxt[0].window_text())
        if ( listTxt[0].window_text() == "New Endpoint"):
            status1 = True
        #table.print_control_identifiers()
        editUrl = table.child_window(auto_id="endpointBucketUrl", control_type="Edit")
        print(editUrl.iface_value.CurrentValue)
        editName = table.child_window(auto_id="endpointName", control_type="Edit")
        curName = editName.iface_value.CurrentValue
        print("curName = " + curName)
        if ( name != ""):
            editName.type_keys("{BACKSPACE}")
            editName.set_text(name)
            editName.type_keys("{ENTER}")
            print(editName.iface_value.CurrentValue)

        region = table.child_window(auto_id="regionMenu")
        regionTxt = region.child_window(control_type='Text')
        print("region txt = " + regionTxt.window_text())
        editAccKey = table.child_window(auto_id="accessKey", control_type="Edit")
        editSecKey = table.child_window(auto_id="secretKey", control_type="Edit")
        if (editAccKey.is_visible()):
            editAccKey.set_text(accessKey)
            editAccKey.type_keys("{ENTER}")
            print("type access key = " + accessKey)
            time.sleep(1)
            status2 = True
        else:
            print("edit Access Key not visible")

        if (editSecKey.is_visible()):
            editSecKey.set_text(secretKey)
            editSecKey.type_keys("{ENTER}")
            print("type secret key = " + secretKey)
            status3 = True
        else:
            print("edit secret Key not visible")

        validateBtn = table.child_window(title="Validate Connection", control_type="Text")

        if (validateBtn.is_visible()):
            validateBtn.click_input()
            time.sleep(2)
            status4 = True
        saveBtn = table.child_window(auto_id="applyButton")
        if (saveBtn.is_visible()):
            saveBtn.click_input()
            status5 = True
        if (status1 and status2 and status3 and status4 and status5):
            status = True
        if (not status):
            print("fail to verify enter new enter point")

        return status
    except:
        raise ValueError("get exception on verify enter new endpoint")

def verify_click_new_folder_endpoint(op):
    status = False
    try:
        time.sleep(1)
        table = op.DevicesTable
        newFolder = table.child_window(title="New Folder", control_type="Text")
        if (newFolder.is_visible()):
            newFolder.click_input()
            status = True

        return status
    except:
        raise ValueError("get exception on verify click new folder endpoint")

def verify_click_create_new_folder(op, folder):
    status = False
    try:
        table = op.DevicesTable2
        newFolder = table.child_window(title="New Folder", auto_id="textInput")
        if (newFolder.is_visible()):
            newFolder.set_text(folder)
            newFolder.type_keys("{ENTER}")
            create = table.child_window(auto_id="activeButton")
            if (create.is_visible()):
                create.click_input()
                time.sleep(1)
                status = True

        return status
    except:
        raise ValueError("get exception on verify click create new folder")

def verify_click_save_endpoint(op, folder):
    status = False
    try:
        time.sleep(1)
        #op.dump_tree()
        table = op.DevicesTable
        if ( folder != ""):
            folderCreated = table.child_window(title=folder, control_type="Text")
            if ( folderCreated.is_visible()):
                print("get new folder created = " + folder)
        save = table.child_window(auto_id="applyButton", control_type="Group")
        if ( save.is_visible()):
            save.click_input()
            status = True
        return status
    except:
        raise ValueError("get exception on verify click save endpoint")

def verify_click_edit_endpoint(op, name):
    status = False
    try:
        time.sleep(2)
        scroll_down(op)
        titleEP = op.child_window(title=name, control_type='Text', found_index=0)
        title = titleEP.window_text()
        print("title = " + title)
        rect = titleEP.rectangle()
        print(rect)
       # mouse.double_click(button='left', coords=(rect.right-40, rect.top-20))
        mouse.double_click(button='left', coords=(rect.right-5, rect.top-20))
        status = True
        return status
    except:
        raise ValueError("get exception on verify click edit endpoint")

def verify_edit_name_endpoint(op, url, name):
    status = False
    try:
        status1 = status2 = status3 = status4 = status5 = False
        table = op.DevicesTable
        time.sleep(1)
        listTxt = table.descendants(control_type="Text")
        print("title = " + listTxt[0].window_text())

        editUrl = table.child_window(auto_id="endpointBucketUrl", control_type="Edit")
        curUrl = editUrl.iface_value.CurrentValue
        if ( url != curUrl):
            editUrl.type_keys("{BACKSPACE}")
            editUrl.set_text(url)
            editUrl.type_keys("{ENTER}")
            print(editUrl.iface_value.CurrentValue)
        editName = table.child_window(auto_id="endpointName", control_type="Edit")
        curName = editName.iface_value.CurrentValue

        if (name != curName):
            editName.type_keys("{BACKSPACE}")
            editName.set_text(name)
            editName.type_keys("{ENTER}")
            print(editName.iface_value.CurrentValue)

        saveBtn = table.child_window(auto_id="applyButton")

        if (saveBtn.is_visible()):
            saveBtn.click_input()
            status = True
        if (not status):
            global_cfg.msg("fail to verify edit name endpoint")

        return status
    except:
        raise ValueError("get exception on verify edit name endpoint")

def verify_click_edit_endpoint_from_activity(op, name):
    status = False
    try:
        time.sleep(2)
       # op.dump_tree()
        print("name=" + name)
        titleEP = op.child_window(title_re=name, control_type='Text', found_index=0)
        title = titleEP.window_text()
        print("title = " + title)
        rect = titleEP.rectangle()
        mouse.double_click(button='left', coords=(rect.right+400, rect.top-20))
        status = True

        return status
    except:
        raise ValueError("get exception on verify click edit endpoint from activity")

def verify_edit_endpoint(op, url, name):
    status = False
    try:
        status1 = status2 = status3 = status4 = status5 = False
        table = op.DevicesTable
       # op.dump_tree()
        time.sleep(1)
        listTxt = table.descendants(control_type="Text")
        print("title = " + listTxt[0].window_text())

        editUrl = table.child_window(auto_id="endpointBucketUrl", control_type="Edit")
        curUrl = editUrl.iface_value.CurrentValue
        print("curUrl = " + curUrl)
        if ( url != curUrl):
            editUrl.type_keys("{BACKSPACE}")
            editUrl.set_text(url)
            editUrl.type_keys("{ENTER}")
            print(editUrl.iface_value.CurrentValue)
            status1 = True
        editName = table.child_window(auto_id="endpointName", control_type="Edit")
        curName = editName.iface_value.CurrentValue

        if (name != curName):
            editName.type_keys("{BACKSPACE}")
            editName.set_text(name)
            editName.type_keys("{ENTER}")
            print(editName.iface_value.CurrentValue)
            status2 = True

        region = table.child_window(auto_id="regionMenu", control_type="Custom")
        regionTxt = region.child_window(control_type='Text')
        saveBtn = table.child_window(auto_id="applyButton")
        if ( status1 ):
            optional = table.child_window(title_re="Optional:")
            optional.click_input()
          #  table.dump_tree()
        if (saveBtn.is_visible()):
            saveBtn.click_input()
            status = True
        if (not status):
            global_cfg.msg("fail to verify edit name endpoint")

        return status
    except:
        raise ValueError("get exception on verify edit endpoint")

def verify_edit_endpoint_with_keys(op, url, name, accessKey, secretKey):
    status = False
    try:
        status1 = status2 = False
        table = op.DevicesTable
       # op.dump_tree()
        time.sleep(1)
        listTxt = table.descendants(control_type="Text")
        print("title = " + listTxt[0].window_text())

        editUrl = table.child_window(auto_id="endpointBucketUrl", control_type="Edit")
        curUrl = editUrl.iface_value.CurrentValue
        print("curUrl = " + curUrl)
        if ( url != curUrl):
            editUrl.type_keys("{BACKSPACE}")
            editUrl.set_text(url)
            editUrl.type_keys("{ENTER}")
            print(editUrl.iface_value.CurrentValue)
        editName = table.child_window(auto_id="endpointName", control_type="Edit")
        curName = editName.iface_value.CurrentValue

        if (name != curName):
            editName.type_keys("{BACKSPACE}")
            editName.set_text(name)
            editName.type_keys("{ENTER}")
            print(editName.iface_value.CurrentValue)

        editAccKey = table.child_window(auto_id="accessKey", control_type="Edit")
        editSecKey = table.child_window(auto_id="secretKey", control_type="Edit")
        if (editAccKey.is_visible()):
            editAccKey.set_text(accessKey)
            editAccKey.type_keys("{ENTER}")
            print("type access key = " + accessKey)
            time.sleep(1)
        else:
            print("edit Access Key not visible")

        if (editSecKey.is_visible()):
            editSecKey.set_text(secretKey)
            editSecKey.type_keys("{ENTER}")
            print("type secret key = " + secretKey)
        else:
            print("edit secret Key not visible")

        validateBtn = table.child_window(title="Validate Connection", control_type="Text")

        if (validateBtn.is_visible()):
            validateBtn.click_input()
            time.sleep(1)
            status1 = True
        nextBtn = table.child_window(auto_id="applyButton")
        if (nextBtn.is_visible()):
            nextBtn.click_input()
            status2 = True
        if (status1 and status2 ):
            status = True
        if (not status):
            global_cfg.msg("fail to verify edit endpoint with keys")

        return status
    except:
        raise ValueError("get exception on verify edit endpoint with keys")

def verify_click_delete_endpoint(op, name):
    status = False
    try:
        time.sleep(1)
        titleEP = op.child_window(title=name, control_type='Text', found_index=0)
        title = titleEP.window_text()
        print("title = " + title)
        rect = titleEP.rectangle()
        print(rect)
       # mouse.move(coords=(rect.right+10, rect.top-20))
        mouse.click(button='left', coords=(rect.right+35, rect.top-20))
        status = True

        return status
    except:
        raise ValueError("get exception on verify click delete External endpoints")

def verify_delete_endpoint(op, name, confirm):
    status = False
    try:
        table = op.DevicesTable2
        listTxt = table.descendants(control_type='Text')
        title = listTxt[0].window_text()
        print("title=" + title)
        msg = listTxt[2].window_text()
        print("msg =" + msg)
        if ( name in msg ):
            print("get correct name endpoint removed = " + name)
        removeBtn = table.child_window(auto_id="upscaleButton", control_type="Group")
        if (confirm):
            removeBtn.click_input()
        else:
            cancelBtn = table.child_window(auto_id="plainCancelButton", control_type="Group")
            cancelBtn.click_input()
        status = True
        time.sleep(1)
        return status
    except:
        raise ValueError("get exception on verify delete endpoint")

def toggle_view(op):
    status = False
    try:
        time.sleep(1)
        rect = op.rectangle()
        print(rect)
        title = op.child_window(title_re='Showing', control_type='Text')
        rect1 = title.rectangle()
        print(rect1)
        mouse.click(button='left', coords=(rect.right-75, rect1.top))
        print("click toggle view")
        status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click toggle list view")
        return status
    except:
        raise ValueError("exception on toggle view")

def click_icon_view(op):
    status = False
    try:
       # op.Document.dump_tree()
        time.sleep(1)
        header = op.child_window(title='Last activity', control_type='Header')
        rect = header.rectangle()

        mouse.click(button='left', coords=(rect.right-20, rect.top-50))
        print("click toggle icon view")
        status = True
        if ( not status ):
            global_cfg.msgs.append("fail to click icon view")
        return status
    except:
        raise ValueError("exception on toggle icon view")

def click_Lyve_drive_link(op):
    status = False
    try:
        op.Document.Hyperlink3.click_input()
        print("click Lyve Client link")
        status = True
        return status
    except:
        raise ValueError("exception on toggle view")

def click_Seagate_icon(op):
    status = False
    try:
        op.Hyperlink3.click_input()
        print("click Seagate Icon")
        status = True
        return status
    except:
        raise ValueError("exception on click Seagate icon")

def click_device_list_link(op):
    status = False
    try:
        print("click device list link")
       # op.Document.dump_tree()
        deviceList = op.child_window(title='Device list', control_type='Hyperlink')
        deviceList.click_input()
        print("click Device list link")
        status = True
        return status
    except:
        raise ValueError("exception on click device list link")

def click_device_inspect(op, deviceName):
    status = False
    try:
        time.sleep(5)
        control = op.child_window(title=deviceName, found_index=0)
        if ( control.is_visible()):
            print("click Inspect = " + control.window_text())
            time.sleep(1)
            control.click_input()
            time.sleep(1)
           # op.dump_tree()
            status = True
        else:
            msg = "device {} not visible".format(deviceName)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on click device inspect")

def click_unlock_device_iconview(op, deviceName, pwd, trusted):
    status = False
    try:
       # op.dump_tree()
        locked = op.child_window(title="locked", control_type="Text")
        if ( locked.exists()):
            rect = locked.rectangle()
            print(rect)
            lyveMobi = op.child_window(title_re="Lyve Mobile Array", control_type="Text")
            rectLyve = lyveMobi.rectangle()
            print(rectLyve)
            mouse.move(coords=(rectLyve.right, rect.top+3))
            mouse.click(button="left", coords=(rectLyve.right, rect.top+3))
            namelocked = "Unlock " + deviceName
            status = input_password_with_trust(op, namelocked, pwd, trusted)
        return status
    except:
        raise ValueError("exception on click unlock device listview")

def click_unlock_device_listview(op, deviceName, pwd, trusted):
    status = False
    try:
        time.sleep(2)
       # op.dump_tree()
        nameTable = op.NameTable
        if ( nameTable.exists()):
            dataItems = nameTable.descendants(control_type='DataItem')
            row = None
            for i in range(len(dataItems)):
                itemTxt = dataItems[i].window_text()
                if (itemTxt == deviceName):
                    print("get name = " + itemTxt)
                    row = dataItems[i].parent()
                    break

            listItem = row.descendants(control_type="DataItem")
            for it in listItem:
                if (it.window_text() == "--"):
                    rect = it.rectangle()
                    print(rect)
                    mouse.double_click(button='left', coords=(rect.right-42, rect.bottom-30))
                    break
            time.sleep(2)
            namelocked = "Unlock " + deviceName
            status = input_password_with_trust(op, namelocked, pwd, trusted)
        return status
    except:
        raise ValueError("exception on click unlock device listview")

def verify_device_volume(op, deviceName):
    status = False
    try:
        status2 = False
       # op.dump_tree()
        deviceTable = op.DeviceVolumesTable
        dataItemList = deviceTable.descendants(control_type='DataItem')
        if ( dataItemList[0].window_text() == deviceName):
            print("get correct device name = " + deviceName)
            status2 = True
        else:
            msg = "device name {} not visible".format(deviceName)
            global_cfg.msgs.append(msg)
        if ( status2 ):
            status = True
        else:
            global_cfg.msgs.append("fail to verify device volume")
        return status
    except:
        raise ValueError("exception on verify device volume")

def verify_device_detail(op, deviceVol, serialNo, connection):
    status = False
    try:
        status1 = status2 = status3 = False

        deviceTable = op.Table1
        nameTable = op.NameTable
        customSer = deviceTable.Custom2
        serialItem = customSer.descendants(control_type='DataItem')
        customUSB = deviceTable.USBCustom
        USBItem = customUSB.descendants(control_type='DataItem')
        nameCustom = nameTable.Custom2
        volumeItem = nameCustom.descendants(control_type='DataItem')
        if ( serialItem[1].window_text() == serialNo):
            print("get correct serial number = " + serialNo)
            status1 = True
        else:
            msg = "serial number {} not visible".format(serialNo)
            global_cfg.msgs.append(msg)
        if ( USBItem[1].window_text() == connection):
            print("get correct connection = " + connection)
            status2 = True
        else:
            msg = "connection {} not visible".format(connection)
            global_cfg.msgs.append(msg)
        if ( volumeItem[0].window_text() == deviceVol):
            print("get correct volume = " + deviceVol)
            status3 = True
        else:
            msg = "volume name  {} not visible".format(deviceVol)
            global_cfg.msgs.append(msg)
        if ( status1 and status2 and status3 ):
            status = True
        else:
            global_cfg.msgs.append("fail to verify device detail")
        return status
    except:
        raise ValueError("exception on verify device detail")

def verify_device_MrA(op, volName, format, firmwareVer):
    status = False
    try:
        status1 = status2 = status3 = False
        time.sleep(2)

        scroll_down(op)
        table = op.child_window(auto_id="raidVolumes", control_type="Table")
        dataItem = table.descendants(control_type='DataItem')
        for i in range(len(dataItem)):
            if (i == 0):
                print("volume name = " + dataItem[i].window_text())
                if ( dataItem[i].window_text() == volName):
                    print("get correct volume name = " + dataItem[i].window_text())
                    status1 = True
            if (i == 1):
                print("format = " + dataItem[i].window_text())
                if ( dataItem[i].window_text().lower() == format.lower()):
                    print("get correct format = " + dataItem[i].window_text())
                    status2 = True
            if ( i == 3 ):
                print("Capacity = " + dataItem[i].window_text())

        fwTable = op.Table7
        customFw = fwTable.descendants(control_type="Custom")
        for j in range(len(customFw)):
            txtList = customFw[j].descendants(control_type='Text')
            if ( j == 0 ):
                for i in range(len(txtList)):
                    if ( i == 0 ):
                        print("title = " + str(txtList[i].window_text()))
                    elif ( i == 1 ):
                        print("value = " + str(txtList[i].window_text()))
                        if ( txtList[i].window_text() == firmwareVer):
                            print("get correct fw = " + firmwareVer)
                            status3 = True
                break
        if ( not status1):
            msg = "get wrong volume name {}".format(volName)
            global_cfg.msgs.append(msg)
        if (not status2):
            msg = "get wrong format {}".format(format)
            global_cfg.msgs.append(msg)
        if (not status3):
            msg = "get wrong firmware version {}".format(firmwareVer)
            global_cfg.msgs.append(msg)
        if ( status1 and status2 and status3):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify device MrA")
        scroll_up(op)
        return status
    except:
        raise ValueError("exception on verify device MrA")

def verify_disk_spare_MrA(op, volName, format, numspare, raid):
    status = False
    try:
        status1 = status2 = status3 = status4 = False
        time.sleep(1)
        title_spare = numspare + " dedicated spare"
        spareSelect = op.child_window(title_re=title_spare, control_type='Text')
        if ( spareSelect.is_visible()):
            if ( numspare in spareSelect.window_text()):
                print("get correct number spare selected = " + spareSelect.window_text())
                status1 = True
        raidSelect = op.child_window(title_re="Disk Group", control_type='Text')
        if (raid in raidSelect.window_text()):
            print("get correct raid = " + raidSelect.window_text())
            status2 = True
        custom = op.NameCustom2
        dataItem = custom.descendants(control_type='DataItem')
        for i in range(len(dataItem)):
            if (i == 0):
                print("volume name = " + dataItem[i].window_text())
                if ( dataItem[i].window_text() == volName):
                    print("get correct volume name = " + dataItem[i].window_text())
                    status3 = True
            if (i == 1):
                print("format = " + dataItem[i].window_text())
                if ( dataItem[i].window_text().lower() == format.lower()):
                    print("get correct format = " + dataItem[i].window_text())
                    status4 = True

        if ( not status1):
            msg = "get wrong num spare {}".format(numspare)
            global_cfg.msgs.append(msg)
        if (not status2):
            msg = "get wrong raid {}".format(raid)
            global_cfg.msgs.append(msg)
        if (not status3):
            msg = "get wrong volume {}".format(volName)
            global_cfg.msgs.append(msg)
        if (not status4):
            msg = "get wrong format {}".format(format)
            global_cfg.msgs.append(msg)
        if ( status1 and status2 and status3 and status4):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify disk spare MrA")

        return status
    except:
        raise ValueError("exception on verify disk spare MrA")

def verify_disk_available_MrA(op, volName, format, numavail, raid):
    status = False
    try:
        status1 = status2 = status3 = status4 = False
        time.sleep(1)
        #op.dump_tree()
        title_avail = "dynamic spare"
        availSelect = op.child_window(title_re=title_avail, control_type='Text')
        if ( availSelect.is_visible()):
            if ( numavail in availSelect.window_text()):
                print("get correct number available selected = " + availSelect.window_text())
                status1 = True
        scroll_down(op)
        raidSelect = op.child_window(title_re="Disk Group", control_type='Text')
        if (raid in raidSelect.window_text()):
            print("get correct raid = " + raidSelect.window_text())
            status2 = True
        table = op.NameTable
        #dataItem = op.descendants(control_type='DataItem')
        dataItem = table.descendants(control_type='DataItem')
        for i in range(len(dataItem)):
            print(dataItem[i].window_text())
            if (i == 0):
                print("volume name = " + dataItem[i].window_text())
                if ( dataItem[i].window_text() == volName):
                    print("get correct volume name = " + dataItem[i].window_text())
                    status3 = True
            if (i == 1):
                print("format = " + dataItem[i].window_text())
                if ( dataItem[i].window_text().lower() == format.lower()):
                    print("get correct format = " + dataItem[i].window_text())
                    status4 = True

        if ( not status1):
            msg = "get wrong num spare {}".format(numavail)
            global_cfg.msgs.append(msg)
        if (not status2):
            msg = "get wrong raid {}".format(raid)
            global_cfg.msgs.append(msg)
        if (not status3):
            msg = "get wrong volume {}".format(volName)
            global_cfg.msgs.append(msg)
        if (not status4):
            msg = "get wrong format {}".format(format)
            global_cfg.msgs.append(msg)
        if ( status1 and status2 and status3 and status4):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to verify disk available MrA")
        scroll_up(op)
        return status
    except:
        raise ValueError("exception on verify disk available MrA")

def verify_disk_available(op, numavail):
    status = False
    try:
        time.sleep(2)
        tilte_avail = "dynamic spare"
        availSelect = op.child_window(title_re=tilte_avail, control_type='Text')
        if ( availSelect.is_visible()):
            print("get dynamic spare")
            if ( numavail in availSelect.window_text()):
                print("get correct number available selected = " + availSelect.window_text())
                status = True
            else:
                global_cfg.msgs.append("get wrong number of available selected")
        if (not status):
            global_cfg.msgs.append("fail to verify disk available")

        return status
    except:
        raise ValueError("exception on verify disk available")

def verify_enable_dynamic_spare(op, dynamic):
    status = False
    try:
        time.sleep(5)
       #op.dump_tree()
        title_avail = "dynamic spare"
        availSelect = op.child_window(title_re=title_avail, control_type='Text')
        if ( availSelect.is_visible()):
            print(availSelect.window_text())
            if ( dynamic in availSelect.window_text()):
                print("get correct dynamic status = " + dynamic)
                status = True

        if (not status):
            global_cfg.msgs.append("fail to verify enable dynamic_spare")

        return status
    except:
        raise ValueError("exception on verify enable dynamic spare")

def verify_disable_dynamic_spare(op, dynamic):
    status = False
    try:
        time.sleep(1)
       #op.dump_tree()
        title_dynamic = "dynamic spare"
        statusSelect = op.child_window(title_re=title_dynamic, control_type='Text')
        if ( statusSelect.is_visible()):
            print(statusSelect.window_text())
            if ( dynamic in statusSelect.window_text()):
                print("get correct dynamic status = " + dynamic)
                status = True

        if (not status):
            global_cfg.msgs.append("fail to verify disable dynamic_spare")

        return status
    except:
        raise ValueError("exception on verify disable dynamic spare")

def verify_click_global_spare(op, diskNo):
    status = False
    try:
        table = op.child_window(auto_id="deviceDisks", control_type='Table')
        #table = op.Table
        rowId = get_disk_global(op, diskNo)
        print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=str(rowId), control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        diskVal = dataList[0].window_text()
        if ( diskVal == diskNo ):
            print("get correct disk = " + diskVal)
            spare = dataList[4]
            rect = spare.rectangle()
            mouse.move(coords=(rect.right-45, rect.top+32))
            time.sleep(1)
            mouse.click(button='left', coords=(rect.right - 45, rect.top + 32))
            print("click +")
            time.sleep(6)
            status = True
        else:
            msg = "get wrong disk {}".format(diskVal)
            global_cfg.msgs.append(msg)
        if ( status ):
            print("verify click global spare")
        else:
            global_cfg.msgs.append("fail to verify click global spare")

        return status
    except:
        raise ValueError("exception on verify click global spare")

def verify_disk_global_spare(op, numglobal):
    status = False
    try:
        time.sleep(3)
        globalSelect = op.child_window(title_re=numglobal, control_type='Text')
        if ( globalSelect.is_visible()):
            if ( numglobal in globalSelect.window_text()):
                print("get correct number global spare selected = " + globalSelect.window_text())
                status = True
            else:
                global_cfg.msgs.append("get wrong number of global spare selected")
        if (not status):
            global_cfg.msgs.append("fail to verify disk global spare")

        return status
    except:
        raise ValueError("exception on verify disk global spare")

def verify_remove_global_spare(op, diskNo):
    status = False
    try:
        #table = op.Table
        table = op.child_window(auto_id="deviceDisks", control_type='Table')
        #table.dump_tree()
        rowId = get_disk_global(op, diskNo)
        print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=str(rowId), control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        diskVal = dataList[0].window_text()
        spare = dataList[4]
        if ( diskVal == diskNo ):
            print("get correct disk = " + diskVal)
            rect = spare.rectangle()
            mouse.move(coords=(rect.right-45, rect.top+32))
            time.sleep(1)
            mouse.click(button='left', coords=(rect.right - 45, rect.top + 32))
            print("click -")
            time.sleep(7)
            status = True
        else:
            msg = "get wrong disk {}".format(diskVal)
            global_cfg.msgs.append(msg)

        if ( status):
            print("verify remove global spare")
        else:
            global_cfg.msgs.append("fail to verify remove global spare")

        return status
    except:
        raise ValueError("exception on verify remove global spare")

def verify_inspect_disk_available(op, diskNo, arrayDisk):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = False
        table = op.Table
        rowId = get_disk_inspect(op, diskNo, arrayDisk)
        print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=str(rowId), control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        diskVal = dataList[0].window_text()

        if ( diskVal == diskNo ):
            print("get correct disk = " + diskVal)
            status1 = True
        else:
            msg = "get wrong disk {}".format(diskVal)
            global_cfg.msgs.append(msg)
        arrayVal = dataList[3].window_text()
        if ( arrayVal == arrayDisk ):
            print("get correct array status = " + arrayVal)
            status2 = True
        else:
            msg = "get wrong array status {}".format(arrayVal)
            global_cfg.msgs.append(msg)

        if ( status1 and status2):
            status = True
        else:
            global_cfg.msgs.append("fail to verify inspect disk available")

        return status
    except:
        raise ValueError("exception on verify inspect disk available")

def verify_inspect_disk_unavailable(op, diskNo, arrayDisk):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = False
        table = op.Table
        rowId = get_disk_inspect(op, diskNo, arrayDisk)
        print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=str(rowId), control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        diskVal = dataList[0].window_text()

        if ( diskVal == diskNo ):
            print("get correct disk = " + diskVal)
            status1 = True
        else:
            msg = "get wrong disk {}".format(diskVal)
            global_cfg.msgs.append(msg)
        arrayVal = dataList[3].window_text()
        if ( arrayVal == arrayDisk ):
            print("get correct array status = " + arrayVal)
            status2 = True
        else:
            msg = "get wrong array status {}".format(arrayVal)
            global_cfg.msgs.append(msg)

        if ( status1 and status2):
            status = True
        else:
            global_cfg.msgs.append("fail to verify inspect disk unavailable")

        return status
    except:
        raise ValueError("exception on verify inspect disk unavailable")

def verify_inspect_disk_spare(op, diskNo, spare):
    status = False
    try:
        time.sleep(2)
        status1 = status2 = False
        #table = op.Table
        table = op.child_window(auto_id="deviceDisks", control_type="Table")
        rowId = get_disk_spare(op, diskNo, spare)
       # print("rowId = " + str(rowId))
        rowCus = table.child_window(auto_id=str(rowId), control_type='Custom')
        dataList = rowCus.descendants(control_type='DataItem')
        diskVal = dataList[0].window_text()

        if ( diskVal == diskNo ):
            print("get correct disk = " + diskVal)
            status1 = True
        else:
            msg = "get wrong disk {}".format(diskVal)
            global_cfg.msgs.append(msg)
        spareVal = dataList[4].window_text()
        if ( spareVal == spare ):
            print("get correct spare status = " + spareVal)
            status2 = True
        else:
            msg = "get wrong spare status {}".format(spareVal)
            global_cfg.msgs.append(msg)

        if ( status1 and status2):
            status = True
        else:
            global_cfg.msgs.append("fail to verify inspect disk spare")
        return status
    except:
        raise ValueError("exception on verify inspect disk spare")

def verify_click_create_diskgroup(op):
    status = False
    try:
        time.sleep(1)
        create = op.child_window(title='Create disk group', control_type='Text')
        if ( create.is_visible()):
            create.click_input()
            status = True
        if (not status):
            global_cfg.msgs.append("fail to click create disk group")
        return status
    except:
        raise ValueError("exception on verify click create disk group")

def verify_click_delete_diskgroup(op):
    status = False
    try:
        time.sleep(1)
        scroll_down(op)
        dotMenu = op.child_window(title='dots-menu', control_type="Image")
        if ( dotMenu.is_visible()):
            dotMenu.click_input()
            op.Delete.click_input()
            print("click Delete")
            status = True
        if (not status):
            global_cfg.msgs.append("fail to click edit disk group")
        scroll_up(op)
        return status
    except:
        raise ValueError("exception on verify click edit disk group")

def verify_diskgroup_info_tooltip(op, raid):
    status = False
    try:
        time.sleep(1)
        scroll_down(op)
        dotMenu = op.child_window(title='dots-menu', control_type="Image")
        if ( dotMenu.is_visible()):
            rect = dotMenu.rectangle()
            mouse.move(coords=(rect.left-30, rect.top+10))
            time.sleep(1)
            popup = op.child_window(title_re="Group 1", control_type="Group")
            if (popup.is_visible()):
                listInfo = popup.descendants(control_type="Text")
                for i in range(len(listInfo)):
                    print(listInfo[i].window_text())
                    if ( listInfo[i].window_text() == "RAID Level"):
                        levelInfo = listInfo[i+1].window_text()
                        if ( levelInfo == raid):
                            print("get correct raid level = " + raid)
                            status = True
                            break
                        else:
                            global_cfg.msgs.append("get wrong raid level")

        scroll_up(op)
        if (not status):
            global_cfg.msgs.append("fail to verify disk group info")
        return status
    except:
        raise ValueError("exception on verify disk group info")

def verify_click_edit_diskgroup(op):
    status = False
    try:
        scroll_down(op)
        time.sleep(1)

        dotMenu = op.child_window(title='dots-menu', control_type="Image")
        if ( dotMenu.is_visible()):
            dotMenu.click_input()
            time.sleep(1)
            op.Edit.click_input()
            print("click Edit")
            status = True
        if (not status):
            global_cfg.msgs.append("fail to click edit disk group")
        scroll_up(op)
        return status
    except:
        raise ValueError("exception on verify click edit disk group")

def verify_select_raid(op, raid):
    status = False
    try:
        selectBtn = None
        if ( raid == "RAID 0"):
            selectBtn = op.RadioButton1
        elif ( raid == "RAID 5"):
            selectBtn = op.RadioButton2
        if ( selectBtn.is_visible()):
            selectBtn.click_input()
            status = True
        nextBtn = op.Next
        if (nextBtn.is_visible()):
            nextBtn.click_input()

        if (not status):
            global_cfg.msgs.append("fail to select raid")
        return status
    except:
        raise ValueError("exception on verify select raid")

def verify_select_raid_spare(op, raid, spareSelected):
    status = False
    try:
       # op.dump_tree()
        selectBtn = None
        if (raid == "RAID 0"):
           selectBtn = op.RadioButton1
        elif (raid == "RAID 5"):
           selectBtn = op.RadioButton2
        if (selectBtn.is_visible()):
           selectBtn.click_input()

        diskSelect = op.child_window(title_re=spareSelected, control_type="Text")
        if ( diskSelect.is_visible()):
            diskSelect.click_input()
            print("select spare = " + spareSelected)
            status = True
        else:
            msg = "disk selected {} not available".format(spareSelected)
            global_cfg.msgs.append(msg)

        nextBtn = op.Next
        if (nextBtn.is_visible()):
            nextBtn.click_input()

        if (not status):
            global_cfg.msgs.append("fail to select spare")
        return status
    except:
        raise ValueError("exception on verify select raid and spare")

def verify_select_spare(op, spareSelected):
    status = False
    try:
       # op.dump_tree()
        diskSelect = op.child_window(title_re=spareSelected, control_type="Text")
        if ( diskSelect.is_visible()):
            diskSelect.click_input()
            diskSelect.click_input()
            print("select spare = " + spareSelected)
            status = True
        else:
            msg = "disk selected {} not available".format(spareSelected)
            global_cfg.msgs.append(msg)
        if (not status):
            global_cfg.msgs.append("fail to select spare")
        return status
    except:
        raise ValueError("exception on verify select spare")

def verify_select_available(op, diskSelected):
    status = False
    try:
        diskSelect = op.child_window(title_re=diskSelected, control_type="Text")
        if ( diskSelect.is_visible()):
            diskSelect.click_input()
            #diskSelect.click_input()
            print("select available = " + diskSelected)
            status = True
        else:
            msg = "disk selected {} not available".format(diskSelected)
            global_cfg.msgs.append(msg)
        if (not status):
            global_cfg.msgs.append("fail to select available")
        return status
    except:
        raise ValueError("exception on verify select available")

def verify_select_unavailable(op, diskSelected):
    status = False
    try:
        diskSelect = op.child_window(title_re=diskSelected, control_type="Text")
        if ( diskSelect.is_visible()):
            diskSelect.click_input()
            print("select unavailable = " + diskSelected)
            status = True
        else:
            msg = "disk selected {} not available".format(diskSelected)
            global_cfg.msgs.append(msg)
        if (not status):
            global_cfg.msgs.append("fail to select unavailable")
        return status
    except:
        raise ValueError("exception on verify select unavailable")

def verify_select_Next_Save(op):
    status = False
    try:
        nextBtn = op.Next
        if (nextBtn.is_visible()):
            nextBtn.click_input()
            saveBtn = op.Save
            if ( saveBtn.is_visible()):
                saveBtn.click_input()
                status = True
            else:
                global_cfg.msgs.append("Save not visible")
        else:
            global_cfg.msgs.append("Next not visible")
        if (not status):
            global_cfg.msgs.append("fail to select Next and save")
        return status

    except:
        raise ValueError("exception on verify next and save")

def verify_select_volume_format(op, raid, volume, format):
    status = False
    try:
        status1 = status2 = status3 = False
        dash = op.DevicesTable
        listTxt = dash.descendants(control_type='Text')
        print("raid group: " + listTxt[3].window_text())
        if ( raid in listTxt[3].window_text()):
            print("get correct raid = " + str(listTxt[3].window_text()))
            status1 = True
        edit = dash.child_window(auto_id='volumeName', control_type="Edit")
        if ( edit.is_visible()):
            edit.type_keys("{BACKSPACE}")
            edit.type_keys(volume)
            print("type volume = " + volume)
            status2 = True
        formatBtn = dash.Button1
        if ( formatBtn.window_text() != format):
            formatBtn.click_input()
            selectBtn = dash.child_window(title=format)
            selectBtn.click_input()
            print("select format = " + format)
            status3 = True
        else:
            status3 = True
        if ( not status1):
            msg = "get wrong raid {}".format(raid)
            global_cfg.msgs.append(msg)
        if (not status2):
            msg = "fail to type volume {}".format(volume)
            global_cfg.msgs.append(msg)
        if (not status3):
            msg = "fail to select format {}".format(format)
            global_cfg.msgs.append(msg)

        if ( status1 and status2 and status3):
            status = True
        if (not status):
            global_cfg.msgs.append("fail to select volume and format")
        return status
    except:
        raise ValueError("exception on verify select volume and format")

def verify_select_format(op, format):
    status = False
    try:
        dash = op.DevicesTable
        formatBtn = dash.Button1
        if ( formatBtn.window_text() != format):
            formatBtn.click_input()
            selectBtn = dash.child_window(title=format)
            if (selectBtn.is_visible()):
                selectBtn.click_input()
                print("select format = " + format)
                status = True
            else:
                status = False
                global_cfg.msgs.append("format not visible = " +format)
        else:
            print("already has same format")
            status = True

        if (not status):
            global_cfg.msgs.append("fail to select format")
        return status
    except:
        raise ValueError("exception on verify select format")

def verify_edit_volume_format(op, raid, volume, format):
    status = False
    try:
        verify_select_volume_format(op, raid, volume, format)
        time.sleep(1)
        saveBtn = op.Save
        if (saveBtn.is_visible()):
            saveBtn.click_input()
            time.sleep(1)
            status = True
        if (not status):
            global_cfg.msgs.append("fail to edit volume and format")
        return status
    except:
        raise ValueError("exception on verify edit volume and format")

def verify_edit_format(op, format):
    status = False
    try:
        verify_select_format(op, format)
        time.sleep(1)
        saveBtn = op.Save
        if (saveBtn.is_visible()):
            saveBtn.click_input()
            time.sleep(1)
            status = True
        if (not status):
            global_cfg.msgs.append("fail to edit format")
        return status
    except:
        raise ValueError("exception on verify edit format")

def verify_create_volume_format(op, raid, volume, format):
    status = False
    try:
        verify_select_volume_format(op, raid, volume, format)
        time.sleep(1)
        createBtn = op.Create
        if (createBtn.is_visible()):
            createBtn.click_input()
            status = True
        if (not status):
            global_cfg.msgs.append("fail to create volume and format")
        return status
    except:
        raise ValueError("exception on verify create volume and format")

def verify_confirm_data_delete(op, confirm):
    status = False
    try:
        time.sleep(1)
        dash2 = op.DevicesTable2
        listTxt = dash2.descendants(control_type='Text')
        for li in listTxt:
            print(li.window_text())
        if ( confirm ):
            okBtn = dash2.OK
            okBtn.click_input()
            status = True
        time.sleep(1)
        if (not status):
            global_cfg.msgs.append("fail to verify confirm data deleted")
        return status
    except:
        raise ValueError("exception on verify confirm data deleted")

def verify_confirm_delete_diskgroup(op, confirm):
    status = False
    try:
        dash2 = op.DevicesTable
        #listTxt = dash2.descendants(control_type='Text')
        '''''
        for li in listTxt:
            print(li.window_text())
        '''''
        if ( confirm ):
            deleteBtn = dash2.Delete
            deleteBtn.click_input()
            status = True

        if (not status):
            global_cfg.msgs.append("fail to verify confirm delete diskgroup")
        return status
    except:
        raise ValueError("exception on verify confirm delete diskgroup")


def open_disk_management(op, devName):
    status = False
    try:
        time.sleep(1)

        deviceTable = op.DeviceVolumesTable
       # deviceTable.dump_tree()

        data = deviceTable.child_window(title=devName, control_type='DataItem')
        if (data.is_visible()):
            custom = data.parent()
            dataItemList = custom.descendants(control_type='DataItem')
            lastAct = dataItemList[4]
            rect = lastAct.rectangle()
           # print(rect)
           # mouse.move(coords=(rect.left + 120, rect.top + 40))
            lastActivity = deviceTable.LastactivityTable
            listAct = lastActivity.descendants(control_type='Text')
            for li in listAct:
                print(li.window_text())
            mouse.click(button='left', coords=(rect.left + 130, rect.top + 40))
            print("click disk management")
            time.sleep(5)
            status = True

        # deviceTable.dump_tree()

        timings.Timings.slow()
        warnings.simplefilter('ignore', category=UserWarning)
        # Application(backend='uia').start('mmc diskmgmt.msc')
        app = Application().connect(title_re='Disk Management', top_level_only=True)
        # app = Desktop().DiskManagement
        # app = Desktop().MMCMainFrame
        # app.print_control_identifiers()
        # app.Properties.print_control_identifiers()
        main = app.window(title='Disk Management', class_name="MMCMainFrame")
        time.sleep(5)
       # main.print_control_identifiers()
        pane1 = main.child_window(class_name='AfxOleControl42u')
        pane2 = pane1.child_window(class_name='AfxWnd42u', found_index=0)
        # pane2.dump_tree()

        listView = pane2.child_window(class_name='SysListView32', found_index=1)
        #  listView.dump_tree()
        # print(listView)
        # listTxt = listView.descendants(control_type='Text')

        # listView.dump_tree()

        status = True
        main.close()
        '''''
       # main.print_control_identifiers()
        childF = main.child_window(class_name='MMCChildFrm')
        header = childF.child_window(class_name='SysHeader32', found_index=0)
        listView = childF.child_window(class_name='SysListView32', found_index=0)
        print(listView.window_text())
        #disk0 = listView.child_window(auto_id='ListViewItem-0')
        #print(disk0.window_text())
        #volume = header.child_window(title='Volume')
        #volume.click()
        print("click Volume")


      #  is64bitbinary(r'C:\Windows\System32\diskmgmt.msc')

        app = Application().connect(path='diskmgmt.msc', timeout=5)
        #app = Application(backend="uia").connect(path="C:\\Windows\\System32\\diskmgmt.msc", timeout=5)
        #app = Application(backend="uia").start(cmd_line='Diskmgmt.msc', timeout=5)
        main = app.window(title='Disk Management')
        '''''

        if (not status):
            global_cfg.msgs.append("fail to open disk managemtn")
        return status
    except:
        raise ValueError("exception on opening disk management")

def click_disk_utility(op):
    status = False
    try:
        time.sleep(1)
        deviceTable = op.DeviceVolumesTable
        dataItemList = deviceTable.descendants(control_type='DataItem')
        lastAct = dataItemList[4]

        rect = lastAct.rectangle()
        mouse.move(coords=(rect.left+20, rect.top+40))

        lastActivity = deviceTable.child_window(auto_id="5Last activity", control_type='Table')
        listAct = lastActivity.descendants(control_type='Text')
        for li in listAct:
            print(li.window_text())
        mouse.click(button='left', coords=(rect.left+180, rect.top+30))
        print("click disk utility")
        time.sleep(5)
        #deviceTable.dump_tree()

        timings.Timings.slow()
        warnings.simplefilter('ignore', category=UserWarning)
       # Application(backend='uia').start('mmc diskmgmt.msc')
        app = Application().connect(title_re='Disk Management', top_level_only=True)
        #app = Desktop().DiskManagement
       # app = Desktop().MMCMainFrame
        #app.print_control_identifiers()
       # app.Properties.print_control_identifiers()
        main = app.window(title='Disk Management',class_name="MMCMainFrame")
        time.sleep(5)
        #main.dump_tree()
        pane1 = main.child_window(class_name='AfxOleControl42u')
        pane2 = pane1.child_window(class_name='AfxWnd42u', found_index=0)
       # pane2.dump_tree()

        listView = pane2.child_window(class_name='SysListView32', found_index=1)
      #  listView.dump_tree()
       # print(listView)
        #listTxt = listView.descendants(control_type='Text')

        #listView.dump_tree()

        status = True
        main.close()
        '''''
       # main.print_control_identifiers()
        childF = main.child_window(class_name='MMCChildFrm')
        header = childF.child_window(class_name='SysHeader32', found_index=0)
        listView = childF.child_window(class_name='SysListView32', found_index=0)
        print(listView.window_text())
        #disk0 = listView.child_window(auto_id='ListViewItem-0')
        #print(disk0.window_text())
        #volume = header.child_window(title='Volume')
        #volume.click()
        print("click Volume")


      #  is64bitbinary(r'C:\Windows\System32\diskmgmt.msc')
        
        app = Application().connect(path='diskmgmt.msc', timeout=5)
        #app = Application(backend="uia").connect(path="C:\\Windows\\System32\\diskmgmt.msc", timeout=5)
        #app = Application(backend="uia").start(cmd_line='Diskmgmt.msc', timeout=5)
        main = app.window(title='Disk Management')
        '''''


        if ( not status ):
            global_cfg.msgs.append("fail to click disk utility")
        return status
    except:
        raise ValueError("exception on click disk utility")
''''
def is64bitbinary(filename):
    """Check if the file is 64-bit binary"""
    print (filename)
    binary_type = win32file.GetBinaryType(str(filename))
    print(binary_type)
'''''
def click_device_folder_view(op):
    status = False
    try:
        #op.dump_tree()
        #deviceTable = op.DeviceVolumesTable
        lastActTable = op.LastactivityTable
        rect = lastActTable.rectangle()
        print(rect)
        mouse.move(coords=(rect.right-30, rect.top + 30))
        mouse.click(button='left', coords=(rect.right-30, rect.top+30))
        '''
        dataItemList = deviceTable.descendants(control_type='DataItem')
        lastAct = dataItemList[4]
        rect = lastAct.rectangle()
        
        mouse.move(coords=(rect.left+20, rect.top+30))
        mouse.double_click(button='left', coords=(rect.left+230, rect.top+40))
        '''''
        print("click folder view")
        time.sleep(1)
        explorer = Application().connect(path='explorer.exe')
        time.sleep(1)
        wd = explorer.window(top_level_only=True, active_only=True,
                                    class_name='CabinetWClass')
        time.sleep(10)
        wd.close()
        status = True
        #deviceTable.dump_tree()

        if ( not status ):
            global_cfg.msgs.append("fail to click device folder view")
        return status
    except:
        raise ValueError("exception on click device folder view")

def get_sub_folders(path):
    listFolders = []
    try:
        fileNames = os.listdir(path)
        for it in fileNames:
            if ( os.path.isdir(os.path.join(os.path.abspath(path), it))):
                listFolders.append(it)
        listFolders.sort()
        print(listFolders)
        return listFolders
    except:
        return None

def verify_same_folders(pathS, pathD):
    status = False
    try:
        if (os.path.exists(pathS)):
            if (os.path.exists(pathD)):
                cmp = filecmp.dircmp(pathS, pathD)
                time.sleep(1)
                cmp.report_full_closure()
                listdiff = cmp.diff_files

                if (len(listdiff) == 0):
                    status = True
                    print("2 folders " + pathS  + " and " + pathD + " are identical")
                else:
                    print("get different file in cmp")
                    for name in listdiff:
                        print("diff files %s found in %s and %s"
                              % (name, cmp.left, cmp.right))
            else:
                print("path destination not existed")
        else:
             print("path source not existed")
        return status

    except AssertionError:
        print("get exception on verify identical folders")
        return False

def verify_empty_folder(pathS):
    status = False
    try:
        if (not os.path.exists(pathS)):
            status = True
        else:
             print("path source not empty")
        return status

    except AssertionError:
        print("get exception on verify empty folder")
        return False

def verify_import_folders_with_delete_source(pathImport, pathSub, pathSrc, pathOri):
    status = False
    try:
        importFolder = None
        strFolder = ""
        folder_path = os.path.join(pathImport, '*')
        print("folder_path = " + str(folder_path))
        folders = sorted(glob.iglob(folder_path), key=os.path.getctime, reverse=False)
        print("pathSub = " + pathSub)
        for fd in folders:
            print("fd = " + fd)
            if (pathSub in fd):
                strFolder = fd
                print("strFolder =" + strFolder)
                break

        # open_path_explorer(strFolder)
        # print("strFolder = " + strFolder)

        list = get_sub_folders(strFolder)
        print("list = " + str(list))
        for sub in list:
            if (sub.find('.') == -1 and sub.find('$') == -1):
                print("folder found = " + sub)
                importFolder = sub
                break

        pathImport = strFolder + "\\" + importFolder
        print("pathImport = " + pathImport)
        print("pathOri = " + pathSrc)
        if (verify_same_folders(pathImport, pathOri) and
            verify_empty_folder(pathSrc)):
            print("get import folders correct")
            time.sleep(1)
            status = True
        else:
            print("fail to get import folders correct")
            global_cfg.msgs.append("fail to get correct import folders")
        # os.system("taskkill /im explorer.exe")
        # time.sleep(2)
        return status

    except NoSuchElementException:
        print("get exception on verify import folderes with delete source")
        return False

def verify_import_folders(pathImport, pathSub, pathSrc):
    status = False
    try:
        importFolder = None
        strFolder = ""
        folder_path = os.path.join(pathImport, '*')
        print("folder_path = " + str(folder_path))
        folders = sorted(glob.iglob(folder_path), key=os.path.getctime, reverse=False)
        print("pathSub = " + pathSub)
        for fd in folders:
            print("fd = " + fd)
            if (pathSub in fd):
                strFolder = fd
                print("strFolder =" + strFolder)
                break

        # open_path_explorer(strFolder)
        # print("strFolder = " + strFolder)

        list = get_sub_folders(strFolder)
        print("list = " + str(list))
        for sub in list:
            if (sub.find('.') == -1 and sub.find('$') == -1):
                print("folder found = " + sub)
                importFolder = sub
                break

        pathImport = strFolder + "\\" + importFolder
        print("pathImport = " + pathImport)
        print("pathOri = " + pathSrc)
        if (verify_same_folders(pathImport, pathSrc)):
            print("get import folders correct")
            time.sleep(1)
            status = True
        else:
            print("fail to get import folders correct")
            global_cfg.msgs.append("fail to get correct import folders")
        # os.system("taskkill /im explorer.exe")
        # time.sleep(2)
        return status

    except NoSuchElementException:
        print("get exception on verify import folderes")
        return False


def verify_import_folder(pathImport, pathOri):
    status = False
    try:
        importFolder = None
        strFolder = ""
        folder_path = os.path.join(pathImport, '*')
        print("folder_path = " + str(folder_path))
        folders = sorted(glob.iglob(folder_path), key=os.path.getctime, reverse=False)

        for fd in folders:
            print(fd)
            if ( fd.find("No Name") ):
                strFolder = fd
        #open_path_explorer(strFolder)
        #print("strFolder = " + strFolder)

        list = get_sub_folders(strFolder)
        print("list = " + str(list))
        for sub in list:
            if ( sub.find('.') == -1 and sub.find('$') == -1):
                print("folder found = " + sub)
                importFolder = sub
                break

        pathImport = strFolder + "\\" + importFolder
        if (verify_same_folders(pathImport, pathOri)):
            print("get import folders correct")
            time.sleep(1)
            status = True
        else:
            print("fail to get import folders correct")
            global_cfg.msgs.append("fail to get correct import folder")
       # os.system("taskkill /im explorer.exe")
        #time.sleep(2)
        return status

    except NoSuchElementException:
        print("get exception on verify import")
        return False

def click_device_export(op):
    status = False
    try:
        deviceTable = op.DeviceVolumesTable
        dataItemList = deviceTable.descendants(control_type='DataItem')
        lastAct = dataItemList[4]
        rect = lastAct.rectangle()
        mouse.move(coords=(rect.left+10, rect.top))
        mouse.double_click(button='left', coords=(rect.left+170, rect.top+40))
        print("click export")
        time.sleep(1)
        cancel = op.Document.Cancel
        cancel.click_input()
        status = True
       #
        if ( not status ):
            global_cfg.msgs.append("fail to click device export")
        return status
    except:
        raise ValueError("exception on click device export")


def verify_data_list_view(op, listName):
    status = False
    try:
        listData = get_data_list_view(op)
        for i in range(len(listName)):
            for j in range(len(listData)):
                if ( listData[j] == listName[i] ):
                    status = True
                    print("get correct data = " + listData[j])
                    break
        if ( not status ):
            msg = "get wrong data list {}".format(listName)
            global_cfg.msgs.append(msg)
        return status
    except:
        raise ValueError("exception on verify data list view")

def get_data_list_view(op):
    listData = []
    try:
        time.sleep(2)
        dataItems = op.Document.descendants(control_type='DataItem')
        lenData = len(dataItems)
        if ( lenData > 0 ):
            print("list data in list view:")
            for it in dataItems:
                print(it.window_text())
                listData.append(it.window_text())
        print(listData)
        return listData
    except:
        raise ValueError("exception on get data list view")

def get_data_icon_view(op):
    listData = []
    try:
        doc = op.Document
        listTxt = doc.descendants(control_type='Text')
        print("list data in icon view:")
        for el in listTxt:
            listData.append((el.window_text()))

        print(listData)
        return listData
    except:
        raise ValueError("exception on get data icon view")

def verify_system_notification(notifyTxt):
    status = False
    try:
        time.sleep(1)
        dt = Desktop(backend='uia')
        notifyWd = dt.window(title_re="New notification")
        #notifyWd.dump_tree()
        listTxt = notifyWd.descendants(control_type='Text')
        for i in range(len(listTxt)):
            print(listTxt[i].window_text())

           # if ( listTxt[0].window_text() == "Lyve Client Notifications" ):
            if (listTxt[1].window_text() == "Lyve Client Notifications"):
                print("get correct title = " + listTxt[0].window_text())
            else:
                msg = "get wrong tiltle {}".format(listTxt[0].window_text())
                global_cfg.msgs.append(msg)
            if ( listTxt[2].window_text() == notifyTxt):
                print("get correct notify msg = " + listTxt[1].window_text())
                status = True
            else:
                msg = "get wrong notify msg {}".format(listTxt[1].window_text())
                global_cfg.msgs.append(msg)

        return status
    except:
        raise ValueError("get exception on verify system notification")

def click_app_in_tray():
    status = False
    try:
        taskbar = Application(backend="uia").connect(path="explorer.exe")
        st = taskbar.window(class_name="Shell_TrayWnd")
        tray = st.child_window(title="Notification Chevron").wrapper_object()
        tray.click()
        time.sleep(1)
        list_box = Application(backend="uia").connect(class_name="NotifyIconOverflowWindow")
        list_box_win = list_box.window(class_name="NotifyIconOverflowWindow")
        list_box_win.print_control_identifiers()
        list_box_win.Button0.click_input()
        print("click LyveClient icon")
        time.sleep(2)
        list_box.kill()
        status = True
        return status
    except:
        raise ValueError("get exception on click app taskbar")

def copy_tree(src, dest):
    status = False
    try:
        if ( os.path.isdir(src)):
            print("dir src = " + src + ", dest = " + dest)
            shutil.copytree(src, dest)
            time.sleep(5)
            print("copy folder from " + src + " to " + dest )
        else:
            shutil.copy(src, dest)
            print("copy file from " + src + " to " + dest)
        time.sleep(10)
        if ( os.path.exists(dest)):
            print("folder copied in drive = " + dest)
            status = True
        if ( not status ):
            msg = "fail to copy from {} to {}".format(src, dest)
            global_cfg.msgs.append(msg)
        return status
    except:
        global_cfg.msgs.append("got error on copy tree")
        return False

def delete_folder(pathS):
    os.system("rmdir /s /q " + pathS)
    print("delete folder in = " + pathS)
    time.sleep(2)
    if (not os.path.exists(pathS)):
        return True
    else:
        msg = "fail to delete folder {}".format(pathS)
        global_cfg.msgs.append(msg)
        return False

def create_log_zip():
    status = False
    try:
        loc_location = params.log_location
        data_location = params.data_location
        log_dir = params.log_folder
        now = datetime.now()
        dt_str = now.strftime("%d_%m_%Y_%H_%M")
        zip_name = "log_" + dt_str
        zip_file = log_dir + zip_name + ".zip"
        print("zip file = " + zip_file)
        mainLog = loc_location + "\\main.log"
        renderLog = loc_location + "\\renderer.log"
        dataLog = data_location + "\\optimus.db"

        with ZipFile(zip_file, "w") as newzip:
            newzip.write(mainLog)
            newzip.write(renderLog)
            newzip.write(dataLog)
        print("create log zip = " + zip_file + " at dir = " + log_dir)
        status = True
        return status
    except:
        global_cfg.msgs.append("got error on create log zip")
        return False

def is_request_type(line, type):
    status = False

    for k, v in line.items():
        if (k == "header"):
            for key, value in v.items():
                if (key == "request_type"):
                    if (value == type):
                        print("get correct request type = " + str(value))
                        status = True
                        break
            if ( status ):
                break
        if ( status ):
            break
    return status