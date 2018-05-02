# for localized messages
from . import _

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, NoSave, ConfigSubsection, config, ConfigSelection, ConfigText, ConfigYesNo
from Components.ActionMap import ActionMap
from Components.Label import Label
import skin
import enigma
from plugin import VERSION
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
		self["key_blue"] = Label(_("Test width"))
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
		self.session.open(FontInfoTestLength, config.plugins.fontinfo.fonts )

class FontInfoTestLength(Screen, ConfigListScreen):
	skin = """
	<screen name="FontInfoTestLength" position="center,center" size="610,520" title="FontInfo - test length" backgroundColor="#31000000">
		<widget name="config" position="5,2" size="600,100" backgroundColor="#31000000"/>
		<widget name="text" position="5,120" size="600,200" font="Regular;30" backgroundColor="#00404040"/>
		<widget name="size" position="5,330" size="300,35" font="Regular;30" zPosition="1" backgroundColor="#31000000"/>
		<ePixmap pixmap="skin_default/div-h.png" position="5,493" zPosition="2" size="600,2"/>
		<widget name="key_red"   position="005,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="red" transparent="1"/>
		<widget name="key_green" position="155,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="green" transparent="1"/>
		<widget name="key_yellow" position="305,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="yellow" transparent="1"/>
		<widget name="key_blue"  position="455,495" zPosition="2" size="150,25" valign="center" halign="center" font="Regular;22" foregroundColor="blue" transparent="1"/>
	</screen>"""

	def __init__(self, session, fonts):
		Screen.__init__(self, session)
		self.session = session
		self.title = _("FontInfo %s - test length" ) % VERSION

		config.plugins.fontinfo = ConfigSubsection()
		config.plugins.fontinfo.fonts = NoSave(ConfigSelection(default = fonts.choices[0], choices = fonts.choices[:]))
		choicelist = []
		for i in range(1, 81):
			choicelist.append((str(i)))
		config.plugins.fontinfo.size = NoSave(ConfigSelection(default = "30", choices = choicelist))
		config.plugins.fontinfo.nowrap = NoSave(ConfigYesNo(default = False))
		config.plugins.fontinfo.text = NoSave(ConfigText(default = "0", visible_width = 1000, fixed_size = False))

		self["text"] = Label()
		self["size"] = Label()

		self.FontInfoTestLengthCfg = []
		self.font = _("Select font")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.font, config.plugins.fontinfo.fonts ))
		self.size = _("Set font size")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.size, config.plugins.fontinfo.size ))
		self.nowrap = _("No wrap")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.nowrap, config.plugins.fontinfo.nowrap ))
		self.text = _("Write text")
		self.FontInfoTestLengthCfg.append(getConfigListEntry(self.text, config.plugins.fontinfo.text ))

		ConfigListScreen.__init__(self, self.FontInfoTestLengthCfg, session = session, on_change = self.changes)

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.close,
				"red": self.close,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self.string = ""
		self.onLayoutFinish.append(self.setString)

	def changes(self):
		if self["config"].getCurrent()[0] == self.font:
			self.setString()
		elif self["config"].getCurrent()[0] == self.size:
			self.setString()
		elif self["config"].getCurrent()[0] == self.nowrap:
			self.setString()
		elif self["config"].getCurrent()[0] == self.text:
			self.setString()

	def setString(self):
		family = config.plugins.fontinfo.fonts.value.split(',')[0]
		size = int(config.plugins.fontinfo.size.value)
		fnt = enigma.gFont(family, size)
		self["text"].instance.setNoWrap(config.plugins.fontinfo.nowrap.value)
		self["text"].instance.setFont(fnt)
		self.string = "%s" % config.plugins.fontinfo.text.value
		self["text"].setText(self.string)
		self["size"].setText("%s x %s" % (self.getLength()))

	def getLength(self):
		return self["text"].instance.calculateSize().width(), self["text"].instance.calculateSize().height()
