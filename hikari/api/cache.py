# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright © Nekoka.tt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Core interface for a cache implementation."""
from __future__ import annotations

__all__: typing.Final[typing.List[str]] = ["ICacheView", "ICacheComponent"]

import abc
import typing

from hikari.api import component
from hikari.api import rest
from hikari.utilities import iterators

if typing.TYPE_CHECKING:
    from hikari.models import channels
    from hikari.models import guilds
    from hikari.models import users
    from hikari.utilities import snowflake


_T = typing.TypeVar("_T", bound="snowflake.Unique")


class ICacheView(typing.Mapping["snowflake.Snowflake", _T], abc.ABC):
    """Interface describing an immutable snapshot view of part of a cache."""

    @abc.abstractmethod
    def get_item_at(self, index: int) -> _T:
        ...

    @abc.abstractmethod
    def iterator(self) -> iterators.LazyIterator[_T]:
        ...


class ICacheComponent(component.IComponent, abc.ABC):
    """Interface describing the operations a cache component should provide.

    This will be used by the gateway and HTTP API to cache specific types of
    objects that the application should attempt to remember for later, depending
    on how this is implemented. The requirement for this stems from the
    assumption by Discord that bot applications will maintain some form of
    "memory" of the events that occur.

    The implementation may choose to use a simple in-memory collection of
    objects, or may decide to use a distributed system such as a Redis cache
    for cross-process bots.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def app(self) -> rest.IRESTApp:
        """The app this cache is bound by."""

    @abc.abstractmethod
    def clear_dm_channels(self) -> ICacheView[channels.DMChannel]:
        """Remove all the DM channel objects from the cache.

        Returns
        -------
        ICacheView[hikari.models.channels.DMChannel]
            The cache view of the DM channel objects that were removed from the
            cache.
        """

    @abc.abstractmethod
    def delete_dm_channel(self, user_id: snowflake.Snowflake) -> typing.Optional[channels.DMChannel]:
        """Remove a DM channel object from the cache.

        Parameters
        ----------
        user_id : hikari.utilities.snowflake.Snowflake
            The ID of the user that the DM channel to remove from the cache is
            with.

        Returns
        -------
        hikari.models.channels.DMChannel or builtins.None
            The object of the DM channel that was removed from the cache if
            found, else `builtins.None`
        """

    @abc.abstractmethod
    def get_dm_channel(self, user_id: snowflake.Snowflake) -> typing.Optional[channels.DMChannel]:
        """Get a DM channel object from the cache.

        Parameters
        ----------
        user_id : hikari.utilities.snowflake.Snowflake
            The ID of the user that the DM channel to get from the cache is with.

        Returns
        -------
        hikari.models.channels.DMChannel or builtins.None
            The object of the DM channel that was found in the cache or
            `builtins.None`.
        """

    @abc.abstractmethod
    def get_dm_channel_view(self) -> ICacheView[channels.DMChannel]:
        """Get a view of the DM channel objects in the cache.

        Returns
        -------
        ICacheView[hikari.models.channels.DMChannel]
            The view of the DM channel objects in the cache.
        """

    @abc.abstractmethod
    def set_dm_channel(self, channel: channels.DMChannel) -> None:
        """Add a DM channel object to the cache.

        Parameters
        ----------
        channel : hikari.models.channels.DMChannel
            The object of the DM channel to add to the cache.
        """

    @abc.abstractmethod
    def update_dm_channel(
        self, channel: channels.DMChannel
    ) -> typing.Tuple[typing.Optional[channels.DMChannel], typing.Optional[channels.DMChannel]]:
        """Update a DM Channel object in the cache.

        Parameters
        ----------
        channel : hikari.models.channels.DMChannel
            The object of the channel to update in the cache.

        Returns
        -------
        typing.Tuple[hikari.models.channels.DMChannel or builtins.None, hikari.models.channels.DMChannel or builtins.None]
            A tuple of the old cached DM channel if found (else `builtins.None`)
            and the new cached DM channel if it could be cached (else
            `builtins.None`).
        """

    @abc.abstractmethod
    def clear_guilds(self) -> ICacheView[guilds.GatewayGuild]:
        """Remove all the guild objects from the cache.

        Returns
        -------
        ICacheView[hikari.models.guilds.GatewayGuild]
            The cache view of the guild objects that were removed from the cache.
        """

    @abc.abstractmethod
    def delete_guild(self, guild_id: snowflake.Snowflake, /) -> typing.Optional[guilds.GatewayGuild]:
        """Remove a guild object from the cache.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild to remove from the cache.

        Returns
        -------
        hikari.models.guilds.GatewayGuild or builtins.None
            The object of the guild that was removed from the cache, will be
            `builtins.None` if not found.
        """

    @abc.abstractmethod
    def get_guild(self, guild_id: snowflake.Snowflake, /) -> typing.Optional[guilds.GatewayGuild]:
        """Get a guild object from the cache.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild to get from the cache.

        Returns
        -------
        hikari.models.guilds.GatewayGuild or builtins.None
            The object of the guild if found, else None.
        """

    @abc.abstractmethod
    def get_guilds_view(self) -> ICacheView[guilds.GatewayGuild]:
        """Get a view of the guild objects in the cache.

        Returns
        -------
        ICacheView[hikari.models.guilds.GatewayGuild]
            A view of the guild objects found in the cache.
        """

    @abc.abstractmethod
    def set_guild_availability(self, guild_id: snowflake.Snowflake, is_available: bool) -> None:
        """Set whether a cached guild is available or not.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild to set the availability for.
        is_available : builtins.bool
            The availability to set for the guild.
        """

    @abc.abstractmethod
    def update_guild(
        self, guild: guilds.GatewayGuild, /
    ) -> typing.Tuple[typing.Optional[guilds.GatewayGuild], typing.Optional[guilds.GatewayGuild]]:
        """Update a guild in the cache.

        Parameters
        ----------
        guild : hikari.models.guilds.GatewayGuild
            The object of the guild to update in the cache.

        Returns
        -------
        typing.Tuple[hikari.models.guilds.GatewayGuild or builtins.None, hikari.models.guilds.GatewayGuild or builtins.None]
            A tuple of the old cached guild object if found (else `builtins.None`)
            and the object of the guild that was added to the cache if it could
            be added (else `builtins.None`).
        """

    @abc.abstractmethod
    def delete_me(self) -> typing.Optional[users.OwnUser]:
        """Remove the own user object from the cache.

        Returns
        -------
        hikari.models.users.OwnUser or builtins.None
            The own user object that was removed from the cache if found,
            else `builtins.None`.
        """

    @abc.abstractmethod
    def get_me(self) -> typing.Optional[users.OwnUser]:
        """Get the own user object from the cache.

        Returns
        -------
        hikari.models.users.OwnUser or builtins.None
            The own user object that was found in the cache, else `builtins.None`.
        """

    @abc.abstractmethod
    def set_me(self, user: users.OwnUser, /):
        """Set the own user object in the cache.

        Parameters
        ----------
        user : hikari.models.users.OwnUser
            The own user object to set in the cache.
        """

    @abc.abstractmethod
    def update_me(
        self, user: users.OwnUser, /
    ) -> typing.Tuple[typing.Optional[users.OwnUser], typing.Optional[users.OwnUser]]:
        """The own user object to update in the cache.

        Parameters
        ----------
        user : hikari.models.users.OwnUser
            The own user object to update in the cache.

        Returns
        -------
        typing.Tuple[hikari.models.users.OwnUser or builtins.None, hikari.models.users.OwnUser or builtins.None]
            A tuple of the old cached own user object if found (else
            `builtins.None`) and the new cached own user object if it could be
            cached else `builtins.None`.
        """

    @abc.abstractmethod
    def clear_members(self, guild_id: snowflake.Snowflake, /) -> ICacheView[guilds.Member]:
        """Remove the members for a specific guild from the cache.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild to remove cached members for.

        Returns
        -------
        ICacheView[hikari.models.guilds.Member]
            The view of the member objects that were removed from the cache.
        """

    @abc.abstractmethod
    def delete_member(
        self, guild_id: snowflake.Snowflake, user_id: snowflake.Snowflake, /
    ) -> typing.Optional[guilds.Member]:
        """Remove a member object from the cache.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild to remove a member from the cache for.
        user_id : hikari.utilities.snowflake.Snowflake
            The ID of the user to remove a member from the cache for.

        Returns
        -------
        hikari.models.guilds.Member or builtins.None
            The object of the member that was removed from the cache if found,
            else `builtins.None`.
        """

    @abc.abstractmethod
    def get_member(
        self, guild_id: snowflake.Snowflake, user_id: snowflake.Snowflake, /
    ) -> typing.Optional[guilds.Member]:
        """Get a member object from the cache.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
        user_id : hikari.utilities.snowflake.Snowflake

        Returns
        -------
        hikari.models.guilds.Member or builtins.None
            The object of the member found in the cache, else `builtins.None`.
        """

    @abc.abstractmethod  # TODO: will be empty if none found.
    def get_members_view(self, guild_id: snowflake.Snowflake, /) -> ICacheView[guilds.Member]:
        """Get a view of the members cached for a specific guild.

        Parameters
        ----------
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild to get the cached member view for.

        Returns
        -------
        ICacheView[hikari.models.guilds.Member]
            The view of the members cached for the specified guild.
        """

    @abc.abstractmethod
    def set_member(self, member: guilds.Member, /) -> None:
        """Add a member object to the cache.

        Parameters
        ----------
        member : hikari.models.guilds.Member
            The object of the member to add to the cache.
        """

    @abc.abstractmethod
    def update_member(
        self, member: guilds.Member
    ) -> typing.Tuple[typing.Optional[guilds.Member], typing.Optional[guilds.Member]]:
        """Update a member in the cache.

        Parameters
        ----------
        member : hikari.models.guilds.Member
            The object of the member to update in the cache.

        Returns
        -------
        typing.Tuple[hikari.models.guilds.Member or builtins.None, hikari.models.guilds.Member or builtins.None]
            A tuple of the old cached member object if found (else `builtins.None`)
            and the new cached member object if it could be cached (else
            `builtins.None`)
        """

    @abc.abstractmethod
    def clear_users(self) -> ICacheView[users.User]:
        """Clear the user objects from the cache.

        Returns
        -------
        ICacheView[hikari.models.users.User]
            The view of the user objects that were removed from the cache.
        """

    @abc.abstractmethod
    def delete_user(self, user_id: snowflake.Snowflake) -> typing.Optional[users.User]:
        """Remove a user object from the cache.

        Parameters
        ----------
        user_id : hikari.utilities.snowflake.Snowflake
            The ID of the user to remove from the cache.

        Returns
        -------
        hikari.models.users.User or builtins.None
            The object of the user that was removed from the cache if found,
            else `builtins.None`.
        """

    @abc.abstractmethod
    def get_user(self, user_id: snowflake.Snowflake) -> typing.Optional[users.User]:
        """Get a user object from the cache.

        Parameters
        ----------
        user_id : hikari.utilities.snowflake.Snowflake
            The ID of the user to get from the cache.

        Returns
        -------
        hikari.models.users.User or builtins.None
            The object of the user that was found in the cache else `builtins.None`.
        """

    @abc.abstractmethod
    def get_users_view(self) -> ICacheView[users.User]:
        """Get a view of the user objects in the cache.

        Returns
        -------
        ICacheView[hikari.models.users.User]
            The view of the users found in the cache.
        """

    @abc.abstractmethod
    def set_user(self, user: users.User) -> None:
        """Add a user object to the cache.

        Parameters
        ----------
        user : hikari.models.users.User
            The object of the user to add to the cache.
        """

    @abc.abstractmethod
    def update_user(self, user: users.User) -> typing.Tuple[typing.Optional[users.User], typing.Optional[users.User]]:
        """Update a user object in the cache.

        Parameters
        ----------
        user : hikari.models.users.User
            The object of the user to update in the cache.

        Returns
        -------
        typing.Tuple[hikari.models.users.User or builtins.None, hikari.models.users.User or builtins.None]
            A tuple of the old cached user if found (else `builtins.None`) and
            the newly cached user if it could be cached (else `builtins.None`).
        """
