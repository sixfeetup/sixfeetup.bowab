from unittest import TestCase
from pyramid.events import BeforeRender
from pyramid import testing
from pyramid.response import Response
from mock import Mock, patch

from sixfeetup.bowab.api import TemplateAPI
from sixfeetup.bowab.subscribers import get_api_class
from sixfeetup.bowab.subscribers import register_api


class Dummy(object):
    def __init__(self, request, rendering_val):
        self.request = request
        self.rendering_val = rendering_val


class TestGetAPIClass(TestCase):

    def test_no_api_class_defined(self):
        registry = Mock()
        registry.settings = {}
        api_class = get_api_class(registry)
        self.assertEqual(api_class, TemplateAPI)

    def test_different_api_class(self):
        registry = Mock()
        registry.settings = {
            'bowab.api_class': 'sixfeetup.bowab.tests.subscribers.Dummy',
        }
        api_class = get_api_class(registry)
        self.assertEqual(api_class, Dummy)

    def test_none_registry(self):
        registry = None
        api_class = get_api_class(registry)
        self.assertEqual(api_class, TemplateAPI)


class TestRegisterAPI(TestCase):
    @staticmethod
    def _generate_event(rendering_val=None, registry=None):
        if rendering_val is None:
            rendering_val = {}
        event = BeforeRender({}, rendering_val=rendering_val)
        event.rendering_val = rendering_val
        event['request'] = testing.DummyRequest()
        if registry is None:
            registry = Mock()
            registry.settings = {}
        event['request'].registry = registry
        return event

    def test_empty_rendering_val(self):
        with patch('sixfeetup.bowab.subscribers.get_api_class') as mocked:
            mocked.return_value = TemplateAPI
            val = {'test': 1}
            event = TestRegisterAPI._generate_event(rendering_val=val)
            register_api(event)
            self.assertEqual(event['api'].rendering_val, val)

    def test_populated_registry(self):
        with patch('sixfeetup.bowab.subscribers.get_api_class') as mocked:
            mocked.return_value = TemplateAPI
            val = Response()
            event = TestRegisterAPI._generate_event(rendering_val=val)
            register_api(event)
            self.assertEqual(event['api'].rendering_val, {})

    def test_none_request(self):
        with patch('sixfeetup.bowab.subscribers.get_api_class') as mocked:
            mocked.return_value = TemplateAPI
            val = Response()
            event = TestRegisterAPI._generate_event(rendering_val=val)
            event.request = None
            register_api(event)
            self.assertTrue(not 'api' not in event)
