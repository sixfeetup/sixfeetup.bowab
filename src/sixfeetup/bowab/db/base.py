from __future__ import absolute_import
import sys

from pyramid.path import DottedNameResolver

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()


def init_sa(config, **connect_kwargs):
    settings = config.registry.settings

    pc_name = settings.pop('sqlalchemy.poolclass', '')
    if pc_name:
        resolver = DottedNameResolver()
        pool_class = resolver.maybe_resolve(pc_name)
        settings['sqlalchemy.poolclass'] = pool_class

    # http://stackoverflow.com/a/15691283
    engine = engine_from_config(settings, 'sqlalchemy.',
                                connect_args=connect_kwargs)

    db_session = get_db_session(None, settings)
    db_session.configure(bind=engine)
    model_paths = config.registry.setdefault('bowab.models', set())
    for emp in model_paths:
        config.scan(emp)

    if '__pypy__' in sys.builtin_module_names:
        from psycopg2cffi import compat
        compat.register()

    return db_session


def get_db_session(request, settings=None):
    if settings is None:
        settings = request.registry.settings
    session_path = settings.get('bowab.db_session', DBSession)
    resolver = DottedNameResolver()
    db_session = resolver.maybe_resolve(session_path)
    return db_session
