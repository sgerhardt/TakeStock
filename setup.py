__author__ = 'Sean Gerhardt'

from distutils.core import setup
import py2exe

py2exe_options = {'py2exe': {'includes': ['sip', 'PyQt4.QtCore']}}
script = [{'script': 'GUI.py'}]
setup(
    windows=script,
    options=py2exe_options
)