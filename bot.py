import os
import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get bot token from environment variable
BOT_TOKEN = ("8514085828:AAHwkWYvMBnNhpvQaZzAA8A89g5uPD0WCik")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

# Instaloader setup
loader = instaloader.Instaloader(download_pictures=False,
                                 download_videos=False,
                                 download_video_thumbnails=False,
                                 save_metadata=False)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome bhai!\n\n"
        "Instagram Profile Analyzer Bot\n\n"
        "Use:\n"
        "/analyze <username>\n\n"
        "Example:\n"
        "/analyze instagram"
    )

# /analyze command
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Username missing\n\nUse:\n/analyze <username>"
        )
        return

    username = context.args[0]

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        text = (
            f"📊 *Instagram Profile Analysis*\n\n"
            f"👤 Username: `{profile.username}`\n"
            f"📝 Name: {profile.full_name}\n"
            f"📌 Bio: {profile.biography or 'N/A'}\n\n"
            f"👥 Followers: {profile.followers}\n"
            f"➡️ Following: {profile.followees}\n"
            f"📸 Posts: {profile.mediacount}\n\n"
            f"🔒 Private: {profile.is_private}\n"
            f"✅ Verified: {profile.is_verified}"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error analyzing profile\n\nReason:\n{str(e)}"
        )

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

