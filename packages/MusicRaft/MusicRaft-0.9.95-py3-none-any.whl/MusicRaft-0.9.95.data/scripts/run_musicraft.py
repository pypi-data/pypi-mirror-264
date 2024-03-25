#!python
"""
WARNING. thisfile got lost somewhere along the way and ha been
hastily reconstructed from 'musicraft_timid.py'
Copyright 2020 Larry Myerscough
"""

# -----------------------------------------------------------------------------
# import the code of the plugins we intend to launch 'on the raft':
from musicraft.abcraft import AbcRaft
from musicraft.pyraft import PyRaft
# -----------------------------------------------------------------------------
# import the code to start 'the raft':
from musicraft.__main__ import main


# -----------------------------------------------------------------------------
# but first let's do some tweaking (customisation)...

# -----------------------------------------------------------------------------
# select a specific MIDI output port name (this is useful for my ubuntu setup)
#from musicraft.abcraft.midiplayer import MidiPlayer
# WARNING: Midi customization does not work with current code!
#MidiPlayer.outputCmdArgs = ["timidity", "-iA"]
#MidiPlayer.outputPort = 'TiMidity:TiMidity port 0' #  128:0'


# addition for testing if fix to abcm2ps by jfg:
# from musicraft.abcraft.external import Abcm2svg
# Abcm2svg.exec_dir = '/home/gill/PycharmProjects/abcm2ps/'
# -----------------------------------------------------------------------------
# # enable the following lines to select a different directory for the abc2midi program.
# from musicraft.abcraft.external import Abc2midi
# Abc2midi.exec_dir = '/usr/local/bin/'
# # ... and maybe tweak the way musicraft parses the output of abc2mdi ...
# Abc2midi.reMsg = r'.*in\s+line-char\s(\d+)\-(\d+).*'
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# # enable the following lines to select a different docking scheme
# # for the various components of 'the raft'.
# from musicraft import QtCore, EditBook, StdBook, DisplayBook
# EditBook.whereToDock = QtCore.Qt.RightDockWidgetArea
# StdBook.whereToDock = QtCore.Qt.RightDockWidgetArea
# DisplayBook.whereToDock = QtCore.Qt.LeftDockWidgetArea


# -----------------------------------------------------------------------------
# now call the 'raft' with the 'abcraft' plugin;
# 'PyRaft' works bu is not needed for general use. Disable this if you wish!
# FreqRaft is currently disabled because it is (forever?) unfinished.
#
main(
    Plugins=(AbcRaft,
             PyRaft,
           #  FreqRaft,
             )
)
