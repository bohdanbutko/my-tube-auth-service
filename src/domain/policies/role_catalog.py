from src.domain.value_objects import Permission, Role


class RoleCatalog:
    _roles: dict[str, Role] = {
        "channel_owner": Role(
            name="channel_owner",
            permissions=[
                Permission(name="channel:delete", description="Delete the channel"),
                Permission(
                    name="channel:permissions:manage",
                    description="Manage channel permissions",
                ),
                Permission(name="channel:view", description="View channel data"),
                Permission(name="channel:edit", description="Edit channel details"),
                Permission(name="video:create", description="Create draft content"),
                Permission(name="video:publish", description="Publish content"),
                Permission(name="video:delete", description="Delete content"),
                Permission(
                    name="video:metadata:edit",
                    description="Edit content metadata and visibility",
                ),
                Permission(
                    name="analytics:view_revenue",
                    description="View revenue and analytics data",
                ),
                Permission(
                    name="live_stream:manage", description="Manage live streams"
                ),
                Permission(
                    name="live_chat:moderate",
                    description="Moderate or participate in live chat",
                ),
                Permission(
                    name="community_post:manage",
                    description="Create and manage community posts",
                ),
                Permission(name="ads:link", description="Link Google Ads accounts"),
            ],
        ),
        "channel_manager": Role(
            name="channel_manager",
            permissions=[
                Permission(
                    name="channel:permissions:manage",
                    description="Manage channel permissions",
                ),
                Permission(name="channel:view", description="View channel data"),
                Permission(name="channel:edit", description="Edit channel details"),
                Permission(name="video:create", description="Create draft content"),
                Permission(name="video:publish", description="Publish content"),
                Permission(name="video:delete", description="Delete content"),
                Permission(
                    name="video:metadata:edit",
                    description="Edit content metadata and visibility",
                ),
                Permission(
                    name="analytics:view_revenue",
                    description="View revenue and analytics data",
                ),
                Permission(
                    name="live_stream:manage", description="Manage live streams"
                ),
                Permission(
                    name="live_chat:moderate",
                    description="Moderate or participate in live chat",
                ),
                Permission(
                    name="community_post:manage",
                    description="Create and manage community posts",
                ),
                Permission(name="ads:link", description="Link Google Ads accounts"),
            ],
        ),
        "channel_editor": Role(
            name="channel_editor",
            permissions=[
                Permission(name="channel:view", description="View channel data"),
                Permission(name="channel:edit", description="Edit channel details"),
                Permission(name="video:create", description="Create draft content"),
                Permission(name="video:publish", description="Publish content"),
                Permission(
                    name="video:metadata:edit",
                    description="Edit content metadata and visibility",
                ),
                Permission(
                    name="analytics:view_revenue",
                    description="View revenue and analytics data",
                ),
                Permission(
                    name="live_stream:manage", description="Manage live streams"
                ),
                Permission(
                    name="live_chat:moderate",
                    description="Moderate or participate in live chat",
                ),
                Permission(
                    name="community_post:manage",
                    description="Create and manage community posts",
                ),
                Permission(name="ads:link", description="Link Google Ads accounts"),
            ],
        ),
        "channel_editor_limited": Role(
            name="channel_editor_limited",
            permissions=[
                Permission(name="channel:view", description="View channel data"),
                Permission(name="channel:edit", description="Edit channel details"),
                Permission(name="video:create", description="Create draft content"),
                Permission(name="video:publish", description="Publish content"),
                Permission(
                    name="video:metadata:edit",
                    description="Edit content metadata and visibility",
                ),
                Permission(
                    name="live_stream:manage", description="Manage live streams"
                ),
                Permission(
                    name="live_chat:moderate",
                    description="Moderate or participate in live chat",
                ),
                Permission(
                    name="community_post:manage",
                    description="Create and manage community posts",
                ),
                Permission(name="ads:link", description="Link Google Ads accounts"),
            ],
        ),
        "channel_subtitle_editor": Role(
            name="channel_subtitle_editor",
            permissions=[
                Permission(
                    name="subtitles:edit",
                    description="Add, edit, publish, and delete subtitles",
                ),
            ],
        ),
        "channel_viewer": Role(
            name="channel_viewer",
            permissions=[
                Permission(name="channel:view", description="View channel data"),
                Permission(
                    name="analytics:view_revenue",
                    description="View revenue and analytics data",
                ),
                Permission(
                    name="live_stream:view",
                    description="View stream status and settings",
                ),
            ],
        ),
        "channel_viewer_limited": Role(
            name="channel_viewer_limited",
            permissions=[
                Permission(name="channel:view", description="View channel data"),
                Permission(
                    name="live_stream:view",
                    description="View stream status and settings",
                ),
            ],
        ),
    }

    @classmethod
    def find_by_name(cls, name: str) -> Role | None:
        return cls._roles.get(name)
