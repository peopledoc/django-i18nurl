from django.conf.urls import patterns, url

from i18nurl.views import guess_language, set_language


urlpatterns = patterns(
    '',
    url(r'^$', guess_language, name='guess_language'),
    url(r'^i18n/$', set_language, name='set_language'),
)
