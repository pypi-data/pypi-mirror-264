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

import telectron
from telectron import raw
from .menu_button import MenuButton


class MenuButtonDefault(MenuButton):
    """Describes that no specific value for the menu button was set.
    """

    def __init__(self):
        super().__init__("default")

    async def write(self, client: "telectron.Client") -> "raw.types.BotMenuButtonDefault":
        return raw.types.BotMenuButtonDefault()
