import locale
import re

from django.conf import settings
from django.utils import translation
from django.utils.translation.trans_real import (check_for_language,
                                                 parse_accept_lang_header,
                                                 to_locale)
from django.utils.cache import patch_vary_headers

from .utils import is_language_supported


class BaseLanguageMiddleware(object):
    def get_language_from_request(self, request):
        raise NotImplementedError()

    def process_request(self, request):
        language_code = getattr(request, 'LANGUAGE_CODE', None)
        if language_code is None:
            language_code = self.get_language_from_request(request)
            if language_code:
                translation.activate(language_code)
                request.LANGUAGE_CODE = language_code
        return None

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response


class DefaultLanguageMiddleware(BaseLanguageMiddleware):
    """Middleware that activate settings.LANGUAGE_CODE."""
    def get_language_from_request(self, request):
        """Return settings.LANGUAGE_CODE."""
        return settings.LANGUAGE_CODE


class UrlPrefixLanguageMiddleware(BaseLanguageMiddleware):
    """Looks after a language prefix in request.path_info."""
    def get_language_from_request(self, request):
        """Search one of settings.LANGUAGES code in request.path_info."""
        alternatives = [code for code, name in settings.LANGUAGES]
        pattern = r'^/(?P<language>%s)(?P<path>/.*|)$' \
                  % '|'.join(alternatives)
        match = re.match(pattern, request.path_info)
        if match is not None:
            requested_language = match.group('language')
            return is_language_supported(requested_language)
        return None


class CookieLanguageMiddleware(BaseLanguageMiddleware):
    def get_language_from_request(self, request):
        lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        return is_language_supported(lang_code)


class SessionLanguageMiddleware(BaseLanguageMiddleware):
    def get_language_from_request(self, request):
        if hasattr(request, 'session'):
            lang_code = request.session.get('django_language', None)
            return is_language_supported(lang_code)
        return None


class HttpAcceptLanguageMiddleware(BaseLanguageMiddleware):
    def get_language_from_request(self, request):
        supported = dict(settings.LANGUAGES)
        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        for accept_lang, unused in parse_accept_lang_header(accept):
            if accept_lang == '*':
                break

            # We have a very restricted form for our language files
            # (no encoding specifier, since they all must be UTF-8 and
            # only one possible language each time. So we avoid the
            # overhead of gettext.find() and work out the MO file
            # manually.

            # 'normalized' is the root name of the locale in POSIX
            # format (which is the format used for the directories
            # holding the MO files).
            normalized = locale.locale_alias.get(to_locale(accept_lang, True))
            if not normalized:
                continue
            # Remove the default encoding from locale_alias.
            normalized = normalized.split('.')[0]

            for lang_code in (accept_lang, accept_lang.split('-')[0]):
                lang_code = lang_code.lower()
                if lang_code in supported and check_for_language(lang_code):
                    return lang_code
        return None


class UserLanguageMiddleware(BaseLanguageMiddleware):
    def get_language_from_request(self, request):
        user = request.user
        requested_language = None
        if hasattr(user, 'language_code'):
            requested_language = user.language_code
        language = is_language_supported(requested_language)
        if language:
            return language
        return None
