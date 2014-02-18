from pyramid.path import DottedNameResolver

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()


def init_sa(config):
    settings = config.registry.settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    db_session = get_db_session(None, settings)
    db_session.configure(bind=engine)
    model_paths = config.registry.setdefault('bowab.models', set())
    for emp in model_paths:
        config.scan(emp)
    return db_session


def get_db_session(request, settings=None):
    if settings is None:
        settings = request.registry.settings
    session_path = settings.get('bowab.db_session', DBSession)
    resolver = DottedNameResolver()
    db_session = resolver.maybe_resolve(session_path)
    return db_session
