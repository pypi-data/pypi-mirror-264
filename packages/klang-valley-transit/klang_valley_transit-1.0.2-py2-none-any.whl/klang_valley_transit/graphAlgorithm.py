from .helper.dataStructure.graph import Graph
from .helper.dataStructure.queue import Queue
from .helper.dataStructure.stack import Stack
from typing import List, Union
from pydantic import BaseModel
import numpy as np

class SearchResponse(BaseModel):
    explored: List[str]
    path: Union[List[str],List[dict]]

class ErrorResponse(BaseModel):
    err:str 
    errInfo:List[str]

class GraphAlgorithm(Graph):
    def __init__(self):
        super().__init__()
        
    def breadthFirstSearch(self,fromID:str,toID:str,fetch_vertices:bool=True):
        try:
            #Validation and parsing
            if(not fromID): raise Exception("fromID is required")
            if(not toID): raise Exception("toID is required")
            fromID = str(fromID)
            toID = str(toID)
    
            if(not self.edges.get(fromID)) : raise Exception(f"there is no edges start with fromID : {fromID}")
            fromIDs = list(self.edges.keys())
            found = [from_id for from_id in fromIDs if self.edges.get(from_id).get(toID)]
            if(len(found) == 0): raise Exception(f"there is no edges end with toID : {toID}")

            # early return
            if(fromID==toID): return SearchResponse(**{"explored":[fromID], "path":[toID]}),None

            #Initialization
            queue = Queue()
            queue.enqueue(fromID)
            visited = []
            backTraceEdge = {}
            

            #iteration : explore path
            while(not queue.isEmpty() ):
                currentNodeID = queue.dequeue()

                if(currentNodeID not in visited): visited.append(currentNodeID)
                
                #early pruning
                if(currentNodeID == toID): break
                if(not self.edges.get(currentNodeID)): continue
                nextNodeIDs = list(self.edges.get(currentNodeID).keys()) 

                for nextNodeID in nextNodeIDs:
                    if(nextNodeID not in visited ): backTraceEdge[nextNodeID] = currentNodeID
                    if(nextNodeID not in visited):  queue.enqueue(nextNodeID)

            #iteration : back Tracing
            backTracePath = Queue([])
            backTracePath.enqueue(toID)
            currentID = toID
            reached = False
            
            while(not reached):
                previousID = backTraceEdge.get(currentID)
                if(previousID not in backTracePath.array): backTracePath.enqueue(previousID)
                if(previousID==fromID):
                    reached = True 
                    break #stopping condition
                currentID = previousID
               
                 
            backTracePath.reverse()
            path = backTracePath.array if fetch_vertices == False else [ self.vertices[verticesID] for verticesID in backTracePath.array]
            return SearchResponse(**{"explored":visited, "path":path}), None 
        
        except Exception as error:
            print(error)
            return None, ErrorResponse(**{"err":str(error), "errInfo":["class GraphAlgorithm","method breadthFirstSearch"]})
        
    def depthFirstSearch(self,fromID:str,toID:str,fetch_vertices:bool=True):
        try:
            #Validation and parsing
            if(not fromID): raise Exception("fromID is required")
            if(not toID): raise Exception("toID is required")
            fromID = str(fromID)
            toID = str(toID)
    
            if(not self.edges.get(fromID)) : raise Exception(f"there is no edges start with fromID : {fromID}")
            fromIDs = list(self.edges.keys())
            found = [from_id for from_id in fromIDs if self.edges.get(from_id).get(toID)]
            if(len(found) == 0): raise Exception(f"there is no edges end with toID : {toID}")

            # early return
            if(fromID==toID): return SearchResponse(**{"explored":[fromID], "path":[toID]}), None 
            #Initialization
            stack = Stack()
            stack.push(fromID)
            visited = []
            backTraceEdge = {}
            

            #iteration : explore path
            while(not stack.isEmpty() ):
                currentNodeID = stack.pop()

                if(currentNodeID not in visited): visited.append(currentNodeID)

                if(not self.edges.get(currentNodeID)): continue
                nextNodeIDs = list(self.edges.get(currentNodeID).keys()) 

                for nextNodeID in nextNodeIDs:
                    if(nextNodeID not in visited): backTraceEdge[nextNodeID] = currentNodeID
                    if(nextNodeID not in visited):  stack.push(nextNodeID)
                
                #early pruning
                if(currentNodeID == toID): break


            #iteration : back Tracing
            backTracePath = Queue([])
            backTracePath.enqueue(toID)
            currentID = toID
            reached = False
            while(not reached):
                previousID = backTraceEdge[currentID]; 
                backTracePath.enqueue(previousID)
                if(previousID==fromID): reached = True
                if(previousID==fromID): break; #stopping condition
                currentID = previousID
            backTracePath.reverse()
            path = backTracePath.array if fetch_vertices == False else [ self.vertices[verticesID] for verticesID in backTracePath.array]
            return SearchResponse(**{"explored":visited, "path":path}), None 
        
        except Exception as error:
            return None, {"err":str(error), "errInfo":["class GraphAlgorithm","method depthFirstSearch"]}
        
    def getRandomVerticesID(self,size=5):
        try:
            randomIDs = []
            sampleSpace = list(self.vertices.keys())
            sampleSize = len(sampleSpace)
            
            while(len(randomIDs) != size):
                randPosition = int(np.floor(np.random.rand()*sampleSize))
                randID = sampleSpace[randPosition]
                found = [d for d in randomIDs if d == randID]
                if len(found)==0 : randomIDs.append(randID)
            return randomIDs, None
        except Exception as error:
            return None, ErrorResponse(**{"err":str(error), "errInfo":["class GraphAlgorithm","method getRandomVerticesID"]})