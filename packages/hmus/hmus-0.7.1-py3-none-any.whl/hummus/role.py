class Role:
  def __init__(self,data):
    self.id = data['id']
    self.name = data['name']
    self.color = data['color']
    from .permissions import Permissions #circular import begone
    self.permissions = Permissions(data['permissions'])
    self.mentionable = data['mentionable']
    self.hoist = data['hoist']
    self.position = data['position']

  def toDict(self):
    return {"id":self.id, "name":self.name, "color":self.color, "permissions":self.permissions.value, "mentionable":self.mentionable, "hoist":self.hoist,"position":self.position}

class FakeRole: #this is really used to provide a placeholder for top role comparison in funcs.py
  def __init__(self,position):
    self.position = position