import os
import telebot
from google import genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client()

conversations = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
    "Hello! I am your AI assistant powered by Gemini. Ask me anything!")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_id = message.chat.id
    user_text = message.text
    prev_id = conversations.get(user_id)
    
    bot.send_message(user_id, "Thinking...")
    
    interaction = client.interactions.create(
        model="gemini-2.5-flash-lite",
        input=user_text,
        previous_interaction_id=prev_id
    )
    
    reply = interaction.output_text
    conversations[user_id] = interaction.id
    bot.send_message(user_id, reply)

print("Bot is running...")
bot.infinity_polling()
