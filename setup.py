from setuptools import setup
import os
# from freecad.FCKeyboard.version import __version__
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "FCKeyboard", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.FCKeyboard',
      version=str(__version__),
      packages=['freecad',
                'freecad.FCKeyboard',
                'freecad.FCKeyboard.klepy'],
      maintainer="ThomasPDye",
      maintainer_email="tompdye@googlemail.com",
      url="https://github.com/ThomasPDye/FCKeyboard",
      description="a freecad extension for creating keyboards",
      install_requires=['pyjson5'],
      include_package_data=True)
