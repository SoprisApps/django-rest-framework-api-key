# django-rest-framework-api-key [![travis][travis-image]][travis-url] [![codecov][codecov-image]][codecov-url] [![pypi][pypi-image]][pypi-url]
Authenticate Web APIs made with Django REST Framework


## Supports
  - Django Rest Framework (>=3.7)
    - Python (2.7, 3.4, 3.5, 3.6)
    - Django (1.10, 1.11)

  - Django Rest Framework (3.4, 3.5, 3.6)
    - Python (2.7, 3.4, 3.5)
    - Django (1.8, 1.9, 1.10)

  - Django Rest Framework (3.3)
    - Python (2.7, 3.4, 3.5)
    - Django (1.8, 1.9)

## Installation

Install using pip:

    pip install drfapikey

Add 'rest_framework_api_key' to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        ...
        'rest_framework_api_key',
    )

There are two ways you can use DRF API Key: with a permission class or
as Django middleware.

## Permission Class
Set the django-rest-framework permissions under your django settings:

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework_api_key.permissions.HasAPIAccess',
        )
    }

This sets the default permission class for all views in your API.  If
you manually set `permission_classes = ` in any view, you need to add
the `HasAPIAccess` class to the tuple or else that API call will not be
protected.

### Middleware
If you would rather install this as Django middleware, then do not set
your permission classes in any DRF views (this would cause the API key
to be tested twice for each API call!).  Instead, append the middleware
to your list:

Django >= 1.10:

    MIDDLEWARE = (
        ...
        'rest_framework_api_key.middleware.HasAPIAccessMiddleware',
    )

Django < 1.10:

    MIDDLEWARE_CLASSES = (
        ...
        'rest_framework_api_key.middleware.HasAPIAccessMiddleware',
    )

And then define a tuple of URL prefixes that this middleware should not
check API access for.  Without the below setting, you won't be able to
access the Django Admin app!

    REST_FRAMEWORK_API_KEY_MIDDLEWARE_EXCLUDED_URL_PREFIXES = (
        '/admin',
    )

## Example Request

```python
response = requests.get(
    url="http://0.0.0.0:8000/api/login",
    headers={
        "Api-Key": "fd8b4a98c8f53035aeab410258430e2d86079c93",
    },
)
```

## Optional Settings
In your Django Settings file, you can change the name of the header
token that should be passed.  The default is `api-key`, as shown in the
example request.  The custom key must not contain the '_' character.

    REST_FRAMEWORK_API_KEY_HEADER_TOKEN = 'x-my-custom-api-key'

Here's an associated example request:

```python
response = requests.get(
    url="http://0.0.0.0:8000/api/login",
    headers={
        "x-my-custom-api-key": "fd8b4a98c8f53035aeab410258430e2d86079c93",
    },
)
```

## Tests
Make sure you have `tox` installed in your global instance of Python.  It is recommended to develop with the latest
version of Python and Django that this library supports.  Make sure you have the appropriate version of Python installed
on your machine to test in that environment.  To see all environments this library supports, run:

    tox --listenvs

Then, choose an environment to run tests using.  Tox will setup the virtual environment and install all appropriate
dependencies.  Travis CI will execute tests on across all environments.

    tox -e py35-django110


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Make sure tests are passing


[travis-image]: https://travis-ci.org/manosim/django-rest-framework-api-key.svg?branch=master
[travis-url]: https://travis-ci.org/manosim/django-rest-framework-api-key

[codecov-image]: https://codecov.io/github/manosim/django-rest-framework-api-key/coverage.svg?branch=master
[codecov-url]:https://codecov.io/github/manosim/django-rest-framework-api-key?branch=master

[pypi-image]: https://badge.fury.io/py/drfapikey.svg
[pypi-url]: https://pypi.python.org/pypi/drfapikey/
