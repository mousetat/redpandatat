import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime 
import random
import os
import time
import pickle
os.system("cls")

imtat = {"I'M", "IM"}
global bdayppl
bdayppl = ""
gprefix = "r!"
corchannel = "491563537278173185"
bday = pickle.load(open("D:\Documents\Red Panda\data.txt", "rb"))

Client = discord.Client()
client = commands.Bot(command_prefix = gprefix)

	
@client.event
async def on_ready():
	print ("Bot is ready!")
	await client.change_presence(game=discord.Game(name='Red Panda type r!help'))
	global bdayppl
	bdayppl = []
	for i in range(0, len(bday)):
		if bday[i]["date"] == datetime.datetime.today().strftime('%d-%m'):
			bdayppl.append(bday[i]["name"])
	if bdayppl != []:
		print(bdayppl)
		for ppl in bdayppl:
			await client.send_message(discord.Object(id=corchannel), "Happy Birthday " + ppl + "! Type ``r!bdaygift`` to open your gift(s) :D")
	
@client.event
async def on_message(message):
	if message.author == client.user:
		return 
		
	if message.content.startswith(gprefix) and message.channel.id != corchannel:
		await client.send_message(discord.Object(id=corchannel),"<@" + message.author.id + "> Wrong Channel. Type commands here instead.")
		
	if message.content == gprefix + "redpanda":
		emoji = discord.utils.get(client.get_all_emojis(), name='redpanda')
		await client.add_reaction(message, emoji)
		imgList = os.listdir("./Red panda images")
		imgString = random.choice(imgList) # Selects a random element from the list
		path = "./Red panda images/" + imgString # Creates a string for the path to the file
		await client.send_file(discord.Object(id=corchannel), path) # Sends the image in the channel the command was used
		
	if message.author.id == "312811631459696641": 
		emoji = discord.utils.get(client.get_all_emojis(), name='kyaaa')
		await client.add_reaction(message, emoji)
		
	if message.content == gprefix + "bday":
		if bdayppl != []:
			for ppl in bdayppl:
				await client.send_message(discord.Object(id=corchannel), "Happy Birthday " + ppl + "! Type ``r!bdaygift`` to open your gift(s) :D")
		else:
			await client.send_message(discord.Object(id=corchannel), "Don't know who's birthday is it today, but you can celebrate mine anytime :)")
			
	if message.content == gprefix + "bdaygift":
		await client.send_message(discord.Object(id=corchannel), "You recieved a: mp3 gift! Join a voice channel and type ``r!bdaysong`` to listen to it :D")

	if message.content == gprefix + "bdaysong":
		author = message.author
		channel = author.voice_channel
		if channel is None:
			await client.send_message(discord.Object(id=corchannel), "You are not in a voice channel.")
		elif any(str(message.author.id) in s for s in bdayppl):
			vc = await client.join_voice_channel(channel)
			player = vc.create_ffmpeg_player('Happy Bday Song.mp3')
			player.start()
			counter = 0
			duration = 13   # In seconds
			while not counter >= duration:
				await asyncio.sleep(1)
				counter = counter + 1
			await vc.disconnect()
		else:
			await client.send_message(discord.Object(id=corchannel), "It's not your bday today!")
			
	if message.content == gprefix + "help":
		await client.send_message(discord.Object(id=corchannel), "Available commands: ``r!bday``, ``r!redpanda``, ``r!addbday`` to change or add new bday, ``r!bdaylist``, ``r!help``")
	
	if message.content.startswith(gprefix + "addbday"):
		if message.content[10:] == None or len(message.content[10:]) != 5:
			await client.send_message(discord.Object(id=corchannel), "Please type ``r!addbday DD/MM``, e.g. ``r!addbday 20/04``.")
		else:
			for x in range(0,len(bday)):
				if bday[x]['name'] == "<@" + str(message.author.id)+ ">":
					await client.send_message(discord.Object(id=corchannel), "You already have this birthday recorded. Your birthday has been changed to " + message.content[10:12] + "/" + message.content[13:15])
					bday[x]['date'] = message.content[10:12] + "-" + message.content[13:15]
					pickle.dump(bday, open("D:\Documents\Red Panda\data.txt", "wb"))
					await on_ready()
					break
				elif x==len(bday)-1:
					await client.send_message(discord.Object(id=corchannel), "Your birthday has been added." )
					bday.append({'name': "<@"+str(message.author.id)+">", 'date': (message.content[10:12] + "-" + message.content[13:15])})
					pickle.dump(bday, open("D:\Documents\Red Panda\data.txt", "wb"))
					await on_ready()
					
	args = message.content.split(" ")
	for x in range(0, len(args)):
		if args[x].upper() in imtat:
			global msg 
			msg = ""
			for i in range(x+1, len(args)):
				msg = msg + " " + args[i]
			print (msg)
			await client.send_message(message.channel, "Hi" + msg + ", I'm tat's slave.")
	if message.content == gprefix + "bdaylist":
		for x in range(0,len(bday)):
			if discord.Server.get_member(message.server, user_id = bday[x]['name'][2:20]) != None:
				await client.send_message(discord.Object(id=corchannel), str(discord.Server.get_member(message.server, user_id = bday[x]['name'][2:20])) + ": " + bday[x]['date'][0:2]+"/"+bday[x]['date'][3:5])						
	if message.author.id == "163927919712927744" and message.content == gprefix + "kill":
		await client.logout()
		
client.run(os.getenv('TOKEN'))

