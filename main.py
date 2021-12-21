import discord,os,csv
import pymongo
from pymongo import MongoClient
import random
key = None
cluster = MongoClient("mongodb+srv://ouassim:1598@cluster0.eroy9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["estin"]
jokes = ["infomratique mafiahch future","esi sba","mais ntoma futures engineers!","esi sba","estin 9raytha sahla","Esi alger 3andhom SIL SIQ SIT","You","Wajhak","Esi alger 3andhom SIL SIQ SIT"]
greetingReplies = ["Wach khasak?","Wah?","Achu?","Wch t7was","Cha bghit?","Bala3"]
client = discord.Client()
def getID(a):
  a = a.replace("<","")
  a = a.replace(">","")
  a = a.replace("@","")
  a = a.replace("!","")
  return a
def loadIntoList():
  r = collection.find({})
  l = []
  for i in r:
      l.append(i)
  return l
def showLeaderboard():
  data = loadIntoList()
  data = sorted(data,key=lambda x: x["points"],reverse=True)
  for i,stud in enumerate(data):
    if i==0:
      message=f"  {str(i+1)}  -  **{stud['name']}**   \tScore : {stud['points']}   \tChallenges Done : {stud['challenges']}" 
    else:
      message+=f"\n\n  {str(i+1)}  -  **{stud['name']}**   \tScore : {stud['points']}   \tChallenges Done : {stud['challenges']}" 
  return message
def addPoints(user,p,name):
  user2 = user[:2]+"!"+user[2:]
  #data = loadIntoList()
  found = False
  results = collection.find_one({"$or":[{"_id":user},{"_id":user2}]})
  if results:
    print(results["_id"])
    results = collection.update_one({"$or":[{"_id":user},{"_id":user2}]},{"$inc":{"points":int(p),"challenges":1}})
  else:
    collection.insert_one({"_id":user,"name":name,"points":int(p),"challenges":1})
  #writeData(data)
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,name="Made by Ouassim Hamdani"))
  print(f"Bot launched as {client.user}")
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$hey'):
    await message.channel.send(greetingReplies[random.randint(0,len(greetingReplies)-1)])
  if message.content.startswith('$joke'):
    await message.channel.send(jokes[random.randint(0,len(jokes)-1)])
  if message.content.startswith('$help'):
    await message.channel.send('Nab9aw nkasro rasna ha hom commands w skatna\n  $hey : bayna\n  $joke : bayna aussi')
  if message.content.startswith('$add'):
    if ("admin" in [y.name.lower() for y in message.author.roles]) or ("mod" in [y.name.lower() for y in message.author.roles]):
      user = await message.guild.query_members(user_ids=getID(message.content.split()[1]))
      user = user[0]
      addPoints(message.content.split()[1],message.content.split()[2],user.display_name)
      await message.channel.send(f'Added {message.content.split()[2]} to {message.content.split()[1]}')
  if message.content.startswith('$leader'):
    if ("admin" in [y.name.lower() for y in message.author.roles]) or ("mod" in [y.name.lower() for y in message.author.roles]):
      embed = discord.Embed(
        title = 'Challenges Leader Board of ESTIN',
        description=showLeaderboard(),
        colour =discord.Colour.blue()
      )
      embed.set_footer(text="École supérieure en sciences et technologies de l'informatique et du numérique")
      embed.set_image(url='https://estin.dz/wp-content/uploads/2020/11/cropped-estin_logo-mini-2-2.jpg')
      await message.channel.send(embed=embed)
client.run(key)
