# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from os import environ as os_environ
import gettext

PLUGIN_NAME = "FontInfo"
PATH = "Extensions/%s" % PLUGIN_NAME

def localeInit():
	lang = language.getLanguage()[:2]
	os_environ["LANGUAGE"] = lang
	gettext.bindtextdomain(PLUGIN_NAME, resolveFilename(SCOPE_PLUGINS, "%s/locale" % PATH))

def _(txt):
	t = gettext.dgettext(PLUGIN_NAME, txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

localeInit()
language.addCallback(localeInit)