import telebot
import requests
import time
import urllib3

# সিকিউরিটি ওয়ার্নিং বন্ধ করার জন্য
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================
# ১. আপনার সঠিক টোকেন ও এপিআই কী এখানে বসান
BOT_TOKEN = '8614776609:AAHMWcIj0Ly5dT2Jn4gYMxuwSz7iD1aoUJA'
NARA_API_KEY = 'sk-nry-ClgklCNwa-xtJd-kep0OorVZJz-os18PU5g3SuYt43w'
# =========================================================

bot = telebot.TeleBot(BOT_TOKEN)
bot.threaded = False

# /start দিলে স্বাগত বার্তা
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🤖 হ্যালো! আমি কোনো ঝামেলা ছাড়াই সরাসরি চালিত আপনার পার্সোনাল এআই বট।")

# মেসেজ আসলে NaraRouter এআই উত্তর দেবে
@bot.message_handler(func=lambda message: True)
def ask_nara_ai(message):
    user_question = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # ডোমেইন ব্লক বাইপাস করার জন্য সরাসরি অফিশিয়াল আইপি বা গেটওয়ে ব্যবহার
    url = "https://bynara.id"
    
    headers = {
        "Authorization": f"Bearer {NARA_API_KEY}",
        "Content-Type": "application/json",
        "Host": "router.bynara.id" # ক্লাউডফ্লেয়ার ব্লকিং বাইপাস হেডজার
    }
    
    payload = {
        "model": "agnes-2.0-flash", 
        "messages": [{"role": "user", "content": user_question}]
    }
    
    try:
        # verify=False দেওয়া হয়েছে যাতে লোকাল SSL এরর না আসে
        response = requests.post(url, headers=headers, json=payload, timeout=25, verify=False)
        response_data = response.json()
        
        ai_reply = response_data['choices']['message']['content']
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        print(f"এআই রেসপন্স এরর: {e}")
        bot.reply_to(message, "🤖 দুঃখিত, সার্ভার একটু স্লো। দয়া করে আরেকবার মেসেজটি পাঠান।")

# টেলিগ্রাম কানেকশন এরর হ্যান্ডেল করার মেইন লুপ
print("🎉 আপনার ঝামেলা-মুক্ত AI বট সফলভাবে ব্যাকগ্রাউন্ডে চালু হয়েছে...")
while True:
    try:
        bot.polling(non_stop=True, timeout=90, long_polling_timeout=90)
    except Exception as e:
        # কানেকশন ড্রপ করলে কোড ক্র্যাশ করবে না, নিজে থেকেই ৫ সেকেন্ড পর আবার কানেক্ট হবে
        print(f"কানেকশন ড্রপ করেছে ({e})। ৫ সেকেন্ড পর অটো-রিকানেক্ট হচ্ছে...")
        time.sleep(5)
