import pyautogui
import pyperclip
import time
import re
import os
from datetime import datetime


# ==========================================
# CONFIGURATION
# ==========================================

WEATHER_URL = (
    "https://weather.com/en-IN/in/tamil-nadu/city/tirunelveli/tenday"
)


# ==========================================
# 1. OPEN GOOGLE CHROME
# ==========================================

print("\n[1] Opening Google Chrome...")

pyautogui.hotkey("command", "space")
time.sleep(1.5)

pyautogui.write("Google Chrome")
time.sleep(1)

pyautogui.press("enter")

# Wait for Chrome
time.sleep(5)


# ==========================================
# 2. OPEN WEATHER WEBSITE IN NEW TAB
# ==========================================

print("[2] Opening weather website...")

pyautogui.hotkey("command", "t")
time.sleep(1.5)

pyautogui.write(WEATHER_URL)
pyautogui.press("enter")

# Wait for Weather.com
time.sleep(7)


# ==========================================
# 3. COPY ENTIRE WEBPAGE
# ==========================================

print("[3] Copying webpage data...")

pyperclip.copy("")

time.sleep(0.5)

pyautogui.hotkey("command", "a")
time.sleep(1)

pyautogui.hotkey("command", "c")
time.sleep(2)

copied_data = pyperclip.paste()

print("Weather data copied successfully.")


# ==========================================
# 4. EXTRACT TODAY'S WEATHER
# ==========================================

print("[4] Extracting weather data...")

pattern = r"""
Today\s+
(\d+)%\s+
(.+?)\s+
(\d+)°\s+
(\d+)°\s+
(\d+)\s+(mph|km/h)\s+
([A-Z]+)
"""

match = re.search(
    pattern,
    copied_data,
    re.VERBOSE
)


if not match:

    print("\nERROR: Could not extract today's weather.")

    print(copied_data[:2000])

    raise SystemExit


rain_chance = match.group(1)
condition = match.group(2).strip()
low_temp = match.group(3)
high_temp = match.group(4)
wind_speed = match.group(5)
wind_unit = match.group(6)
wind_direction = match.group(7)


# ==========================================
# 5. DISPLAY WEATHER
# ==========================================

print("\n----- EXTRACTED WEATHER -----")

print("Rain Chance:", rain_chance + "%")
print("Condition:", condition)
print("Low:", low_temp + "°")
print("High:", high_temp + "°")
print(
    "Wind:",
    wind_speed,
    wind_unit,
    wind_direction
)


# ==========================================
# 6. DATE & TIME
# ==========================================

print("\n[5] Generating date and time...")

now = datetime.now()

current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%I:%M %p")


print("Date:", current_date)
print("Time:", current_time)


# ==========================================
# 7. GENERATE COMMENT
# ==========================================

comment = (
    f"{condition} today with a "
    f"{rain_chance}% chance of rain. "
    f"Temperature may reach {high_temp}°."
)


print("\n----- COMMENT -----")
print(comment)


# ==========================================
# 8. PREPARE NUMBERS DATA
# ==========================================

print("\n[6] Preparing spreadsheet data...")

headers = (
    "Date\t"
    "Time\t"
    "Condition\t"
    "Low Temperature\t"
    "High Temperature\t"
    "Rain Chance\t"
    "Wind\t"
    "Comment"
)


weather_row = (
    f"{current_date}\t"
    f"{current_time}\t"
    f"{condition}\t"
    f"{low_temp}°\t"
    f"{high_temp}°\t"
    f"{rain_chance}%\t"
    f"{wind_speed} {wind_unit} {wind_direction}\t"
    f"{comment}"
)


sheet_data = (
    headers
    + "\n"
    + weather_row
)


# ==========================================
# 9. COPY DATA TO CLIPBOARD
# ==========================================

print("[7] Preparing clipboard...")

pyperclip.copy(sheet_data)

# Give clipboard time
time.sleep(2)


# ==========================================
# 10. OPEN NUMBERS USING SPOTLIGHT
# ==========================================

print("\n[8] Opening Numbers...")

pyautogui.hotkey("command", "space")

time.sleep(1.5)

pyautogui.write("Numbers")

time.sleep(1.5)

pyautogui.press("enter")

# Wait for Numbers to launch
time.sleep(8)


# ==========================================
# 11. SELECT WEATHER FILE
# ==========================================

print("[9] Selecting Weather spreadsheet...")

# Wait for Numbers document chooser
time.sleep(2)

# Select Weather
pyautogui.press("down")

time.sleep(2)

# Open Weather
pyautogui.press("enter")


# ==========================================
# 12. WAIT FOR WEATHER SPREADSHEET
# ==========================================

print("[10] Waiting for Weather spreadsheet...")

# IMPORTANT:
# Do NOT click any cell.
#
# Numbers should open the spreadsheet with
# the appropriate cell already selected.
#
# We simply wait and then paste.

time.sleep(5)


# ==========================================
# 13. PASTE DATA
# ==========================================

print("[11] Pasting weather data...")

# Clipboard is already prepared.
#
# Use Command + V exactly like manual operation.

pyautogui.hotkey("command", "v")

# Give Numbers time to paste
time.sleep(6)

print("Weather data paste completed.")


# ==========================================
# 14. SAVE
# ==========================================

print("[12] Saving Numbers spreadsheet...")

pyautogui.hotkey("command", "s")

time.sleep(5)


# ==========================================
# 15. TAKE SCREENSHOT
# ==========================================

print("[13] Taking final screenshot...")

project_folder = os.getcwd()

screenshot_filename = (
    f"numbers_weather_report_{current_date}.png"
)

screenshot_path = os.path.join(
    project_folder,
    screenshot_filename
)


try:

    screenshot = pyautogui.screenshot()

    screenshot.save(screenshot_path)

    if os.path.exists(screenshot_path):

        file_size = os.path.getsize(
            screenshot_path
        )

        print("\nScreenshot saved successfully!")

        print("Path:")
        print(screenshot_path)

        print(
            "File size:",
            file_size,
            "bytes"
        )

    else:

        print(
            "\nERROR: Screenshot file was not created."
        )


except Exception as e:

    print("\nERROR while saving screenshot:")

    print(e)


# ==========================================
# 16. FINAL OUTPUT
# ==========================================

print("\n")
print("==========================================")
print("       NUMBERS TEST COMPLETED 🚀")
print("==========================================")

print("\nDate:", current_date)
print("Time:", current_time)

print("\nSpreadsheet: Weather")

print("\nScreenshot:")
print(screenshot_path)

print("\nDone!")