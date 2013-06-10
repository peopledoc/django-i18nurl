"""Views to manage active language."""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import override
from django.views.generic import FormView, RedirectView

from i18nurl.settings import I18N_REDIRECT_URL_NAME
from i18nurl.forms import LanguageSelectionForm


class GuessLanguageView(RedirectView):
    """Guess language and redirect to the matching URL."""
    permanent = False

    def get_redirect_url(self, **kwargs):
        """Try to guess language from the request and to redirect to
        the matching language.

        If not able to guess the adequate site, redirects to the
        default site and display a message which includes language
        selection links.

        """
        return reverse(I18N_REDIRECT_URL_NAME)


guess_language = GuessLanguageView.as_view()


class SetLanguageView(FormView):
    """Display language selection form, or, if form submitted, remember
    selected language and redirects to the adequate URL."""
    form_class = LanguageSelectionForm
    template_name = 'i18n/set_language.html'

    def form_valid(self, form):
        """Rememeber selected language and redirects to the adequate URL."""
        #next = self.request.META.get('HTTP_REFERER', next)
        language_code = form.cleaned_data['language']
        redirect_url = form.cleaned_data['next']
        remember = not form.cleaned_data['temporary']
        if not redirect_url:
            with override(language_code):
                redirect_url = reverse(I18N_REDIRECT_URL_NAME)
        response = HttpResponseRedirect(redirect_url)
        if remember:
            # Write in user's profile.
            user = self.request.user
            if hasattr(user, 'language_code') and \
                    user.language_code != language_code:
                user.language_code = language_code
                user.save()
            # Write in session.
            if hasattr(self.request, 'session'):
                self.request.session['django_language'] = language_code
            # Write in a cookie.
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                                    language_code)
        return response


set_language = SetLanguageView.as_view()
