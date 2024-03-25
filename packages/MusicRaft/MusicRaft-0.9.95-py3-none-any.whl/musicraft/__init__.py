version = '0.9.94'

import sys, os, tempfile, platform

qt_module_name = os.getenv('MUSICRAFT_QT', 'PySide2')

if qt_module_name == 'PySide2':
    from PySide2 import (QtCore, QtGui, QtWidgets, QtPrintSupport, QtSvg, QtWebEngine, QtWebEngineWidgets)
    Signal = QtCore.Signal
    print("using PySide2!")
    NameFromDialog = lambda x: x[0]
elif qt_module_name == 'PyQt5':
    from PyQt5 import (QtCore, QtGui, QtWidgets, QtSvg, QtPrintSupport, QtWebEngine, QtWebEngineWidgets)
    Signal = QtCore.pyqtSignal
    print("using Pyqt5!")
    NameFromDialog = lambda x:x  # March 2020; not checked this lately!
else:
    raise NameError("bad value: MUSICRAFT_QT = " + qt_module_name)

WebView = QtWebEngineWidgets.QWebEngineView # historical but tolerable!

print(f"using version {version} of package 'musicraft'  from {os.path.split(__file__)[0]}")

# locate the directory in which this file, thus package musicraft, resides
head_dir = os.path.realpath(os.path.split(__file__)[0]+ '/../')

# Depending on the install method, this may or may not also be the parent or our 'share' directory.
# There's got to be a better way, but this should work:

if head_dir.endswith('-packages'):
    head_dir = os.path.normpath(head_dir + ((platform.system()=='Windows') and '/../../' or '/../../../'))

print("head_dir....", head_dir)

def packagePathName(fn, *pp):
    # relate path name to package location if necessary
    if not fn or fn[0] in '/\\.':  # don't mess with absolute or empty path name; path names starting with
        return fn                  # '.' are also taken to be deliberately NOT package relative.
    return os.path.join(head_dir, *pp, fn)

temp_dir = tempfile.gettempdir()


from .shared import *
from .raft import *
from .abcraft import *
from .pyraft import *
# from .freqraft import *


