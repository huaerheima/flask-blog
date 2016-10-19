import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY") or 'you guess what'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	REDIS_URL = "redis://:password@localhost:6379/0"

config = {
	'development' : DevelopmentConfig,

	'default' : DevelopmentConfig
}
