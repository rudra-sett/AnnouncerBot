import discord
import os
import pickle

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('ab'):
    await processmessage(message)

responses = {}
@client.event
async def on_voice_state_update(member, before, after):
  if (before.channel == None and not after.channel == None):
    try:
      #chan = responses[after.channel.guild.name+member.name][1]
      #resp = responses[after.channel.guild.name+member.name][0]
      resp,chan = responses[after.channel.guild.name+member.name].split("||||||||||")
      print("request to send "+resp+" to "+chan)
      for c in after.channel.guild.channels:
        #print(c.name)
        #print(chan)
        if (c.name == chan):
          print("sending message...")
          sent = await c.send(resp,tts=True)
          await sent.delete(delay = 5)
    except:
      return
  pass
scores = {}
async def processmessage(message):
  #commands 
  #print("okay...")
  arguments = None
  command = None
  #has an argument
  #ab command arguments
  try:
    command = message.content.split(" ",2)[1]
    arguments = message.content.split(" ",2)[2]
  except IndexError:
    print("A command without an argument was passed!")

  if (command == "set"):
    target = None
    resp = None
    try:
      #nonlocal target
      target = message.mentions[0]
    except:
      await message.channel.send("You didn't say who the announcement is for!")
      return
    #argument is in this format:
    #<mention> <message>
    try:
      #nonlocal resp
      resp = arguments.split(" ",1)[1][:15]
    except IndexError:
      await message.channel.send("You didn't say what to announce for "+target.name+"!")
    responses[message.guild.name+target.name] = resp+"||||||||||"+message.channel.name
    with open('responsefile.pkl', 'wb') as output:
      pickle.dump(responses, output, pickle.HIGHEST_PROTOCOL)
  pass
with open('responsefile.pkl', 'rb') as input:
    responses = pickle.load(input)
    print(responses)
    if (responses == None):
        print("didn't actually get anything")
        responses = {}
client.run(os.getenv('TOKEN'))