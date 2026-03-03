from telegram import InlineKeyboardButton, helpers
from typing import Dict, List
from bot.utils.language import get_msg_string

HELP_MODULES: Dict[str, dict] = {}


def register_module_help(module_name: str, help_key: str, sections: dict | None = None):
    """
    Register a module in the help menu.
    sections: optional dict of {label: help_key} for submenu buttons.
    Example:
        register_module_help("Moderation", "moderation.help", sections={
            "Bans":  "moderation.ban.help",
            "Mutes": "moderation.mute.help",
            "Warns": "moderation.warn.help",
        })
    """
    HELP_MODULES[module_name] = {"key": help_key, "sections": sections or {}}


def get_help_keyboard(back_text: str = "« Back") -> List[List[InlineKeyboardButton]]:
    buttons = [
        InlineKeyboardButton(name, callback_data=f"help_mod_{name}")
        for name in sorted(HELP_MODULES.keys())
    ]
    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton(back_text, callback_data="start_main")])
    return keyboard


def get_sections_keyboard(
    module_name: str, back_text: str
) -> List[List[InlineKeyboardButton]] | None:
    module = HELP_MODULES.get(module_name)
    if not module or not module["sections"]:
        return None
    buttons = [
        InlineKeyboardButton(label, callback_data=f"help_sec_{label}")
        for label in module["sections"]
    ]
    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton(back_text, callback_data="help_main")])
    return keyboard


def get_module_help(module_name: str) -> str | None:
    module = HELP_MODULES.get(module_name)
    return module["key"] if module else None


def get_section_help(label: str) -> str | None:
    for module in HELP_MODULES.values():
        if label in module["sections"]:
            return module["sections"][label]
    return None


def get_section_parent(label: str) -> str | None:
    for name, module in HELP_MODULES.items():
        if label in module["sections"]:
            return name
    return None


def get_string_helper(update):
    def s(key, **kwargs):
        return get_msg_string(update, key, **kwargs)

    def e(value):
        return helpers.escape_markdown(str(value), version=2)

    return s, e


def e_list(items: list) -> str:
    return ", ".join(f"`{helpers.escape_markdown(i, version=2)}`" for i in items)
