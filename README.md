# django-rest-durin

[![django-rest-durin on pypi](https://img.shields.io/pypi/v/django-rest-durin)](https://pypi.org/project/django-rest-durin/)
[![Build Status](https://travis-ci.com/Eshaan7/django-rest-durin.svg?branch=main)](https://travis-ci.com/Eshaan7/django-rest-durin)
[![codecov](https://codecov.io/gh/Eshaan7/django-rest-durin/branch/main/graph/badge.svg?token=S9KEI0PU05)](https://codecov.io/gh/Eshaan7/django-rest-durin/)
[![CodeFactor](https://www.codefactor.io/repository/github/eshaan7/django-rest-durin/badge)](https://www.codefactor.io/repository/github/eshaan7/django-rest-durin)
<a href="https://lgtm.com/projects/g/Eshaan7/django-rest-durin/context:python">
  <img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/Eshaan7/django-rest-durin.svg?logo=lgtm&logoWidth=18"/>
</a>

Per client token authentication Module for django rest auth.

Durin provides easy to use authentication for [Django REST
Framework](http://www.django-rest-framework.org/) The aim is to allow
for common patterns in applications that are REST based, with little
extra effort; and to ensure that connections remain secure.

Durin authentication is token based, similar to the `TokenAuthentication`
built in to DRF. However, it overcomes some problems present in the
default implementation:

-   DRF tokens are limited to one per user. This does not facilitate
    securely signing in from multiple devices, as the token is shared.
    It also requires *all* devices to be logged out if a server-side
    logout is required (i.e. the token is deleted).

    Durin provides one token per call to the login view - allowing each
    client to have its own token which is deleted on the server side
    when the client logs out.

    Durin also provides an option for a logged in client to remove *all*
    tokens that the server has - forcing all clients to re-authenticate.

-   DRF tokens track their creation time, but have no inbuilt mechanism
    for tokens expiring. Durin tokens can have an expiry configured in
    the app settings (default is 10 hours.)

More information can be found in the [Documentation]()

## Cache Backend

If you want to use a cache for the session store, you can install [django-memoize](https://pythonhosted.org/django-memoize/) and add `'memoize'` to `INSTALLED_APPS`.

Then you need to use ``CachedTokenAuthentication`` instead of ``TokenAuthentication``.

```bash
pip install django-memoize
```

## Django Compatibility Matrix

If your project uses an older verison of Django or Django Rest Framework, you can choose an older version of this project.

| This Project | Python Version | Django Version | Django Rest Framework |
|--------------|----------------|----------------|-----------------------|
| 0.1.*        | 3.5 - 3.9      | 2.2, 3.0, 3.1  | 3.7>=                 |

Make sure to use at least `DRF 3.10` when using `Django 3.0` or newer.

## Changelog / Releases

All releases should be listed in the [releases tab on github](https://github.com/Eshaan7/django-rest-durin/releases).

See [CHANGELOG.md](CHANGELOG.md) for a more detailed listing.

## License

This project is published with the [MIT License](LICENSE). See [https://choosealicense.com/licenses/mit/](https://choosealicense.com/licenses/mit/) for more information about what this means.