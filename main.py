import discord
import data
from discord.ext import commands
from discord import Intents
from datetime import datetime
import sqlite3
import pytz
import threading
import time
import random
import os

playersdb = sqlite3.connect('players.db')
matchesdb = sqlite3.connect('matches.db')
tournamentdb = sqlite3.connect('tournament.db')

pc = playersdb.cursor()
mc = matchesdb.cursor()
tc = tournamentdb.cursor()

# pc.execute("CREATE TABLE players (username text,userid integer, matchid integer,live integer,wins integer,losses integer,elo integer,winstreak integer, placements integer,bonus integer)")
# mc.execute("CREATE TABLE matches (matchid integer, matchtime text, team1 text, team2 text, hpmap text, sndmap text, ctrlmap text, cancelr integer, canceled integer, cancelteam  integer, result integer, reported text, final integer)")

t_zone = pytz.timezone('US/Central')
intents = Intents.all()
client = commands.Bot(command_prefix='=', intents = intents)
client.remove_command('help')

#Channels
leaderboardChannel = 815695021411532817
eloGeneral = 810618583548952586
eloMatches = 815693259523227678

eloMod = 812963773430235146

euelomatches = 819727651635593236
eueloGeneral = 819727914839834635
euLeaderboardChannel = 820395943932461066

#role
eloRegistered = 815684387668361267
EUeloRegistered = 819714736073211931

diamondrole = 825494494110941194
goldrole = 825495322998472705
silverrole = 825497110182363167
bronzerole = 825497383806566431
meatrole = 825497726879793204
waitwut = 828660084318011472


timert = []
q = []
euQ = []

CLOSEQUEUE = False

@client.event
async def on_ready():
  print("Bot is online...")

@client.event
async def on_member_join(member):
  pass

@client.command()
@commands.has_role("AoV")
async def lb(ctx):
  await leaderboard()

@client.command()
@commands.has_role("AoV")
async def members(ctx,*args):
  pc.execute("SELECT * FROM players")
  temp = pc.fetchall()

  for each in temp:
    print(each)


@client.command()
@commands.has_role("AoV")
async def sendmsg(ctx,*args):
  channel = client.get_channel(eloMod)
  msg = ""
  for x in range(len(args)):
    msg = msg + args[x] + " "

  await channel.send(msg)

@client.command()
@commands.has_role("AoV")
async def remove(ctx,*args):
  try:
    pc.execute("DELETE FROM players WHERE userid=?",(int(args[0]),))
    playersdb.commit()
    channel = client.get_channel(eloMod)
    await channel.send("Member has been removed.")
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Could not find member.")


@client.command()
@commands.has_role("AoV")
async def updatenames(ctx):
  pc.execute("Select * From players")
  temp = pc.fetchall()

  for each in temp:
    
    try:
      member = ctx.guild.get_member(each[1])
      print(each[1])
      print(member.name)
      pc.execute("UPDATE players SET username = ? WHERE userid= ?",(member.name,each[1],))
      playersdb.commit()
      print("finished updating")
    except:
      print("failed to get member")


@client.command()
@commands.has_role("AoV")
async def giverole(ctx):
  pc.execute("Select * From players")
  temp = pc.fetchall()

  for each in temp:
    print(each[1])
    member = ctx.guild.get_member(each[1])
    role = ctx.guild.get_role(eloRegistered)
    await member.add_roles(role)

@client.command()
@commands.has_role("AoV")
async def checkcolor(ctx):
  pc.execute("Select * From players")
  temp = pc.fetchall()

  for each in temp:
    await checkroles(ctx,each)


@client.command()
@commands.has_role("AoV")
async def checkrank(ctx):
  pc.execute("Select * From players")
  temp = pc.fetchall()

  for each in temp:
    await checkroles(ctx,each)

@client.command()
@commands.has_role("AoV")
async def givecolor(ctx):
  pc.execute("Select * From players")
  temp = pc.fetchall()

  for each in temp:
    try:
      member = ctx.guild.get_member(each[1])
    
      if each[6] < 850:
        role = ctx.guild.get_role(meatrole)
      elif each[6] >= 850 and each[6] < 1000:
        role = ctx.guild.get_role(bronzerole)
      elif each[6] >= 1000 and each[6] < 1200:
        role = ctx.guild.get_role(silverrole)
      elif each[6] >= 1200 and each[6] < 1500:
        role = ctx.guild.get_role(goldrole)
      elif each[6] >= 1500:
        role = ctx.guild.get_role(diamondrole)
      else:
        print("user has no elo????")
      
      await member.add_roles(role)
    except:
      print("failed to get member")
    

@client.command()
async def EUregister(ctx):

  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  if user != None:
    await directmsg(ctx.author.id,"Seems you are already registered.")
    print("Found!")

  else:
    pc.execute('''INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(str(ctx.author.name),ctx.author.id,-1,False,0,0,1000,0,True,0,1))
    playersdb.commit()

    member = ctx.author
    role = ctx.guild.get_role(EUeloRegistered)
    await member.add_roles(role)
    await directmsg(ctx.author.id,"You have successfully registered!")

@client.command()
async def register(ctx):

  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  if user != None:
    await directmsg(ctx.author.id,"Seems you are already registered.")
    print("Found!")

  else:
    pc.execute('''INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(str(ctx.author.name),ctx.author.id,-1,False,0,0,1000,0,True,0,0))
    playersdb.commit()

    member = ctx.author
    role = ctx.guild.get_role(eloRegistered)
    await member.add_roles(role)
    await directmsg(ctx.author.id,"You have successfully registered!")
    
