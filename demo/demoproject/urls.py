from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy as reverse

from .views import reroute

home = TemplateView.as_view(template_name='home.html')

#: IHM URL: language sensitive patterns.
ihm_patterns = patterns(
    '',
    url(_(r'^home/'), home, name='home'),
)


urlpatterns = patterns(
    '',
    url(r'', include('i18nurl.urls')),
    url(r'^$', reroute),
    url(_(r'^en/'), include(ihm_patterns)),
)
