from urlparse import urljoin
from django import forms
from django.utils.translation import ugettext_lazy as _
from i18nurl import settings


class LanguageSelectionForm(forms.Form):
    """Language selection form."""
    language = forms.ChoiceField(
        label=_('language'),
        choices=settings.I18N_LANGUAGES,
    )
    next = forms.CharField(
        label=_('next'),
        required=False,
        widget=forms.HiddenInput,
    )
    temporary = forms.BooleanField(
        label=_('remember'),
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )
