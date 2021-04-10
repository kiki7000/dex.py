class Permissions:
    """The permissions class

    In default, Everything except `on_error` is enabled

    Attributes
    ----------
    ready_event_handle: :class:`bool`
        If enabled, the extension can be runned in on_ready event

        .. note::
            If this is enabled this extension can use `on_ready`.

    message_event_handle: :class:`bool`
        If enabled, the extension can be runned in on_message event

        .. note::
            If this is enabled this extension can use `on_typing`, `on_message`, `on_message_delete`, `on_message_edit`.

    react_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in message reacts

        .. note::
            If this is enabled this extension can use `on_reaction_add`, `on_reaction_remove`, `on_reaction_clear`, `on_reaction_clear_emoji`.

    channel_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in channel

        .. note::
            If this is enabled this extension can use `on_guild_channel_delete`, `on_guild_channel_create`, `on_guild_channel_update`, `on_guild_channel_pins_update`, `on_webhooks_update`, `on_invite_create`, `on_invite_delete`.

    guild_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in guild

        .. note::
            If this is enabled this extension can use `on_guild_integrations_update`, `on_guild_join`, `on_guild_remove`, `on_guild_update`, `on_guild_emojis_update`, `on_guild_available`, `on_guild_unavailable`, `on_member_ban`, `on_member_unban`.

    user_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in users (guild members)

        .. note::
            If this is enabled this extension can use `on_member_join`, `on_member_remove`, `on_member_update`, `on_user_update`, `on_voice_state_update`.

    role_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in roles

        .. note::
            If this is enabled this extension can use `on_guild_role_create`, `on_guild_role_delete`, `on_guild_role_updatee`.

    extension_handle: :class:`bool`
        If enabled, the extension can control the extensions

        .. note::
            If this is enabled this extension can use `on_ready`.

    shard_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in shard

        .. note::
            If this is enabled this extension can use `on_shard_connect`, `on_shard_disconnect`, `on_shard_ready`, `on_shard_resumed`.

    socket_event_handle: :class:`bool`
        If enabled, the extension can be runned in events related in socket

        .. note::
            If this is enabled this extension can use `on_socket_raw_receive`, `on_socket_raw_send`.

    error_handle: :class:`bool`
        If enabled, the extension can be runned in events related in bot errors (The extension error event does not require permissions)

        .. note::
            If this is enabled this extension can use `on_error`.
    """

    def __init__(self, **kwargs):
        self.ready_event_handle: bool = kwargs.pop('ready_event_handle', True)
        self.message_event_handle: bool = kwargs.pop('message_event_handle', True)
        self.react_event_handle: bool = kwargs.pop('react_event_handle', True)
        self.channel_event_handle: bool = kwargs.pop('channel_event_handle', True)
        self.user_event_handle: bool = kwargs.pop('user_event_handle', True)
        self.guild_event_handle: bool = kwargs.pop('guild_event_handle', True)
        self.role_event_handle: bool = kwargs.pop('role_event_handle', True)
        self.extension_handle: bool = kwargs.pop('extension_handle', True)
        self.shard_event_handle: bool = kwargs.pop('shard_event_handle', True)
        self.socket_event_handle: bool = kwargs.pop('socket_event_handle', True)
        self.error_handle: bool = kwargs.pop('error_handle', False)
