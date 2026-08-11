import telebot
import requests
import time
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# রেন্ডার ড্যাশবোর্ড থেকে অটোমেটিক সিক্রেট কী ও টোকেন রিড করার সিস্টেম
BOT_TOKEN = os.environ.get('BOT_TOKEN')
NARA_API_KEY = os.environ.get('NARA_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
bot.threaded = False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🤖 হ্যালো! আমি ২৪ ঘণ্টা সচল থাকা আপনার পার্সোনাল এআই বট।")

@bot.message_handler(func=lambda message: True)
def ask_nara_ai(message):
    user_question = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # এপিআই এন্ডপয়েন্ট গেটওয়ে সঠিক করা হয়েছে
    url = "https://bynara.id"
    
    headers = {
        "Authorization": f"Bearer {NARA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "agnes-2.0-flash", 
        "messages": [{"role": "user", "content": user_question}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        response_data = response.json()
        ai_reply = response_data['choices']['message']['content']
        bot.reply_to(message, ai_reply)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "🤖 দুঃখিত, উত্তর তৈরি করতে সমস্যা হচ্ছে। দয়া করে আবার চেষ্টা করুন।")

print("বট সচল আছে...")
while True:
    try:
        bot.polling(non_stop=True, timeout=90, long_polling_timeout=90)
    except Exception:
        time.sleep(5)
