from distutils.core import setup
import setup_translate

pkg = 'Extensions.FontInfo'
setup (name = 'enigma2-plugin-extensions-fontinfo',
       version = '1.14',
       description = 'display lineheight for font size',
       packages = [pkg],
       package_dir = {pkg: 'plugin'},
       package_data = {pkg: ['*.txt', 'locale/*.pot', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass = setup_translate.cmdclass, # for translation
      )
