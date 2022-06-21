from datetime import datetime
import time
import requests
from requests import *
import PySimpleGUI as sg
import json
import webbrowser
import os
from pathlib import Path
import pyautogui
import cv2
from PIL import ImageGrab
import numpy as np
import random
from colorama import Fore, Back, Style
import colorama
import base64
import asyncio
from timeit import default_timer
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
op = os.name == 'nt'
if op: import winsound
from plyer import notification



colorama.init(autoreset=True) #reset colorama after each print

os.system("cls") #flush the console

print(f"{Fore.LIGHTBLUE_EX}Starting INIT phase...")

chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe" # assing chrome path
webbrowser.register('google-chrome', None, webbrowser.BackgroundBrowser(chrome_path)) # register chrome as the browser to use

path = Path(__file__).parent.absolute() # get current file path

# ###################################################################################################################### init/data folder

try:
    print(f"{Fore.LIGHTBLUE_EX}[INIT] Checking for data folder...")
    os.makedirs(path / "data")
    print(f"{Fore.LIGHTBLUE_EX}[INIT] Data folder created!")
except FileExistsError:
    print(f"{Fore.LIGHTBLUE_EX}[INIT] Data folder already exists")

# ###################################################################################################################### config.json file creation

if not os.path.exists(path / "data" / "config.json"):
    print(f"{Fore.CYAN}[SETUP] Creating config file...")
    open(path / "data" / "config.json", "w").write(json.dumps({"debug": "False"}, indent=4))
else:
    print(f"{Fore.LIGHTGREEN_EX}[DEBUG] Config file already exists!")

# ###################################################################################################################### API key

try:
    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.WHITE} Getting your API key...")
    with open(f"{path}/data/apikey.dat", 'r') as f:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.WHITE} API Key found!")
        apikey = f.read()
        #apikey = base64.b64decode(apikey).decode('utf-8')
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.WHITE} API Key decoded!")
        apikey = str(apikey)
except FileNotFoundError:
    print(f"{Fore.RED}[!] Error{Fore.WHITE}: No API key found!")
    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.WHITE} Creating API key file...")
    with open(f'{path}/data/apikey.dat','w') as f:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.WHITE} Done!")
        print(f'{Fore.RED}[!]{Fore.WHITE} Please enter your API key!')
        apikey = input("Enter your API key: ")
        print(f"{Fore.LIGHTRED_EX}Encoding API key...")
        #apikey = base64.b64encode(apikey.encode('utf-8'))
        apikey = str(apikey)
        print(f"{Fore.LIGHTRED_EX} API Key encoded!")

        f.write(apikey)
        apikey = str(apikey)
        f.close()
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.WHITE} API Key saved!")

# ###################################################################################################################### reading config.json file

with open(path / "data" / "config.json", "r") as f:
    data = json.load(f)
    debug = data["debug"]

# ###################################################################################################################### general debug files

if debug == "True":
    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Preparing debug files...")
    if not os.path.exists(path / "data" / "debug"):
        os.makedirs(path / "data" / "debug")
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Debug folder created!")
    else:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Debug folder already exists!")
    print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Preparing log files...")
    if not os.path.exists(path / "data" / "debug" / "log"):
        os.makedirs(path / "data" / "debug" / "log")
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Log folder created!")
    else:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Log folder already exists!")
    if not os.path.exists(path / "data" / "debug" / "log" / "debug-log.log"):
        with open('debug-log.log', 'w+') as f:
            print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Log file created!")
            f.close()
    else:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} Log file already exists!")

print(f"{Fore.LIGHTGREEN_EX}[DEBUG] Debug mode is set to {debug}")
apikey = str(apikey)

print(f"Your API Key - {Fore.YELLOW}{apikey}")


