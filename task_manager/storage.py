class InMemoryStage():
    def __init__(self):
        self.data = {}

    def add(self,id,item):
        self.data[id] = item

    def get(self,id):
        return self.data.get(id)
    
    def get_all(self,id):
        return list(self.data[id])
        
    def delete(self,id):
        if id in self.data:
            self.data.pop(id)
            return True
        return False

    def clear(self):
        self.data.clear()