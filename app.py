import os
import sys

from dotenv import load_dotenv
from flask import Flask

__appname__ = 'pickem-app'
__rootdir__ = os.path.abspath(os.getcwd())
__appdir__ = os.path.dirname(os.path.realpath(__file__))

sys.path.append(__rootdir__)
from config import *

# Load .env
load_dotenv(verbose=True, dotenv_path=__rootdir__ + '/.env')

staticfolder = __appdir__ + '/static'
templatefolder = __appdir__ + '/templates'

# Set up Flask app
app = Flask(__appname__, static_folder=staticfolder, template_folder=templatefolder, root_path=__rootdir__)
app.config.from_object(os.getenv('APP_SETTINGS'))

# Compile scss
if app.config['ENV'] == 'local':
    pass
    # from sassutils.wsgi import SassMiddleware
    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     __appname__: ('static/scss', 'static/css', '/static/css'),
    # })
else:
    pass
# import sass
    # cssStr = sass.compile(filename=staticfolder + '/scss/app.scss', output_style='compressed')
    # with open(staticfolder + '/css/app.css', 'w') as css:
    #     css.write(cssStr)