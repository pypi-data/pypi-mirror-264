import sys
import json
import argparse
import pyperclip
import subprocess

from queky.utils import JSON_FILE
from queky.gpt import gemini_answers


def is_api_present():
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

def main():
    parser = argparse.ArgumentParser(description="hey wassup lol :3")
    parser.add_argument("-r", "--reset", action="store_true", help="reset api key.")

    args = parser.parse_args()

    if not any(vars(args).values()):
        print("\033[H\033[J")
        try:
            if not is_api_present():
                api_key = str(input("Gemini API key: "))
                
                if len(api_key) < 38:
                    print("Invalid API key.")
                    sys.exit(0)

                with open(JSON_FILE, "r") as file: data = json.load(file)
                data["GOOGLE_API_KEY"] = api_key.strip()
                with open(JSON_FILE, "w") as file: json.dump(data, file)
                    
                print("API key saved successfully.")
                subprocess.run(["qk"])
            else:
                while True:
                    user_input = input("\n<<< waiting >>>\n")
                    print("\033[H\033[J")
                    if user_input == "":
                        clipboard_content = pyperclip.paste()
                        answers = gemini_answers(clipboard_content)
                        print(answers.replace('\n\n', '\n'))
                    elif user_input == "exit":
                        sys.exit(0)
                    elif user_input == "cls" or user_input == "clear":
                        print("\033[H\033[J")
                        
                    else:
                        break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(0)

        except KeyboardInterrupt:
            sys.exit(0)
            
    elif args.reset:
        with open(JSON_FILE, "r") as file: data = json.load(file)
        data["GOOGLE_API_KEY"] = ""
        with open(JSON_FILE, "w") as file: json.dump(data, file)
            
        print("API key reset successfully.")
        subprocess.run(["qk"])
        
if __name__ == "__main__":
    main()