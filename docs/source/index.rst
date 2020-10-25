Welcome to Django-Rest-Durin!
================================

.. image:: https://img.shields.io/pypi/v/django-rest-durin
.. image:: https://img.shields.io/lgtm/grade/python/g/Eshaan7/django-rest-durin.svg?logo=lgtm&logoWidth=18
.. image:: https://travis-ci.com/Eshaan7/django-rest-durin.svg?branch=main
.. image:: https://codecov.io/gh/Eshaan7/django-rest-durin/branch/main/graph/badge.svg?token=S9KEI0PU05

Per API client token authentication Module for Django-REST-Framework_

The idea is to provide one library that does token auth for multiple Web/CLI/Mobile API clients via one interface but allows different token configuration for each client.

Durin authentication is token based, similar to the ``TokenAuthentication``
built in to DRF. However, it adds some extra sauce:

- Durin allows **multiple tokens** per user. But only one token each user per API client.
- Each user token is associated with an API Client. 

   - These API Clients (:class:`durin.models.Client`) are configurable via Django's Admin Interface. 
   - Includes permission enforcing to allow only specific clients to make authenticated requests to certain ``APIViews`` or vice-a-versa.
- All Durin **tokens have an expiration time**. This expiration time can be different per API client.
- Durin provides an option for a logged in user to **remove all tokens** that the server has - forcing him/her to re-authenticate for all API clients.
- Durin **tokens can be renewed** to get a fresh expiry.
- Durin provides a :class:`durin.auth.CachedTokenAuthentication` backend as well which uses memoization for faster look ups.

.. _Django-REST-Framework: http://www.django-rest-framework.org/

Index
-------------------------------
Get started at :doc:`installation`.

.. toctree::
   :maxdepth: 2
   
   installation
   settings
   auth
   views
   urls
   permissions
   signals
   faq
   changelog
   contribute

API Reference
-------------------------------
If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2
   
   durin

Indices and tables
================================

* :ref:`genindex`
* :ref:`modindex`