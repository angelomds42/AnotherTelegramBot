from bot.utils.help import register_module_help

register_module_help(
    "Moderation",
    "moderation.help",
    sections={
        "Bans": "moderation.ban.help",
        "Mutes": "moderation.mute.help",
        "Warns": "moderation.warn.help",
    },
)
