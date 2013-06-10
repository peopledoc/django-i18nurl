"""Context processors."""


def i18n(request):
    """Context processor which returns a dictionary containing I18N_SITES."""
    from i18nurl import settings
    return {'I18N_LANGUAGES': settings.I18N_LANGUAGES,
            'I18N_REDIRECT_URL_NAME': settings.I18N_REDIRECT_URL_NAME}
