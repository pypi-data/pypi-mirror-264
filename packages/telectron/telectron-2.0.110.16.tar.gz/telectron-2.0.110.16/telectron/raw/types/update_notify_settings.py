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


class UpdateNotifySettings(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.Update`.

    Details:
        - Layer: ``170``
        - ID: ``BEC268EF``

    Parameters:
        peer (:obj:`NotifyPeer <telectron.raw.base.NotifyPeer>`):
            N/A

        notify_settings (:obj:`PeerNotifySettings <telectron.raw.base.PeerNotifySettings>`):
            N/A

    """

    __slots__: List[str] = ["peer", "notify_settings"]

    ID = 0xbec268ef
    QUALNAME = "types.UpdateNotifySettings"

    def __init__(self, *, peer: "raw.base.NotifyPeer", notify_settings: "raw.base.PeerNotifySettings") -> None:
        self.peer = peer  # NotifyPeer
        self.notify_settings = notify_settings  # PeerNotifySettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateNotifySettings":
        # No flags
        
        peer = TLObject.read(b)
        
        notify_settings = TLObject.read(b)
        
        return UpdateNotifySettings(peer=peer, notify_settings=notify_settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.notify_settings.write())
        
        return b.getvalue()
