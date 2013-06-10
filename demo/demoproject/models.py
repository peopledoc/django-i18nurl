# -*- coding: utf-8 -*-
from i18nurl import reverse_i18n

# At startup print some urls

print 'French', reverse_i18n('home', 'fr')
print 'English', reverse_i18n('home', 'en')
print 'German', reverse_i18n('home', 'de')
