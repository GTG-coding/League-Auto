version = 'v1.0'

import requests #not default
from bs4 import BeautifulSoup #not default
import pyautogui #not default
import time
import keyboard #not default
import os, threading
#import win32gui

dirpath = os.path.dirname(os.path.abspath(__file__))
champselected = False

def img(imgname): #retruns full imgs path
    imgfolder = dirpath + '\\buttons\\'
    return imgfolder + imgname

def locate(imgname): #locate the given img x,y
    imgfolder = dirpath + '\\buttons\\'
    fullpath = imgfolder + imgname + '.png'
    return pyautogui.locateCenterOnScreen(fullpath)

def ghostclick(imgname): #Does a invisible click
    x,y = locate(imgname)
    mousepos = pyautogui.position()
    pyautogui.click(x,y)
    pyautogui.moveTo(mousepos)

def auto_accept(): #auto accepts games
    accepted = False
    while keyboard.is_pressed('q') == False:
        time.sleep(1)
        if accepted == False:
          #  print('Looking for accept title..')
           # if locate('accepttitle'):
            #    print('Found accept title!')
            print('Looking for accept button..')
            if locate('accept'):
                ghostclick('accept')
                break #currently is the way of stopping the print spam

def selectlane(givenlane): #selects lanes
    mousepos = pyautogui.position()
    if givenlane == 'MID':
        pyautogui.move(0,-90)
        pyautogui.click()
    if givenlane == 'JUNGLE':
        pyautogui.move(-70,-75)
        pyautogui.click()
    if givenlane == 'TOP':
        pyautogui.move(-90,0)
        pyautogui.click()
    if givenlane == 'ADC':
        pyautogui.move(70,-75)
        pyautogui.click()
    if givenlane == 'SUPPORT':
        pyautogui.move(90,0)
        pyautogui.click()

    pyautogui.moveTo(mousepos)

def startgame(firstlane,secondlane): #starts games
    print('Started Thread')
    while keyboard.is_pressed('q') == False:
        print('Loop beginning..')

        if locate('mainplay'):
            print('Mainplay was located')
            ghostclick('mainplay')
            continue

        #time.sleep(1.5)

        if locate('rankedcheck'):
            print('Checkbox was located')
            ghostclick('rankedcheck')
            continue

        if locate('quesubmit'):
            print('Beginning queue..')
            ghostclick('quesubmit')
            continue

        #time.sleep(2)

        if locate('partylabel'):
            print('in party')

            if locate('laneselect'):
                pyautogui.click(locate('laneselect'))
                time.sleep(1)
                selectlane(firstlane)
                continue

        #time.sleep(2)

        if locate('laneselect2'):
            print("located 2")
            pyautogui.click(locate('laneselect2'))
            time.sleep(1)
            selectlane(secondlane)
            continue

        #time.sleep(2)

        if locate('quesearch'):
            pyautogui.click(locate('quesearch'))
            print('Started Game.')
            continue

    print('Loop stopped..')

def ban_pick(ban): #bans picks
    champbanned = False    
    while keyboard.is_pressed('q') == False:
        time.sleep(1)
        if champbanned == False:
            print("Checking for banning phase...")
            if locate('banchamplabel'):
                print("Banning phase started, finding search bar...")
                if locate('bansearch2'):
                    print("found searchbar, typing ban choice")
                    pyautogui.click(locate('bansearch2'))
                    pyautogui.write(ban)
                    pyautogui.move(-460,60)
                    time.sleep(0.1)
                    pyautogui.click()          
                    time.sleep(0.1)
                if locate('bansubmit'):
                    pyautogui.click(locate("bansubmit"))
                    print('Champion banned!')
                    champbanned = True #currently is the way of stopping the print spam
                    break

def champ_pick(champ1,champ2): #chooses picks
    champselected = False
    while keyboard.is_pressed('q') == False:
        time.sleep(1)
        if champselected == False:
            print("Checking for champ selection phase...")
            if locate('selectchamplabel'):
                print("Champ selection started, finding search bar...")
                if locate('champsearch2'):               #champsearch is transparent, need another image
                    print("Found searchbar, typing ban choice..")
                    pyautogui.click(locate('champsearch2'))
                    pyautogui.write(champ1)
                    pyautogui.move(-460,60)
                    time.sleep(0.1)
                    pyautogui.click()
                    time.sleep(0.1)
            if locate('selectchamp'):
                pyautogui.click(locate('selectchamp'))
                print("Champion selected!")
                champselected = True #currently is the way of stopping the print spam
                break

#checking if client is up to date
getversion = ""
url = "https://github.com/GTG-coding/League-Auto" #link to github repo
response = requests.get(url)
status = response.status_code
html = BeautifulSoup(str(response.text),"html.parser")

getversion = str(html.find(attrs='Link--primary d-flex no-underline'))
toggle = False
content = ""

for letter in getversion:
    if toggle == True and not letter == '"':
        content += letter
    elif letter == '"' and toggle == False:
        toggle = True
    elif letter == '"' and toggle == True:
        content += " "
        toggle = False

content = content.split()
content = str(content[3])

getversion = ""

for letter in content:
    if toggle == True and not letter == '/':
        getversion += letter
    elif letter == '/' and toggle == False:
        toggle = True
    elif letter == '/' and toggle == True:
        getversion += " "
        toggle = False

getversion = getversion.split()
getversion = getversion[2]

if getversion == version:
    sameversion = True
else:
    sameversion = False

#checking the settings
toggle = False
content = ""
settings = open("settings.txt","r+")
for lines in settings:
    for letter in lines:
        if toggle == True and not letter == "'":
            content += letter
        elif letter == "'" and toggle == False:
            toggle = True
        elif letter == "'" and toggle == True:
            content += " "
            toggle = False
settings.close()

content = content.split(" ")            
for stuff in content:
    if stuff == '':
        content.remove(stuff)


#settings organizer which is chosen by the symbol: '
t_aa = content[0]
t_start = content[1]
t_ban = content[2]
t_champselect = content[3]
lane1 = content[4]
lane2 = content[5]
champ1 = content[6]
champ2 = content[7]
ban = content[8]

#prints
if sameversion == True:
    print(f'Version: {version} | UP TO DATE')
elif sameversion == False:
    print(f'Version: {version} | OUTDATED, UPDATE AT: {url}')
print('League Auto Accept PLUS | Support me here: https://www.paypal.com/paypalme/c1ose | ENJOY')
print(' ')
print('TOGGLES:')
print(f'Auto accept: {t_aa} | Auto start: {t_start} | Auto Ban: {t_ban} | Auto champ select: {t_champselect}')
print('PREFERENCES:')
print(f'Lanes: {lane1},{lane2} | Champs: {champ1},{champ2} | Bans: {ban}')
print(' ')
print('OUTPUT:')

#window_title = 'League of Legends'
#hwnd = win32gui.FindWindow(None, window_title)
#win32gui.SetForegroundWindow(hwnd)


#starting the engines
t1 = threading.Thread(target=auto_accept)
t2 = threading.Thread(target=startgame,args=(lane1,lane2))
t3 = threading.Thread(target=ban_pick,args=([ban]))
t4 = threading.Thread(target=champ_pick,args=(champ1,champ2))

#checks the settings for on/off
if t_aa == "ON":
    t1.start() #auto accept
if t_start == "ON":
    t2.start() #start game
if t_ban == "ON":
    t3.start() #ban pick
if t_champselect == "ON":
    t4.start() #champ pick
