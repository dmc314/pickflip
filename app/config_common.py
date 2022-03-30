TIMEZONE = 'Europe/Paris'

# Secret key for generating tokens
SECRET_KEY = 'secret_password'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'secret_password')

# Database choice
# SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'secret_password@email.com'
MAIL_PASSWORD = 'secret_password'
ADMINS = ['secret_password@email.com']

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12
