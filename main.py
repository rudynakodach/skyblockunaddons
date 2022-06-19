import time
import requests
from requests import *
import PySimpleGUI as sg
import json
import webbrowser
import os
import pyautogui
import cv2
from PIL import ImageGrab
import numpy as np
import random

os.system("cls")

print("Starting INIT phase...")

chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser(chrome_path))


try:
    print("[+] Starting...")
    with open('apikey.txt', 'r') as f:
        print("[+] API Key found and read!")
        apikey = f.read()
        apikey = str(apikey)
except:
    print("[!] Error: No API key found!")
    with open('apikey.txt','w+') as f:
        print("[+] Creating API-Key file...")
        print("[+] Done!")
        print('[!] Please enter your API key:')
        apikey = input("Enter your API key: ")
        f.write(apikey)
        apikey = str(apikey)



print(f"Your API Key - {apikey}")

#apikey = "148671b2-ef98-426d-907d-58fca94b720a"

mainLayout = [
    [sg.Text("Wybierz tryb")],
    [sg.Combo(['Material calculator','Command macros','Quick Wiki','StatTrak','Igor'],key='-MODE-',default_value='Material calculator',size=(20,1))],
    [sg.Text("")],
    [sg.Button("Run",key='-RUN-')]
]

calcLayout = [
    [sg.Text("Ench na surowce")],
    [sg.Text("Wpisz ilość ench materiału: "),sg.InputText(key='-ENCH-NUM-',size=(6,1)),sg.Text('Ilość: '),sg.InputText("1",key='-ENCH-MULT-',size=(5,1))],
    [sg.Button("Przelicz",key='-CALC-E2R-')],
    [sg.Text("Ilośc surowych materiałów - "),sg.Text("",key='-ENCH-RESULT-')],
    [sg.Text("")],
    [sg.Text("Surowce na ench")],
    [sg.Text("Wpisz ilośc materiałów: "),sg.InputText(key='-MATERIAL-NUM-',size=(6,1)),sg.Text('Ilość: '),sg.InputText("1",key='-MAT-MULT-',size=(5,1))],
    [sg.Button("Przelicz",key='-CALC-R2E-')],
    [sg.Text("Ilośc ench materiałów: "),sg.Text("",key='-MATERIAL-RESULT-')],
    [sg.InputText("",key='-CALC-1-',size=(5,1)), sg.Text("*"), sg.InputText("",key='-CALC-2-',size=(5,1)), sg.Text("="), sg.InputText("",key='-CALC-R-',readonly=True,size=(5,1))],
    [sg.Button("Przelicz",key='-CALC-RES-')],
    [sg.Button("Wróć",key='-BACK-'), sg.Button("Zamknij",key='-CLOSE-')]
]

macroLayout = [
    [sg.Checkbox("Włącz makra",key='-MACRO-',change_submits=True)],
    [sg.Text("",key='-MACRO-TEXT1-')],
    [sg.Text("")],
    [sg.Text("Wyspy Główne")],
    [sg.Button("Hub",key='-HUB-'),sg.Button("Wyspa",key='-IS-'),sg.Button("Dungeon Hub",key='-DUNGEON-HUB-')],
    [sg.Text("Wyspy Farmingowe")],
    [sg.Button("The Park",key='-THE-PARK-'),sg.Button("The Barn",key='-BARN-')],
    [sg.Text("Wyspy Combatowe")],
    [sg.Button("The End",key='-THE-END-'),sg.Button("Crimson Isle",key='-CRIMSON-ISLE-')],
    [sg.Text("Wyspy Kopalniowe")],
    [sg.Button("Gold Mine",key='-GOLD-MINE-'),sg.Button("Deep Caverns",key='-DEEP-CAVERNS-')],
    [sg.Button("Dwarven Mines",key='-DWARVEN-'),sg.Button("The Forge",key='-FORGE-'),sg.Button("Crystal Hollows",key='-CRYSTALS-')],
    [sg.Text("")],
    [sg.Button("Wróć",key='-BACK-'),sg.Button("Zamknij",key='-CLOSE-')]
]

qwLayout = [
    [sg.Text("")],
    [sg.Text("Wpisz szukaną frazę: "),sg.InputText(key='-QW-INPUT-',size=(8,1))],
    [sg.Button("Szukaj",key='-QW-SEARCH-')],
    [sg.Text("",key='-LOG-')]
]

