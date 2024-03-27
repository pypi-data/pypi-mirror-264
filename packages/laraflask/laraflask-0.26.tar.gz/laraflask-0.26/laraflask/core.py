
# Import app configuration class
from config.app import AppConfiguration

# Import app.py bootstrap file
from bootstrap.app import AppBootstrap

# Import service provider
from app.Providers.RouteServiceProvider import RouteServiceProvider

# Import middleware
from laraflask.Http.Middleware.ExcludeCSRF import ExcludeCSRF

# Import Flask
from flask import Flask

# Install necessary packages
from flask_wtf.csrf import CSRFProtect
from flask import request

# Create a Core class
class Core:

    # Initialize the Core class
    def __init__(self):
        # Create a Flask app
        self.app = Flask(__name__, 
                        template_folder=AppBootstrap().app_templates_path,
                        static_folder=AppBootstrap().app_static_path,
                        root_path=AppBootstrap().app_base_path
                    )
        
        # Set the app secret key
        self.app.secret_key = AppConfiguration().secret_key

        # Create a CSRF protection
        self.csrf = CSRFProtect()

    # Run the Flask app
    def run(self):
        # Register before request middleware
        @self.app.before_request 
        def exclude_csrf():
            # Register the ExcludeCSRF middleware
            return ExcludeCSRF(
                app=self.app,
                request=request,
                csrf=self.csrf
            ).register()
        
        # Register after request middleware
        @self.app.after_request
        def after_request(response):
            return response

        # Register routes
        self.register_routes()

        # Register CSRF protection
        self.register_csrf()

        # Run the Flask app
        return self.app.run(
            host=AppConfiguration().app_host,
            port=AppConfiguration().app_port,
            debug=AppConfiguration().app_debug
        )

    # Register routes
    def register_routes(self):
        return RouteServiceProvider(self.app).boot()
    
    # Register CSRF protection
    def register_csrf(self):
        return self.csrf.init_app(self.app)

    # Call the Flask app
    def __call__(self):
        return self.app