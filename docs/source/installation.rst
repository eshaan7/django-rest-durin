Installation
================

Django Compatibility Matrix
--------------------------------
If your project uses an older verison of Django or Django Rest Framework, you can choose an older version of this project.

+--------------+----------------+----------------+----------------------+
| This Project | Python Version | Django Version | Django Rest Framework|
+--------------+----------------+----------------+----------------------+
| 0.1.*        | 3.5 - 3.9      | 2.2, 3.0, 3.1  | 3.7>=                |
+--------------+----------------+----------------+----------------------+


Make sure to use at least ``DRF 3.10`` when using ``Django 3.0`` or newer.

Install Durin
--------------

Durin should be installed with ``pip``:

.. parsed-literal::
    $ pip install django-rest-durin


Setup Durin
--------------

- Add ``rest_framework`` and :mod:`durin` to your ``INSTALLED_APPS``, remove 
  ``rest_framework.authtoken`` if you were using it.::

    INSTALLED_APPS = (
      ...
      'rest_framework',
      'durin',
      ...
    )

- Make Durin's :class:`durin.auth.TokenAuthentication` your default authentication class
  for django-rest-framework::

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': ('durin.auth.TokenAuthentication',),
        ...
    }

- Add the Durin's :doc:`urls` patterns to your project.

- Customize Durin's :doc:`settings` for your project.

- Apply the migrations for the models:

  .. parsed-literal::
      $ python manage.py migrate


.. Hint:: To use the cache backend for faster lookups, see :class:`durin.auth.CachedTokenAuthentication`.