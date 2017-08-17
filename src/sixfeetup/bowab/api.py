# The API that should be available to templates.

from __future__ import absolute_import
import datetime

from pyramid.security import authenticated_userid
from pyramid.settings import asbool

from gaq_hub import GaqHub


class TemplateAPI(object):
    def __init__(self, request, rendering_val):
        if not request:
            return
        self.request = request
        self.rendering_val = rendering_val
        self.init_forms(rendering_val)
        self.init_gaq()

    @property
    def settings(self):
        return self.request.registry.settings

    @property
    def utc_now(self):
        # totally naive as to timezone.
        return datetime.datetime.utcnow()

    def init_forms(self, rendering_val):
        # Initialize any necessary form resources
        self.css_resources = []
        self.js_resources = []
        for form in rendering_val.get('forms', []):
            resources = form.get_widget_resources()
            # XXX: Is the path always going to have this prefix?
            self.css_resources.extend(resources['css'])
            self.js_resources.extend(resources['js'])

    def is_active_tab(self, route_name):
        if self.request.matched_route and \
           self.request.matched_route.name == route_name:
            return 'active'
        else:
            return ''

    @property
    def current_userid(self):
        userid = authenticated_userid(self.request)
        if not userid:
            return ''
        return userid

    def init_gaq(self):
        if 'gaq.account' in self.settings:
            self.gaq = GaqHub(self.settings['gaq.account'])
            if 'gaq.allow_linker' in self.settings:
                allow_linker = asbool(self.settings['gaq.allow_linker'])
                self.gaq.setAllowLinker(allow_linker)
            if 'gaq.domain_name' in self.settings:
                self.gaq.setDomainName(self.settings['gaq.domain_name'])
            if 'gaq.single_push' in self.settings:
                single_push = asbool(self.settings['gaq.single_push'])
                self.gaq.setSinglePush(single_push)
        else:
            self.gaq = None
