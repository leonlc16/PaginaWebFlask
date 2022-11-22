from decouple import config
class Config:
    SECRET_KEY='secretkey'
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345@localhost/flask'
    

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}