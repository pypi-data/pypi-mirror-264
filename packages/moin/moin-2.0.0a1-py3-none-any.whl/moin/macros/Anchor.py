# Copyright: 2008,2011 MoinMoin:ThomasWaldmann
# License: GNU GPL v2 (or any later version), see LICENSE.txt for details.

"""
MoinMoin - Anchor Macro to put an anchor at the place where it is used.
"""


from moin.utils.tree import moin_page
from moin.macros._base import MacroInlineBase


class Macro(MacroInlineBase):
    def macro(self, content, arguments, page_url, alternative):
        if not arguments:
            raise ValueError("Anchor: you need to specify an anchor name.")

        anchor = arguments[0]
        return moin_page.span(attrib={moin_page.id: anchor})