@client.command()
@commands.has_role("AoV")
async def setbonus(ctx,*args):
  
  try:
    pc.execute("UPDATE players SET bonus = ? WHERE userid= ?",(int(args[1]),int(args[0]),))
    playersdb.commit()
   
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Error check spelling and format.")

@client.command()
@commands.has_role("AoV")
async def setelo(ctx,*args):
  
  try:
    pc.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(args[1]),int(args[0]),))
    playersdb.commit()
   
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Error check spelling and format.")

@client.command()
@commands.has_role("AoV")
async def setwins(ctx,*args):

  try:
    pc.execute("UPDATE players SET wins = ? WHERE userid= ?",(int(args[1]),int(args[0])))
    playersdb.commit()
    print(pc.fetchone())
      
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Error check spelling and format.")
  
@client.command()
@commands.has_role("AoV")
async def setlosses(ctx,*args):

  try:
    pc.execute("UPDATE players SET losses = ? WHERE userid= ?",(int(args[1]),int(args[0])))
    playersdb.commit()

      
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Error check spelling and format.")

@client.command()
@commands.has_role("AoV")
async def setlive(ctx,*args):
  
  try:
    if(str(args[1]).lower() == "false"):
      pc.execute("UPDATE players SET live = ? WHERE userid= ?",(0 ,int(args[0]),))
      playersdb.commit()
      print("setting live")

    if(str(args[1]).lower() == "true"):
      pc.execute("UPDATE players SET live = ? WHERE userid= ?",(1 ,int(args[0]),))
      playersdb.commit()
      print("setting live")
   
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Error check spelling and format.")


@client.command()
@commands.has_role("AoV")
async def seteu(ctx,*args):

  try:
    pc.execute("UPDATE players SET eu = ? WHERE userid= ?",(int(args[1]),int(args[0])))
    playersdb.commit()

  except:
    channel = client.get_channel(eloMod)
    await channel.send("Error check spelling and format.")

  
@client.command()
@commands.has_role("AoV")
async def matchinfo(ctx, *args):
  matchid = int(args[0].strip())
  mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mc.fetchone()
  print(match)
  
@client.command()
@commands.has_role("AoV")
async def clearq(ctx):
  q.clear()
  channel = client.get_channel(eloMod)
  await channel.send("The queue has been emptied.")

@client.command()
@commands.has_role("AoV")
async def EUclearq(ctx):
  euQ.clear()
  channel = client.get_channel(eloMod)
  await channel.send("The EU queue has been emptied.")


@client.command()
@commands.has_role("AoV")
async def EUaddq(ctx, *args):

  for each in args:
    euQ.append(int(each))

  if len(euQ) == 8:
    listp = euQ
    euQ.clear()
    channel = client.get_channel(eloMatches)
    await channel.send("8 Players in queue, forming teams...")
    await channel.send(await makeMatch(listp))

@client.command()
@commands.has_role("AoV")
async def addq(ctx, *args):

  for each in args:
    q.append(int(each))

  if len(q) == 8:
    listp = q
    q.clear()
    channel = client.get_channel(eloMatches)
    await channel.send("8 Players in queue, forming teams...")
    await channel.send(await makeMatch(listp))
    
@client.command()
@commands.has_role("AoV")
async def resolve(ctx, *args):

  matchid = int(args[0].strip())
  mc.execute("SELECT * FROM matches")
  temp = mc.fetchall()

  try:
    
    if(matchid <= len(temp) ):
      mc.execute("UPDATE matches SET result = ? WHERE matchid = ?",(int(args[1]), matchid,))
      mc.execute("UPDATE matches SET final = ? WHERE matchid = ?",(True, matchid,))
      matchesdb.commit()

      calculateElo(matchid,mc,matchesdb,pc,playersdb)
      await leaderboard()
      mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
      match = mc.fetchone()
      
      team1 = list(match[2].split("‰"))
      team2 = list(match[3].split("‰"))

      players = team1 + team2

      for each in players:
        pc.execute("SELECT * FROM players WHERE userid=?",(each,))
        temp = pc.fetchone()
        await checkroles(ctx,temp)

        if each not in match[11]:
          pc.execute("UPDATE players SET live = ? WHERE userid= ?",(False, each,))
          

      playersdb.commit()

      channel = client.get_channel(eloMatches)

      await channel.send("Team " + args[1].strip() + " has been awarded the win for match #" + args[0].strip())
      
    else:
      channel = client.get_channel(eloMod)
      await channel.send("Match " + str(matchid) + " does not exsist.")


  except ValueError:
    channel = client.get_channel(eloMod)
    await channel.send("Syntax error use: =resolve <matchid> <winning team #>")

@client.command()
@commands.has_role("AoV")
async def removeq(ctx, *args):
  try:
    q.remove(int(args[0]))
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Something went wrong.")

@client.command()
@commands.has_role("AoV")
async def EUremoveq(ctx, *args):
  try:
    euQ.remove(int(args[0]))
  except:
    channel = client.get_channel(eloMod)
    await channel.send("Something went wrong.")

@client.command()
@commands.has_role("AoV")
async def closeq(ctx):
  global CLOSEQUEUE 
  CLOSEQUEUE = True
  await clearq(ctx)
  await EUclearq(ctx)

@client.command()
@commands.has_role("AoV")
async def openq(ctx):
  global CLOSEQUEUE
  CLOSEQUEUE = False
  await clearq(ctx)
  await EUclearq(ctx)


