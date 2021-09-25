import os
import discord
import requests
import json
import random
from replit import db


#Create variable to initiate Discord client object
client = discord.Client()
my_secret = os.environ['TOKEN']

#Create array of sad words to trigger the bot
sad_words = ["sad", "awit", "sayang", "talo", "olats", "natalo", "hirap", "lungkot"]

start_encouragements = ["Hey Partner, Cheer up", "Yo, kapit lang. Baka need mo ng help", "Don't worry, bawi tayo next", "Baka need mo lang ng break, partner."]

#Create a function to get quote from zenquotes.io API server
def  get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

#Create event listener for discord object
@client.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#Create event listener as soon as message received in channel
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = start_encouragements
  if "encouragements" in db.keys():
    options.extend(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith('$new'):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouranging message added. ")
  
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    keys = db.keys()
    await message.channel.send(keys)


#Run the bot command
client.run(my_secret)



