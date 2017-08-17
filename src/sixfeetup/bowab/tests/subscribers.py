from __future__ import absolute_import
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


class TestGAQ(TestCase):
    def _setup_api(self, settings=None):
        if settings is None:
            settings = {}
        request = testing.DummyRequest()
        request.registry = Mock()
        request.registry.settings = settings
        api_class = get_api_class(request.registry)
        api = api_class(request, {})
        return api

    def test_no_account(self):
        api = self._setup_api()
        self.assertTrue(api.gaq is None)

    def _test_option(self, option, struct_key, val, account='foo'):
        settings = {}
        if account is not None:
            settings['gaq.account'] = account
        settings[option] = val
        api = self._setup_api(settings)
        self.assertTrue(api.gaq is not None)
        self.assertTrue(api.gaq.data_struct[struct_key] == val)

    def test_account(self):
        self._test_option('gaq.account', '_setAccount', 'foo', None)

    def test_allow_linker(self):
        self._test_option('gaq.allow_linker', '_setAllowLinker', True)

    def test_domain_name(self):
        self._test_option('gaq.domain_name', '_setDomainName',
                          'foo.example.com')

    def test_single_push(self):
        self._test_option('gaq.single_push', '__singlePush', True)
