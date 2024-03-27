from .role import Role

import fake_useragent
import requests
import json

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random

class Avatar:
  def __init__(self,id,avatar,cdn):
    self.id = id
    self.avatar = avatar
    self.url = f"{cdn}avatars/{self.id}/{self.avatar}.png"

class User:
  def __init__(self,instance,data,cdn,token,url,guild_id=None):
    self.instance = instance
    self.guild_id = guild_id
    self.base_url = url
    self.token = token
    self.id = data['id']
    self.username = data['username']
    self.discriminator = data['discriminator']
    self.mention = f"<@{data['id']}>"
    self.avatar = Avatar(self.id,data['avatar'],cdn)
    self.bot = data['bot']

  async def toDict(self):
    return {"id":self.id,"username":self.username,"discriminator":self.discriminator,"mention":self.mention,"avatar":self.avatar.url,"bot":self.bot}

  async def ban(self,reason=None,delete_message_days=0):
    if not self.guild_id:
      raise Exception("This user was not found in a guild.")
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'delete-message-days':int(delete_message_days),'reason':reason})
    requests.put(url=f"{self.base_url}guilds/{self.guild_id}/bans/{self.id}",headers=headers,data=data)

  async def unban(self):
    if not self.guild_id:
      raise Exception("This user was not found in a guild.")
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    requests.delete(url=f"{self.base_url}guilds/{self.guild_id}/bans/{self.id}",headers=headers)

  async def setRoles(self,roles:list):
    if type(roles[0]) == Role:
      roles = [role.id for role in roles]
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def removeRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    idx = 0
    for role in roles:
      if type(roles[0]) == Role:
        temp.remove(role.id)
      else:
        temp.remove(role)
      idx += 1
    roles = temp
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def addRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    if type(roles[0]) == Role:
      for role in roles:
        temp.append(role.id)
    else:
      for role in roles:
        temp.append(role)
    roles = temp
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def kick(self):
    headers = {
      'Authorization': f'Bot {self.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent
      }
    e = requests.delete(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}", headers=headers)
    return e

  async def nick(self,nick):
    headers = {
        'Authorization': f'Bot {self.token}',
        'Content-Type': 'application/json',
        'User-Agent': agent,
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    e = requests.patch(url=f"{self.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

class Member:
  def __init__(self,instance,data,cdn,token,url,guild):
    self.instance = instance
    self.guild_id = guild
    self.id = data['id']
    self.mention = f"<@{data['id']}>"
    self.nick = data['nick']
    self.roles = data['roles']
    self.joined_at = data['joined_at']
    self.deaf = data['deaf']
    self.mute = data['mute']
    self.user = User(instance,data['user'],cdn,token,url,guild)

  def toDict(self):
    return {"id":self.id, "nick":self.nick, "roles":self.roles,"joined_at":self.joined_at, "deaf":self.deaf, "mute":self.mute,"user":self.user.toDict()}

  async def ban(self,reason=None,delete_message_days=0):
    headers = {
      'Authorization': f'Bot {self.user.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'delete-message-days':int(delete_message_days),'reason':reason})
    e = requests.put(url=f"{self.user.base_url}guilds/{self.guild_id}/bans/{self.id}",headers=headers,data=data)

  async def unban(self):
    headers = {
      'Authorization': f'Bot {self.user.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    requests.delete(url=f"{self.user.base_url}guilds/{self.guild_id}/bans/{self.id}",headers=headers)

  async def setRoles(self,roles:list):
    if type(roles[0]) == Role:
      roles = [role.id for role in roles]
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.instance.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def removeRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    idx = 0
    for role in roles:
      if type(roles[0]) == Role:
        temp.remove(role.id)
      else:
        temp.remove(role)
      idx += 1
    roles = temp
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.instance.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def addRoles(self,roles:list):
    temp = []
    for guild in self.instance.allGuilds:
      if guild.id == self.guild_id:
        for member in guild.members:
          if self.id == member.id:
            temp = member.roles
    if type(roles[0]) == Role:
      for role in roles:
        temp.append(role.id)
    else:
      for role in roles:
        temp.append(role)
    roles = temp
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
    }
    data = json.dumps({'roles': roles})
    e = requests.patch(url=f"{self.instance.base_url}guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

  async def kick(self):
    headers = {
      'Authorization': f'Bot {self.instance.token}',
      'Content-Type': 'application/json',
      'User-Agent': agent,
      }
    e = requests.delete(url=f"{self.user.base_url}guilds/{self.guild_id}/members/{self.id}", headers=headers)
    return e

  async def nick(self,nick):
    headers = {
        'Authorization': f'Bot {self.user.token}',
        'Content-Type': 'application/json',
      'User-Agent': agent,
        }
    if nick == "None":
        data = json.dumps({'nick': ""})
    else:
        data = json.dumps({'nick': nick})
    e = requests.patch(url=f"{self.user.base_url}/guilds/{self.guild_id}/members/{self.id}",headers=headers,data=data)
    return e

class Presence:
  def __init__(self,instance,data,cdn,token,url,guild):
    self.instance = instance
    self.guild_id = guild
    self.game = data['game']
    self.status = data['status']
    self.user = User(instance,data['user'],cdn,token,url,guild)

  def toDict(self):
    return {"game":self.game,"status":self.status,"user":self.user.toDict()}