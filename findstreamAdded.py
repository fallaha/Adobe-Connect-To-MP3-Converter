import elementpath
import xml.etree.ElementTree as ET

def finTotalTime():
    pass
def findStreamAddedInYourDestination(path = "",typeFinding="findStreamAddedInYourDestination"):
    name=""
    startTime=""
    totalTime=""
    audios=[]
    finalizeTime=False
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        nextInvisted=False
        for child in root:
            if finalizeTime ==False:
                totalTime = child.attrib
            for childChild in child:
                if nextInvisted and childChild.tag=="Array":

                    for myObject in childChild.findall('Object'):
                        startTime = myObject.find("startTime").text
                        name = myObject.find("streamName").text
                        tempDict={"name":name,"startTime":startTime}
                        audios.append(tempDict)


                    
                    nextInvisted=False

                if childChild.tag=="String" and childChild.text=="streamAdded" :

                    nextInvisted =True#next one tag should be visited becaus condition are hold
                if childChild.tag == "String":
                    if childChild.text == "__stop__":
                        finalizeTime=True
    except:
        print("there is an error in your file")
    if typeFinding=="findStreamAddedInYourDestination" :
        return audios
    elif typeFinding == "totalTime":
        try:
           totalTime =  totalTime["time"]
           return totalTime
        except:
            return None
        


print(findStreamAddedInYourDestination("C:\\Users\\rahimi\\Documents\\1\\mainstream.xml","findStreamAddedInYourDestination"))
print(findStreamAddedInYourDestination("C:\\Users\\rahimi\\Documents\\1\\mainstream.xml","totalTime"))