@client.command()
@commands.has_role("AoV")
async def tournamentmsg(ctx, *args):

  msg = "PLEASE TYPE =checkin TO CONFIRM U ARE HERE FOR THE TOURNAMENT EVEN IF U ALREADY DID. IF U GET THIS MSG AND ARE READY PLEASE TYPE =checkin."

  for each in args:
    pc.execute("SELECT * FROM players WHERE userid=?",(each,))
    user = pc.fetchone()
    
    await directmsg(user[1], msg)


@client.command()
@commands.has_role("AoV")
async def tournamentcheckin(ctx, *args):

  msg = "PLEASE TYPE =checkin TO CONFIRM THAT YOU ARE READY FOR THE TOURNAMENT."

  for each in args:
    pc.execute("SELECT * FROM players WHERE userid=?",(each,))
    user = pc.fetchone()
    
    tc.execute('''INSERT INTO tournament VALUES (?,?,?)''',(user[0],user[1],0))
    tournamentdb.commit()

    await directmsg(user[1], msg)

@client.command()
async def checkin(ctx):
  tc.execute("UPDATE tournament SET checkin = ? WHERE userid= ?",(1, ctx.author.id, ))
  tournamentdb.commit()
  msg = "YOU HAVE CHECKED IN xD"
  await directmsg(ctx.author.id, msg)

@client.command()
async def stats(ctx,*args):

  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  if(len(args) == 0):
    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send(ctx.author.mention + " Wins: " + str(user[4]) + " Losses: " + str(user[5]) + " ELO: " + str(user[6]) + " " + rankIcon(user[6]))
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send(ctx.author.mention + " Wins: " + str(user[4]) + " Losses: " + str(user[5]) + " ELO: " + str(user[6]) + " " + rankIcon(user[6]))

  elif(len(args) == 1):
    pc.execute("SELECT * FROM players WHERE username=?",(args[0],))
    temp = pc.fetchone()

    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send(args[0] + " Wins: " + str(temp[4]) + " Losses: " + str(temp[5]) + " ELO: " + str(temp[6]) + " " + rankIcon(temp[6]))
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send(args[0] + " Wins: " + str(temp[4]) + " Losses: " + str(temp[5]) + " ELO: " + str(temp[6]) + " " + rankIcon(temp[6]))
    
  else:
    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send("Syntax error use: =stats <user#1234>")

    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("Syntax error use: =stats <user#1234>")


@client.command(aliases=['mh'])
async def matchhistory(ctx,*args):
  mc.execute("SELECT * FROM matches")
  matchlist = mc.fetchall()

  matchhist = []

  for each in matchlist:
    team1 = list(each[2].split("‰"))
    team2 = list(each[3].split("‰"))

    if(str(ctx.author.id) in team1 or str(ctx.author.id) in team2):
      matchhist.append(each)
        
  message = ""
  
  count = 0
  for each in matchhist:
    team1 = list(each[2].split("‰"))
    team2 = list(each[3].split("‰"))
    names1 = []
    names2 = []

    for userid in team1:
      pc.execute("SELECT * FROM players WHERE userid=?",(int(userid),))
      temp = pc.fetchone()
      names1.append(temp[0])
    
    for userid in team2:
      pc.execute("SELECT * FROM players WHERE userid=?",(int(userid),))
      temp = pc.fetchone()
      names2.append(temp[0])

    result = ""
    if (each[10] == 1 and str(ctx.author.id) in team1) or (each[10] == 2 and str(ctx.author.id) in team2):
      result = "WIN"
    elif(each[8] == 1):
      result = "CANCELED"
    else:
      result = "LOSS"

    
    msg = ""
    msg = msg + "Match ID: " + str(each[0]) + "\n"
    msg = msg + "Team 1: " + names1[0] + " " + names1[1] + " " + names1[2] + " " + names1[3] + "\n"
    msg = msg + "Team 2: " + names2[0] + " " + names2[1] + " " + names2[2] + " " + names2[3] + " \n"
    msg = msg + "Result: " + result + "\n"
    msg = msg + "========================================================================================\n"

    if len(message) + len(msg) >= 2000:
      await directmsg(ctx.author.id, message)
      message = ""
    
    message = message + msg
    
    count = count + 1
    
    if count == len(matchhist):
      await directmsg(ctx.author.id, message)
      
  notice = "*PLEASE NOTE MATCH 1 THROUGH MATCH 27 WILL NOT APPEAR ON THIS LIST SORRY FOR INCONVENIENCE*"
  await directmsg(ctx.author.id, notice)

@client.command(aliases=['vs'])
async def versus(ctx,*args):
  mc.execute("SELECT * FROM matches")
  matchlist = mc.fetchall()

  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  authoruser = pc.fetchone()
  
  userfound = False
  try:
    pc.execute("SELECT * FROM players WHERE username=?",(args[0],))
    oppenentuser = pc.fetchone()
    userfound = True
  except:
    pass

  authorwins = 0
  opponentwins = 0

  if len(args) == 0:
    if authoruser[10] == 1:
      channel = client.get_channel(eueloGeneral)
    else:
      channel = client.get_channel(eloGeneral)
    await channel.send("Syntax error use: =versus <username>")
  
  elif len(args) == 1 and userfound == True:

    for each in matchlist:
      team1 = list(each[2].split("‰"))
      team2 = list(each[3].split("‰"))

      if(str(ctx.author.id) in team1 and str(oppenentuser[1]) in team2):
        if each[8] == 0:
        
          if each[10] == 1:
            authorwins = authorwins + 1 
          else:
            opponentwins = opponentwins + 1

      if(str(ctx.author.id) in team2 and str(oppenentuser[1]) in team1):
        if each[8] == 0:
          if each[10] == 2:
            authorwins = authorwins + 1 
          else:
            opponentwins = opponentwins + 1
    
    if authoruser[10] == 1:
      channel = client.get_channel(eueloGeneral)
    else:
      channel = client.get_channel(eloGeneral)
    await channel.send(authoruser[0] + " Wins: " + str(authorwins) +" VS "+ oppenentuser[0] + " Wins: " + str(opponentwins))

  else:
    if authoruser[10] == 1:
      channel = client.get_channel(eueloGeneral)
    else:
      channel = client.get_channel(eloGeneral)
    await channel.send("Couldn't find a user by that name")
 

