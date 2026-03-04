from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.help import get_string_helper, register_module_help
from bot.utils.message import reply, edit

import time

from bot.utils.user import resolve_target


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s, e = get_string_helper(update)

    before = time.time()
    message = await reply(update, f"Pinging\\!")

    after = time.time()
    latency = int((after - before) * 1000)
    await edit(message, f"Pong\\! `{e(latency)}ms`")


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_dice(emoji="🎲")


async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s, e = get_string_helper(update)

    if not update.message.reply_to_message and not context.args:
        return await reply(
            update,
            s(
                "misc.id.self",
                user_id=e(update.effective_user.id),
                chat_id=e(update.effective_chat.id),
            ),
        )

    user_id, display_name = await resolve_target(update, context)

    if not user_id:
        return await reply(update, s("misc.id.not_found"))

    await reply(
        update,
        s("misc.id.user", display_name=e(display_name), user_id=e(user_id)),
    )


def __init_module__(application):
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("id", id))
    register_module_help("Misc", "misc.help")