statLayout = [
    [sg.Text("")],
    [sg.Text("Wpisz nick: "),sg.InputText(key='-STAT-NICK-')],
    [sg.Button("Pobierz",key='-STAT-GET-')],
    [sg.Text("",key='-STAT-RESULT-')],
    [sg.Button("Zamknij",key='-CLOSE-'),sg.Button("Wróć",key='-BACK-')]
]

igorLayout = [
    [sg.Text("")],
    [sg.Text("WYŁĄCZ WSZYSTKIE TEXTUREPACKI!!!")],
    [sg.Button("Start",key='-START-'),sg.Button("STOP",key='-STOP-')]
]


mainWindow = sg.Window("SkyBlock UnAddons Menu", mainLayout, keep_on_top=True,element_justification='center',finalize=True,size=(300,300))

#read the window
while True:
    event, values = mainWindow.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '-MODE-':
        print(values['-MODE-'])
    if event == '-RUN-':
        mode = values['-MODE-']
        if mode == 'Material calculator':
            calcWindow = sg.Window("Material calculator", calcLayout)
            while True:
                event, values = calcWindow.read()
                if event == sg.WIN_CLOSED or event == '-CLOSE-':
                    break

                if event == '-CALC-E2R-':
                    try:
                        enchNum = int(values['-ENCH-NUM-'])
                        enchResult = (enchNum * 160) * int(values['-ENCH-MULT-'])
                        calcWindow['-ENCH-RESULT-'].update(enchResult)
                    except:
                        calcWindow['-ENCH-RESULT-'].update("Niepoprawny format")

                elif event == '-CALC-R2E-':
                    try:
                        materialNum = int(values['-MATERIAL-NUM-'])
                        materialResult = (materialNum / 160) * int(values['-MAT-MULT-'])
                        calcWindow['-MATERIAL-RESULT-'].update(materialResult)
                    except:
                        calcWindow['-MATERIAL-RESULT-'].update("Niepoprawny format")

                if event == '-CALC-RES-':
                    try:
                        calc1 = int(values['-CALC-1-'])
                        calc2 = int(values['-CALC-2-'])
                        calcResult = calc1 * calc2
                        calcWindow['-CALC-R-'].update(calcResult)
                    except:
                        calcWindow['-CALC-R-'].update("Niepoprawny format")

                if event == '-BACK-':
                    calcWindow.close()
                


        elif mode == 'Command macros':
            macroWindow = sg.Window("Command macros", macroLayout, keep_on_top=True,element_justification='center',finalize=True)
            while True:
                event, values = macroWindow.read()
                if event == sg.WIN_CLOSED or event == '-CLOSE-':
                    break
                
                if event == '-BACK-':
                    macroWindow.close()


                if event == '-MACRO-':
                    if values['-MACRO-'] == True:
                        macroWindow['-MACRO-TEXT1-'].update("Włączono makra")
                    elif values['-MACRO-'] == False:
                        macroWindow['-MACRO-TEXT1-'].update("")
            
                if event == '-HUB-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/hub')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-IS-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/is')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-DUNGEON-HUB-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp dungeon_hub')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-THE-PARK-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp park')
                        time.sleep(0.2)
                        pyautogui.press('enter')                

                elif event == '-BARN-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp barn')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-THE-END-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp end')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-CRIMSON-ISLE-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp crimson')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event ==  '-BARN-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp barn')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-GOLD-MINE-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp gold')
                        time.sleep(0.2)
                        pyautogui.press('enter')
                
                elif event == "-DEEP-CAVERNS-":
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp deep')
                        time.sleep(0.2)
                        pyautogui.press('enter')
                    
                elif event == "-DWARVEN-":
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp mines')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-FORGE-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp forge')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                elif event == '-CRYSTALS-':
                    if values['-MACRO-'] == True:
                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.typewrite('/warp crystals')
                        time.sleep(0.2)
                        pyautogui.press('enter')

                else:
                    print("[ERROR] Macros are not enabled")

                if event == '-BACK-':
                    macroWindow.close()
                    mainWindow = sg.Window("SkyBlock UnAddons", mainLayout, keep_on_top=True,element_justification='center',finalize=True)
                    break

        elif mode == 'Quick Wiki':
            mainWindow.close()
            wikiWindow = sg.Window("SkyBlock UnAddons", qwLayout, keep_on_top=True,element_justification='center',finalize=True)
            while True:
                event, values = wikiWindow.read()

                if event == sg.WIN_CLOSED:
                    break

                if event == '-QW-SEARCH-':
                    searchedData = values['-QW-INPUT-']
                    if get(f"https://wiki.hypixel.net/{searchedData}").status_code == 200:
                        webbrowser.open_new_tab(f"https://wiki.hypixel.net/{searchedData}")
                    else:
                        wikiWindow['-LOG-'].update("[ERROR] Wiki page not found")
        
        elif mode == 'StatTrak':
            statWindow = sg.Window("SkyBlock UnAddons", statLayout, keep_on_top=True,element_justification='center',finalize=True)
            while True:
                event, values = statWindow.read()

                if event == '-BACK-':
                    statWindow.close()

                if event == sg.WIN_CLOSED or event == '-CLOSE-':  
                    break

                if event == '-STAT-GET-':
                    nick = values['-STAT-NICK-']
                    if get(f"https://api.mojang.com/users/profiles/minecraft/{nick}").status_code == 200:

                        
                        uuid = json.loads(get(f"https://api.mojang.com/users/profiles/minecraft/{nick}").text)['id']

                        print(uuid)

                        money = get(f"https://api.hypixel.net/skyblock/profiles?key={apikey}&uuid={uuid}").text
                        
                        data = json.loads(money)['profile'][0]['stats']['coins']

                        print(data)

                    elif get(f"https://api.mojang.com/users/profiles/minecraft/{nick}").status_code != 200:
                        print(f"[ERROR] Nick not found")
                    else:
                        print(f"[ERROR] Something went wrong")


            
        elif mode == 'Igor':
            igorWindow = sg.Window("SkyBlock UnAddons", igorLayout, keep_on_top=True,element_justification='center',finalize=True)
            while True:
                event, values = igorWindow.read()
                if event == '-START-':
                    igorWindow.close()
                    print("Starting 'Igor' Fishing Bot.")
                    time.sleep(0.5)
                    


                    def initializePyAutoGUI():
                        print("Initializing PyAutoGUI...")
                        pyautogui.FAILSAFE = True
                        print("Initializing PyAutoGUI... Done!")
                    def take_capture(magnification):
                        mx, my = pyautogui.position()  
                        x = mx - 5  
                        y = my - 5
                        capture = ImageGrab.grab(
                            bbox=(x, y, x + 20, y + 20)
                        )  
                        arr = np.array(capture)
                        res = cv2.cvtColor(
                                cv2.resize(
                                    arr, 
                                    None, 
                                    fx=magnification, 
                                    fy=magnification, 
                                    interpolation=cv2.INTER_CUBIC
                                ), cv2.COLOR_BGR2GRAY
                            )
                        return res
                    def autofish(tick_interval, threshold, magnification):
                        print("Casting the fishing line...")
                        pyautogui.rightClick()
                        time.sleep(2)  
                        img = take_capture(magnification)  
                        print("Taking initial capture...")
                        print("Showing converted image...")
                        while np.sum(img == 0) > threshold:  
                            img = take_capture(magnification)
                            time.sleep(tick_interval)
                            cv2.imshow('window', img)
                            if cv2.waitKey(25) & 0xFF == ord('q'):
                                cv2.destroyAllWindows()
                                break
                        pyautogui.rightClick()
                        time.sleep(1)
                    def main():
                        print("Starting...")
                        initializePyAutoGUI()
                        time.sleep(5)  
                        i = 0
                        while i < 1000:
                            autofish(0.01, 0, 5)
                            print(f"Found someting! Fisehd {i} items so far. Continuing...")
                            i += 1
                    main()
                elif event == '-STOP-' or event == sg.WIN_CLOSED:
                    break
                elif event == '-INFO-':
                    print(f"Igor Fishing Bot v0.2")
                    print(f"Aby łowić za pomocą sztucznej inteligencji, program musi wykrywać spławik.\nWyłącz FullScreena aby widziec okno OpenCV \nMINECRAFT MUSI BYĆ WIDOCZNY NA EKRANIE")
