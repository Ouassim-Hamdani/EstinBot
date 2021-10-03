import discord,os,csv
from keep_alive import keep_alive
import random
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
  with open('data.csv') as cdata:
    reader = csv.reader(cdata)
    return [x for x in reader]
def writeData(data):
  with open('data.csv',"w") as cdata:
    writer = csv.writer(cdata)
    writer.writerows(data)
def showLeaderboard():
  message = "-----> Challenges Leader Board of ESTIN <-----"
  data = loadIntoList()
  data = sorted(data,key=lambda x: int(x[2]),reverse=True)
  for i,stud in enumerate(data):
    message+=f"\n\n  {str(i+1)}  -  {stud[1]}   Score : {stud[2]}   Challanges Done : {stud[3]}" 
  return message
def addPoints(user,p,name):
  data = loadIntoList()
  found = False
  for i,stud in enumerate(data):
    if stud[0] == user or stud[0].replace("!","") == user:
      found = True
      data[i][2] = str(int(data[i][2])+int(p))
      data[i][3] = str(int(data[i][3])+1)
  if found == False:
    data.append([user,name,p,"1"])
  writeData(data)
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
      await message.channel.send(showLeaderboard())

keep_alive()
client.run(os.getenv('TOKEN'))
