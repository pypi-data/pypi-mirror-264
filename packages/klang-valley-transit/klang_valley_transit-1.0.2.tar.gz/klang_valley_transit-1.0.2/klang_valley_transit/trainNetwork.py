from .graphAlgorithm import GraphAlgorithm
from .helper.distance.haversineDistance import HaversineDist
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path
from re import search, IGNORECASE

current_directory = CUR_DIR = Path(__file__).parent.absolute()

class LineNameEnum(str,Enum):
    AG = "AMPANG_LRT"
    KJ = "KELANA_JAYA_LRT"
    SP = "SRI_PETALING_LRT"
    KG = "KAJANG_MRT"
    PY = "PUTRAJAYA_MRT"
    ALL= "*"

LineCodeMap = {
    LineNameEnum.AG:r"AG",
    LineNameEnum.KJ:r"KJ",
    LineNameEnum.SP:r"SP",
    LineNameEnum.KG:r"KG",
    LineNameEnum.PY:r"PY",
}

class SearchFilter(BaseModel):
    code: Optional[str] = Field(default=None)
    station_name: Optional[str] = Field(default=None)
    line_name: LineNameEnum = Field(default="*")



class TrainNetwork(GraphAlgorithm):
    def __init__(self):
        super().__init__()
        self.load(f"{current_directory}/trainNetwork.save.json")

    def dataLoadingAndPreprocessing(self,data:Dict):
        try:
            # initialization
            Vertices = []
            Edges = []
            
            #load data
            # data = loadData()
            keys = list(data.keys())
            values = list(data.values())
            
            #process data
            for key in keys:
                for value in values:
                    if value.get(key) :
                        stations = value.get(key)
                        for i in range(len(stations)):
                            Vertices.append({ 
                                "id": stations[i]["id"],
                                "stationName": stations[i]["stationName"], 
                                "coordinate": stations[i]["coordinate"] 
                            })

                            #Station Edges
                            if(i<len(stations)-1):
                                fromID = stations[i]["id"]
                                toID = stations[i+1]["id"]

                                disRes = HaversineDist(stations[i]["coordinate"],stations[i+1]["coordinate"])
                                if(disRes.get("err")): raise Exception(f'haversine dist error : {str(disRes["err"])}' )
                                distance = disRes["res"]

                                #Bidirectional
                                Edges.append({ "fromID":fromID, "toID":toID, "distance":distance});
                                Edges.append({ "toID": fromID, "fromID": toID, "distance":distance});

                            # Interchange Station Edges
                            if(stations[i].get("interchangeStation")):
                                for itc in stations[i]["interchangeStation"]:
                                    distRes = HaversineDist(stations[i]["coordinate"],itc["coordinate"])
                                    if(distRes.get("err")): raise Exception("exec2 "+str(distRes.get("err")))
                                    dist = distRes["res"]

                                    Edges.append({"fromID": stations[i]["id"], "toID": itc["id"], "distance":dist})
                                 
            return {"Vertices":Vertices,"Edges":Edges}
 
                    
        except Exception as error:
            print("dataLoadingAndPreprocessing error: ",error)
            return {"err":str(error), "errInfo":["class TrainNetwork","method verticesAndEdgesPopulation"]}
            
    def verticesAndEdgesPopulation(self):
        try:
            loadRes = self.dataLoadingAndPreprocessing()
            if(loadRes.get("err")): raise Exception(loadRes.get("err"))
            Vertices = loadRes["Vertices"]
            Edges = loadRes["Edges"]
                
            for v in Vertices:
                self.addVertices(v)

            for e in Edges:
                fromID = e["fromID"] 
                toID = e["toID"]
                distance = e["distance"]
                self.addEdges(fromID, toID, {"distance":distance})

        except Exception as error:
            return {"err":str(error), "errInfo":["class TrainNetwork","method verticesAndEdgesPopulation"]}
        
    def ListStation(self,filter:SearchFilter):
        try:
            all_stations:List[Dict] = [value for value in self.vertices.values()]

            searched_line = all_stations if filter.line_name=="*" else [st for st in all_stations if search(LineCodeMap[filter.line_name],st.get("id")) is not None]
            searched_line = searched_line if filter.code is None else [st for st in searched_line if st.get("id") == filter.code]
            searched_line = searched_line if filter.station_name is None else [st for st in searched_line if search(filter.station_name,st.get("stationName"),IGNORECASE)]

            return searched_line,None
        except Exception as error:
            return None, error



# def getTrainNetwork()->TrainNetwork:  
#     print(getcwd())
#     trainNetwork = TrainNetwork() 
#     trainNetwork.load("./trainNetwork.save.json")
#     return trainNetwork

# t = getTrainNetwork()