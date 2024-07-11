from os.path import expanduser
from core_framework.config import params, global_cfg

home                                = expanduser("~")

index_page_for_builds               = "https://wiki.corp.lyveminds.com/display/OMNI/Getting+the+latest+Module+builds"
build_ini_version_pattern           = params.build_version
ini_file_pattern                    = "update_mac_" + build_ini_version_pattern +".ini"
ini_file_loc                        = "C:\\Users\\534026\\Downloads\\TestServerForOmni.txt"
app_download_path                 = "C:\\Users\\534026\\Downloads\\Installer_Lacie.exe"
toolkit_installer_folder            =  "C:\\Users\\534026\\Downloads\\"
toolkit_installer_destination_folder  =  "C:\\Users\\534026\\Documents\\"
app_install_path                 = "C:\\Users\\534026\\Documents\\Installer_Seagate.exe"
url_plugin_win                   = "http://csg-apps.blackpearlsystems.net/Win/"
url_plugin_raid                  = "http://csg-apps.blackpearlsystems.net/Win/omni-plugin-raid/1.4.0/latest/"
url_plugin_help                  = "http://csg-apps.blackpearlsystems.net/Win/omni-plugin-help/1.2.0/latest/"
url_plugin_import                = "http://csg-apps.blackpearlsystems.net/Win/omni-plugin-import/2.1.0/latest/"
url_plugin_security              = "http://csg-apps.blackpearlsystems.net/Win/omni-plugin-security/1.7.0/latest/"
url_plugin_sync                  = "http://csg-apps.blackpearlsystems.net/Win/omni-plugin-sync/7.7.7/latest/"
user_es                          = r'CUP-U534026L005\user-es3'
user_de                          = r'CUP-U534026L005\user-de1'
user_fr                          = r'CUP-U534026L005\user-fr1'
user_en_location                 = r'C:\Users\534026'
user_es_location                 = r'C:\Users\user-es3'
user_de_location                 = r'C:\Users\user-de1'
user_fr_location                 = r'C:\Users\user-fr1'
user_location                    = ""
user_pwd                         = "Auto1234"

plugin_folder                      = ""
omni_folder                        = ""
smartcard_file                     = ""

#plugin_folder                      = r"C:\Users\534026\Downloads\Strings_Sync_1.2.0.10"
#omni_folder                        = r"C:\Users\534026\Downloads\Strings_Toolkit_1.8.4.43"
#smartcard_file                     = r"C:\Users\534026\Downloads\smartcards_1_7_86.txt"

app_instance                       = None
op_instance                        = None
testrail_report                    = True
xray_report                        = False
localize_test                      = True
app_mode                           = "standalone"
email_LyveHub                      = "tammyngo87+04@gmail.com"
user_LyveHub                       = "tammyngo_01"
lyve_pwd                           = "Test1234"
mrA_pwd                            = "AutoTest"
bucket_url1                         = "https://optimus-s3-sync.s3.us-west-2.amazonaws.com/optimus-sandbox/tammy_n"
bucket_url2                         = "https://optimus-s3-sync.s3.us-west-2.amazonaws.com/optimus-sandbox/tammy_n2"
bucket_url_sub1                     = "https://optimus-s3-sync.s3.us-west-2.amazonaws.com/optimus-sandbox/tammy_n/Sub1"
bucket_url_sub2                     = "https://optimus-s3-sync.s3.us-west-2.amazonaws.com/optimus-sandbox/tammy_n/Sub2"
bucket_url_sub3                     = "https://optimus-s3-sync.s3.us-west-2.amazonaws.com/optimus-sandbox/tammy_n/Sub3"
bucket_url_sub2_sub21               = "https://optimus-s3-sync.s3.us-west-2.amazonaws.com/optimus-sandbox/tammy_n/Sub2/Sub21"
ep_name2                           = "optimus-s3-sync-tammy_n2"
ep_name_sub1                       = "optimus-s3-sync-tammy_n_Sub1"
ep_name_sub2                       = "optimus-s3-sync-tammy_n_Sub2"
ep_name_sub2_sub21                 = "optimus-s3-sync-Sub2_Sub21"
ep_name_sub3                       = "optimus-s3-sync-tammy_n_Sub3"
access_key                         = "AKIASVQFPTQ2W5L7AEXX"
secret_access_key                  = "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"
recovery_code                      = "LBD9 - VZQ4 - J2PJ - 7WP1 - T1VT - 22XA"
localized_file                      = "LocalizedDictionary.xaml"
language                            = "en-US"
platform_name                       = "PC"
device_product_name                 = ""
window_handle                    = ""
toolkit_installer_pattern           = ""
toolkit_installer_name             = ""
toolkit_installer_file              = ""
toolkit_installer_app_name          = ""
if(params.installer_type == "Seagate"):
    toolkit_installer_pattern     = "Installer_Seagate_"
    toolkit_installer_name        = "Installer_Seagate"
    toolkit_installer_file        = "Installer_Seagate.exe"
    toolkit_installer_app_name    = "Seagate\ Toolkit\ Installer.exe/"
