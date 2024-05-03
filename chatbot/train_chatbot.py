import os
import csv
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


def train():
    bot = ChatBot('Bot',
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                  'chatterbot.logic.BestMatch'],
                  database_uri='sqlite:///database.db')

    # Create corpus training and train from .yml files
    corpus_trainer = ChatterBotCorpusTrainer(bot)
    corpus_trainer.train("chatbot/chat_data")

    # Create list trainer
    list_trainer = ListTrainer(bot)

    # Read human_chat.txt
    human_chat = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "chat_data", "human_chat.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if 'Human 1: ' in line:
                human_chat.append(line.split('Human 1: ')[-1].replace('\n', ''))
            elif 'Human 2: ' in line:
                human_chat.append(line.split('Human 2: ')[-1].replace('\n', ''))
    # Train from human_chat.txt
    list_trainer.train(human_chat)

    # Read conversation.csv
    conversation = []
    file_path = os.path.join(script_dir, "chat_data", "conversation.csv")
    with open(file_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        conversation.extend([item.strip() for row in reader for item in row[1:]])
    # Train from conversation
    list_trainer.train(conversation)


if __name__ == '__main__':
    train()
