# establish prefix
# listen for i and trigger
# delete prefix and trigger and type 
import keyboard
import pyperclip
import time
import json

# keyboard.write('The quick brown fox jumps over the lazy dog.')
# move triggers to csv file 
# read triggers file


    
# Load triggers from JSON file
    

with open("data.json", "r") as f:
    TRIGGERS = json.load(f)
def main():
    buffer = ""

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name

            if key == "space":
                if buffer in TRIGGERS:
                    for _ in range(len(buffer)):
                        keyboard.send("backspace")
                   # pyperclip.copy()
                    keyboard.write(TRIGGERS[buffer])
                buffer = ""
            elif key == "backspace":
                buffer = buffer[:-1]
            elif len(key) == 1:
                buffer += key
            elif key == "esc":
                print("Exiting...")
                TypingMacroApp.keyboard_listener.stop()
                break

if __name__ == "__main__":
    print("Text expander running... (Press ESC to stop)")
    main()
