from MainApp.utils.config import check_if_config_exists
from MainApp.utils.dependencies import download_dependencies
from MainApp.utils.model import download_model
from MainApp.utils.constants import CONFIG_PATH


# create a config file if it doesn't exist
check_if_config_exists()

# download requirments, models and dependencies here
download_dependencies()
download_model()


from MainApp.run import launchApp
# launch the app
launchApp()