mainLayout = [
    [sg.Text("Wybierz tryb")],
    [sg.Combo(['Material calculator','Command macros','Quick Wiki','Mr Fisher','SkyblockSniper'],key='-MODE-',default_value='Material calculator',size=(20,1))],
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
    [sg.Button("Start",key='-START-'),sg.Button("STOP",key='-STOP-'),sg.Button("Info",key='-INFO-')],
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
                    print("{Fore.RED}[ERROR]{Fore.WHITE} Macros are not enabled")

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
                        print(f"{Fore.RED}[ERROR]{Fore.WHITE} Nickname not found!")
                    else:
                        print(f"{Fore.RED}[ERROR]{Fore.WHITE} Something went wrong!")


            
        elif mode == 'Igor':
            mainWindow.close()
            igorWindow = sg.Window("SkyBlock UnAddons", igorLayout, keep_on_top=True,element_justification='center',finalize=True)
            while True:
                event, values = igorWindow.read()
                if event == '-START-':
                    igorWindow.close()
                    print("Starting the Fishing Bot.")
                    time.sleep(0.5)
                    def initializePyAutoGUI():
                        print("Initializing PyAutoGUI...")
                        pyautogui.FAILSAFE = True
                        print("Initializing PyAutoGUI... Done!")
                    def take_capture(magnification):
                        mx, my = pyautogui.position()  
                        x = mx - 10  
                        y = my - 10
                        capture = ImageGrab.grab(
                            bbox=(x, y, x + 30, y + 30)
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
                        mx, my = pyautogui.position()
                        pyautogui.moveTo(mx, my+5)

                        print("Casting the fishing line...")
                        pyautogui.rightClick()
                        time.sleep(0.05)
                        pyautogui.moveTo(mx,my-5)
                        time.sleep(2)
                        print("Taking initial capture...")
                        img = take_capture(magnification)
                        print("Showing converted image...")
                        while np.sum(img == 0) > threshold:
                            img = take_capture(magnification)
                            time.sleep(tick_interval)
                            cv2.imshow('window', img)
                            if cv2.waitKey(25) & 0xFF == ord('q'):
                                print("Destroying all windows...")
                                cv2.destroyAllWindows()
                                print(f"{Fore.GREEN}[!]{Fore.RESET} Done!")
                                print(f"{Fore.YELLOW}[-]{Fore.RESET} Exiting...")
                                break
                        pyautogui.rightClick()
                        time.sleep(1)
                    def Fishmain():
                        print("Starting...")
                        initializePyAutoGUI()
                        time.sleep(5)
                        i = 0
                        while i < 1000:
                            autofish(0.01, 0, 4)
                            posx, posy = pyautogui.position()
                            pyautogui.moveTo(posx-2,posy)
                            time.sleep(0.05)
                            pyautogui.moveTo(posx+2,posy)
                            i += 1
                            time = datetime.now().strftime("%H:%M:%S")
                            print(f"[{time}] Found someting! Fisehd {Fore.LIGHTCYAN_EX}{i}{Fore.RESET} items so far. Continuing...")
                            if debug == "True":
                                with open(f'{path}/data/log/debug-log.log','a') as log:
                                    log.write(f"[{time}] Found someting! Fished {Fore.LIGHTCYAN_EX}{i}{Fore.RESET} items so far. \n{Fore.BLUE}Continuing...")
                    Fishmain()
                elif event == '-STOP-' or event == sg.WIN_CLOSED:
                    break
                elif event == '-INFO-':
                    print(f"Mr Fisherman Bot v0.2\nAby łowić za pomocą sztucznej inteligencji, program musi wykrywać spławik.\nWyłącz FullScreena aby widziec okno Open ComputerVision\nMINECRAFT MUSI BYĆ WIDOCZNY NA EKRANIE")
        elif mode == 'SkyblockSniper':
            mainWindow.close()
            print(f"{Fore.GREEN}[!]{Fore.RESET} Starting Skyblock Sniper...")
            print(f"Made by {Fore.BLUE} csjh{Fore.RESET}")  
            c = requests.get("https://api.hypixel.net/skyblock/auctions?page=0")
            resp = c.json()
            now = resp['lastUpdated']
            toppage = resp['totalPages']

            results = []
            prices = {}

            # stuff to remove
            REFORGES = [" ✦", "⚚ ", " ✪", "✪", "Stiff ", "Lucky ", "Jerry's ", "Dirty ", "Fabled ", "Suspicious ", "Gilded ", "Warped ", "Withered ", "Bulky ", "Stellar ", "Heated ", "Ambered ", "Fruitful ", "Magnetic ", "Fleet ", "Mithraic ", "Auspicious ", "Refined ", "Headstrong ", "Precise ", "Spiritual ", "Moil ", "Blessed ", "Toil ", "Bountiful ", "Candied ", "Submerged ", "Reinforced ", "Cubic ", "Warped ", "Undead ", "Ridiculous ", "Necrotic ", "Spiked ", "Jaded ", "Loving ", "Perfect ", "Renowned ", "Giant ", "Empowered ", "Ancient ", "Sweet ", "Silky ", "Bloody ", "Shaded ", "Gentle ", "Odd ", "Fast ", "Fair ", "Epic ", "Sharp ", "Heroic ", "Spicy ", "Legendary ", "Deadly ", "Fine ", "Grand ", "Hasty ", "Neat ", "Rapid ", "Unreal ", "Awkward ", "Rich ", "Clean ", "Fierce ", "Heavy ", "Light ", "Mythic ", "Pure ", "Smart ", "Titanic ", "Wise ", "Bizarre ", "Itchy ", "Ominous ", "Pleasant ", "Pretty ", "Shiny ", "Simple ", "Strange ", "Vivid ", "Godly ", "Demonic ", "Forceful ", "Hurtful ", "Keen ", "Strong ", "Superior ", "Unpleasant ", "Zealous "]

            # Constant for the lowest priced item you want to be shown to you; feel free to change this
            LOWEST_PRICE = 5

            # Constant to turn on/off desktop notifications
            NOTIFY = False

            LOWEST_PERCENT_MARGIN = 1/2

            START_TIME = default_timer()

            def fetch(session, page):
                global toppage
                base_url = "https://api.hypixel.net/skyblock/auctions?page="
                with session.get(base_url + page) as response:
                    data = response.json()
                    toppage = data['totalPages']
                    if data['success']:
                        toppage = data['totalPages']
                        for auction in data['auctions']:
                            if not auction['claimed'] and auction['bin'] == True and not "Furniture" in auction["item_lore"]:
                                index = re.sub("\[[^\]]*\]", "", auction['item_name']) + auction['tier']
                                for reforge in REFORGES: index = index.replace(reforge, "")
                                if index in prices:
                                    if prices[index][0] > auction['starting_bid']:
                                        prices[index][1] = prices[index][0]
                                        prices[index][0] = auction['starting_bid']
                                    elif prices[index][1] > auction['starting_bid']:
                                        prices[index][1] = auction['starting_bid']
                                else:
                                    prices[index] = [auction['starting_bid'], float("inf")]
                                    
                                if prices[index][1] > LOWEST_PRICE and prices[index][0]/prices[index][1] < LOWEST_PERCENT_MARGIN and auction['start']+60000 > now:
                                    results.append([auction['uuid'], auction['item_name'], auction['starting_bid'], index])
                    return data

            async def get_data_asynchronous():
                pages = [str(x) for x in range(toppage)]
                with ThreadPoolExecutor(max_workers=10) as executor:
                    with requests.Session() as session:
                        loop = asyncio.get_event_loop()
                        START_TIME = default_timer()
                        tasks = [
                            loop.run_in_executor(
                                executor,
                                fetch,
                                *(session, page)
                            )
                            for page in pages if int(page) < toppage
                        ]
                        for response in await asyncio.gather(*tasks):
                            pass

            def SSmain():
                global results, prices, START_TIME
                START_TIME = default_timer()
                results = []
                prices = {}
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                future = asyncio.ensure_future(get_data_asynchronous())
                loop.run_until_complete(future)
                
                if len(results): results = [[entry, prices[entry[3]][1]] for entry in results if (entry[2] > LOWEST_PRICE and prices[entry[3]][1] != float('inf') and prices[entry[3]][0] == entry[2] and prices[entry[3]][0]/prices[entry[3]][1] < LOWEST_PERCENT_MARGIN)]
                
                if len(results): 

                    if NOTIFY: 
                        notification.notify(
                            title = max(results, key=lambda entry:entry[1])[0][1],
                            message = "Lowest BIN: " + f'{max(results, key=lambda entry:entry[1])[0][2]:,}' + "\nSecond Lowest: " + f'{max(results, key=lambda entry:entry[1])[1]:,}',
                            app_icon = None,
                            timeout = 4,
                        )
                    
                    df=pd.DataFrame(['/viewauction ' + str(max(results, key=lambda entry:entry[1])[0][0])])
                    df.to_clipboard(index=False,header=False) 
                    
                    done = default_timer() - START_TIME
                    if op: winsound.Beep(700, 500)
                    for result in results:
                        print("Auction UUID: " + str(result[0][0]) + " | Item Name: " + str(result[0][1]) + " | Item price: {:,}".format(result[0][2]), " | Second lowest BIN: {:,}".format(result[1]) + " | Time to refresh AH: " + str(round(done, 2)))
                    print("\nLooking for auctions...")

            print("Looking for auctions...")
            SSmain()

            def dostuff():
                global now, toppage

                if time.time()*1000 > now + 60000:
                    prevnow = now
                    now = float('inf')
                    c = requests.get("https://api.hypixel.net/skyblock/auctions?page=0").json()
                    if c['lastUpdated'] != prevnow:
                        now = c['lastUpdated']
                        toppage = c['totalPages']
                        SSmain()
                    else:
                        now = prevnow
                time.sleep(0.25)

            while True:
                dostuff()