else:
    toolkit_installer_pattern     = "Installer_LaCie_"
    toolkit_installer_name        = "Installer_LaCie"
    toolkit_instalAuto1234ler_file        = "Installer_LaCie.exe"
    toolkit_installer_app_name    = "LaCie\ Toolkit\ Installer.exe/"

start_installer_cmd                 = "C:\\Users\\534026\\Desktop\\start_install.exe"

app_name                            = "Toolkit"
auto_test_folder                    = "auto_dev" + global_cfg.rand_str
raid_config_file                    = ".raid_config"
cp_raid_cfg_file                    = "cp %s /Volumes/AutoTest/" %raid_config_file
uninstall_status                    = {'status': True}
build_download_status               = {'status': True}
install_status                      = {'status': True}
file_for_add                        = "auto_file_added_"
file_for_edit_plan                  = "auto_file_for_edit_plan_"

file_for_delete                     = "auto_file_to_be_deleted_"
file_for_archive_delete_off         = "auto_file_for_archive_delete_off_"
file_for_archive_delete_on          = "auto_file_for_archive_delete_on_"
file_for_2_way_sync_off             = "auto_file_for_2_way_sync_off_"
file_for_new_destination            = "auto_file_for_new_dest"
file_for_restore                    = "auto_file_for_restore_"
file_for_view                       = "auto_file_for_view_"
file_for_archive_version_off        = "auto_file_for_archive_version_off_"
file_for_archive_version_on         = "auto_file_for_archive_version_on_"
scroll_path                         = "scrollAreas.at(0).scrollBars.at(1).buttons.at(2)"
scroll_path_main_scr                = "scrollAreas.at(0).scrollBars.at(0).buttons.at(2)"
fname_main_scr                      = "app_window.png"
file_to_be_renamed                  = "auto_file_to_be_renamed"+ global_cfg.rand_str + ".jpg"
units_to_left_for_drop_down         = 52
units_to_left_for_checkbox          = 32
units_down_for_checkbox             = 8
sync_plus_plan_counter              = 0
remove_from_source                  = "source"
plan_type_custom                    = "custom"
plan_type_new                       = "new"
remove_from_drive                   = "drive"
sync_plus_folder_name               = "Sync Plus Plan"
config_2_way_sync_off               = "2_way_sync_off"
config_archive_versions_off         = "archive_version_off"
config_archive_deleted_files_off    = "archive_deleted_files_off"
build_download_path                 = "/Applications/LaCie Toolkit Installer.zip"
open_unlocker_tool                   = "open /Volumes/Secure\ Drive\ \(Locked\)/Unlock\ Drive\ for\ Mac.app/"

