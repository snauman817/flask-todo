from . import item

class Manager(object):

    def __init__(self, item_list=[]):
        self.item_list = item_list

    def add_item(self, task):
        self.item_list.append(item.Item(task))

    # maybe do this later? could be on page too
    # def list_items(self):

