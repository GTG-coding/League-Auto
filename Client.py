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

def main(autoaccept,autoban,autochamppick,ban,champ1,champ2): #the main function, does it all
    accepted = False
    ingame = False
    inchampselect = False
    
    while ingame == False:
        if locate('inmenu') and accepted == True: ##checks to see if player is in menu after accept
            print('player is back in menu, resetting')
            accepted = False
            ingame = False
            inchampselect = False
        elif accepted == False: ##checks for accept button
            print('Looking for accept button..')
            if locate('accept'):
                ghostclick('accept')
                accepted = True
        elif inchampselect == False and accepted == True: ##checks to see if player is in champ select
            print('Ensuring player reaches champ select phase')
            if locate('champmenu'):
                print('player is now in champ select')
                inchampselect = True
            if autoban == True and inchampselect == True:
                ban_pick(ban)
            if autochamppick == True and inchampselect == True:
                champ_pick(champ1,champ2)
        elif ingame == False and inchampselect == True: ##checks to see if player is in game
            print('Ensuring player reaches game phase')
            if locate('ingame'):
                print('player is now in game')
                ingame = True

def ban_pick(ban): #bans picks
    champbanned = False    
    while champbanned == False:
        if locate('inmenu'): ##checks to see if player is in menu after accept
            print('player is back in menu, resetting')
            break
            ##add reset here
        elif champbanned == False:
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
    while champselected == False:
        if locate('inmenu'):
            print('player is back in menu, resetting')
            break
            ##add reset here
        elif champselected == False:
            print("Checking for champ selection phase...")
            if locate('selectchamplabel'):
                print("Champ selection started, finding search bar...")
                if locate('champsearch2'):               #champsearch is transparent, need another image
                    print("Found searchbar, typing champ pick choice..")
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
t_ban = content[1]
t_champselect = content[2]
champ1 = content[3]
champ2 = content[4]
ban = content[5]

#prints
if sameversion == True:
    print(f'Version: {version} | UP TO DATE')
elif sameversion == False:
    print(f'Version: {version} | OUTDATED, UPDATE AT: {url}')
print('League-Auto | ENJOY')
print(' ')
print('TOGGLES:')
print(f'Auto accept: {t_aa} | Auto Ban: {t_ban} | Auto champ select: {t_champselect}')
print('PREFERENCES:')
print(f'Champs: {champ1},{champ2} | Bans: {ban}')
print(' ')
print('OUTPUT:')

#window_title = 'League of Legends'
#hwnd = win32gui.FindWindow(None, window_title)
#win32gui.SetForegroundWindow(hwnd)


#starting the engines
t3 = threading.Thread(target=ban_pick,args=(ban))
t4 = threading.Thread(target=champ_pick,args=(champ1,champ2))

#checks the settings for on/off
autoaccept = False
autoban = False
autochamppick = False
if t_aa == "ON":
    autoaccept = True #auto accept
if t_ban == "ON":
    autoban = True #ban pick
if t_champselect == "ON":
    autochamppick = True #champ pick

main(autoaccept,autoban,autochamppick,ban,champ1,champ1)


#TO DO#
#fix the autoban and autochamppick:
 #ensure code doesnt get stuck anywhere if someone dodges during a part
 
