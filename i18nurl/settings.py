from django.conf import settings

I18N_LANGUAGES = getattr(settings, 'I18N_LANGUAGES',
                         settings.LANGUAGES)

I18N_REDIRECT_URL_NAME = getattr(settings, 'I18N_REDIRECT_URL_NAME',
                                 'home')
