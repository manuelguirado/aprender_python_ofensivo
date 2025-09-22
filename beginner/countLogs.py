import json 
with open("/var/log/boot.log", "r", encoding="utf-8") as path:
    #status of the logs
    estados =  ["FAILURE", "ERROR","OK"]
    #read the lines
    readFile = path.readlines()
    for line in readFile:     
        #check if any log contain the status
       if any(estado in line for estado in estados):
         cleanOuput = line.replace("\n", "")
         print(json.dumps(cleanOuput))
           
                 

