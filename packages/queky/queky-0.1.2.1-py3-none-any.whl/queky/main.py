import sys
import time
import json
import argparse
import pyperclip
import subprocess
import pyautogui as pg

from queky.constants import JSON_FILE
from queky.utils import gemini_answers, set_terminal_opacity, is_api_present

count = 0

def modify_env(transparent: bool = True) -> None:
    set_terminal_opacity(transparent)
    
    print("\033[H\033[J")
    
    pg.press('f11')
    time.sleep(0.05)
    pg.hotkey('fn', 'f11')
    time.sleep(0.05)
    pg.press('f11')
    
    print("\033[H\033[J")

def fetch_input() -> None:
    user_input = input("\n<<< press enter to paste >>>\n")
    print("\033[H\033[J")
    
    if user_input == "":
        clipboard_content = pyperclip.paste()
        answers = gemini_answers(clipboard_content)
        print(answers.replace('\n\n', '\n'))

    elif user_input == "exit":
        modify_env(transparent=False)
        sys.exit(0)
    elif user_input == "cls" or user_input == "clear":
        print("\033[H\033[J")


def main():
    parser = argparse.ArgumentParser(description="hey wassup lol :3")
    parser.add_argument("-r", "--reset", action="store_true", help="reset api key.")

    args = parser.parse_args()

    if not any(vars(args).values()):
        try:
            if not is_api_present():
                api_key = str(input("Gemini API key: "))
                
                if len(api_key) < 38:
                    print("Invalid API key.")
                    sys.exit(0)

                with open(JSON_FILE, "r") as file:
                    data = json.load(file)
                    
                data["GOOGLE_API_KEY"] = api_key.strip()
                
                with open(JSON_FILE, "w") as file: 
                    json.dump(data, file)
                    
                print("API key saved successfully.")
                subprocess.run(["qk"])
                
            else:
                _ = modify_env(True)

                while True:
                    user_input = input("\n<<< press enter to paste >>>\n")
                    print("\033[H\033[J")
                    
                    if user_input == "":
                        clipboard_content = pyperclip.paste()
                        answers = gemini_answers(clipboard_content)
                        print(answers.replace('\n\n', '\n'))

                    elif user_input == "exit":
                        modify_env(transparent=False)
                        sys.exit(0)
                    elif user_input == "cls" or user_input == "clear":
                        print("\033[H\033[J")
                        
                    else:
                        break
                    
        except KeyboardInterrupt:
            modify_env(transparent=False)
            sys.exit(0)
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            modify_env(transparent=False)
            sys.exit(0)
            
    elif args.reset:
        with open(JSON_FILE, "r") as file: data = json.load(file)
        data["GOOGLE_API_KEY"] = ""
        with open(JSON_FILE, "w") as file: json.dump(data, file)
            
        print("API key reset successfully.")
        subprocess.run(["qk"])
        
if __name__ == "__main__":
    main()