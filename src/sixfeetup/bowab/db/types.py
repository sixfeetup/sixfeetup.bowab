from __future__ import absolute_import
import codecs
from json import loads

from colander import SchemaNode

from pyramid.path import DottedNameResolver
from pyramid.renderers import render_to_response

from sqlalchemy.ext.compiler import compiles
from sqlalchemy import types


class CIText(types.TypeDecorator):
    '''Wrap citext functionality into UnicodeText.
    '''

    impl = types.UnicodeText

    def compare_values(self, x, y):
        try:
            return x.lower() == y.lower()
        except (AttributeError,) as err:
            return False

    def copy(self):
        return CIText(self.impl.length)

    def process_result_value(self, value, dialect):
        if value is None:
            return
        decoder = codecs.getdecoder(dialect.encoding)
        return decoder(value)[0]


class DottedPath(types.TypeDecorator):
    '''Return the resolved dotted path on the way out.
    '''

    impl = types.UnicodeText
    resolver = DottedNameResolver()

    def copy(self):
        return DottedPath(self.impl.length)

    def process_result_value(self, value, dialect):
        return self.resolver.resolve(value)


class JSON(types.TypeDecorator):
    '''Serializes to JSON on the way in and loads from JSON
    on the way out.
    '''

    impl = types.UnicodeText

    def copy(self):
        return JSON(self.impl.length)

    def process_bind_param(self, value, dialect):
        if isinstance(value, SchemaNode):
            json = render_to_response('json', value.serialize()).unicode_body
        elif value is None:
            json = u'null'
        else:
            json = render_to_response('json', value).unicode_body
        return json

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return loads(value)


class TSVector(types.TypeDecorator):
    impl = types.UnicodeText


@compiles(CIText, 'postgresql')
def compile_citext(element, compiler, **kw):
    return 'CITEXT'


@compiles(TSVector, 'postgresql')
def compile_tsvector(element, compiler, **kw):
    return 'TSVECTOR'
