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


class SetSecureValueErrors(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``170``
        - ID: ``90C894B5``

    Parameters:
        id (:obj:`InputUser <telectron.raw.base.InputUser>`):
            N/A

        errors (List of :obj:`SecureValueError <telectron.raw.base.SecureValueError>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["id", "errors"]

    ID = 0x90c894b5
    QUALNAME = "functions.users.SetSecureValueErrors"

    def __init__(self, *, id: "raw.base.InputUser", errors: List["raw.base.SecureValueError"]) -> None:
        self.id = id  # InputUser
        self.errors = errors  # Vector<SecureValueError>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetSecureValueErrors":
        # No flags
        
        id = TLObject.read(b)
        
        errors = TLObject.read(b)
        
        return SetSecureValueErrors(id=id, errors=errors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        b.write(Vector(self.errors))
        
        return b.getvalue()
