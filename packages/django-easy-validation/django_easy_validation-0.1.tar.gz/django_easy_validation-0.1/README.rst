Django Easy Validation |pypi version|
---------------------------------------

.. |pypi version|
   image:: https://img.shields.io/pypi/v/django-image-optimizer.svg
   :target: https://pypi.python.org/pypi/django-image-optimizer

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/agusmakmun/django-image-optimizer/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/django-image-optimizer.svg
   :target: https://pypi.python.org/pypi/django-image-optimizer

.. image:: https://img.shields.io/badge/Django-1.8%20%3E=%203.0-green.svg
  :target: https://www.djangoproject.com


Django Easy Validation is a simple Django library that allows validation for forms via ajax in a simple and elegant way.


Installation
------------------------------

Django Easy Validation is available directly from `PyPI <https://pypi.python.org/pypi/django-easy-validation>`_:

1. Installing the package.

::

    $ pip install django-easy-validation




4. You may use the package by importing it

::

    from easy_validations import Validatior

    @require_http_methods('POST')
    def store(request):
       data = json.loads(request.body)
       errors = Validator.validate(request, {
           "name": "required|unique:rating_metrices|max:100|min:6",
           "score": "required|numeric"
       })
       if errors:
           return JsonResponse(errors, status=422, safe=False)

       if errors and is_ajax:
           return JsonResponse(errors, status=422, safe=False)

    return JsonResponse('success', safe=False)



