# for localized messages
from . import _ , PATH
#################################################################################
#
#    FontInfo - plugin for PLi enigma2
#    version:
VERSION = "1.18"
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

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, NoSave, ConfigSubsection, config, ConfigSelection, ConfigText, ConfigYesNo
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.Boolean import Boolean
import skin
from enigma import getDesktop, gFont, eSize
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, fileExists, SCOPE_PLUGINS
import xml.etree.cElementTree as ET

FILENAME = "testtext.txt"

config.plugins.fontinfo = ConfigSubsection()
cfg = config.plugins.fontinfo

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

		choicelist = self.readFonts()
		cfg.fonts = NoSave(ConfigSelection(default = choicelist[0], choices = choicelist))

		self["info"] = Label(_("Font size / line height (px)"))
		self["fontsinfo"] = Label()

		self.FontInfoCfg = [getConfigListEntry(_("Select font"), cfg.fonts )]
		ConfigListScreen.__init__(self, self.FontInfoCfg, session = session, on_change = self.displayValues)

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"red": self.close,
				"blue": self.testLength,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["key_blue"] = Label(_("Tests"))
		self.onLayoutFinish.append(self.displayValues)

	def displayValues(self):
		family = cfg.fonts.value.split(',')[0]
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
		fnt = gFont(family, size)
		self["tmp"].instance.setFont(fnt)
		return self["tmp"].instance.calculateSize().height()

	def readFonts(self):
		fontslist = []
		path = config.skin.primary_skin.value.split('/')[0]
		skin = resolveFilename(SCOPE_CURRENT_SKIN, "skin_default.xml" if path is "." else config.skin.primary_skin.value)
		if fileExists(skin):
			fontslist = self.parseSkin(skin)
			if not len(fontslist): # try non standard fonts info placement
				root = ET.parse(skin).getroot()
				files = root.findall('include')
				for file in files:
					path = root.find('include').attrib.get('filename', None)
					skin = resolveFilename(SCOPE_CURRENT_SKIN, path)
					if fileExists(skin):
						fontslist += self.parseSkin(skin)
		skin = resolveFilename(SCOPE_CURRENT_SKIN, "skin_display.xml")
		if fileExists(skin):
			fontslist += self.parseSkin(skin)

		 # unfortunately, both variants changing order
#		return list(dict.fromkeys(fontslist))
#		return list(set(fontslist))
		return self.getUniqueList(fontslist)

	def getUniqueList(self, originalList):
		uniqueList = []
		[uniqueList.append(item) for item in originalList if item not in uniqueList]
		return uniqueList

	def parseSkin(self, skin):
		fontList = []
		root = ET.parse(skin).getroot()
		fonts = root.find('fonts')
		if fonts:
			for font in fonts.findall('font'):
				rec = ("%s, %s") % (font.attrib.get('name', None), font.attrib.get('filename', None))
				if not fontList.count(rec):
					fontList.append(rec)
		return fontList

	def testLength(self):
		self.session.open(FontInfoTestLength)

RES = "sd"
if getDesktop(0).size().width() >= 1920:
	RES = "fullhd"
elif getDesktop(0).size().width() >= 1280:
	RES = "hd"

