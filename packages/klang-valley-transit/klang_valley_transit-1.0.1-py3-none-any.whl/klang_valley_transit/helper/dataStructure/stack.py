from typing import List

class Stack:
    def __init__(self, array:List=[]):
        self.array = array.copy()
        
    def push(self,doc):
        self.array.append(doc)
        
    def pop(self):
        return self.array.pop()
    
    def reverse(self):
        self.array.reverse()
    
    def show(self):
        print(self.array)
        
    def isEmpty(self):
        return len(self.array)==0