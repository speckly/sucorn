import pyautogui
import time
import keyboard
import threading
import pyperclip
import playsound

def perform_action(action, x, y, delay):
    PROMPT = "colored drawing of an anime girl with cat ears energetically jumping and leaping and bouncing on a big space hopper ball with a handle, both ball and handle must be of the same color, ball has a cartoon face print, girl is sitting on the ball and is holding onto its handle, girl's legs must be stretched out wide forwards towards the camera, ball off the ground and very high up in the air, space hopper ball has a handle that is big, field of flowers, close up on the focus"
    time.sleep(delay / 1000)  # ms to s
    if x and y:  # Check if x and y are provided
        pyautogui.moveTo(x, y, duration=0.1)
    match action:
        case "Left Click":
            pyautogui.click()
        case "Ctrl + C":
            pyautogui.hotkey('ctrl', 'c')
            text = pyperclip.paste()
            if len(text) > 200:
                return "break"
        case "Ctrl + A":
            pyautogui.hotkey('ctrl', 'a')
        case "Ctrl + V":
            pyautogui.hotkey('ctrl', 'v')
        case "Press Enter":
            pyautogui.press('enter')
        case "Prompt":
            for c in PROMPT:
                pyautogui.press(c, _pause=False)
        case "Right Click":
            pyautogui.click(button='right')
        case _:
            print(f"Unknown action: {action}")

def report(run_start, errors, cycle, instanceN):
    runtime_seconds = time.time() - run_start
    hours = runtime_seconds // 3600
    minutes = (runtime_seconds % 3600) // 60
    remaining_seconds = runtime_seconds % 60
    completed = (cycle-1)*INSTANCES+instanceN
    total = REPEATS*INSTANCES
    return f"""Instances completed: {completed}/{total}
Runtime: {hours:.0f} hours, {minutes:.0f} minutes, {remaining_seconds:.2f} seconds
Average {(runtime_seconds/completed):.4f} seconds per instance
Errors {errors}/{completed}, {(errors/completed*100):.2f}%"""

def loop():
    run_start = time.time()
    errors = 0
    for cycle in range(1, REPEATS+1):
        s = time.time()
        for i in range(INSTANCES):
            if terminate_flag:
                print("Script terminated by user.\n", report(run_start, errors, cycle, i))
                return
            for line in lines:
                data = line.split(',')
                action, x, y, delay, comment = data[1:6]
                if delay:
                    x, y, delay = int(x) if x and x != " " else None, int(y) if y and y != " " else None, int(delay)
                    if comment == "Instance":
                        x = 120 + 140 * i # X in the window pos is a placeholder, this formula depends on browser
                    flag = perform_action(action, x, y, delay)
                    if flag:
                        errors += 1
                        playsound.playsound('./tests/vine-boom.wav')
                        perform_action("Left Click",1575,260,20) # Click create before skipping to next instance
                        break
                else:
                    print(f"Skipping line: {line} - Missing delay value.")
        if PRINT_CYCLE_TIME:
            print(f'Cycle number {cycle}: {time.time()-s}s')
        time.sleep(CYCLE_DELAY)

    print("Automation complete\n", report(run_start, errors, cycle, i)) # End of loop

# ID, ACTION, X, Y, DELAYMS, DESCRIPTION
DISCORD_X, DISCORD_Y = 1186, 1051
RELOAD_TIME = 1300
bing_image = f"""1,Left Click,0,21,20,Instance
2,Left Click,113,84,20,Reload
3,Left Click,894,73,{RELOAD_TIME},Copy
4,Ctrl + C,,,20,Copy
5,Left Click,1043,251,20,Box
6,Ctrl + A,,,20,Select
7,Prompt,,,20,Text
8,Left Click,1565,247,20,Create
9,Left Click,{DISCORD_X},{DISCORD_Y},20,Discord
10,Ctrl + V,,,20,Discord
11,Press Enter,,,20,Discord
12,Left Click,1202,1041,20,Discord
"""
# Must be on 170% because of flexibility
leave_servers = """1,Right Click,80,452,450,Options
2,Left Click,277,944,20,Leave
3,Left Click,1278,744,50,Confirm
4,Left Click,217,639,500,Exit"""

macro = bing_image
lines = macro.strip().split('\n')
INSTANCES = 11
REPEATS = 500
CYCLE_DELAY = 0
# 250 -> 4/5 instances broken after approximately 8-12 hours
PRINT_CYCLE_TIME = True
terminate_flag = False
# PROMPT = "colored drawing of two anime girls with cat ears and tail, jumping and bouncing on big space hopper balls with a handle in a race against each other, space hopper off the ground and in the air, in a garden"

time.sleep(2) # Initial delay in seconds

script_thread = threading.Thread(target=loop)
script_thread.start()
keyboard.wait('esc')
terminate_flag = True
script_thread.join()