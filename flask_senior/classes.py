class FormInput:
    def __init__(self, id, name, value, checked, text):
        self.id = id
        self.name = name
        self.value = value
        self.checked = checked
        self.text = text
        

class Nav:
    def __init__(self, title, url='#', children=[]):
        self.title = title
        self.url = url
        self.children = children
