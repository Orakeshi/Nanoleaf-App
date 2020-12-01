import requests
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
import time
from kivy.clock import Clock
import schedule
from steam import globalid
import threading
import GetIP
from datetime import datetime
from datetime import timedelta
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup #Importing the Popup feature for the GUI
#----------------------------------------------ESSENTIAL IMPORTS----------------------------------------------------------------------------------
global UniversalIP
global UniversalAuthCode
global defaultPort
defaultPort = "16021"
UniversalIP = GetIP.UniversalIP.rstrip()
UniversalAuthCode = GetIP.UniversalAuthCode.rstrip()



def cool():
    if UniversalIP == "" and UniversalAuthCode=="":
        sm.current = "leafchecker"
    else:
        sm.current = "main"

def RefreshIP():
    file = open(r'\\TOMMY-PC\Work - GameDev\Solarflare\Nanoleaf\NanoLeafData.txt', "r")
    firstLine = file.readline()
    lines = file.readlines()
    try:
        NewUniversalIP = str(firstLine)
        NewUniversalAuthCode = str(lines[0])
        return NewUniversalIP, NewUniversalAuthCode
    except:
        file.close()


class mainMenu(Screen):
    def CheckIfOn(self):
        threading.Timer(0.5, self.CheckIfOn).start()
        TestUniversalIP, TestUniversalAuthCode = RefreshIP()

        #NewUniversalIP =
        #NewUniversalAuthCode=

        response = requests.get("http://"+str(TestUniversalIP.rstrip())+":"+defaultPort+"/api/v1/"+str(TestUniversalAuthCode.rstrip())+"/state/on")
        new = str(response.json())
        wow = new.replace('{', '').replace("value", '').replace(":", '').replace(" ", '').replace("'", '').replace("{", '').replace("}", '')
        if wow == "True":
            self.online.opacity = 100
            self.offline.opacity = 0
            #self.switch.active = True

        else:
            self.offline.opacity = 100
            self.online.opacity = 0
            #self.switch.active = False

    def switch_on(self):
        onData = '{"on": {"value": true}}'
        TestUniversalIP, TestUniversalAuthCode = RefreshIP()
        newResponse = requests.put("http://"+str(TestUniversalIP.rstrip())+":"+defaultPort+"/api/v1/"+str(TestUniversalAuthCode.rstrip())+"/state", onData)
        self.CheckIfOn()

    def switch_off(self):
        onData = '{"on": {"value": false}}'
        TestUniversalIP, TestUniversalAuthCode = RefreshIP()
        newResponse = requests.put("http://"+str(TestUniversalIP.rstrip())+":"+defaultPort+"/api/v1/"+str(TestUniversalAuthCode.rstrip())+"/state", onData)
        self.CheckIfOn()

    def red(self):
        Red = '{"write" : {"command": "display","animType": "static","animData": "1 2 1 255 0 0 0 1","loop": false}}'
        TestUniversalIP, TestUniversalAuthCode = RefreshIP()
        newResponse = requests.put("http://"+str(TestUniversalIP.rstrip())+":"+defaultPort+"/api/v1/"+str(TestUniversalAuthCode.rstrip())+"/effects", Red)

    def PanelLayoutOpen(self):
        sm.current = "panellayout"

    def on_enter(self, *args):
        status = ObjectProperty(None)
        self.CheckIfOn()

