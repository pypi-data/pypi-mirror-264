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

from typing import List

import telectron
from telectron import raw
from telectron import types


class ImportContacts:
    async def import_contacts(
        self: "telectron.Client",
        contacts: List["types.InputPhoneContact"]
    ):
        """Import contacts to your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            contacts (List of :obj:`~telectron.types.InputPhoneContact`):
                The contact list to be added

        Returns:
            :obj:`types.contacts.ImportedContacts`

        Example:
            .. code-block:: python

                from telectron.types import InputPhoneContact

                await app.import_contacts([
                    InputPhoneContact("+1-123-456-7890", "Foo"),
                    InputPhoneContact("+1-456-789-0123", "Bar"),
                    InputPhoneContact("+1-789-012-3456", "Baz")])
        """
        imported_contacts = await self.invoke(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
