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