class addNanoLeaf(Screen):
    ip = ObjectProperty(None)
    authCode=ObjectProperty(None)
    def getCode(self):
        global defaultPort
        IP = self.ip.text
        AuthCode = self.authCode.text

        file = open(r'\\TOMMY-PC\Work - GameDev\Solarflare\Nanoleaf\NanoLeafData.txt', "w")

        try:
            response = requests.post("http://"+str(IP)+":"+str(defaultPort)+"/api/v1/new")
            new = (str(response.json()))
            wow = new.replace("'", '').replace(":", '').replace("auth_token", '').replace("{", '').replace("}", '').lstrip()

            file.write(str(IP+'\n'))
            file.write(str(wow))
            self.authCode.text = str(wow)
            file.close()
            sm.current="main"

        except:
            pop = Popup(title="ERROR - Request not Sent!", content=Label(text="Hold down power button for 5-7 seconds until LED flashes""\n""\n""      Try Again!!!"), size_hint=(None, None), size=(400,400))
            pop.open()
            sm.current = "addleaf"

        #http://192.168.x.x:16021/api/v1/:auth_token/panelLayout/layout
        #AuthCodes Generated for testing below
        #3a4d2U9SuMy1yob8IWZAq7O2LChYpT9C
        #v1Ny5ticKHO3B6StHNqMqnul3iO2UniZ
        #bAPejmqpLVVPEBcEFd1WG2wSN0BEv1f2
        #2tx6bvz6jV397bg2QiVX2vUs5E9zZcms
        #zmeXKIYzCxJeWysjtKDbaNeOHLWHk3gt
        #bM4QaxSLrI0bpqJhdxzm7ufCi1HW040I

class panelLayout(Screen):

    def GetPanelIDS(self):
        f = open(r"\\TOMMY-PC\Work - GameDev\Solarflare\Nanoleaf\Panel_IDS.txt", "r")
        contents = f.readlines()
        self.ids.main_label.text = str(contents)

        print (str(contents))



    def on_enter(self, *args):
        TestUniversalIP, TestUniversalAuthCode = RefreshIP()
        newResponse = requests.get("http://"+str(TestUniversalIP.rstrip())+":"+defaultPort+"/api/v1/"+str(TestUniversalAuthCode.rstrip())+"/panelLayout/layout")
        f = open(r"\\TOMMY-PC\Work - GameDev\Solarflare\Nanoleaf\Panel_IDS.txt", "w")
        new = (str(newResponse.json()))
        wow = new.replace("'", '').replace(":", '').replace("auth_token", '').replace("{", '').replace("}", '').lstrip()
        f.write(wow)
        self.GetPanelIDS()

class existingNanoLeaf(Screen):
    ip = ObjectProperty(None)
    authCode=ObjectProperty(None)

    def addData(self):
        global defaultPort
        IP = self.ip.text
        AuthCode = self.authCode.text

        file = open(r'\\TOMMY-PC\Work - GameDev\Solarflare\Nanoleaf\NanoLeafData.txt', "w")
        file.write(str(IP+'\n'))
        file.write(str(AuthCode))

        file.close()
        sm.current="main"

class leafChecker(Screen):
    def existingUser(self):
        sm.current = "existingleaf"

    def newUser(self):
        sm.current = "addleaf"

class WindowManager(ScreenManager): #This class hold all the windows in
    pass #When script run and class is open pass to next line

kv = Builder.load_file("my.kv")  # Load up the kivy style sheet file


#------------------------ALL RELATED TO THE WINDOWS-----------------------------------------------------------------------------------------------
sm = WindowManager() #Store the Window manager in a variable called sm

screens = [leafChecker(name="leafchecker"),addNanoLeaf(name="addleaf"), mainMenu(name="main"), existingNanoLeaf(name="existingleaf"), panelLayout(name="panellayout")] #List of all the current windows and there names they are assigned to
for screen in screens: #Kivy uses widgets to write screens - For the current screen in the list of screens ...
    sm.add_widget(screen) #Write all screens [Create each screen as a widget]

cool() #When the script is run the current window displayed is the scan window

#-------------------------BELOW ARE ESSENTIAL IN ORDER TO RUN THE KIVY APP------------------------------------------------------------------------
class MyMainApp(App): #This class hold the entire aplication - the class named "MyMainApp" holds the APP [Whole script]
    def build(self): #This procedure builds the entire app
        return sm # Return the file when building the app
Window.size = (900, 600)
if __name__ == "__main__":
    MyMainApp().run() #Runs the app

rawData = '{"on": {"value": true}}'
rawData2 = '{"hue" : {"value":10}}'
rawData3 = '{"select" : "Fireworks"}'
