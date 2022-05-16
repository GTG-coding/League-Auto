version = 'v1.6'

import requests #not default
from bs4 import BeautifulSoup #not default
import pyautogui #not default
import time
import keyboard #not default
import os, threading
from win32gui import FindWindow, GetWindowRect #not default
import sys

dirpath = os.path.dirname(os.path.abspath(__file__))
champselected = False

def img(imgname): #retruns full imgs path
    imgfolder = dirpath + '\\buttons\\'
    return imgfolder + imgname

def locate(imgname, conf): #locate the given img x,y
    imgfolder = dirpath + '\\buttons\\'
    fullpath = imgfolder + imgname + '.png'
    return pyautogui.locateCenterOnScreen(fullpath, confidence=conf)

def ghostclick(imgname, conf): #Does a invisible click
    x,y = locate(imgname, conf)
    mousepos = pyautogui.position()
    pyautogui.click(x,y)
    pyautogui.moveTo(mousepos)

def main(autoaccept,autoban,autochamppick,ban,champ1,champ2): #the main function, does it all
    accepted = False
    ingame = False
    inchampselect = False
    
    while ingame == False:
        if locate('inmenu', 0.9) and accepted == True: ##checks to see if player is in menu after accept
            print('player is back in menu, resetting')
            accepted = False
            ingame = False
            inchampselect = False
        elif accepted == False: ##checks for accept button
            print('Looking for accept button..')
            if locate('accept', 0.9):
                ghostclick('accept', 0.9)
                accepted = True
        elif inchampselect == False and accepted == True: ##checks to see if player is in champ select
            print('Ensuring player reaches champ select phase')
            if locate('champmenu', 0.9):
                print('player is now in champ select')
                inchampselect = True
            if autoban == True and inchampselect == True:
                ban_pick(ban)
            if autochamppick == True and inchampselect == True:
                champ_pick(champ1,champ2)
        elif ingame == False and inchampselect == True: ##checks to see if player is in game
            print('Ensuring player reaches game phase')
            if locate('ingame', 0.9):
                print('player is now in game')
                ingame = True

def ban_pick(ban): #bans picks
    champbanned = False
    champclicked = False    
    while champbanned == False:
        if locate('inmenu', 0.9): ##checks to see if player is in menu after accept
            print('player is back in menu, resetting')
            break
            ##add reset here
        elif champbanned == False:
            print("Checking for banning phase...")
            if locate('banchamplabel', 0.9) and champclicked == False:
                print("Banning phase started, finding search bar...")
                if locate('bansearch2', 0.9):
                    print("found searchbar, typing ban choice")
                    pyautogui.click(locate('bansearch2', 0.9))
                    pyautogui.write(ban)
                    pyautogui.move(-460,60)
                    time.sleep(0.1)
                    pyautogui.click()
                    champclicked = True
                    time.sleep(0.1)
            elif locate('bansubmit', 0.9) and champclicked == True:
                pyautogui.click(locate("bansubmit", 0.9))
                print('Champion banned!')
                champbanned = True #currently is the way of stopping the print spam
                break

def champ_pick(champ1,champ2): #chooses picks
    champselected = False
    champclicked = False
    while champselected == False:
        if locate('inmenu', 0.9):
            print('player is back in menu, resetting')
            break
            ##add reset here
        elif champselected == False:
            print("Checking for champ selection phase...")
            if locate('selectchamplabel', 0.9) and champclicked == False:
                print("Champ selection started, finding search bar...")
                if locate('champsearch2', 0.9):               #champsearch is transparent, need another image
                    print("Found searchbar, typing champ pick choice..")
                    pyautogui.click(locate('champsearch2', 0.9))
                    pyautogui.write(champ1)
                    pyautogui.move(-460,60)
                    time.sleep(0.1)
                    pyautogui.click()
                    champclicked = True
                    time.sleep(0.1)
            elif locate('selectchamp', 0.9) and champclicked == True:
                pyautogui.click(locate('selectchamp', 0.9))
                print("Champion selected!")
                champselected = True #currently is the way of stopping the print spam
                break

#CHECKVERSION IS BROKEN FIX SOMETIME
"""
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
"""

#checking the settings
toggle = False
content = ""
settings = open(dirpath + "\\settings.txt","r+")
for lines in settings:
    for letter in lines:
        if toggle == True and not letter == "'":
            content += letter
        elif letter == "'" and toggle == False:
            toggle = True
        elif letter == "'" and toggle == True:
            content += "|"
            toggle = False
settings.close()

content = content.split("|")            
for stuff in content:
    if stuff == '':
        content.remove(stuff)

#checking if client size is 1600 x 900
if FindWindow(None, 'League of Legends'):
    league_client = FindWindow(None, 'League of Legends')
    window_size = GetWindowRect(league_client)
    realwindowsize = ''
    realwindowsize = str(window_size[2] - window_size[0])
    realwindowsize += ' x ' + str(window_size[3] - window_size[1])
    if realwindowsize != '1600 x 900':
        print(f'Window size is {realwindowsize}')
        print(f'Window size MUST BE 1600 x 900')
        print(' ')
        print(f'Please change window size in the league client settings to 1600 x 900')
        print(' ')
        timer = 10
        while timer != 0:
            print(f'client will close in {timer}')
            timer -= 1
            time.sleep(1)
        sys.exit()
else:
    print('League of legends is not opened, please open league before running the client')
    print(' ')
    timer = 5
    while timer != 0:
        print(f'client will close in {timer}')
        timer -= 1
        time.sleep(1)
    sys.exit()

#settings organizer which is chosen by the symbol: '
t_aa = content[0]
t_ban = content[1]
t_champselect = content[2]
champ1 = content[3]
champ2 = content[4]
ban = content[5]

#prints
#version checker bugged fix sometime
"""
if sameversion == True:
    print(f'Version: {version} | UP TO DATE')
elif sameversion == False:
    print(f'Version: {version} | OUTDATED, UPDATE AT: {url}')
"""
print(f'League-Auto | ENJOY | Version: {version}')
print(' ')
print('TOGGLES:')
print(f'Auto accept: {t_aa} | Auto Ban: {t_ban} | Auto champ select: {t_champselect}')
print('PREFERENCES:')
print(f'Champs: {champ1},{champ2} | Bans: {ban}')
print(' ')
print('OUTPUT:')

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
 