cmd_kext_unload                     = "sudo kextunload /Library/Extensions/Seagate*.kext"
cmd_rm_kext                         = "sudo rm -rf /Library/Extensions/Seagate*.kext"
cmd_invalidate_kext_cache           = "sudo kextcache -invalidate /"
cmd_clear_staging_kext_cache        = "sudo kextcache --clear-staging"

setup_info                          = {'status' : False}
driver                              = None
idriver                             = None
driver_instance                     = {'driver': driver}
idriver_instance                    = {'idriver' : idriver}

sd_card_volume_name                 = ""
drive_SN                            = None
victory_SN                          = None
victory_drive_name                  = "Backup Plus Ultra Touch"
victory_drive_SID                       = "GHBW432X"
victory_drive_SID_with_space_at_end     = "GHBW432X "
victory_drive_SID_with_space_at_start   = " GHBW432X"
victory_drive_invalid_SID               = "InvalidSID"
tele_reqs_out                           = "danni_test.txt"

victory_drive_PSID                    = "GHBW432XJ3L79VB5NFVQSHC0AGXR05NX"
victory_drive_PSID_invalid            = "y8vZ46PG2S3EPUFDLZnPY0JJ5EARY6Bt"
victory_drive_password                = "123456"
victory_drive_updated_password        = "AutoTest123456!_updated"
victory_drive_password_hint           = "AutoTest"
victory_drive_invalid_password        = "InvalidPass"

ovo_drive_PSID                        = "1H71AB800CBZDHKTH1SZNXN190712297"
ovo_drive_SID                         = "1H71AB80"
ovo_admin                             = "Admin"
ovo_admin_password                    = "123456"
ovo_admin_new_password                = "123456"
ovo_admin_password_hint               = "numeric"
ovo_ssd_drive_name                    = "LaCie Rugged SSD"
ovo_user1                             = "user1"
ovo_user1_password                    = "abc123"
ovo_user1_new_password                = "abc123"
ovo_user1_password_hint               = "alphanumeric"

rugged_pegasus_SN                     = None
rugged_pegasus_drive_name             = "LaCie Rugged RAID Pro Drive"

rugged_shuttle_drive_PSID1                      = "BVZ27XE339KWHCR7HPQ43D87P1ZLGW2V"
rugged_shuttle_drive_PSID2                      = "ZL8U6QVCQ2KZL880R7L5CUM0XYP1X9YZ"
rugged_shuttle_drive_SID                        = "BVZ2ZL8U"
rugged_shuttle_drive_SID_with_space_at_end      = "BVZ2ZL8U "
rugged_shuttle_drive_SID_with_space_at_start    = " BVZ2ZL8U"
rugged_shuttle_drive_invalid_SID                = "InvalidSID"
rugged_shuttle_drive_PSID_invalid               = "y8vZ46PG2S3EPUFDLZnPY0JJ5EARY6Bt"
rugged_shuttle_SN                               = None
rugged_shuttle_admin                            = "Admin"
rugged_shuttle_admin_password                   = "password"
rugged_shuttle_admin_new_password               = "password"
rugged_shuttle_admin_password_hint              = "pwd"
rugged_shuttle_user1                            = "user1"
rugged_shuttle_user1_password                   = "abc123"
rugged_shuttle_user1_new_password               = "abc123"
rugged_shuttle_user1_password_hint              = "alphanumberic"
rugged_shuttle_drive_name                       = "LaCie Rugged RAID Shuttle"
rugged_ssd_drive_name                           = "LaCie Rugged SSD"
rugged_ssd_drive_PSID                      = "531190416005CNE00120190416000037"
rugged_ssd_drive_SID                        = "53119041"
rugged_ssd_drive_SID_with_space_at_end      = "53119041 "
rugged_ssd_drive_SID_with_space_at_start    = " 53119041"
rugged_ssd_drive_invalid_SID                = "InvalidSID"
rugged_ssd_drive_PSID_invalid               = "y8vZ46PG2S3EPUFDLZnPY0JJ5EARY6Bt"
rugged_ssd_drive_password                   = "123456"
rugged_ssd_drive_updated_password           = "123456_updated"
rugged_ssd_drive_password_hint              = "AutoTest"
def_browser                                     = "Safari"
curr_screen_image                               = "curr_screen_image.png"
finder_app                          = "Finder"
danni_drive_invalid_password        = "InvalidPass"
special_chars_password              = "Jd=0=%.D5^-#nk>&/VYFcP;`EgjA_L"
folder_for_pause_resume             = "auto_fol_pause_resume"
folder_for_restore                  = "auto_folder_for_restore"
folder_for_view                     = "auto_folder_for_view"
folder_for_cancel_edit              = "auto_fol_for_cancel_edit"
folder_for_pre_edit_plan            = "auto_fol_for_pre_edit"
folder_for_edit_plan                = "auto_fol_for_edit"
folder_for_edit_sync_in_progress    = "auto_fol_edit_while_syncing"
folder_for_delete_plan              = "auto_fol_for_delete"
folder_for_sync1                    = "auto_folder_for_sync1"
folder_for_archive_delete_off       = "auto_folder_for_archive_delete_off"
folder_for_archive_delete_on        = "auto_folder_for_archive_delete_on"
folder_for_archive_version_off      = "auto_folder_for_archive_version_off"
folder_for_archive_version_on           = "auto_folder_for_archive_version_on"
folder_for_2_way_sync_off_del_from_src  = "auto_fol_2_way_sync_off_del_src"
folder_for_2_way_sync_off_del_on_dr     = "auto_fol_2_way_sync_off_delfrdr"
folder_for_cross_mod              = "auto_fol_cross_mod"

