from pyramid.response import Response
from pyramid.path import DottedNameResolver
from sixfeetup.bowab.api import TemplateAPI


def get_api_class(registry):
    """Looks up a the API class to use within a Pyramid configuration registry.
    It will return the TemplateAPI class if none is found.
    """
    api_class = TemplateAPI
    if hasattr(registry, 'settings'):
        api_class_path = registry.settings.get('api_class', None)
        resolver = DottedNameResolver()
        try:
            api_class = resolver.resolve(api_class_path)
        except ValueError:
            pass
    return api_class


def register_api(event):
    """Provides and 'api' variable to all templates.

    This is intended to be registered with Pyramid's 'BeforeRender'
    event so that a TemplateAPI object (or subclass) will be injected
    into the environment, without having to explicitly add it in each
    view function.
    """
    api_class = get_api_class(event['request'].registry)
    if isinstance(event.rendering_val, Response) or \
       isinstance(event.rendering_val, basestring):
        event['api'] = api_class(event['request'], {})
    else:
        event['api'] = api_class(event['request'], event.rendering_val)
