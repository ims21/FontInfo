# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from os import environ as os_environ
import gettext

PATH = "Extensions/FontInfo"

def localeInit():
	lang = language.getLanguage()[:2]
	os_environ["LANGUAGE"] = lang
	gettext.bindtextdomain("FontInfo", resolveFilename(SCOPE_PLUGINS, "%s/locale" % PATH))

def _(txt):
	t = gettext.dgettext("FontInfo", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)