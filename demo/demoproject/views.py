# -*- coding: utf-8 -*-
from django.utils.translation import get_language
from django.views.generic import RedirectView
from i18nurl import reverse_i18n


class RerouteView(RedirectView):
    """Home page."""
    def get_redirect_url(self, **kwargs):
        """Redirect user to the right page."""
        return reverse_i18n('home', language=get_language())


# Pre-configured views.
reroute = RerouteView.as_view()
