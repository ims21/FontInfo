# for localized messages
from . import _
#################################################################################
#
#    FontInfo - plugin for Enigma2
#    version:
VERSION = "1.03"
#    Coded by ims (c)2018
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
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, NoSave, ConfigSubsection, config, ConfigSelection, ConfigText, ConfigYesNo
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
import skin
import enigma
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, fileExists
import xml.etree.cElementTree as ET

class FontInfo(Screen, ConfigListScreen):
	skin = """
	<screen name="FontInfo" position="center,center" size="610,520" title="FontInfo" backgroundColor="#31000000">
		<widget name="config" position="5,2" size="600,25"/>
		<widget name="info" position="20,29" size="600,18" font="Regular;16" halign="left" transparent="1"/>
		<ePixmap pixmap="skin_default/div-h.png" position="5,48" zPosition="2" size="600,2"/>
		<widget name="fontsinfo" position="20,53" size="590,440" font="Regular;19" zPosition="1" backgroundColor="#31000000" scrollbarMode="showOnDemand"/>
		<ePixmap pixmap="skin_default/div-h.png" position="5,493" zPosition="2" size="600,2"/>
		<widget name="key_red"   position="005,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="red" transparent="1"/>
		<widget name="key_green" position="155,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="green" transparent="1"/>
		<widget name="key_yellow" position="305,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="yellow" transparent="1"/>
		<widget name="key_blue"  position="455,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="blue" transparent="1"/>
	</screen>"""

	def __init__(self, session, ):
		Screen.__init__(self, session)
		self.session = session
		self.title = _("FontInfo %s") % VERSION

		### do not remove self["tmp"] !!!
		self["tmp"] = Label("")
		###

		config.plugins.fontinfo = ConfigSubsection()
		choicelist = self.readFonts()
		config.plugins.fontinfo.fonts = NoSave(ConfigSelection(default = choicelist[0], choices = choicelist))

		self["info"] = Label(_("Font size / line height (px)"))
		self["fontsinfo"] = Label()

		self.FontInfoCfg = [getConfigListEntry(_("Select font"), config.plugins.fontinfo.fonts )]

		ConfigListScreen.__init__(self, self.FontInfoCfg, session = session, on_change = self.displayValues)

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.close,
				"red": self.close,
				"blue": self.testLength,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["key_blue"] = Label(_("Tests"))
		self.onLayoutFinish.append(self.displayValues)

	def displayValues(self):
		family = config.plugins.fontinfo.fonts.value.split(',')[0]
		self["tmp"].instance.setNoWrap(1)
		self["tmp"].setText("W")
		info = ""
		for h in range(1,21):
			info += ("%02d / %02d\t") % ( h, self.lineHeight(h, family))
			info += ("%02d / %02d\t") % ( h+20, self.lineHeight(h+20, family))
			info += ("%02d / %02d\t") % ( h+40, self.lineHeight(h+40, family))
			info += ("%02d / %02d") % ( h+60, self.lineHeight(h+60, family))
			info += ("\n")
		self["fontsinfo"].setText(info)

	def lineHeight(self, size, family):
		fnt = enigma.gFont(family, size)
		self["tmp"].instance.setFont(fnt)
		return self["tmp"].instance.calculateSize().height()

	def readFonts(self):
		path = config.skin.primary_skin.value.split('/')[0]
		if path is ".":
			skin = resolveFilename(SCOPE_CURRENT_SKIN, "skin_default.xml")
		else:
			skin = resolveFilename(SCOPE_CURRENT_SKIN, config.skin.primary_skin.value)
		root = ET.parse(skin).getroot()
		fonts = root.find('fonts')
		list = []
		for font in fonts.findall('font'):
			list.append(("%s, %s") % (font.attrib.get('name', None), font.attrib.get('filename', None)))
		return list

	def testLength(self):
		self.session.open(FontInfoTestLength)

class FontInfoTestLength(Screen, ConfigListScreen):
	skin = """
	<screen name="FontInfoTestLength" position="center,center" size="710,490" title="FontInfo - tests" backgroundColor="#31000000">
		<widget name="config" position="5,2" size="700,100" backgroundColor="#31000000"/>
		<widget name="text" position="5,120" size="700,300" font="Regular;30" backgroundColor="#00404040"/>
		<widget name="size" position="5,425" size="300,35" font="Regular;30" zPosition="1" backgroundColor="#31000000"/>
		<ePixmap pixmap="skin_default/div-h.png" position="5,462" zPosition="2" size="700,2"/>
		<widget name="key_red"   position="005,465" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="red" transparent="1"/>
		<widget name="key_green" position="155,465" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="green" transparent="1"/>
		<widget name="key_yellow" position="305,465" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="yellow" transparent="1"/>
		<widget name="key_blue"  position="455,465" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="blue" transparent="1"/>
		<widget name="HelpWindow" position="0,0" size="0,0"/>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.title = _("FontInfo %s - tests" ) % VERSION

		### do not remove self["tmp"] !!!
		self["tmp"] = Label("")
		###

		choicelist = []
		for i in range(1, 81):
			choicelist.append((str(i)))
		config.plugins.fontinfo.size = NoSave(ConfigSelection(default = "30", choices = choicelist))
		config.plugins.fontinfo.nowrap = NoSave(ConfigYesNo(default = False))
		config.plugins.fontinfo.text = NoSave(ConfigText(default = "Hello", visible_width = 2000, fixed_size = False))

		self["text"] = Label()
		self["size"] = Label()

		self.FontInfoTestLengthCfg = []
		self.cfgText = _("Write text")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgText, config.plugins.fontinfo.text ))
		self.cfgFont = _("Select font")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgFont, config.plugins.fontinfo.fonts ))
		self.cfgSize = _("Set font size")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgSize, config.plugins.fontinfo.size ))
		self.cfgNowrap = _("No wrap")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgNowrap, config.plugins.fontinfo.nowrap ))


		ConfigListScreen.__init__(self, self.FontInfoTestLengthCfg, session = session, on_change = self.changes)

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.close,
				"red": self.close,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self.onLayoutFinish.append(self.setString)

	def changes(self):
		if self["config"].getCurrent()[0] == self.cfgFont:
			self.setString()
		elif self["config"].getCurrent()[0] == self.cfgSize:
			self.setString()
		elif self["config"].getCurrent()[0] == self.cfgNowrap:
			self.setString()
		elif self["config"].getCurrent()[0] == self.cfgText:
			self.setString()

	def setString(self):
		self["text"].instance.setNoWrap(self.nowrap())
		self["text"].instance.setFont(self.font())
		self["text"].setText("%s" % self.text())
		self["size"].setText(("%s x %s (px)" % self.getLength()) + (" / %s" % self.lineHeight()))

	def getLength(self):
		return self["text"].instance.calculateSize().width(), self["text"].instance.calculateSize().height()

	def font(self):
		return enigma.gFont(self.family(), self.size())

	def lineHeight(self):
		self["tmp"].instance.setNoWrap(1)
		self["tmp"].setText("W")
		self["tmp"].instance.setFont(self.font())
		return self["tmp"].instance.calculateSize().height()

	def family(self):
		return config.plugins.fontinfo.fonts.value.split(',')[0]
	def size(self):
		return int(config.plugins.fontinfo.size.value)
	def nowrap(self):
		return config.plugins.fontinfo.nowrap.value
	def text(self):
		return config.plugins.fontinfo.text.value
	def setLabel(self):
		pass
