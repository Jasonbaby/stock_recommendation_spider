
class Content():
    """docstring for content"""
    def __init__(self, id, timestamp, content):
        self.id = id
        self.timestamp = timestamp
        self.content = content



class Question():
    def __init__(self, timestamp, content, id = 0):
        self.id = id
        self.q_timestamp = timestamp[0]
        self.question = content[0]
        if(len(timestamp) > 1 and len(content) > 1):
            self.a_timestamp = timestamp[1]
            self.answer = content[1]