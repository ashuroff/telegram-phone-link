import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Bot token (seniki to'g'ridan-to'g'ri yozilgan)
BOT_TOKEN = "8418928372:AAEX0Xm2oO-6ZiKwLcvxeSxbJ5xR1OESBic"

def normalize_phone(raw: str) -> str | None:
    digits = re.sub(r"\D", "", raw)

    if not digits:
        return None

    if digits.startswith("998") and len(digits) == 12:
        return f"+{digits}"

    if len(digits) == 9 and digits[0] == "9":
        return f"+998{digits}"

    if digits.startswith("0") and len(digits) == 10:
        return f"+998{digits[1:]}"

    if 10 <= len(digits) <= 15:
        return f"+{digits}"

    return None

def build_links(e164: str) -> str:
    return (
        f"📞 Raqam: `{e164}`\n\n"
        f"🔗 Links:\n"
        f"- [t.me](https://t.me/{e164.replace('+','+')})\n"
        f"- [tg://resolve](tg://resolve?phone={e164.replace('+','')})\n"
        f"- [tel]({e164})\n\n"
        "_Eslatma: Foydalanuvchi maxfiylik sozlamasiga qarab chat ochilishi mumkin yoki mumkin emas._"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Menga telefon raqam yuboring.\n"
        "Masalan: `907447180` yoki `90-744-71-80` → `+998907447180` link chiqadi.",
        parse_mode="Markdown"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    candidates = re.findall(r"[+()]?\d[\d\s().-]{7,}", text)
    if not candidates:
        await update.message.reply_text("Telefon raqam topilmadi.")
        return

    for c in candidates:
        e164 = normalize_phone(c)
        if e164:
            await update.message.reply_text(
                build_links(e164),
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(f"Bu raqamni tushunmadim: `{c}`", parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
