import json 
with open("/var/log/boot.log", "r", encoding="utf-8") as path:
    estados =  ["FAILURE", "ERROR","OK"]
    readFile = path.readlines()
    for line in readFile:     
       if any(estado in line for estado in estados):
         cleanOuput = line.replace("\n", "")
         print(json.dumps(cleanOuput))
           
                 

