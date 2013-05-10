# This package may contain traces of nuts

from pyramid.events import BeforeRender

from sixfeetup.bowab.subscribers import register_api


def includeme(config):
    config.add_subscriber(register_api, BeforeRender)
