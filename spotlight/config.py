__author__ = 'vikram'

from optparse import OptionParser
import os
from StringIO import StringIO

from iniparse import INIConfig

UWSGI_ENV = 'SERVER_ENV'
PRODUCTION_ENV = 'production'

# for local environment
# python app.py -e kmarkiv
parser = OptionParser(usage="Usage: %prog [options] filename")
parser.add_option("-e", "--environment", dest="environment", help="Set the application environment")
(options, args) = parser.parse_args()

if options.environment:
    ENV = options.environment
else:
    ENV = os.environ.get(UWSGI_ENV, PRODUCTION_ENV)


def get_data(env="production"):
    # ideal to cache this in redis for production
    config_text = open('config.ini', 'r').read()
    f = StringIO(config_text)
    cfg = INIConfig(f)
    config = cfg[env]
    return config


config = get_data(ENV)
DB_URL = "mysql://%s:%s@%s/%s?charset=utf8" % (
    config['username'], config['password'], config['host'],
    config['database'])
