from .message import Message

import requests
import base64
import json

import fake_useragent

ua = fake_useragent.UserAgent(browsers=['chrome', "firefox", "opera", "safari", "edge", "internet explorer"])
agent = ua.random

class State:
	def __init__(self,instance):
			self.instance = instance

	async def update_avatar(self,file):
			headers = {
					'Authorization': f'Bot {self.instance.token}',
					'Content-Type': 'application/json',
					'User-Agent': agent
			}
			img = base64.b64encode(open(file,'rb').read()).decode('utf-8')
			data = {"avatar":f"data:image/png;base64,{img}"}
			e = requests.patch(f"{self.instance.base_url}users/@me/",json=data,headers=headers)
			return e.json()

	async def update_status(self,status=None,game=None):
			self.instance.connection.send(json.dumps({"op":3,"d":{"status":status,"game":{"name":game,"type":1}}}))

	async def add_friend(self,user):
			headers = {
					'Authorization': f'Bot {self.instance.token}',
					'Content-Type': 'application/json',
					'User-Agent': agent
			}
			e = requests.put(f"{self.instance.base_url}users/@me/relationships/{user}",headers=headers,json={"type":False})

	async def edit(self, channel_id, id, content):
		headers = {
				'Authorization': f'Bot {self.instance.token}',
				'Content-Type': 'application/json',
				'User-Agent': agent
		}
		data = {"content":content}
		r = requests.patch(f"{self.instance.base_url}channels/{channel_id}/messages/{id}",headers=headers,data=json.dumps(data))
		return Message(r.json(),self.instance.token,agent,self.instance.base_url,self.instance.cdn,self.instance,reply=False)