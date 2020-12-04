file = open(r'\\TOMMY-PC\Work - GameDev\Solarflare\Nanoleaf\NanoLeafData.txt', "r+")

firstLine = file.readline()
lines = file.readlines()

if firstLine!="":
    UniversalIP = str(firstLine)
    UniversalAuthCode = str(lines[0])

else:
    UniversalIP = ""
    UniversalAuthCode = ""

file.close()

#while True:
    #if lines :
        #file.write("\n"+"HELLO")
        #break
    #else:
        #break