@client.command(aliases=['q'])
async def queue(ctx):

  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()
  global CLOSEQUEUE
  if CLOSEQUEUE == False:
    if user[3] == False:
      if user[1] in q or user[1] in euQ:
        if user[1] in euQ:
          euQ.remove(user[1])
          channel = client.get_channel(eueloGeneral)
          await channel.send(str(user[0]) + " has left the queue. " + str(len(euQ)) + " member(s) in queue.")
        else:
          q.remove(user[1])
          channel = client.get_channel(eloGeneral)
          await channel.send(str(user[0]) + " has left the queue. " + str(len(q)) + " member(s) in queue.")
      else:
        if user[10] == 1:
          euQ.append(user[1])
          channel = client.get_channel(eueloGeneral)
          await channel.send(str(user[0]) + " has joined the queue. " +  str(len(euQ)) + " member(s) in queue.")
        else:
          q.append(user[1])
          channel = client.get_channel(eloGeneral)
          await channel.send(str(user[0]) + " has joined the queue. " +  str(len(q)) + " member(s) in queue.")

    else:
      if user[10] == 1:
        channel = client.get_channel(eueloGeneral)
        await channel.send("You have not reported the result of match " + str(user[2]))
      else:
        channel = client.get_channel(eloGeneral)
        await channel.send("You have not reported the result of match " + str(user[2]))

    if len(q) == 8:
      listp = []
      for each in q:
        listp.append(each)
      q.clear()
      channel = client.get_channel(eloMatches)

      await channel.send(await makeMatch(listp))

    if len(euQ) == 8:
      listp = []
      for each in euQ:
        listp.append(each)
      euQ.clear()
      channel = client.get_channel(euelomatches)

      await channel.send(await makeMatch(listp))
  else:
    if user[10] == 1:
        channel = client.get_channel(eueloGeneral)
        await channel.send("The EU queue is currently closed.")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("The NA queue is currently closed.")

@client.command()
async def showqueue(ctx):

  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  if user[10] == 1:
    if len(euQ) == 0:
      channel = client.get_channel(eueloGeneral)
      await channel.send("The queue is currently empty.")
    else:
      msg = "{len} member(s) in queue: \n".format(len = len(euQ))
      for each in euQ:
        pc.execute("SELECT * FROM players WHERE userid=?",(each,))
        temp = pc.fetchone()
        msg = msg + str(temp[0]) + "\n"
      channel = client.get_channel(eueloGeneral)
      await channel.send(msg)

  else:
    if len(q) == 0:
      channel = client.get_channel(eloGeneral)
      await channel.send("The queue is currently empty.")
    else:
      msg = "{len} member(s) in queue: \n".format(len = len(q))
      for each in q:
        pc.execute("SELECT * FROM players WHERE userid=?",(each,))
        temp = pc.fetchone()
        msg = msg + str(temp[0]) + "\n"
      channel = client.get_channel(eloGeneral)
      await channel.send(msg)

 
