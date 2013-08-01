.. contents::

Introduction
============

This package is a collection of utility code to make building Pyramid applications
backed by SQLAlchemy easier. It includes:
* a TemplateAPI class to inject variables into all your templates
* A Deform CSRF-validation schema
* A Deform Recaptcha widget
* SQLAlchemy DBSession and declarative_base stubs

Extra Models
------------

If you have models that you would like the main `initialize_db` script to create,
they need to inherit from `sixfeetup.bowab.db.Base`. Then add the following to your config:

.. code-block:: ini
    bowab.models =
        dotted.python.path.to.models

Using the TemplateAPI
---------------------

If you would like to the included `sixfeetup.bowab.api.TemplateAPI` class as is, you simply need to
include this in your Pyramid app configuration::

.. code-block: python
    config.include('sixfeetup.bowab')

This will add an event subscriber to the `pyramid.events.BeforeRender` event. This means that all
templates will have access to an `api` variable that represents the `TemplateAPI` instance.

Google Analytics
================

The TemplateAPI class supports extracting Google Analytics settings from the Pyramid settings registry. The following keys are supported:

* gaq.account
  - Property ID from Google
* gaq.allow_linker
  - http://code.google.com/apis/analytics/docs/gaJS/gaJSApiDomainDirectory.html#_gat.GA_Tracker_._setAllowLinker
* gaq.domain_name
  - explicit domain name to use
* gaq.single_push
  - boolean; use a push per setting, or one single push

To use this in your project, update base.pt to include:

.. code-block: tal
    <!-- Google Analytics -->
    <tal:gaq condition="api.gaq">
        <tal:code replace="structure api.gaq.as_html()" />
    </tal:gaq>

Customizing the TemplateAPI
---------------------------

Often, you will want to use the `sixfeetup.bowab.api.TemplateAPI` class as a base for your own API
instances, since you may have extra variables that should be available to templates.

To do this, you need to include `sixfeetup.bowab` as specified in the 'Using the TemplateAPI' section.

Then, create a subclass within your project that inherits from `sixfeetup.bowab.api.TemplateAPI`::

.. code-block: python
    from sixfeetup.bowab.api import TemplateAPI

    class MyTemplateAPI(TemplateAPI):
        def __init__(self, request, rendering_val):
            super(MyTemplateAPI, self).__init__(request, rendering_val)
            # Any custom initalization

        def my_func(self):
            return 'my func'

Then, in you `paster.ini` file, include the following::

.. code-block: ini
    bowab.api_class = my_project.MyTemplateAPI

Make sure the `bowab.api_class` variable points to the full dotted path of your custom class. This class will
then be registered by the `sixfeetup.bowab` include process.

Using the Recaptcha Widget
--------------------------

The Recaptcha widget needs the private and public keys for your Recaptcha account.
These can be set in your config file using the `bowab.recaptcha_private_key` and
`bowab.recaptcha_public_key` values, respectively.
