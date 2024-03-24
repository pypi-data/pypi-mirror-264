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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from telectron import raw
from telectron.raw.core import TLObject

ChannelAdminLogEventAction = Union[raw.types.ChannelAdminLogEventActionChangeAbout, raw.types.ChannelAdminLogEventActionChangeAvailableReactions, raw.types.ChannelAdminLogEventActionChangeEmojiStatus, raw.types.ChannelAdminLogEventActionChangeHistoryTTL, raw.types.ChannelAdminLogEventActionChangeLinkedChat, raw.types.ChannelAdminLogEventActionChangeLocation, raw.types.ChannelAdminLogEventActionChangePeerColor, raw.types.ChannelAdminLogEventActionChangePhoto, raw.types.ChannelAdminLogEventActionChangeProfilePeerColor, raw.types.ChannelAdminLogEventActionChangeStickerSet, raw.types.ChannelAdminLogEventActionChangeTitle, raw.types.ChannelAdminLogEventActionChangeUsername, raw.types.ChannelAdminLogEventActionChangeUsernames, raw.types.ChannelAdminLogEventActionChangeWallpaper, raw.types.ChannelAdminLogEventActionCreateTopic, raw.types.ChannelAdminLogEventActionDefaultBannedRights, raw.types.ChannelAdminLogEventActionDeleteMessage, raw.types.ChannelAdminLogEventActionDeleteTopic, raw.types.ChannelAdminLogEventActionDiscardGroupCall, raw.types.ChannelAdminLogEventActionEditMessage, raw.types.ChannelAdminLogEventActionEditTopic, raw.types.ChannelAdminLogEventActionExportedInviteDelete, raw.types.ChannelAdminLogEventActionExportedInviteEdit, raw.types.ChannelAdminLogEventActionExportedInviteRevoke, raw.types.ChannelAdminLogEventActionParticipantInvite, raw.types.ChannelAdminLogEventActionParticipantJoin, raw.types.ChannelAdminLogEventActionParticipantJoinByInvite, raw.types.ChannelAdminLogEventActionParticipantJoinByRequest, raw.types.ChannelAdminLogEventActionParticipantLeave, raw.types.ChannelAdminLogEventActionParticipantMute, raw.types.ChannelAdminLogEventActionParticipantToggleAdmin, raw.types.ChannelAdminLogEventActionParticipantToggleBan, raw.types.ChannelAdminLogEventActionParticipantUnmute, raw.types.ChannelAdminLogEventActionParticipantVolume, raw.types.ChannelAdminLogEventActionPinTopic, raw.types.ChannelAdminLogEventActionSendMessage, raw.types.ChannelAdminLogEventActionStartGroupCall, raw.types.ChannelAdminLogEventActionStopPoll, raw.types.ChannelAdminLogEventActionToggleAntiSpam, raw.types.ChannelAdminLogEventActionToggleForum, raw.types.ChannelAdminLogEventActionToggleGroupCallSetting, raw.types.ChannelAdminLogEventActionToggleInvites, raw.types.ChannelAdminLogEventActionToggleNoForwards, raw.types.ChannelAdminLogEventActionTogglePreHistoryHidden, raw.types.ChannelAdminLogEventActionToggleSignatures, raw.types.ChannelAdminLogEventActionToggleSlowMode, raw.types.ChannelAdminLogEventActionUpdatePinned]


# noinspection PyRedeclaration
class ChannelAdminLogEventAction:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 47 constructors available.

        .. currentmodule:: telectron.raw.types

        .. autosummary::
            :nosignatures:

            ChannelAdminLogEventActionChangeAbout
            ChannelAdminLogEventActionChangeAvailableReactions
            ChannelAdminLogEventActionChangeEmojiStatus
            ChannelAdminLogEventActionChangeHistoryTTL
            ChannelAdminLogEventActionChangeLinkedChat
            ChannelAdminLogEventActionChangeLocation
            ChannelAdminLogEventActionChangePeerColor
            ChannelAdminLogEventActionChangePhoto
            ChannelAdminLogEventActionChangeProfilePeerColor
            ChannelAdminLogEventActionChangeStickerSet
            ChannelAdminLogEventActionChangeTitle
            ChannelAdminLogEventActionChangeUsername
            ChannelAdminLogEventActionChangeUsernames
            ChannelAdminLogEventActionChangeWallpaper
            ChannelAdminLogEventActionCreateTopic
            ChannelAdminLogEventActionDefaultBannedRights
            ChannelAdminLogEventActionDeleteMessage
            ChannelAdminLogEventActionDeleteTopic
            ChannelAdminLogEventActionDiscardGroupCall
            ChannelAdminLogEventActionEditMessage
            ChannelAdminLogEventActionEditTopic
            ChannelAdminLogEventActionExportedInviteDelete
            ChannelAdminLogEventActionExportedInviteEdit
            ChannelAdminLogEventActionExportedInviteRevoke
            ChannelAdminLogEventActionParticipantInvite
            ChannelAdminLogEventActionParticipantJoin
            ChannelAdminLogEventActionParticipantJoinByInvite
            ChannelAdminLogEventActionParticipantJoinByRequest
            ChannelAdminLogEventActionParticipantLeave
            ChannelAdminLogEventActionParticipantMute
            ChannelAdminLogEventActionParticipantToggleAdmin
            ChannelAdminLogEventActionParticipantToggleBan
            ChannelAdminLogEventActionParticipantUnmute
            ChannelAdminLogEventActionParticipantVolume
            ChannelAdminLogEventActionPinTopic
            ChannelAdminLogEventActionSendMessage
            ChannelAdminLogEventActionStartGroupCall
            ChannelAdminLogEventActionStopPoll
            ChannelAdminLogEventActionToggleAntiSpam
            ChannelAdminLogEventActionToggleForum
            ChannelAdminLogEventActionToggleGroupCallSetting
            ChannelAdminLogEventActionToggleInvites
            ChannelAdminLogEventActionToggleNoForwards
            ChannelAdminLogEventActionTogglePreHistoryHidden
            ChannelAdminLogEventActionToggleSignatures
            ChannelAdminLogEventActionToggleSlowMode
            ChannelAdminLogEventActionUpdatePinned
    """

    QUALNAME = "telectron.raw.base.ChannelAdminLogEventAction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.telectron.org/telegram/base/channel-admin-log-event-action")
