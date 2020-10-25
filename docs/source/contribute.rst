Development
================================

If you would like to contribute to django-rest-durin, you can clone the `repository <https://github.com/Eshaan7/django-rest-durin>`__ from GitHub.

.. parsed-literal::
    git clone https://github.com/Eshaan7/django-rest-durin

Extra dependencies required during testing or development can be installed with:

.. parsed-literal::
    pip install django-rest-durin[dev]

Before committing your changes with git or pushing them to remote, please run the following:

.. parsed-literal::
    bash pre-commit.sh

Run the tests locally
================================

If you need to debug a test locally and if you have `docker <https://www.docker.com/>`__ installed:

simply run the ``./docker-run-tests.sh`` script and it will run the test suite in every Python /
Django versions.

You could also simply run regular ``tox`` in the root folder as well, but that would make testing the matrix of
Python / Django versions a bit more tricky.
