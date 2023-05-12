#$# Written by Daksh #$#

from MainApp.utils.config import check_if_config_exists
from MainApp.utils.dependencies import download_dependencies
import os

# clear the terminal
os.system("clear")

# check if config exists
check_if_config_exists()

# download dependencies
download_dependencies()

from MainApp.app import launchApp
# launch the app
launchApp()