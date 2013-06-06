from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

home = TemplateView.as_view(template_name='home.html')

#: IHM URL: language sensitive patterns.
ihm_patterns = patterns(
    '',
    url(_(r'^home/'), home, name='home'),
)


urlpatterns = patterns(
    '',
    # Standard download views.
    url(_(r'^en/'), include(ihm_patterns)),
)
