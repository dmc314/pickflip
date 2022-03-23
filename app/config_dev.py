import logging

from app.config_common import *


# DEBUG can only be set to True in a development environment for security reasons
DEBUG = True

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pN27S39@kvqS^8Kp')

# Database choice
# SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
# SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:7crzNYZ#b8kH4_8@database-1.cjgjppmlnjua.us-east-2.rds.amazonaws.com:3306/pickflip'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'pickflip.info'
MAIL_PASSWORD = 'gl8zed-donut&1cofee'
ADMINS = ['pickflip.info@gmail.com']

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2

UPLOAD_FOLDER = '/flaskSaaS/app/uploads'
