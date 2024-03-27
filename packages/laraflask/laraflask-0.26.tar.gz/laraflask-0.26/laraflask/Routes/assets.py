from flask import Blueprint, send_file

# Import bootstrap file
from bootstrap.app import AppBootstrap

import os

# Create a class for assets routes process
class AssetsRoute:
    def __init__(self):
        # Define assets mime type
        self.defined_assets_mime_type = {
            'css': 'text/css',
            'js': 'text/javascript',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'svg': 'image/svg+xml',
            'ico': 'image/x-icon',
            'webp': 'image/webp',
            'pdf': 'application/pdf',
            'mp4': 'video/mp4',
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'ogg': 'audio/ogg',
            'scss': 'text/scss',
        }

        # default mime type
        self.default_mime_type = 'text/plain'

        return

    def register(self, path):
        # Get end of endpoint path
        # css/tes.css -> test.css
        # js/test.js -> test.js
        # img/test.jpg -> test.jpg
        filename = path.split('/')[-1]

        # Get the file extension
        file_extension = filename.split('.')[-1]

        # Get the assets path
        assets_path = AppBootstrap().app_static_path
        requested_file_path = assets_path + '/' + path

        # Check if the file exists
        if not os.path.isfile(requested_file_path):
            return 'The file '+ requested_file_path +' does not exist'

        # Get the requested file
        requested_file = open(requested_file_path, 'rb')

        # Check if the file extension is in the defined assets mime type
        if file_extension in self.defined_assets_mime_type:
            # Get the file mime type
            file_mime_type = self.defined_assets_mime_type[file_extension]
        else:
            file_mime_type = self.default_mime_type

        # Return the requested file
        return send_file(requested_file, mimetype=file_mime_type)
    
# Create a Blueprint for assets routes
assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/<path:path>')
def assets(path):
    return AssetsRoute().register(path)