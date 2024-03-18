import pyautogui
import time
import subprocess

# Get the running process
#process_name = "ArelliaDisplayXamlAction.exe"
process_name = "ArelliaACSvc.exe"
processes = subprocess.Popen(["tasklist"], stdout=subprocess.PIPE).stdout.readlines()
processes = [p for p in subprocess.Popen(["tasklist"], stdout=subprocess.PIPE).stdout.readlines() if process_name.encode() in p]
if len(processes) == 0:
    print("Process not found")
    exit()

# Assuming there is one process running with the specified name
process_id = int(processes[0].split()[1])

# Attach to the process window
win_title = "Privilege Manager Application Elevation: Windows Command Processor"
window = pyautogui.getWindowsWithTitle(win_title)[0]

#pyautogui._pyautogui_win = pyautogui._pygetwin.GetForegroundWindow()
#pyautogui._pyautogui_win.set_foreground()

# Wait for the window to appear
time.sleep(2)  # Adjust the delay as needed

# Enter text in the text box
pyautogui.click(x = window.left + 100, y = window.bottom - 100)  # Replace with the actual coordinates of the textbox
pyautogui.typewrite("f")

# Click the button
pyautogui.click(x = window.right - 150, y = window.bottom - 30)  # Replace with the actual coordinates of the button