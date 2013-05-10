# This package may contain traces of nuts

from pyramid.events import BeforeRender

from sixfeetup.bowab.configuration import get_db_session
from sixfeetup.bowab.subscribers import register_api


def includeme(config):
    config.add_subscriber(register_api, BeforeRender)
    config.add_request_method(get_db_session, 'db_session', reify=True)
