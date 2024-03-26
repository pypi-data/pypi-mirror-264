import os
import time
import json
import pkg_resources
import google.generativeai as genai
from queky.constants import SETTINGS_PATH, GOOGLE_API_KEY, JSON_FILE

genai.configure(api_key=GOOGLE_API_KEY)

def path_convertor(path: str) -> str:
        try:
            return pkg_resources.resource_filename('queky', path)
        except FileNotFoundError and ModuleNotFoundError:
            return path
        
def set_terminal_opacity(transparent: bool = True) -> str:
    print(f"{'Restoring' if not transparent else 'Modifying'} terminal opacity...")
    
    opacity_value = 0 if transparent else 100
    
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, 'r') as f:
                settings_content = json.load(f)
            
            opacity = int(settings_content["profiles"]["defaults"]["opacity"])
            
            if opacity != opacity_value:
                with open(SETTINGS_PATH, "r") as file: 
                    settings_content = json.load(file)
                    
                settings_content["profiles"]["defaults"]["opacity"] = opacity_value
                
                with open(SETTINGS_PATH, "w") as file: 
                    json.dump(settings_content, file)
            
            return "Success"

        else:
            return "Settings file not found."
        
    except Exception as e:
        return f"An exception occurred {e}"
    
def set_font_size(font_size_new: float, font_weight: str) -> str:
    try:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r") as file: 
                settings_content = json.load(file)
                
            settings_content["profiles"]["defaults"]["font"]["size"] = font_size_new
            settings_content["profiles"]["defaults"]["font"]["weight"] = font_weight
            
            with open(SETTINGS_PATH, "w") as file:
                json.dump(settings_content, file)
            
            return "Success"

        else:
            return "Settings file not found."
        
    except Exception as e:
        return f"An exception occurred {e}"    

def is_api_present() -> bool:
    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
        api_key = data.get("GOOGLE_API_KEY")
        return False if api_key=="" else api_key
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
def gemini_answers(question_string: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question_string)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__=="__main__":
    while 1:
        set_terminal_opacity(transparent=True)
        time.sleep(2)
        set_terminal_opacity(transparent=False)
        time.sleep(2)