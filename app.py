#imports
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask.wrappers import Response
# from flask_sqlalchemy import SQLAlchemy
import wikipedia
import os
from wikipedia.exceptions import PageError
from boto.s3.connection import S3Connection
# import nltk
# nltk.download('punkt')

app = Flask(__name__)
#create chatbot
englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.MongoDatabaseAdapter")
trainer = ChatterBotCorpusTrainer(englishBot)
trainer.train("chatterbot.corpus.english")
read_only=True
s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
#define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    if "search" in userText or "find" in userText or "pedia"in userText or"wiki"in userText:
        try:
            statement="According to Wikipedia "+wikipedia.summary(userText, sentences=3)
        except:
            response="Sorry,try something else"
            return response
    else:
        statement=str(englishBot.get_response(userText))
    return statement

if __name__ == "__main__":
    app.run()
