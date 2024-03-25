from typing import List

class Queue:
    def __init__(self, array:List =[]):
        self.array = array.copy()
        
    def enqueue(self,doc):
        self.array.append(doc)
        
    def dequeue(self):
        return self.array.pop(0)
    
    def reverse(self):
        self.array.reverse()
    
    def show(self):
        print(self.array)
        
    def isEmpty(self):
        return len(self.array)==0