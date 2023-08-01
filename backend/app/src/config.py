# Common attributes
class Config:
    pass

# Development attributes
class DevelopmentConfig(Config):
    DEBUG = True

# Production attributes
class ProductionConfig(Config):
    DEBUG = False

configs = dict(development=DevelopmentConfig, producution=ProductionConfig)
