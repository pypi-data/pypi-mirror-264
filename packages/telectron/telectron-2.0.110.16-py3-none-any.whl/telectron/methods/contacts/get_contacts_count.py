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


class GetContactsCount:
    async def get_contacts_count(
        self: "telectron.Client"
    ) -> int:
        """Get the total count of contacts from your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``int``: On success, the contacts count is returned.

        Example:
            .. code-block:: python

                count = await app.get_contacts_count()
                print(count)
        """

        return len((await self.invoke(raw.functions.contacts.GetContacts(hash=0))).contacts)
