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


class SavedGifs(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.messages.SavedGifs`.

    Details:
        - Layer: ``170``
        - ID: ``84A02A0D``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        gifs (List of :obj:`Document <telectron.raw.base.Document>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: telectron.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetSavedGifs
    """

    __slots__: List[str] = ["hash", "gifs"]

    ID = 0x84a02a0d
    QUALNAME = "types.messages.SavedGifs"

    def __init__(self, *, hash: int, gifs: List["raw.base.Document"]) -> None:
        self.hash = hash  # long
        self.gifs = gifs  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SavedGifs":
        # No flags
        
        hash = Long.read(b)
        
        gifs = TLObject.read(b)
        
        return SavedGifs(hash=hash, gifs=gifs)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.gifs))
        
        return b.getvalue()
