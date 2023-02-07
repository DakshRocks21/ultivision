from MainApp.run import launchApp
from MainApp.utils.config import check_if_config_exists
from MainApp.utils.dependencies import download_dependencies
from MainApp.utils.constants import CONFIG_PATH
import json
# download requirments, models and dependencies here
# download_dependencies()


# create a config file if it doesn't exist
check_if_config_exists()

# launch the app
launchApp()