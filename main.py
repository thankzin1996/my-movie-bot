import os
import telebot
import google.generativeai as genai

# Secrets ထဲက Key တွေကို ခေါ်ယူခြင်း
api_key = os.environ.get("GEMINI_API_KEY")
token = os.environ.get("TELEGRAM_TOKEN")

# API ချိတ်ဆက်မှုကို စစ်ဆေးခြင်း
if not api_key or not token:
    print("Error: Secrets ထဲတွင် Key များ မရှိပါ။ ကျေးဇူးပြု၍ စစ်ဆေးပါ။")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "Bot အဆင်သင့်ဖြစ်ပါပြီ! ရုပ်ရှင်နာမည် တစ်ခုခု ရိုက်ပို့ပေးပါ။")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            bot.reply_to(message, "ဇာတ်ညွှန်းရေးနေပါပြီ...")
            response = model.generate_content(f"Write a movie recap in Burmese for: {message.text}")
            bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.polling(none_stop=True)
  
