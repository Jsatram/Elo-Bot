import multiprocessing
import time
from datetime import datetime
import pytz

t_zone = pytz.timezone('US/Central')

class Player:
  def __init__(self, username, userid, matchid=0,live=False,wins=0,losses=0,elo=1000):
    self.username = username #discord username
    self.userid = userid #discord user id #
    self.matchid = matchid #id of current or last match
    self.live = live  #boolean if player is in match
    self.wins = wins #number of wins
    self.losses = losses #number of losses
    self.elo = elo #current elo
  
class Match:
  def __init__(self, matchid, matchtime, team1, team2, hpmap, sndmap, ctrlmap, cancelr=False, canceled = False, cancelteam = [], result=0, reported = [], final = False):
    self.matchid = matchid #match id number
    self.matchtime = matchtime #match time

    self.team1 = team1 #list of players on team 1
    self.team2 = team2 #list of players on team 2

    self.hpmap = hpmap #harpoint map for match
    self.sndmap = sndmap #snd map for match
    self.ctrlmap = ctrlmap #ctrl map for match
    self.cancelr = cancelr #cancel request
    self.canceled = canceled
    self.cancelteam = cancelteam
    self.result = result #result of who won match (1 for team 1 or 2 for team 2)
    self.final = final #boolean if match has been finalized
    self.reported = reported
    self.reported.clear()
    

  def requestcancel(self,username):

    if username in self.team1:
      self.cancelteam = self.team1
      self.cancelr = True
    elif username in self.team2:
      self.cancelteam = self.team2
      self.cancelr = True
  
  def matchinfo(self):
    print("Matchid: " + str(self.matchid))
    print("Match time: " + str(self.matchtime.strftime("%m/%d/%Y, %H:%M")))

    for each in self.team1:
      print("team 1: " + each.username)
    for each in self.team2:
      print("team 2: " + each.username)

    print("hp map: " + self.hpmap)
    print("snd map: " + self.sndmap)
    print("ctrl map: " + self.ctrlmap)
   
    print("Cancel request: " + str(self.cancelr))
    print("Canceled: " + str(self.canceled))

    for each in self.cancelteam:
      print("cancel team: " + each.username)

    print("result: " + str(self.result))

    for each in self.reported:
      print("reported: " + each)

    print("final: " + str(self.final))

  def getPlayers(self):
    players = []
    players.append(self.team1)
    players.append(self.team2)
    return players
  
  def showmatch(self):
    current_time = self.matchtime.strftime("%m/%d/%Y, %H:%M")
    msg = ""
    msg = "Match #" + str(self.matchid) + ": " + str(current_time) + "\n"
    msg = msg + "======================== \n" + "Team 1: \n" 
    msg = msg + self.team1[0].username + " " + str(self.team1[0].elo) + "\n"
    msg = msg + self.team1[1].username + " " + str(self.team1[1].elo) + "\n"
    msg = msg + self.team1[2].username + " " + str(self.team1[2].elo) + "\n"
    msg = msg + self.team1[3].username + " " + str(self.team1[3].elo) + "\n"
    msg = msg + "======================== \n" + "Team 2: \n"
    msg = msg + self.team2[0].username + " " + str(self.team2[0].elo) + "\n"
    msg = msg + self.team2[1].username + " " + str(self.team2[1].elo) + "\n"
    msg = msg + self.team2[2].username + " " + str(self.team2[2].elo) + "\n"
    msg = msg + self.team2[3].username + " " + str(self.team2[3].elo) + "\n" 
    msg = msg + "======================== \n" 
    msg = msg + "Harpoint: " + str(self.hpmap) +"\n"
    msg = msg + "Search and Destroy: " + str(self.sndmap) +"\n"
    msg = msg + "Control: " + str(self.ctrlmap) +"\n"
    msg = msg + "======================== \n" 
    if self.result == 0:
      msg = msg + "Winners: N/A \n"
    else:
      msg = msg + "Winners: Team "+ str(self.result) + " \n"
    if(self.canceled):
      msg = msg + "*CANCELED* \n"

    if(self.final):
      msg = msg + "*FINAL* \n"

    return msg