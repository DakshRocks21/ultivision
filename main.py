#$# Written by Daksh #$#

from MainApp.utils.config import check_if_config_exists
from MainApp.utils.dependencies import download_dependencies

# check if config exists
check_if_config_exists()

# download dependencies
#download_dependencies()

# download model
from MainApp.utils.model import download_model
#download_model()

#import appTest.audio as audio
# test all the sound effects
#audio.test()

#import appTest.kivy_settings as kivy_settings
# test UI quicker
#kivy_settings.MainApp().run()

from MainApp.run import launchApp
# launch the app
launchApp()