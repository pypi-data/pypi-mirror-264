from klang_valley_transit.trainNetwork import TrainNetwork
from klang_valley_transit.trainNetwork import SearchFilter, LineNameEnum

t = TrainNetwork()
[fromID,toID], Error = t.getRandomVerticesID(2)
if Error: raise(Error)
print(fromID,toID)

res,err = t.breadthFirstSearch(fromID,toID)
if err : raise(err)
print("explored : ",res.explored )
print("path : ",res.path)

s,err = t.ListStation(SearchFilter(line_name=LineNameEnum.AG, code="AG11"))
if err: raise(err)
print(s)
