from os.path import expanduser
from core_framework.config import params

home                                = expanduser("~")
index_page_for_builds               = "https://wiki.corp.lyveminds.com/display/OMNI/Getting+the+latest+Module+builds"
build_ini_version_pattern           = params.build_version
ini_file_pattern                    = "update_mac_" + build_ini_version_pattern +".ini"
ini_file_loc                        = home + "/Downloads/TestServerForOmni.txt"
lacie_toolkit_installer_pattern     = "LaCie_Toolkit_Installer_"
lacie_toolkit_installer_name        = "LaCie Toolkit Installer"
toolkit_installer_file              = "LaCie\ Toolkit\ Installer.zip"
lacie_toolkit_installer_app_name    = "LaCie\ Toolkit\ Installer.app/"
destn_folder_toolkit_installer      = "/Applications/"
toolkit_installer_file_Apps         = "/Applications/LaCie\ Toolkit\ Installer.zip"
installed_lacie_installer_path      = "/Applications/LaCie\ Toolkit\ Installer.app"



cmd_rm_app                          = "rm -rf {}".format(installed_lacie_installer_path)
cmd_rm_file                         = "rm -rf {}".format(toolkit_installer_file_Apps)
app_path                            = "/Applications/Toolkit.app"

cmd_rm_toolkit_app                  = "rm -rf {}".format(app_path)
uninstall_status                    = {'status': True}
build_download_status               = {'status': True}
install_status                      = {'status': True}

build_download_path                 = "/Applications/LaCie Toolkit Installer.zip"