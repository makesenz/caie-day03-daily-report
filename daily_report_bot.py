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
    "https://weather.com/en-IN/in/tamil-nadu/"
    "city/tirunelveli/tenday"
)

GOOGLE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1aZMtr8axyS1TvWlN6ahcAPPxi9nfan690mPJQcHNwUg/edit?gid=0#gid=0"
)


# ==========================================
# 1. OPEN GOOGLE CHROME
# ==========================================

print("\nOpening Google Chrome...")

pyautogui.hotkey("command", "space")
time.sleep(1)

pyautogui.write("Google Chrome")
pyautogui.press("enter")

time.sleep(4)


# ==========================================
# 2. OPEN WEATHER WEBSITE IN NEW TAB
# ==========================================

print("Opening weather website...")

# Create a new tab
pyautogui.hotkey("command", "t")

time.sleep(1)

# Open weather URL
pyautogui.write(WEATHER_URL)
pyautogui.press("enter")

# Wait for website to load
time.sleep(6)


# ==========================================
# 3. COPY ENTIRE WEBPAGE CONTENT
# ==========================================

print("Copying webpage data...")

# Clear old clipboard
pyperclip.copy("")

# Select webpage content
pyautogui.hotkey("command", "a")

# Copy
pyautogui.hotkey("command", "c")

time.sleep(1)


# ==========================================
# 4. GET COPIED DATA
# ==========================================

copied_data = pyperclip.paste()

print("Weather data copied successfully.")


# ==========================================
# 5. EXTRACT TODAY'S WEATHER
# ==========================================

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


# Stop if extraction fails
if not match:

    print("\nERROR: Could not extract today's weather.")

    print("\nCopied webpage data:")
    print(copied_data[:2000])

    raise SystemExit


# Extract weather values

rain_chance = match.group(1)
condition = match.group(2).strip()
low_temp = match.group(3)
high_temp = match.group(4)
wind_speed = match.group(5)
wind_unit = match.group(6)
wind_direction = match.group(7)


# ==========================================
# 6. DISPLAY EXTRACTED WEATHER
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
# 7. GET CURRENT DATE & TIME
# ==========================================

now = datetime.now()

current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%I:%M %p")


print("\n----- DATE & TIME -----")

print("Date:", current_date)
print("Time:", current_time)


# ==========================================
# 8. GENERATE COMMENT
# ==========================================

comment = (
    f"{condition} today with a "
    f"{rain_chance}% chance of rain. "
    f"Temperature may reach {high_temp}°."
)


print("\n----- COMMENT -----")

print(comment)


# ==========================================
# 9. PREPARE GOOGLE SHEETS DATA
# ==========================================

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


# Combine header and today's data
sheet_data = (
    headers
    + "\n"
    + weather_row
)


# ==========================================
# 10. OPEN GOOGLE SHEETS
# ==========================================

print("\nOpening Google Sheets...")

# Create new Chrome tab
pyautogui.hotkey("command", "t")

time.sleep(1)

# Open Google Sheet
pyautogui.write(GOOGLE_SHEET_URL)

pyautogui.press("enter")

# Wait for Google Sheets to load
time.sleep(8)


# ==========================================
# 11. PASTE REPORT INTO GOOGLE SHEETS
# ==========================================

print("Adding weather report to Google Sheets...")

# Copy report data
pyperclip.copy(sheet_data)

time.sleep(1)

# Paste into selected cell
pyautogui.hotkey("command", "v")

# Wait for Google Sheets
time.sleep(5)


# ==========================================
# 12. TAKE FINAL SCREENSHOT
# ==========================================

print("Taking final screenshot...")

project_folder = os.getcwd()

screenshot_filename = (
    f"daily_weather_report_{current_date}.png"
)

screenshot_path = os.path.join(
    project_folder,
    screenshot_filename
)


# Capture screen
try:

    screenshot = pyautogui.screenshot()

    # Save screenshot
    screenshot.save(screenshot_path)

    # Verify file exists
    if os.path.exists(screenshot_path):

        file_size = os.path.getsize(
            screenshot_path
        )

        print("\nScreenshot saved successfully!")

        print(
            "Path:",
            screenshot_path
        )

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

    print(
        "\nERROR while saving screenshot:"
    )

    print(e)


# ==========================================
# 13. FINAL OUTPUT
# ==========================================

print("\n")
print("==========================================")
print("       DAILY REPORT COMPLETED")
print("==========================================")

print("\nDate:", current_date)

print("Time:", current_time)

print("\nGoogle Sheet:")
print(GOOGLE_SHEET_URL)

print("\nScreenshot:")
print(screenshot_path)

print("\nBot finished successfully! 🚀")