from .queue import Queue
from .stack import Stack
import json

from typing import Dict

class Graph:
    def __init__(self):
        self.edges = {}
        self.vertices = {}
        
    def addVertices(self,doc:Dict):
        try:
            if(not doc.get("id")): raise Exception("data.id is required")
            
            #parsing and checking
            doc["id"] = str(doc["id"])
            found = self.vertices.get(doc["id"]) 
            if(found):raise Exception("duplicated Insert")
            
            # Create
            self.vertices[doc["id"]] = doc
            
        except Exception as error:
             print(str(error))
                
    def addEdges(self,fromID:str,toID:str,EdgeProps):
        try:
            #Validation and parsing
            if(not fromID): raise Exception("fromID is required")
            if(not toID): raise Exception("toID is required")
            fromID = str(fromID)
            toID = str(toID)

            if(not self.vertices.get(fromID)): raise Exception(f"vertices with fromID({fromID}) not exist")
            if(not self.vertices.get(toID)): raise Exception(f"vertices with toID({toID}) not exist")

            #Initialization
            if(not self.edges.get(fromID)): self.edges[fromID] = {}
            if(not self.edges.get(fromID).get(toID)): self.edges[fromID][toID] = {}

            #Create
            if(EdgeProps): self.edges[fromID][toID]  = EdgeProps

        except Exception as error:
             print(str(error))
        
    def load(self,path:str):
        try:
            with open(path) as json_file:
                parsedData = json.load(json_file)
                if(not parsedData.get("edges")): raise Exception("there is no edges in the file")
                if(not parsedData.get("vertices")): raise Exception("there is no vertices in the file")
        
            self.edges = parsedData.get("edges")
            self.vertices = parsedData.get("vertices")
            print("loaded edges and vertices")
        except Exception as error:
            print(str(error))
            
    def save(self,path:str):
        try:
            json_object = json.dumps({
                "edges": self.edges,
                "vertices": self.vertices
            }, indent=4)
            
            with open(path, "w") as outfile:
                outfile.write(json_object)
        except Exception as error:
            print(str(error))