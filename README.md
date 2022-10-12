# Django-Rest-Durin

[![django-rest-durin on pypi](https://img.shields.io/pypi/v/django-rest-durin)](https://pypi.org/project/django-rest-durin/)
[![Build Status](https://github.com/Eshaan7/django-rest-durin/workflows/Linter%20&%20Tests/badge.svg)](https://github.com/Eshaan7/django-rest-durin/actions?query=workflow%3A%22Linter+%26+Tests%22)
[![codecov](https://codecov.io/gh/Eshaan7/django-rest-durin/branch/main/graph/badge.svg?token=S9KEI0PU05)](https://codecov.io/gh/Eshaan7/django-rest-durin/)
[![CodeFactor](https://www.codefactor.io/repository/github/eshaan7/django-rest-durin/badge)](https://www.codefactor.io/repository/github/eshaan7/django-rest-durin)
<a href="https://lgtm.com/projects/g/Eshaan7/django-rest-durin/context:python">
<img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/Eshaan7/django-rest-durin.svg?logo=lgtm&logoWidth=18"/>
</a>

Per API client token authentication Module for [Django REST Framework](http://www.django-rest-framework.org/).

The idea is to provide one library that does token auth for multiple Web/CLI/Mobile API clients (i.e. devices/user-agents) via one interface but allows different token configuration for each client.

Durin authentication is token based, similar to the `TokenAuthentication`
built in to DRF. However, it adds some extra sauce:

- Durin allows **multiple tokens per user**. But only one token each user per API client.
- Each user token is associated with an API Client.
  - These API Clients are configurable via Django's Admin Interface.
  - Includes [permission enforcing](https://django-rest-durin.readthedocs.io/en/latest/permissions.html) to allow only specific clients to make authenticated requests to certain `APIViews` or vice-a-versa.
  - Configure [Rate-Throttling](https://django-rest-durin.readthedocs.io/en/latest/throttling.html) per User <-> Client pair.
- Durin provides an option for a logged in user to **remove all tokens** that the server has - forcing them to re-authenticate for all API clients.
- Durin **tokens can be renewed** to get a fresh expiry.
- Durin provides a `CachedTokenAuthentication` backend as well which uses memoization for faster look ups.
- Durin provides **Session Management** features. Refer to [Session Management Views](https://django-rest-durin.readthedocs.io/en/latest/views.html#session-management-views) i.e.,
  - REST view for an authenticated user to get list of sessions (in context of django-rest-durin, this means `AuthToken` instances) and revoke a session. Useful for pages like "View active browser sessions".
  - REST view for an authenticated user to get/create/delete token against a pre-defined client. Useful for pages like "Get API key" where a user can get an API key to be able to interact directly with your project's RESTful API using cURL or a custom client.

More information can be found in the [Documentation](https://django-rest-durin.readthedocs.io/en/latest/installation.html). I'd also recommend going through the `example_project/` included in this repository.

## Django Compatibility Matrix

![PyPi versions - Python](https://img.shields.io/pypi/pyversions/django-rest-durin)

If your project uses an older verison of Django or Django Rest Framework, you can choose an older version of this project.

| This Project | Python Version | Django Version          | Django Rest Framework |
| ------------ | -------------- | ----------------------- | --------------------- |
| 0.1+         | 3.5 - 3.10     | 2.2, 3.0, 3.1, 3.2, 4.0 | 3.7>=                 |

Make sure to use at least `DRF 3.10` when using `Django 3.0` or newer.

## Changelog / Releases

All releases should be listed in the [releases tab on GitHub](https://github.com/Eshaan7/django-rest-durin/releases).

See [CHANGELOG](https://django-rest-durin.readthedocs.io/en/latest/changelog.html) for a more detailed listing.

## License

This project is published with the [MIT License](LICENSE). See [https://choosealicense.com/licenses/mit/](https://choosealicense.com/licenses/mit/) for more information about what this means.

## Credits

Durin is inpired by the [django-rest-knox](https://github.com/James1345/django-rest-knox) and [django-rest-multitokenauth](https://github.com/anexia-it/django-rest-multitokenauth) libraries and adopts some learnings and code from both.
