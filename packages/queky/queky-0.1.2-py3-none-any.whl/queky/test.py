import os
import json
import time

LOCALAPP_DATA = os.getenv('LOCALAPPDATA')
PACKAGE_PATH = os.path.join(LOCALAPP_DATA, 'Packages', 'Microsoft.WindowsTerminal_8wekyb3d8bbwe')
SETTINGS_PATH = os.path.join(PACKAGE_PATH, 'LocalState', 'settings.json')

# def modify_font(count):
#     font_size = 12.0 if count%2==0 else 0.0
#     font_weight = 'normal' if count%2==0 else 'extra-light'
#     set_font_size(font_size, font_weight)
    
def set_font_size(font_size_new: float, font_weight: str) -> str:
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r") as file: 
                settings_content = json.load(file)
                
            settings_content["profiles"]["defaults"]["font"]["size"] = font_size_new
            settings_content["profiles"]["defaults"]["font"]["weight"] = str(font_weight)
            
            with open(SETTINGS_PATH, "w") as file:
                json.dump(settings_content, file)
            
            return "Success"

        else:
            return "Settings file not found."
        
    except Exception as e:
        return f"An exception occurred {e}"

    
count = 0
while 1:
    print(set_font_size(12.0 if count%2==0 else 0.0, 'normal' if count%2==0 else 'extra-light'))
    time.sleep(1)
    print(count)