@client.command()
async def report(ctx,*args):
  
  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()
  matchid = user[2]

  mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mc.fetchone()
  
  winners = int(args[0].strip())

  try:
    if(user[3] == True):
      print("Got this far 1")
      if(winners == 1 or winners == 2):
          if(match[10] == winners or match[10] == 0):
            print("Got this far 2")
            if(len(match[11]) == 0 or str(ctx.author.id) not in match[11]):
              print("Got this far 3")
              mc.execute("UPDATE matches SET result = ? WHERE matchid= ?",(winners, matchid))
              pc.execute("UPDATE players SET live = ? WHERE userid= ?",(0, ctx.author.id))
              playersdb.commit()
    
              string = match[11] + str(ctx.author.id) + "‰"

              mc.execute("UPDATE matches SET reported = ? WHERE matchid= ?",(string, matchid))
              matchesdb.commit()
              
              if checkFinal(matchid) == True and match[12] == False:
                print("Got this far 4")
                calculateElo(matchid,mc,matchesdb,pc,playersdb)
                mc.execute("UPDATE matches SET final = ? WHERE matchid= ?",(True, matchid))
                matchesdb.commit()
                msg = "Team #" + str(winners) + " has been awarded the win for match #" + str(matchid)
                team1 = list(match[2].split("‰"))
                team2 = list(match[3].split("‰"))

                players = team1 + team2

                for each in players:
                  
                  if each not in match[11]:
                    pc.execute("UPDATE players SET live = ? WHERE userid= ?",(0, int(each)))
                    playersdb.commit()
                  pc.execute("SELECT * FROM players WHERE userid=?",(each,))                 
                  temp = pc.fetchone()
                  await directmsg(temp[1],msg)
                  await checkroles(ctx,temp)
                  
                
                await leaderboard()

                if user[10] == 1:
                  channel = client.get_channel(eueloGeneral)
                  await channel.send(msg)
                  channel = client.get_channel(euelomatches)
                  await channel.send(msg)
                
                else:
                  channel = client.get_channel(eloGeneral)
                  await channel.send(msg)
                  channel = client.get_channel(eloMatches)
                  await channel.send(msg)

              else:
                if user[10] == 1:
                  channel = client.get_channel(eueloGeneral)
                  await channel.send("Match #" + str(matchid) + " has been reported thank you!")

                else:
                  channel = client.get_channel(eloGeneral)
                  await channel.send("Match #" + str(matchid) + " has been reported thank you!")
            
            else:
              if user[10] == 1:
                channel = client.get_channel(eueloGeneral)
                await channel.send("You seem to have already reported for Match #" + str(matchid)) 
              else:
                channel = client.get_channel(eloGeneral)
                await channel.send("You seem to have already reported for Match #" + str(matchid)) 

          else:
            pc.execute("UPDATE players SET live = ? WHERE userid= ?",(0, ctx.author.id))
            playersdb.commit()
            
            string = match[11] + str(ctx.author.id) + "‰"

            mc.execute("UPDATE matches SET reported = ? WHERE matchid= ?",(string, matchid))
            matchesdb.commit()

            mc.execute("UPDATE matches SET result = ? WHERE matchid= ?",(0, matchid,))
            matchesdb.commit()

            team1 = list(match[2].split("‰"))
            team2 = list(match[3].split("‰"))

            players = team1 + team2

            for each in players:
              pc.execute("UPDATE players SET live = ? WHERE userid= ?",(0, each))
              playersdb.commit()

            msg = "Match #" + str(matchid) + " has been disputed please help these lads... =resolve <matchid> <winning team>"
            
            if user[10] == 1:
              channel = client.get_channel(eueloGeneral)
              await channel.send("Match #" + str(matchid) + " has been disputed a admin will be notified!")
            else:
              channel = client.get_channel(eloGeneral)
              await channel.send("Match #" + str(matchid) + " has been disputed a admin will be notified!")


            await directmsg(396409631561220096, msg) #Tanner
            await directmsg(139185336721997824, msg) #Blake
            await directmsg(255113353460973571, msg) #Andrew
            await directmsg(151515155983761408, msg) #Me
            await directmsg(812948033468760064, msg) #Edgar
            await directmsg(812923098931265547, msg) #Kevin
            
      else:
        if user[10] == 1:
          channel = client.get_channel(eueloGeneral)
          await channel.send("Team # does not exsist.")
        else:
          channel = client.get_channel(eloGeneral)
          await channel.send("Team # does not exsist.")
    else:

      if user[10] == 1:
        channel = client.get_channel(eueloGeneral)
        await channel.send("You do not seem to be in a match.")
      else:
        channel = client.get_channel(eloGeneral)
        await channel.send("You do not seem to be in a match.")
        

  except:
    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send("Something went wrong..")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("Something went wrong..")

  
@client.command()
async def cancel(ctx):
  
  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  matchid = user[2]

  mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))

  match = mc.fetchone()
  team1 = list(match[2].split("‰"))
  team2 = list(match[3].split("‰"))

  cancelteam = 0
  notcancel = 0
  if match[12] == False:
    mc.execute("UPDATE matches SET cancelr = ? WHERE matchid = ?",(True, matchid,))
    matchesdb.commit()
    
    if str(ctx.author.id) in team1:
      cancelteam = 1
      notcancel = 2
      mc.execute("UPDATE matches SET cancelteam = ? WHERE matchid = ?",(cancelteam, matchid,))
      matchesdb.commit()
    if str(ctx.author.id) in team2:
      cancelteam = 2
      notcancel = 1
      mc.execute("UPDATE matches SET cancelteam = ? WHERE matchid = ?",(cancelteam, matchid,))
      matchesdb.commit()

    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send("A cancel for match #" + str(matchid) + " has been requested." + "Team " + str(notcancel) + " please type =accept or =decline.")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("A cancel for match #" + str(matchid) + " has been requested." + "Team " + str(notcancel) + " please type =accept or =decline.")

  else:
    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send("Match is already final.")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("Match is already final.")


@client.command()
async def accept(ctx):
  
  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  matchid = user[2]

  mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mc.fetchone()

  team1 = list(match[2].split("‰"))
  team2 = list(match[3].split("‰"))

  if str(ctx.author.id) in team1:
    myteam = 1
      
  else:
    myteam = 2

  if myteam != match[9] and match[12] != True:
    mc.execute("UPDATE matches SET canceled = ? WHERE matchid = ?",(True, matchid,))
    mc.execute("UPDATE matches SET result = ? WHERE matchid = ?",(0, matchid,))
    mc.execute("UPDATE matches SET final = ? WHERE matchid = ?",(True, matchid,))
    matchesdb.commit()

    for each in team1:
      pc.execute("UPDATE players SET live = ? WHERE userid= ?",(False, each,))

    for each in team2:
      pc.execute("UPDATE players SET live = ? WHERE userid= ?",(False, each,))
    playersdb.commit()

    if user[10] == 1:
      channel = client.get_channel(euelomatches)
      await channel.send("Match #" + str(matchid) + " has been canceled.")
    else:
      channel = client.get_channel(eloMatches)
      await channel.send("Match #" + str(matchid) + " has been canceled.")
    
  else:
    if user[10] == 1:      
      channel = client.get_channel(eueloGeneral)
      await channel.send("You cannot accept your own teams cancel request.")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("You cannot accept your own teams cancel request.")


