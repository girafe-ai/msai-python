import telebot
import random

bot = telebot.TeleBot("5188887338:AAEkmGdVyFHkIw4gt_-oiksnYBJuvdl3bY0")

YesNoKeyboard = telebot.types.ReplyKeyboardMarkup(True,True)
YesNoKeyboard.row("Yes", "No")

q = "\U00002753"

words = list()

with open("words.txt", 'r') as file:
	words = file.readlines()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	reply = bot.send_message(message.chat.id, "Hey! This is a Hangman bot. Wanna play?", reply_markup=YesNoKeyboard)

	# bot.send_message(message.chat.id, "".join("\U00002753" for i in range(5)).join("A").join("\U00002753" for i in range(5)))

	bot.register_next_step_handler(reply, Handle)

def Handle(message):
	word = random.choice(words)

	reply = bot.reply_to(message, f"Here is your word: {word}. Make a guess!")

	bot.register_next_step_handler(reply, CheckLetterHandler, word)

def CheckLetterHandler(message, word):
	if (CheckLetter(word, message.text)):
		bot.send_message(message.chat.id, "Letter found!")
	else:
		bot.send_message(message.chat.id, "Letter not found!")

def CheckLetter(word, letter):
	if letter in word:
		return True
	return False

bot.infinity_polling()