folder_for_2_way_sync_off_add_to_src    = "auto_fol_2_way_sync_off_addtosrc"
dotted_button_path                  = ""
sel_source                          = "source"
sel_dest                            = "destination"
auto_fol_cancel_create_fol          = "auto_fol_cancel_create"
auto_fol_sync_destination           = "auto_fol_sync_dest"
sync_destination                    = "auto_custom_sync_dest"
folder_for_sync2                    = "auto_folder_for_sync2"
folder_for_sync3                    = "auto_folder_for_sync3"
folder_for_delete                   = "auto_folder_for_delete"
folder_for_custom_plan              = "auto_folder_for_custom_plan"
folder_for_content_validation       = "auto_folder_for_content_validation"
select_folders_img_name             = "select_folder_img.png"

toolkit_app_name                    = "Toolkit"
max_files                           = 3

############################ SYNC PERFORMANCE #############################################
wait_time_for_sync_5_100kb_files    = 20
wait_time_for_sync_5_500kb_files    = 40
wait_time_for_sync_5_1MB_files      = 100
wait_time_for_sync_5_5MB_files      = 200
wait_time_for_sync_5_10MB_files     = 250
wait_time_for_sync_5_25MB_files     = 900
wait_time_for_sync_5_50MB_files     = 1200
wait_time_for_sync_5_1GB_files      = 1500
wait_time_for_sync_5_5GB_files      = 1800
wait_time_for_sync_5_10GB_files     = 2000
wait_time_for_sync_5_25GB_files     = 2500
wait_time_for_sync_5_50GB_files     = 3000


size_100KB                          = "100_KB"
size_500KB                          = "500_KB"
size_1MB                            = "1_MB"
size_5MB                            = "5_MB"
size_10MB                           = "10_MB"
size_25MB                           = "25_MB"
size_50MB                           = "50_MB"
size_1GB                            = "1_GB"
size_5GB                            = "5_GB"
size_10GB                           = "10_GB"

###############################TELEMETRY
op_dump_file                          = "C:\\Users\\534026\\optimus_win_auto\\tests\\op_dump.txt"
req_payload                             = None


