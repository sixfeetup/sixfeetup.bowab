# The API that should be available to templates.
import datetime

from pyramid.renderers import get_renderer
from pyramid.security import authenticated_userid


class TemplateAPI(object):
    def __init__(self, request, rendering_val):
        if not request:
            return
        self.request = request
        self.init_macros()
        self.init_forms(rendering_val)

    @property
    def settings(self):
        return self.request.registry.settings

    @property
    def utc_now(self):
        # totally naive as to timezone.
        return datetime.datetime.utcnow()

    def init_macros(self):
        macro_names = ['footer', 'quick_links', 'nav', 'logo', 'head_elements', 'admin_nav']
        self.macros = {}
        for mname in macro_names:
            renderer = get_renderer('templates/macros/%s#%s.pt' % (mname, mname))
            self.macros[mname] = renderer.implementation()

    def init_forms(self, rendering_val):
        # Initialize any necessary form resources
        self.css_resources = []
        self.js_resources = []
        for form in rendering_val.get('forms', []):
            resources = form.get_widget_resources()
            # XXX: Is the path always going to have this prefix?
            self.css_resources.extend([
                'deform:static/%s' % css_path
                for css_path in resources['css']
            ])
            self.js_resources.extend([
                'deform:static/%s' % js_path
                for js_path in resources['js']
            ])

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

    @property
    def is_superuser(self):
        return self.request.user and self.request.user.is_superuser