@client.command()
async def decline(ctx):
  
  pc.execute("SELECT * FROM players WHERE userid=?",(ctx.author.id,))
  user = pc.fetchone()

  matchid = user[2]

  mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mc.fetchone()

  team1 = list(match[2].split("‰"))

  if str(ctx.author.id) in team1:
    myteam = 1
      
  else:
    myteam = 2

  if myteam != match[9] and match[12] != True:
    mc.execute("UPDATE matches SET canceled = ? WHERE matchid = ?",(False, matchid,))
    mc.execute("UPDATE matches SET result = ? WHERE matchid = ?",(0, matchid,))
    mc.execute("UPDATE matches SET final = ? WHERE matchid = ?",(False, matchid,))
    matchesdb.commit()

    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send("Cancel request for Match #" + str(matchid) + " has been declined.")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("Cancel request for Match #" + str(matchid) + " has been declined.")

  else:
    if user[10] == 1:
      channel = client.get_channel(eueloGeneral)
      await channel.send("You cannot decline your own teams cancel request.")
    else:
      channel = client.get_channel(eloGeneral)
      await channel.send("You cannot decline your own teams cancel request.")
    


async def directmsg(userid,msg):

  try:
    user = client.get_user(userid)
    await user.send(msg)
  except:
    print("failed to msg " + str(user))

