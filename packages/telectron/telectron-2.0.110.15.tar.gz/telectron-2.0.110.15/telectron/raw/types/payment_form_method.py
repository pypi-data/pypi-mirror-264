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


class PaymentFormMethod(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~telectron.raw.base.PaymentFormMethod`.

    Details:
        - Layer: ``170``
        - ID: ``88F8F21B``

    Parameters:
        url (``str``):
            N/A

        title (``str``):
            N/A

    """

    __slots__: List[str] = ["url", "title"]

    ID = 0x88f8f21b
    QUALNAME = "types.PaymentFormMethod"

    def __init__(self, *, url: str, title: str) -> None:
        self.url = url  # string
        self.title = title  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PaymentFormMethod":
        # No flags
        
        url = String.read(b)
        
        title = String.read(b)
        
        return PaymentFormMethod(url=url, title=title)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(String(self.title))
        
        return b.getvalue()
