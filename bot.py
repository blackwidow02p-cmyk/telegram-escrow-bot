import telebot

TOKEN = 8745759872:AAFVEbkPjI-E-ljbOfKVUPlc0OmX5hlYbU0
OWNER_WALLET = 0x19961E4210fF1A439DA8107C9a914F3EAc580c76

bot = telebot.TeleBot(TOKEN)

deals = {}

# START DEAL
@bot.message_handler(commands=['deal'])
def start_deal(message):
    deals[message.chat.id] = {
        "buyer": None,
        "seller": None,
        "paid": False,
        "confirmed": False
    }

    bot.send_message(message.chat.id,
                     "📌 Send BUYER username (@username)")

# SET BUYER
@bot.message_handler(func=lambda m: m.chat.id in deals and deals[m.chat.id]["buyer"] is None)
def set_buyer(message):
    deals[message.chat.id]["buyer"] = message.text
    bot.send_message(message.chat.id,
                     "📌 Send SELLER username (@username)")

# SET SELLER
@bot.message_handler(func=lambda m: m.chat.id in deals and deals[m.chat.id]["seller"] is None)
def set_seller(message):
    deals[message.chat.id]["seller"] = message.text

    bot.send_message(message.chat.id,
                     f"💰 Buyer send payment to OWNER wallet:\n{OWNER_WALLET}\n\n"
                     "After payment type: PAID")

# BUYER PAID
@bot.message_handler(func=lambda m: m.text and m.text.lower() == "paid")
def mark_paid(message):
    if message.chat.id not in deals:
        return

    deals[message.chat.id]["paid"] = True

    bot.send_message(message.chat.id,
                     "✅ Payment marked\nSeller send product\n\n"
                     "Buyer type CONFIRM after receiving")

# BUYER CONFIRM
@bot.message_handler(func=lambda m: m.text and m.text.lower() == "confirm")
def confirm_received(message):
    if message.chat.id not in deals:
        return

    deals[message.chat.id]["confirmed"] = True

    bot.send_message(message.chat.id,
                     "🔓 Funds ready to release\nOwner type RELEASE")

# OWNER RELEASE
@bot.message_handler(func=lambda m: m.text and m.text.lower() == "release")
def release_funds(message):
    if message.chat.id not in deals:
        return

    bot.send_message(message.chat.id,
                     "🎉 Funds Released to Seller\nDeal Completed")

bot.infinity_polling()