async def makeMatch(listp):

  mc.execute("SELECT * FROM matches")
  games = mc.fetchall()
 
  matchid = len(games) + 1
  now = datetime.now(tz = t_zone)
  current_time = now.strftime("%m/%d/%Y, %H:%M")

  temp = []

  for each in listp:
    pc.execute("UPDATE players SET live = ? WHERE userid= ?",(True, each,))
    pc.execute("UPDATE players SET matchid = ? WHERE userid= ?",(matchid, each,))
    playersdb.commit()
    pc.execute("SELECT * FROM players WHERE userid=?",(each,))
    user = pc.fetchone()
    temp.append(user)
          
  temp.sort(key=lambda x: x[6], reverse = True)

  hpmaps = open("hpmaps.txt").read().splitlines()
  hp = random.choice(hpmaps)
  sndmaps = open("sndmaps.txt").read().splitlines()
  snd = random.choice(sndmaps)
  ctrlmaps = open("ctrlmaps.txt").read().splitlines()
  ctrl = random.choice(ctrlmaps)

  team1 = ""
  team1 = team1 + str(temp[0][1]) + "‰"
  team1 = team1 + str(temp[2][1]) + "‰"
  team1 = team1 + str(temp[5][1]) + "‰"
  team1 = team1 + str(temp[7][1])

  team2 = ""
  team2 = team2 + str(temp[1][1]) + "‰"
  team2 = team2 + str(temp[3][1]) + "‰"
  team2 = team2 + str(temp[4][1]) + "‰"
  team2 = team2 + str(temp[6][1])

  msg = "Match #" + str(matchid) + ": " + str(current_time) + "\n"
  msg = msg + "======================== \n" + "Team 1: \n" 
  msg = msg + rankIcon(str(temp[0][6])) + " " + temp[0][0] +"\n"
  msg = msg + rankIcon(str(temp[2][6])) + " " + temp[2][0] + "\n"
  msg = msg + rankIcon(str(temp[5][6])) + " " + temp[5][0] + "\n"
  msg = msg + rankIcon(str(temp[7][6])) + " " + temp[7][0] + "\n"
  msg = msg + "======================== \n" + "Team 2: \n"
  msg = msg + rankIcon(str(temp[1][6])) + " " + temp[1][0] + "\n"
  msg = msg + rankIcon(str(temp[3][6])) + " " + temp[3][0] + "\n"
  msg = msg + rankIcon(str(temp[4][6])) + " " + temp[4][0] + "\n"
  msg = msg + rankIcon(str(temp[6][6])) + " " + temp[6][0] + "\n" 
  msg = msg + "======================== \n" 
  msg = msg + "Harpoint: " + str(hp) +"\n"
  msg = msg + "Search and Destroy: " + str(snd) +"\n"
  msg = msg + "Control: " + str(ctrl) +"\n\n"
 

  mc.execute("INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(matchid , str(current_time), team1, team2 , hp, snd, ctrl, False,False,0 ,0,"",False))
  matchesdb.commit()

  timert.append(threading.Timer(7200,timesup,[matchid]))
  timert[int(len(timert)-1)].start()
  

  await directmsg(temp[0][1],msg)
  await directmsg(temp[2][1],msg)
  await directmsg(temp[5][1],msg)
  await directmsg(temp[7][1],msg)

  await directmsg(temp[1][1],msg)
  await directmsg(temp[3][1],msg)
  await directmsg(temp[4][1],msg)
  await directmsg(temp[6][1],msg)
  
  return msg

async def checkroles(ctx,user):
  try:
    
    member = ctx.guild.get_member(user[1])
    roles = [meatrole,bronzerole,silverrole,goldrole,diamondrole]

    if user[6] < 850:
      expectedrole = meatrole
    elif user[6] >= 850 and user[6] < 1000:
      expectedrole = bronzerole
    elif user[6] >= 1000 and user[6] < 1200:
      expectedrole = silverrole
    elif user[6] >= 1200 and user[6] < 1500:
      expectedrole = goldrole
    elif user[6] >= 1500:
      expectedrole = diamondrole
    else:
      print("user has no expected role????")

    rolecount = 0
    for each in member.roles:
      if each.id in roles:
        rolecount = rolecount + 1
        if each.id == expectedrole:
          print("Already had correct role")
        else:
          print("Changed role")
          temp = ctx.guild.get_role(each.id)
          await member.remove_roles(temp)
          temp = ctx.guild.get_role(expectedrole)
          try:
            await member.add_roles(temp)
          except:
            print("failed to give user role, may already have it")

    if rolecount == 0:
      print("member " + user[0] + " had no rank role. giving now...")
      temp = ctx.guild.get_role(expectedrole)
      await member.add_roles(temp)
  except:
    print("failed to get member")


async def leaderboard():
  msgNa = ":crown: Leaderboard :crown: \n "
  msgEu = ":crown: Leaderboard :crown: \n "
  pc.execute("SELECT * FROM players WHERE eu=?",(0,))
  na = pc.fetchall()
  pc.execute("SELECT * FROM players WHERE eu=?",(1,))
  eu = pc.fetchall()
 
  na.sort(key=lambda x: x[6], reverse = True)
  eu.sort(key=lambda x: x[6], reverse = True)

  if len(na) < 10:
    for x in range(len(na)):
      msgNa = msgNa + str(x+1) + ". " + rankIcon(na[x][6]) + " " + na[x][0] +  " " + str(na[x][6]) + "\n"
  else:
    for x in range(10):
      msgNa = msgNa + str(x+1) + ". " + rankIcon(na[x][6]) + " " + na[x][0] +  " " + str(na[x][6]) + "\n"
  
  if len(eu) < 10:
    for x in range(len(eu)):
      msgEu = msgEu + str(x+1) + ". " + rankIcon(eu[x][6]) + " " + eu[x][0] +  " " + str(eu[x][6]) + "\n"
  else:
    for x in range(10):
      msgEu = msgEu + str(x+1) + ". " + rankIcon(eu[x][6]) + " " + eu[x][0] +  " " + str(eu[x][6]) + "\n"

  channel = client.get_channel(leaderboardChannel)
  await channel.send(msgNa)
  channel = client.get_channel(euLeaderboardChannel)
  await channel.send(msgEu)

def calculateElo(matchid,mcur,mconn,pcur,pconn):

  mcur.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mcur.fetchone()
  
  team1 = list(match[2].split("‰"))
  team2 = list(match[3].split("‰"))

  print(team1)
  print(team2)

  rank1 = 0
  rank2 = 0

  for player in team1:
    pcur.execute("SELECT * FROM players WHERE userid=?",(player,))
    user = pcur.fetchone()
    rank1 = rank1 + user[6]

  rank1 = rank1/4 #team average elo
  for player in team2:
    pcur.execute("SELECT * FROM players WHERE userid=?",(player,))
    user = pcur.fetchone()
    rank2 = rank2 + user[6]

  rank2 = rank2/4 #team average elo
  
  if match[10] == 1:
    
    r1 = 10**(rank1/400)
    r2 = 10**(rank2/400)
    e1 = r1 / (r1 + r2)
    e2 = r2/ (r1 + r2)
    f1 = rank1 + 35 *(1 - e1)
    f2 = rank2 + 35 *(0 - e2)
    t1 = f1 - rank1
    t2 = f2 - rank2

    for each in team1:
      pcur.execute("SELECT * FROM players WHERE userid=?",(each,))
      user = pcur.fetchone()
      user=list(user)

      if user[4] + user[5] >= 5:
        user[8] = False
        pcur.execute("UPDATE players SET placements = ? WHERE userid= ?",(user[8],each,))
        pconn.commit()

      user[7] = calcStreak(user,True)
      pcur.execute("UPDATE players SET winstreak = ? WHERE userid= ?",(user[7],each,))
      pconn.commit()
      
      bonus = calcBonus(user,True)
      pcur.execute("UPDATE players SET bonus = ? WHERE userid= ?",(bonus,each,))
      pconn.commit()

      if user[8] == True:
        pcur.execute("UPDATE players SET wins = ? WHERE userid= ?",(int(user[4]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]+35+bonus),each,))
        pconn.commit()
      else:
        pcur.execute("UPDATE players SET wins = ? WHERE userid= ?",(int(user[4]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]+t1+bonus),each,))
        pconn.commit()
     
  
    for each in team2:
      pcur.execute("SELECT * FROM players WHERE userid=?",(each,))
      user = pcur.fetchone()
      user=list(user)

      if user[4] + user[5] >= 5:
        user[8] = False
        pcur.execute("UPDATE players SET placements = ? WHERE userid= ?",(user[8],each,))
        pconn.commit()
  
      user[7] = calcStreak(user,False)
      pcur.execute("UPDATE players SET winstreak = ? WHERE userid= ?",(user[7],each,))
      pconn.commit()
      bonus = calcBonus(user,False)
      pcur.execute("UPDATE players SET bonus = ? WHERE userid= ?",(bonus,each,))
      pconn.commit()

      if user[8] == True:
        pcur.execute("UPDATE players SET losses = ? WHERE userid= ?",(int(user[5]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]-35+bonus),each,))
        pconn.commit()
      else:
        pcur.execute("UPDATE players SET losses = ? WHERE userid= ?",(int(user[5]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]+t2+bonus),each,))
        pconn.commit()
      
  elif match[10] == 2:
    
    r1 = 10**(rank1/400)
    r2 = 10**(rank2/400)
    e1 = r1 / (r1 + r2)
    e2 = r2/ (r1 + r2)
    f1 = rank1 + 35 *(0 - e1)
    f2 = rank2 + 35 *(1 - e2)
    t1 = f1 - rank1
    t2 = f2 - rank2

    for each in team1:
      pcur.execute("SELECT * FROM players WHERE userid=?",(each,))
      user = pcur.fetchone()
      user=list(user)

      if user[4] + user[5] >= 5:
        user[8] = False
        pcur.execute("UPDATE players SET placements = ? WHERE userid= ?",(user[8],each,))
        pconn.commit()

      user[7] = calcStreak(user,False)
      pcur.execute("UPDATE players SET winstreak = ? WHERE userid= ?",(user[7],each,))
      pconn.commit()
      bonus = calcBonus(user,False)
      pcur.execute("UPDATE players SET bonus = ? WHERE userid= ?",(bonus,each,))
      pconn.commit()

      if user[8] == True:
        pcur.execute("UPDATE players SET losses = ? WHERE userid= ?",(int(user[5]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]-35+bonus),each,))
        pconn.commit()
        
      else:
        pcur.execute("UPDATE players SET losses = ? WHERE userid= ?",(int(user[5]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]+t1+bonus),each,))
        pconn.commit()
        
  
    for each in team2:
      pcur.execute("SELECT * FROM players WHERE userid=?",(each,))
      user = pcur.fetchone()
      user=list(user)

      if user[4] + user[5] >= 5:
        user[8] = False
        pcur.execute("UPDATE players SET placements = ? WHERE userid= ?",(user[8],each,))
        pconn.commit()

      user[7] = calcStreak(user,True)
      pcur.execute("UPDATE players SET winstreak = ? WHERE userid= ?",(user[7],each,))
      pconn.commit()
      bonus = calcBonus(user,True)
      pcur.execute("UPDATE players SET bonus = ? WHERE userid= ?",(bonus,each,))
      pconn.commit()

      if user[8] == True:
        pcur.execute("UPDATE players SET wins = ? WHERE userid= ?",(int(user[4]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]+35+bonus),each,))
        pconn.commit()
      else:
        pcur.execute("UPDATE players SET wins = ? WHERE userid= ?",(int(user[4]+1),each,))
        pcur.execute("UPDATE players SET elo = ? WHERE userid= ?",(int(user[6]+t2+bonus),each,))
        pconn.commit()

