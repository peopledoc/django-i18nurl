# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


def read_relative_file(filename):
    """Returns contents of the given file, whose path is supposed relative
    to this module."""
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


if __name__ == '__main__':  # ``import setup`` doesn't trigger setup().
    setup(name='django-i18nurl',
          version=read_relative_file('VERSION').strip(),
          description="Django i18n URL",
          long_description=read_relative_file('README.rst'),
          classifiers=['Development Status :: 3 - Alpha',
                       'Environment :: Web Environment',
                       'Framework :: Django',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: BSD License',
                       'Natural Language :: English',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 3',
          ],
          keywords='django i18n url',
          author='Rémy Hubscher',
          author_email='hubscher.remy@gmail.com',
          url='https://github.com/novagile/django-i18nurl',
          license='BSD Licence',
          packages=find_packages(),
          include_package_data=True,
          zip_safe=False,
          install_requires=[]  # depends on Django
    )
