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


class GetGroupCallStreamRtmpUrl(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``170``
        - ID: ``DEB3ABBF``

    Parameters:
        peer (:obj:`InputPeer <telectron.raw.base.InputPeer>`):
            N/A

        revoke (``bool``):
            N/A

    Returns:
        :obj:`phone.GroupCallStreamRtmpUrl <telectron.raw.base.phone.GroupCallStreamRtmpUrl>`
    """

    __slots__: List[str] = ["peer", "revoke"]

    ID = 0xdeb3abbf
    QUALNAME = "functions.phone.GetGroupCallStreamRtmpUrl"

    def __init__(self, *, peer: "raw.base.InputPeer", revoke: bool) -> None:
        self.peer = peer  # InputPeer
        self.revoke = revoke  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetGroupCallStreamRtmpUrl":
        # No flags
        
        peer = TLObject.read(b)
        
        revoke = Bool.read(b)
        
        return GetGroupCallStreamRtmpUrl(peer=peer, revoke=revoke)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bool(self.revoke))
        
        return b.getvalue()
