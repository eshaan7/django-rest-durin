Welcome to Django-Rest-Durin!
================================

.. image:: https://img.shields.io/pypi/v/django-rest-durin
.. image:: https://img.shields.io/lgtm/grade/python/g/Eshaan7/django-rest-durin.svg?logo=lgtm&logoWidth=18
.. image:: https://github.com/Eshaan7/django-rest-durin/workflows/Linter%20&%20Tests/badge.svg
.. image:: https://codecov.io/gh/Eshaan7/django-rest-durin/branch/main/graph/badge.svg?token=S9KEI0PU05

Per API client token authentication Module for Django-REST-Framework_

The idea is to provide one library that does token auth for multiple Web/CLI/Mobile API clients via one interface but allows different token configuration for each client.

Durin authentication is token based, similar to the ``TokenAuthentication``
built in to DRF. However, it adds some extra sauce:

- Durin allows **multiple tokens** per user. But only one token each user per API client.
- Each user token is associated with an API Client. 

   - These API Clients (:class:`durin.models.Client`) are configurable via Django's Admin Interface. 
   - Includes Permission-enforcing_ to allow only specific clients to make authenticated requests to certain ``APIViews`` or vice-a-versa.
   - Configure Rate-Throttling_ per User <-> Client pair.
- All Durin **tokens have an expiration time**. This expiration time can be different per API client.
- Durin provides an option for a logged in user to **remove all tokens** that the server has - forcing him/her to re-authenticate for all API clients.
- Durin **tokens can be renewed** to get a fresh expiry.
- Durin provides a :class:`durin.auth.CachedTokenAuthentication` backend as well which uses memoization for faster look ups.
- Durin provides  **Session-Management**_  features i.e.,
   - REST view for an authenticated user to get list of sessions (in context of django-rest-durin, this means ``AuthToken`` instances) and revoke a session. Useful for pages like "View active browser sessions".
   - REST view for an authenticated user to get/create/delete token against a pre-defined client. Useful for pages like "Get API key" where a user can get an API key to be able to interact directly with your project's RESTful API using cURL or a custom client.

.. _Django-REST-Framework: http://www.django-rest-framework.org/
.. _Permission-enforcing: permissions.html
.. _Rate-Throttling: throttling.html
.. _Session-Management: views.html#session-management-views

Index
-------------------------------
Get started at :doc:`installation`.

.. toctree::
   :maxdepth: 2
   :caption: Setup
   
   installation
   settings

.. toctree::
   :maxdepth: 2
   :glob:
   :caption: API

   auth
   views
   urls
   signals

.. toctree::
   :maxdepth: 2
   :glob:
   :caption: Modules

   models
   permissions
   throttling
   sub_modules

.. toctree::
   :maxdepth: 2
   :caption: Other

   faq

.. toctree::
   :maxdepth: 2
   :caption: Development

   contribute
   changelog


Indices and tables
================================

* :ref:`genindex`
* :ref:`modindex`