def calcStreak(user, win):

  if user[7] >= 0 and win == True:
    return user[7] + 1

  if user[7] > 0 and win == False:
    return -1

  if user[7] <= 0 and win == False:
    return user[7] - 1

  if user[7] < 0 and win == True:
    return 1

  return 0

def calcBonus(user, win):
  
  bonus = user[9]
  streak = user[7]

  if streak >= 2:
    bonus = bonus + 5
    if bonus > 15:
      bonus = 15
    return bonus
  
  if streak <= -2:
    bonus = bonus - 5
    if bonus < -15:
      bonus = -15
    return bonus

  return 0

def checkFinal(matchid):
  mc.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mc.fetchone()

  string = match[11]
  temp = list(string.split("‰"))

  team1 = list(match[2].split("‰"))
  team2 = list(match[3].split("‰"))

  t1count = 0
  t2count = 0

  for each in temp:
    if each in team1:
      t1count = t1count +1

    elif each in team2:
      t2count = t2count +1

  if t1count >= 2 and t2count >= 2:
    return True
  else:
    return False

def rankIcon(elo):

  elo = int(elo)

  meat =  "<:aovmeat:814672185477169162>"
  bronze = "<:aovbronze:814671100377169981>"
  silver = "<:aovsilver:814671960588025886>"
  gold = "<:aovgold:814672091743780876>"
  diamond = "<:aovdiamond:824357703395573811>"
  placements = "<:WaitWhat:722327247247114270>"


  if elo < 850:
    return meat
  elif elo >= 850 and elo < 1000:
    return bronze
  elif elo >= 1000 and elo < 1200:
    return silver
  elif elo >= 1200 and elo < 1500:
    return gold
  elif elo >= 1500:
    return diamond
  else:
    return ":WaitWhat:"
    
def timesup(matchid):

  mconn = sqlite3.connect("matches.db")
  mcur = mconn.cursor()

  pconn = sqlite3.connect("players.db")
  pcur = pconn.cursor()

  mcur.execute("SELECT * FROM matches WHERE matchid=?",(matchid,))
  match = mcur.fetchone()
  team1 = list(match[2].split("‰"))
  team2 = list(match[3].split("‰"))
  if match[10] != 0 and match[12] == False:
    calculateElo(matchid,mcur,mconn,pcur,pconn)
    mcur.execute("UPDATE matches SET final = ? WHERE matchid= ?",(True,matchid,))
    
    for each in team1:
      pcur.execute("UPDATE players SET live = ? WHERE userid= ?",(False, each,))

    for each in team2:
      pcur.execute("UPDATE players SET live = ? WHERE userid= ?",(False, each,))
      
    pconn.commit()
    mconn.commit()
    print("Team " + str(match[10]) + " has been awarded the win for match #" + str(matchid))

  elif match[10] == 0 and match[12] == False:
    print("Match #" + str(matchid) + " is disputed. or not reported.")

  else:
    print("Something went wrong")
client.run("TOKEN")