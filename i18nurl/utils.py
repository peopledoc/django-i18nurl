import locale

from django.utils.translation.trans_real import to_locale


def normalize_language(language):
    return locale.locale_alias.get(to_locale(language, True))


def is_language_supported(language, supported_languages=None):
    if supported_languages is None:
        from django.conf import settings
        supported_languages = dict(settings.LANGUAGES).keys()
    if not language:
        return None
    normalized = normalize_language(language)
    if not normalized:
        return None
    # Remove the default encoding from locale_alias.
    normalized = normalized.split('.')[0]
    for lang in (normalized, normalized.split('_')[0]):
        if lang.lower() in supported_languages:
            return lang
    return None
