import datetime


class FlaskConfig:
    # General Config
    # TESTING = True
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SERVER_NAME = "0.0.0.0:5000"
    LOG_LEVEL = 'debug'
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///models/database.db'
    # SQLALCHEMY_USERNAME='admin'
    # SQLALCHEMY_PASSWORD='admin'
    # SQLALCHEMY_DATABASE_NAME='security'
    # SQLALCHEMY_TABLE='passwords'
    # SQLALCHEMY_DB_SCHEMA='public'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # My API
    # API_ENDPOINT = 'http://unsecureendpoint.com/'
    # API_ACCESS_TOKEN = 'HBV%^&UDFIUGFYGJHVIFUJ'
    # API_CLIENT_ID = '3857463'

    # Session
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=1)


class PaypalConfig:
    PAYMENT_RETURN_URI = 'http://0.0.0.0:5000/balance'
    PAYMENT_CANCEL_URI = 'http://0.0.0.0:5000/cancel-payment'
    PAYMENT_PRICE = '1'
    PAYMENT_EXPIRE_TIME = 30
    SDK_CONFIG = {
        "mode": "sandbox",  # sandbox or live
        "client_id": "AfnAfJVtzh_PF6dtM9MWJSuHaXvLbP2QzYuQzE28GXpdFG1F9i2tIUG8MkHhahUkh-mPfYOT8_VjMQ-M",
        "client_secret": "EGrwwObDHKf9xyOiGyF_G-FfBKvGATJjDW7pC0iRAXuTQUmfEkYdYIh-7mRAyadcZDadCZNhEE_P4D8Q"
    }