class FontInfoTestLength(Screen, ConfigListScreen):
	if RES == "fullhd":
		skin = """
		<screen name="FontInfoTestLength" position="center,center" size="1200,800" title="FontInfo - Tests screen" backgroundColor="#00000000">
			<widget name="config" position="10,5" size="1180,228" itemHeight="38" font="Regular;28" backgroundColor="#00000000"/>
			<widget name="text" position="150,260" size="900,200" font="Regular;30" zPosition="1" backgroundColor="#00404040"/>
			<widget name="size" position="150,470" size="900,35" font="Regular;30" zPosition="1" backgroundColor="#00000000"/>
			<widget name="HelpWindow" position="center,670" size="120,0"/>
			<widget name="key_red" position="5,770" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="red" transparent="1"/>
			<widget name="key_yellow" position="400,770" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="yellow" transparent="1"/>
			<widget name="key_blue"  position="600,770" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="blue" transparent="1"/>
		</screen>"""
	elif RES == "hd":
		skin = """
		<screen name="FontInfoTestLength" position="center,center" size="1000,580" title="FontInfo - Tests screen" backgroundColor="#00000000">
			<widget name="config" position="10,5" size="980,150" backgroundColor="#00000000"/>
			<widget name="text" position="50,170" size="700,200" font="Regular;20" zPosition="1" backgroundColor="#00404040"/>
			<widget name="size" position="50,390" size="700,23" font="Regular;20" zPosition="1" backgroundColor="#00000000"/>
			<widget name="HelpWindow" position="center,470" size="100,0"/>
			<widget name="key_red" position="5,555" zPosition="2" size="150,23" valign="center" halign="center" font="Regular;20" foregroundColor="red" transparent="1"/>
			<widget name="key_yellow" position="300,555" zPosition="2" size="150,23" valign="center" halign="center" font="Regular;20" foregroundColor="yellow" transparent="1"/>
			<widget name="key_blue"  position="450,555" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="blue" transparent="1"/>
		</screen>"""
	else:
		skin = """
		<screen name="FontInfoTestLength" position="center,center" size="610,515" title="FontInfo - Tests screen" backgroundColor="#00000000">
			<widget name="config" position="5,2" size="600,125" backgroundColor="#31000000"/>
			<widget name="text" position="5,145" size="600,100" font="Regular;20" backgroundColor="#00404040"/>
			<widget name="size" position="5,350" size="300,23" font="Regular;20" zPosition="1" backgroundColor="#00000000"/>
			<ePixmap pixmap="skin_default/div-h.png" position="5,487" zPosition="2" size="700,2"/>
			<widget name="HelpWindow" position="center,380" size="100,0"/>
			<widget name="key_red" position="10,490" zPosition="2" size="150,23" valign="center" halign="center" font="Regular;20" foregroundColor="red" transparent="1"/>
			<widget name="key_yellow" position="300,490" zPosition="2" size="150,23" valign="center" halign="center" font="Regular;20" foregroundColor="yellow" transparent="1"/>
			<widget name="key_blue"  position="450,490" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="blue" transparent="1"/>
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.title = _("FontInfo %s - Test screen" ) % VERSION

		### do not remove self["tmp"] !!!
		self["tmp"] = Label("")
		###

		self.testText = "Write text to Label. If you want not so large Label, use UP and change it. You can put text to %s under plugin directory." % FILENAME
		self.testText = self.readText() or self.testText
		cfg.text = NoSave(ConfigText(default = self.testText, visible_width = 80, fixed_size = False))

		choicelist = []
		for i in range(1, 81):
			choicelist.append(("%d"%i,i))
		fontsize = "20"
		if RES == "fullhd":
			fontsize = "30"
		cfg.size = NoSave(ConfigSelection(default=fontsize, choices=choicelist))
		cfg.nowrap = NoSave(ConfigYesNo(default=False))
		choicelist = [("0","left"), (1, "center"),("2", "right"), ("3", "block")]
		cfg.halign = NoSave(ConfigSelection(default="0", choices=choicelist))
		choicelist = [("0","top"), (1, "center"),("2", "bottom")]
		cfg.valign = NoSave(ConfigSelection(default="0", choices=choicelist))

		choicelist = []
		x_default = "600"
		if RES == "fullhd":
			x_default = "900"
		for i in range(10, int(x_default) + 1, 10):
			choicelist.append(("%d"%i,i))
		cfg.lx = NoSave(ConfigSelection(default=x_default, choices=choicelist))

		choicelist = []
		for i in range(10, 201, 10):
			choicelist.append(("%d"%i,i))
		y_default = "200"
		if RES == "sd":
			y_default = "100"
		cfg.ly = NoSave(ConfigSelection(default=y_default, choices=choicelist))

		self["text"] = Label()
		self["size"] = Label()

		self.FontInfoTestLengthCfg = []
		ConfigListScreen.__init__(self, self.FontInfoTestLengthCfg, session = self.session, on_change = self.changes)
		self.createCFG()

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"red": self.close,
				"yellow": self.clearText,
				"blue": self.reloadText
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["key_yellow"] = Label(_("Clear"))
		self["key_blue"] = Label(_("Reload"))
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self["VKeyIcon"] = Boolean(False)
		self.onLayoutFinish.append(self.setString)

	def createCFG(self):
		self.FontInfoTestLengthCfg = []
		self.cfgText = _("Write text")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgText, cfg.text ))
		self.cfgFont = _("Select font")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgFont, cfg.fonts ))
		self.cfgSize = _("Set font size")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgSize, cfg.size ))
		self.cfgNowrap = _("noWrap")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgNowrap, cfg.nowrap ))
		self.cfgHalign = _("halign")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgHalign, cfg.halign ))
		self.cfgValign = _("valign")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgValign, cfg.valign ))
		self.cfgLx = _("Label width")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgLx, cfg.lx ))
		self.cfgLy = _("Label height")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.cfgLy, cfg.ly ))
		self["config"].list = self.FontInfoTestLengthCfg
		self["config"].l.setList(self.FontInfoTestLengthCfg)

	def changes(self):
		if self["config"].getCurrent()[0] in (self.cfgFont, self.cfgSize, self.cfgNowrap, self.cfgText, self.cfgHalign, self.cfgValign):
			self.setString()
		elif self["config"].getCurrent()[0] in (self.cfgLx, self.cfgLy):
			self.setLabel()

	def setString(self):
		self["text"].instance.setNoWrap(self.nowrap())
		self["text"].instance.setFont(self.font())
		self["text"].instance.setHAlign(self.halign())
		self["text"].instance.setVAlign(self.valign())
		self["text"].setText("%s" % self.text())
		x, y = self.getLength()
		if x > 0:
			self["size"].setText(("%s x %s (px)" % (x, y)) + (" | %s" % self.lineHeight()))
		else:
			self["size"].setText("")

	def clearText(self):
		cfg.text.deleteAllChars()
		cfg.text.value=""
		self.createCFG()
		self.setString()

	def reloadText(self):
		cfg.text.deleteAllChars()
		cfg.text.value=self.readText()
		self.createCFG()
		self.setString()

	def readText(self):
		text = ""
		path = resolveFilename(SCOPE_PLUGINS, "%s/%s" % (PATH, FILENAME))
		if fileExists(path):
			fi = open(path,"r")
			text = fi.readline()
			fi.close()
		return text

	def getLength(self):
		return self["text"].instance.calculateSize().width(), self["text"].instance.calculateSize().height()

	def font(self):
		return gFont(self.family(), self.size())

	def lineHeight(self):
		self["tmp"].instance.setNoWrap(1)
		self["tmp"].setText("W")
		self["tmp"].instance.setFont(self.font())
		return self["tmp"].instance.calculateSize().height()

	def setLabel(self):
		listsize = (int(self.lx()), int(self.ly()))
		self["text"].instance.resize(eSize(*listsize))

	def family(self):
		return cfg.fonts.value.split(',')[0]
	def size(self):
		return int(cfg.size.value)
	def nowrap(self):
		return cfg.nowrap.value
	def text(self):
		return cfg.text.value
	def halign(self):
		return int(cfg.halign.value)
	def valign(self):
		return int(cfg.valign.value)
	def lx(self):
		return int(cfg.lx.value)
	def ly(self):
		return int(cfg.ly.value)
