import os
import telebot
import google.generativeai as genai
from gtts import gTTS

api_key = os.environ.get("GEMINI_API_KEY")
token = os.environ.get("TELEGRAM_TOKEN")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')
bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "⏳ ဇာတ်ညွှန်းရေးနေပါပြီ...")
    try:
        response = model.generate_content(f"Write a short movie recap in Burmese for: {message.text}")
        script = response.text
        bot.reply_to(message, script)
        
        bot.send_message(message.chat.id, "🎙️ အသံဖိုင် ပြောင်းနေပါပြီ...")
        tts = gTTS(text=script, lang='my')
        audio_path = "/tmp/recap_audio.mp3"
        tts.save(audio_path)
        
        with open(audio_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(audio_path)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.polling()
