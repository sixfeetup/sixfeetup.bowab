import os
import sys

from pyramid.config import Configurator
from pyramid.paster import get_appsettings, setup_logging
from pyramid.paster import bootstrap

from sixfeetup.bowab.db import Base, init_sa


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    env = bootstrap(config_uri)
    settings = get_appsettings(config_uri)
    config = Configurator(settings=settings)
    db_session = init_sa(config)
    Base.metadata.bind = db_session.get_bind()
    Base.metadata.create_all(db_session.get_bind())

    return config, db_session
