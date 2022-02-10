# for localized messages
from . import _
#################################################################################
#
#    FontInfo - plugin for Enigma2
#
#
#    Coded by ims (c)2018-2022
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#################################################################################

from Plugins.Plugin import PluginDescriptor

def main(session, **kwargs):
	import ui
	session.open(ui.FontInfo)

def Plugins(path, **kwargs):
	name = _("FontInfo")
	descr = _("Display line height for fonts used in skin")
	return [
		PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main),
	]