import json


user = json.loads('{"id":100, "name":"송승수"}')

# print(f'username is {user["name"]}') 


def userinfo(u):
    id = u["id"]
    name = u["name"]
    return f'ID is {id}, Name is {name}'

print(f'User Infomation: {userinfo(user)}')