#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class SetDiscussionGroup(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``170``
        - ID: ``40582BB2``

    Parameters:
        broadcast (:obj:`InputChannel <telectron.raw.base.InputChannel>`):
            N/A

        group (:obj:`InputChannel <telectron.raw.base.InputChannel>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["broadcast", "group"]

    ID = 0x40582bb2
    QUALNAME = "functions.channels.SetDiscussionGroup"

    def __init__(self, *, broadcast: "raw.base.InputChannel", group: "raw.base.InputChannel") -> None:
        self.broadcast = broadcast  # InputChannel
        self.group = group  # InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetDiscussionGroup":
        # No flags
        
        broadcast = TLObject.read(b)
        
        group = TLObject.read(b)
        
        return SetDiscussionGroup(broadcast=broadcast, group=group)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.broadcast.write())
        
        b.write(self.group.write())
        
        return b.getvalue()
