# establish prefix
# listen for i and trigger
# delete prefix and trigger and type 
import keyboard
import pyperclip
import time


# keyboard.write('The quick brown fox jumps over the lazy dog.')
# move triggers to csv file 
# read triggers file


    
# Load triggers from JSON file
    

def main(TRIGGERS,logger):
    buffer = ""
    maxlength = 0
    for key in TRIGGERS:
        if len(key) > maxlength:
            maxlength = len(key)
        
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            
#            if key == "space":
#                if buffer in TRIGGERS:
 #                      keyboard.send("backspace")
                   # pyperclip.copy()
  #                  keyboard.write(TRIGGERS[buffer],delay=0.008)
   #             buffer = ""

            if key == "backspace":
                buffer = buffer[:-1]
            elif len(key) == 1:
                buffer += key
                if buffer in TRIGGERS:
                    for _ in range(len(buffer)+1):
                        keyboard.send("backspace")
                   # pyp    erclip.copy()
                    keyboard.write(TRIGGERS[buffer],delay=0.008)
                    buffer = ""
                if len(buffer) > maxlength:
                    buffer = buffer[-maxlength:]
                logger.info(f"Buffer: {buffer}")
            elif key == "esc":
                print("Exiting...")
                
                break
if __name__ == "__main__":
    print("Text expander running... (Press ESC to stop)")
    main()