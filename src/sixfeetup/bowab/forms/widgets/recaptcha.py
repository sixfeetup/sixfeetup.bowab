from __future__ import absolute_import
import colander
import json
from colander import null
from colander import Invalid

from deform.widget import CheckedInputWidget

import requests


class RecaptchaWidget(CheckedInputWidget):
    template = 'sixfeetup.bowab:templates/widgets/recaptcha.pt'
    requirements = ()
    url = "https://www.google.com/recaptcha/api/siteverify"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        settings = self.request.registry.settings
        self.public_key = settings['bowab.recaptcha_public_key']
        self.private_key = settings['bowab.recaptcha_private_key']
        self.recaptcha_options = '{%s}' % settings['bowab.recaptcha_options']
        super(RecaptchaWidget, self).__init__(*args, **kwargs)

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct,
                              public_key=self.public_key,
                              recaptcha_options=self.recaptcha_options)

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        response = pstruct.get('g-recaptcha-response') or ''
        if not response:
            raise Invalid(field.schema, 'No input')
        remoteip = self.request.remote_addr
        data = dict(secret=self.private_key,
                    response=response,
                    remoteip=remoteip)
        try:
            resp = requests.post(self.url, data=data, timeout=10)
        except (requests.exceptions.RequestException,) as err:
            raise Invalid(field.schema,
                          "There was an error talking to the recaptcha \
                          server {err}".format(err=err))
        if not resp.status_code == 200:
            raise Invalid(field.schema,
                          "There was an error talking to the recaptcha \
                          server{0}".format(resp['status']))
        resp_info = json.loads(resp.text)
        if not resp_info['success']:
            reason = ''
            if 'error-codes' in resp_info:
                reason = resp_info['error-codes']
            raise Invalid(field.schema, ", ".join(reason))
        return 'True'


@colander.deferred
def deferred_recaptcha_widget(node, kw):
    return RecaptchaWidget(request=kw['request'])
