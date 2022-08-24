import telebot
import random

class Hangman:
	def __init__(self):
		self.bot = telebot.TeleBot("5188887338:AAEkmGdVyFHkIw4gt_-oiksnYBJuvdl3bY0")

		self.YesNoKeyboard = telebot.types.ReplyKeyboardMarkup(True,True)
		self.YesNoKeyboard.row("Yes", "No")

		self.q = "\U00002753"

		with open("words.txt", 'r') as file:
			self.words = file.readlines()

		@self.bot.message_handler(commands=['start', 'help'])
		def Welcome(message):
			reply = self.bot.send_message(message.chat.id, "Hey! This is a Hangman bot. Wanna play?", reply_markup=self.YesNoKeyboard)

			# bot.send_message(message.chat.id, "".join("\U00002753" for i in range(5)).join("A").join("\U00002753" for i in range(5)))

			self.bot.register_next_step_handler(reply, self.Handle)

	def Handle(self, message):
		word = random.choice(self.words)
		
		reply = self.bot.reply_to(message, f"Here is your word: {word}. Make a guess!")

		self.bot.register_next_step_handler(reply, self.CheckLetterHandler, word)

	def CheckLetterHandler(self, message, word):
		if (self.CheckLetter(word, message.text)):
			self.bot.send_message(message.chat.id, "Letter found!")
		else:
			self.bot.send_message(message.chat.id, "Letter not found!")

	def CheckLetter(self, word, letter):
		if letter in word:
			return True
		return False

	def Run(self):
		self.bot.infinity_polling()

hangman = Hangman()
hangman.Run()