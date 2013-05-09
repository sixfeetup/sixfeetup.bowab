import json


import colander
from colander import null
from colander import Invalid

from deform.widget import CheckedInputWidget

import requests


class RecaptchaWidget(CheckedInputWidget):
    template = 'widgets/recaptcha'
    requirements = ()
    url = "https://www.google.com/recaptcha/api/verify"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        settings = self.request.registry.settings
        self.public_key = settings['recaptcha_public_key']
        self.private_key = settings['recaptcha_private_key']
        self.recaptcha_options = '{%s}' % settings['recaptcha_options']
        super(RecaptchaWidget, self).__init__(*args, **kwargs)

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        confirm = getattr(field, 'confirm', '')
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, field=field, cstruct=cstruct,
                              public_key=self.public_key,
                              recaptcha_options=self.recaptcha_options)

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        challenge = pstruct.get('recaptcha_challenge_field') or ''
        response = pstruct.get('recaptcha_response_field') or ''
        if not response:
            raise Invalid(field.schema, 'No input')
        if not challenge:
            raise Invalid(field.schema, 'Missing challenge')
        remoteip = self.request.remote_addr
        data = dict(privatekey=self.private_key,
                    remoteip=remoteip,
                    challenge=challenge,
                    response=response)
        try:
            resp = requests.post(self.url, data=data, timeout=10)
        except (requests.exceptions.RequestException,), err:
            raise Invalid(field.schema,
                          "There was an error talking to the recaptcha \
                          server {err}".format(err=err))
        if not resp.status_code == 200:
            raise Invalid(field.schema,
                          "There was an error talking to the recaptcha \
                          server{0}".format(resp['status']))
        valid, reason = resp.text.split('\n')
        if not valid == 'true':
            if reason == 'incorrect-captcha-sol':
                reason = "Incorrect solution"
            raise Invalid(field.schema, reason.replace('\\n', ' ').strip("'") )
        return pstruct


@colander.deferred
def deferred_recaptcha_widget(node, kw):
    return RecaptchaWidget(request=kw['request'])
