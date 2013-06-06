###############
Django i18n URL
###############

Django i18n url lets you manage your multilingual url using Django.
You can change the language and stay on the same page.

* Authors: Rémy Hubscher and `contributors
  <https://github.com/novagile/django-mail-factory/graphs/contributors>`_
* Licence: BSD
* Compatibility: Django 1.5+, python2.7 up to python3.3
* Project URL: https://github.com/novagile/django-i18nurl


Getting Started
===============

Install django-i18nurl::

    pip install django-i18nurl


Add it to your ``INSTALLED_APPS`` settings::

    INSTALLED_APPS = (
        '...',
        'i18nurl',
    )


Using it
========

Python
++++++

Use it in Python code::

    from i18nurl import reverse_i18n

    url_de = reverse_i18n('app:home', 'de')


Django template
+++++++++++++++

Use it as a templatetag::

    {% load i18nurl %}
    {% i18nurl 'app:home' 'de' %}


Get the current page in other languages::

    {% load i18nurl %}
    {% current_i18nurl 'de' %}
    

Note: to use ``current_i18nurl`` template tag you will need the request context processors::

    TEMPLATE_CONTEXT_PROCESSORS = (
        "...",
        "django.core.context_processors.request",
        "...",
    )
