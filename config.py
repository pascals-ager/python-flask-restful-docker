class BaseConfig(object):
    """Base configuration."""
    PROJECT = "vimcar"
    SECRET_KEY = 'thisissecret'
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vimcar@127.0.0.1:5432/vimcar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisisdevsecret'
    SALT_KEY = 'saltthisthing'

class TestConfig(BaseConfig):
    """Development configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vimcar@postgres_db/vimcartest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisistestsecret'
    SALT_KEY = 'saltthisthing'