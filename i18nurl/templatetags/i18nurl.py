# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.base import Library, TemplateSyntaxError, kwarg_re, Node
from django.utils.encoding import smart_text
from django.core.urlresolvers import NoReverseMatch

from .. import reverse_i18n

register = Library()


class URLNode(Node):
    def __init__(self, view_name, language, args, kwargs, asvar):
        self.view_name = view_name
        self.language = language
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_text(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        view_name = self.view_name.resolve(context)
        language = self.language.resolve(context)

        if not view_name:
            raise NoReverseMatch(
                "'url' requires a non-empty first argument. "
                "The syntax changed in Django 1.5, see the docs.")

        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which case return nothing.
        url = ''
        try:
            url = reverse_i18n(view_name, language,
                               args=args, kwargs=kwargs,
                               current_app=context.current_app)
        except NoReverseMatch as e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse_i18n(project_name + '.' + view_name,
                                       language,
                                       args=args, kwargs=kwargs,
                                       current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


@register.tag
def i18nurl(parser, token):
    """
    Returns an absolute URL matching given view with its parameters in
    the good language.

        {% i18nurl "path.to.some_view" "language" arg1 arg2 %}

        or

        {% i18nurl "path.to.some_view" "language" name1=value1 name2=value2 %}

    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two argument"
                                  " (path to a view and language)" % bits[0])
    try:
        viewname = parser.compile_filter(bits[1])
    except TemplateSyntaxError as exc:
        exc.args = (exc.args[0] + ". The syntax of 'url' "
                    "changed in Django 1.5, see the docs."),
        raise

    language = parser.compile_filter(bits[2])

    args = []
    kwargs = {}
    asvar = None
    bits = bits[3:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return URLNode(viewname, language, args, kwargs, asvar)


class CurrentURLNode(Node):
    def __init__(self, language, asvar):
        self.language = language
        self.asvar = asvar

    def render(self, context):
        try:
            resolver_match = context['request'].resolver_match
        except AttributeError:
            return ''
        app_name = resolver_match.app_name
        url_name = resolver_match.url_name
        args = resolver_match.args
        kwargs = resolver_match.kwargs

        language = self.language.resolve(context)

        if app_name:
            view_name = '{app_name}:{url_name}'.format(app_name=app_name,
                                                       url_name=url_name)
        else:
            view_name = '{url_name}'.format(url_name=url_name)

        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which case return nothing.
        url = ''
        try:
            url = reverse_i18n(view_name, language,
                               args=args, kwargs=kwargs,
                               current_app=context.current_app)
        except NoReverseMatch as e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse_i18n(project_name + '.' + view_name,
                                       language,
                                       args=args, kwargs=kwargs,
                                       current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


@register.tag
def current_i18nurl(parser, token):
    """
    Returns the current page absolute url in the right language.

        {% current_i18nurl "language" %}

    """

    bits = token.split_contents()
    asvar = None

    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes one argument"
                                  " (language)" % bits[0])
    language = parser.compile_filter(bits[1])

    bits = bits[3:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    return CurrentURLNode(language, asvar)
