Changelog
============


`v1.1.0 <https://github.com/eshaan7/django-rest-durin/releases/tag/v1.1.0>`__
--------------------------------------------------------------------------------

**Features:**

- New ``ClientSerializer`` class.
- New Django management command ``create_client``. (Issue 6_)

**Other:**

- Bunch of small fixes and refactor.

.. _6: https://github.com/Eshaan7/django-rest-durin/issues/6


`v1.0.0 <https://github.com/eshaan7/django-rest-durin/releases/tag/v1.0.0>`__
--------------------------------------------------------------------------------

.. Note::
   If in your ``urls.py`` you have a url pattern with ``include("durin.urls"))``, then
   2 new URL paths ``apiaccess/`` and ``sessions/`` will get added
   to your project if you upgrade to this version.

   If you do not wish to have these new views, remove the above include statement and 
   refer to `durin/urls.py`_ on how to define the URL patterns selectively for the views you want.

**Features:**

- Session Management serializers and views. (Issue 19_)

Refer to Session-Management-Views_ i.e.,
   - REST view for an authenticated user to get list of sessions (in context of django-rest-durin, this means ``AuthToken`` instances) and revoke a session. Useful for pages like "View active browser sessions".
   - REST view for an authenticated user to get/create/delete token against a pre-defined client. Useful for pages like "Get API key" where a user can get an API key to be able to interact directly with your project's RESTful API using cURL or a custom client.

.. _19: https://github.com/Eshaan7/django-rest-durin/issues/19
.. _Session-Management-Views: views.html#session-management-views
.. _durin/urls.py: https://github.com/Eshaan7/django-rest-durin/blob/main/durin/urls.py


`v0.4.0 <https://github.com/eshaan7/django-rest-durin/releases/tag/v0.4.0>`__
--------------------------------------------------------------------------------

**Breaking Changes:**

- Remove the hard-coding of ``authentication_classes``, ``permission_classes`` variables in :doc:`views`. 
  Meaning they will now use the defaults set under ``REST_FRAMEWORK`` in ``settings.py``.
  
**Other:**

- Support for Python 3.10. Enable CI tests for same.
- Support for Django 4.0. Enable CI tests for same.


`v0.3.0 <https://github.com/eshaan7/django-rest-durin/releases/tag/v0.3.0>`__
--------------------------------------------------------------------------------

**Features:**

- `AUTHTOKEN_SELECT_RELATED_LIST <settings.html#AUTHTOKEN_SELECT_RELATED_LIST>`_ setting to enable performance optimization. (Issue 16_)

**Other:**

- More advanced use-cases in `example_project/permissions.py`_.
- Test cases now cover the :doc:`permissions`.

.. _16: https://github.com/Eshaan7/django-rest-durin/issues/16
.. _example_project/permissions.py: https://github.com/Eshaan7/django-rest-durin/blob/main/example_project/permissions.py


`v0.2.0 <https://github.com/eshaan7/django-rest-durin/releases/tag/v0.2.0>`__
--------------------------------------------------------------------------------

**Breaking Changes:**

- Replace ``django-memoize`` with ``django-cache-memoize`` package. Refer to updated :class:`durin.auth.CachedTokenAuthentication`. (Issue 13_)
- Update arguments passed to durin's signals and remove ``providing_args`` argument (Django `deprecation notice <https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-4-0>`_). Please see updated :doc:`signals`.
- The ``get_client_obj``, ``get_token_obj`` and ``renew_token`` member methods of :class:`durin.views.LoginView` are no longer ``staticmethod`` or ``classmethod``.

**Features:**

- :class:`durin.throttling.UserClientRateThrottle` throttle class. (Issue 9_)
- ``ClientSettings`` model in `example_project`_. (Issue 14_)
- ``renew_token`` method on :class:`durin.views.RefreshView` to enable easier extensibility.

**Bug Fixes:**

- Fix bug in ``AuthTokenAdminView`` ("save and continue editing" button was not working).
- Exception handling was missing in ``get_client_obj`` member method of :class:`durin.views.LoginView`.

**Other:**

- Enable CI tests for Django 3.2.
- Better document ``models.py`` and categorize modules in documentation.

.. _9: https://github.com/Eshaan7/django-rest-durin/issues/9
.. _13: https://github.com/Eshaan7/django-rest-durin/issues/13
.. _14: https://github.com/Eshaan7/django-rest-durin/issues/14
.. _example_project: https://github.com/Eshaan7/django-rest-durin/blob/main/example_project/models.py


`v0.1.0 <https://github.com/eshaan7/django-rest-durin/releases/tag/v0.1.0>`__
--------------------------------------------------------------------------------

- Initial release
