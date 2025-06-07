from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_contacts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚨 Help Me")],
        [KeyboardButton("📍 Share Location", request_location=True)],
        [KeyboardButton("📇 Emergency Contacts")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Hello! I’m Raksha AI+, your safety assistant.\n\nChoose an option below:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚨 Help Me":
        await update.message.reply_text("⚠️ SOS Triggered!\n\nPlease share your location now.")
    elif text == "📍 Share Location":
        await update.message.reply_text("📍 Please use the button to share your live location.")
    elif text == "📇 Emergency Contacts":
        await update.message.reply_text(
            "Manage your emergency contacts with these commands:\n"
            "/addcontact <number> - Add a contact\n"
            "/viewcontacts - View saved contacts\n"
            "/deletecontact <number> - Delete a contact"
        )
    else:
        await update.message.reply_text("❓ Sorry, I didn’t understand that command.")

async def add_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not context.args:
        await update.message.reply_text(
            "Please send the command followed by the contact number.\nExample: /addcontact 9876543210"
        )
        return
    contact = context.args[0]
    if user_id not in user_contacts:
        user_contacts[user_id] = []
    user_contacts[user_id].append(contact)
    await update.message.reply_text(f"Contact {contact} added successfully.")

async def view_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    contacts = user_contacts.get(user_id, [])
    if not contacts:
        await update.message.reply_text("You have no saved emergency contacts.")
        return
    msg = "Your emergency contacts:\n" + "\n".join(f"{i+1}. {c}" for i, c in enumerate(contacts))
    await update.message.reply_text(msg)

async def delete_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not context.args:
        await update.message.reply_text(
            "Please send the command followed by the contact number to delete.\nExample: /deletecontact 9876543210"
        )
        return
    contact = context.args[0]
    contacts = user_contacts.get(user_id, [])
    if contact in contacts:
        contacts.remove(contact)
        await update.message.reply_text(f"Contact {contact} deleted successfully.")
    else:
        await update.message.reply_text("Contact not found in your list.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addcontact", add_contact))
app.add_handler(CommandHandler("viewcontacts", view_contacts))
app.add_handler(CommandHandler("deletecontact", delete_contact))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
