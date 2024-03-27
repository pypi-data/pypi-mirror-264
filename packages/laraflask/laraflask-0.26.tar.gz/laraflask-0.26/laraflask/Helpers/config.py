import os
from bootstrap import app

class Config:

    def __init__(self):
        return
    
    # To get the value of a key from the config file
    def get(self, key):
        # A sample of usage of the method
        # from laraflask.Helpers.config import config
        # config().get('app.app_name')
        # where app is the name of the file inside the config folder
        # app_name is the key

        # Split the key to get the file name and the key
        key = key.split('.')

        # Get the file name
        file_name = key[0]

        # Get the key
        key = key[1]

        # config file location
        config_location = app.AppBootstrap().app_config_path

        # config class name
        config_class_name = file_name.capitalize() + 'Configuration'

        # config file location
        config_file = config_location + '/' + file_name + '.py'

        # Check if the file exists
        if not os.path.isfile(config_file):
            return 'The file does not exist'
        
        # Import the file
        config_module = __import__('config.' + file_name, fromlist=[config_class_name])

        # Get the class
        config_class = getattr(config_module, config_class_name)

        # Get the value of the key
        return getattr(config_class(), key)

