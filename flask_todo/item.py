import datetime

class Item(object):

    def __init__(self, task, datetime_created=datetime.datetime.now, is_completed=False):
        self.task = task
        self.datetime_created = datetime_created
        self.is_completed = is_completed