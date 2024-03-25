#!python
"""
This in example of how to customise the (default) settings of musicraft.
The script name reflects the fact that the primary customisation in effect
concerns "Timidity", but several other possibilities are shown, some of
 them in 'commented out' form.
Copyright 2020 Larry Myerscough
"""
import musicraft
print(f"!using musicraft from {musicraft.__file__}!")
# -----------------------------------------------------------------------------
# See 'musicraft_custom.py' for more customization options, better commented.
# This is a special customization to facilitate colouring note heads according to
# the assumed left hand position when playing the cello.

from musicraft.abcraft import AbcRaft
from musicraft.__main__ import main
from musicraft.abcraft.syntax import AbcHighlighter

AbcHighlighter.snippets.update(
    {
        '1=' : (r'"^$21="[I:voicecolor #000000]',),
        '1\\': (r'"^$21\\"[I:voicecolor #504000]',),
        '1/' : (r'"^$21/"[I:voicecolor purple]',),
        '2-' : (r'"^$22-"[I:voicecolor #008000]',),
        '3=' : (r'"^$23="[I:voicecolor #000080]',),
        '3/' : (r'"^$23/"[I:voicecolor #007070]',),
        '4\\': (r'"^$24\\"[I:voicecolor #800000]',),
    }
)
#
main(
    Plugins=(AbcRaft,
             )
)
