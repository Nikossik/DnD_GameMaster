import telebot
import openai
from config import BOT_TOKEN, MASTER_PROMPT, OPENAI_API_KEY

bot = telebot.TeleBot(BOT_TOKEN)
user_conversations = {}

def chat_with_master(MASTER_PROMPT, user_input, conversation_history, key):
    client = openai.OpenAI(api_key=key)
    
    if len(conversation_history) == 0:
        conversation_history.append({"role": "system", "content": MASTER_PROMPT})
        
    conversation_history.append({"role": "user", "content": user_input})
    
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-3.5-turbo",
        max_tokens=300,
        temperature=0.9
    )
    
    master_response = chat_completion.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": master_response})
    
    return master_response, conversation_history

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я твой мастер DnD! Напиши /adventure, чтобы начать новую игру!")


@bot.message_handler(commands=['adventure'])
def start_adventure(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello Adventurer! What's your name?")
    
    if chat_id not in user_conversations:
        user_conversations[chat_id] = []


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id in user_conversations:
        user_input = message.text
        conversation_history = user_conversations[chat_id]

        response, conversation_history = chat_with_master(MASTER_PROMPT, user_input, conversation_history, OPENAI_API_KEY)

        user_conversations[chat_id] = conversation_history

        bot.send_message(chat_id, response)


if __name__ == '__main__':
    print('Bot is running...')
    bot.polling()