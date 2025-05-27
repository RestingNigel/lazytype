import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from ttkthemes import ThemedTk
import logging
import json
import lazytype
import threading
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
try:
    with open("data.json", "r") as f:
        TRIGGERS = json.load(f)
except FileNotFoundError:
    TRIGGERS = {":sig": "Best regards,\nJohn Doe"}
    with open("data.json", "w") as f:
        json.dump(TRIGGERS, f, indent=4)
        logger.info("File created successfully.")
class TypingMacroApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="yaru")

        self.title("Lazy Type UI")
        self.geometry("600x400")
        self.configure(padx=10, pady=10)
     
        self.create_widgets()
        self.update_list()
        self.check_state =  tk.BooleanVar()
        self.check_state.set(False)  

    def create_widgets(self):
        # Frames for layout
        trigger_frame = ttk.LabelFrame(self, text="Triggers")
        output_frame = ttk.LabelFrame(self, text="Outputs")

        trigger_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        Macro_frame = ttk.LabelFrame(self, text="Keyboard Listener")
        Macro_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Trigger Listbox and Buttons
        self.trigger_listbox = tk.Listbox(trigger_frame, height=10)
        self.trigger_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        #self.add_box = ttk.Entry(trigger_frame)
       # self.add_box.pack()
        trigger_btn_frame = tk.Frame(trigger_frame)
        trigger_btn_frame.pack(fill="x", pady=5)

        ttk.Button(trigger_btn_frame, text="Add",command=self.add_trigger).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(trigger_btn_frame, text="Edit",command=self.edit_trigger).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(trigger_btn_frame, text="Delete",command=self.delete_trigger ).pack(side="left", expand=True, fill="x", padx=2)

        # Output Listbox and Buttons
        self.output_listbox = tk.Listbox(output_frame, height=10)
        self.output_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        #self.add_outbox=ttk.Entry(output_frame)
        #self.add_outbox.pack()
        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill="x", pady=5)

        #keyboard listener checkbox
        self.enablelistener=ttk.Button(Macro_frame, text="Enable Keyboard Listener", command=self.start_macro)
        self.enablelistener.pack(side="left", expand=False, fill="x", padx=2)

    
    def add_trigger(self):
        add_window = Toplevel(self)
        add_window.title("Add Window")
        
        add_window.geometry("300x150")
        ttk.Label(add_window, text="Trigger:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        key_entry = ttk.Entry(add_window)
        
        key_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(add_window, text="Output:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        value_entry = ttk.Entry(add_window)
        
        value_entry.grid(row=1, column=1, padx=10, pady=10) 
        def save_changes():
            key = key_entry.get()
            value = value_entry.get()
            if key and value:
                TRIGGERS[key] = value
                self.update_list()
                add_window.destroy()
            else:
                messagebox.showerror("Error", "Both trigger and output must be provided")
            self.update_file()
            self.update_list()
        ttk.Button(add_window, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)
        
    def update_file(self): #updates the json file with the current triggers
        with open("data.json", "w") as f:
            json.dump(TRIGGERS, f, indent=4)
        logger.info("File updated successfully.")
        
    def delete_trigger(self):
        selected_index = self.trigger_listbox.curselection()
        if selected_index:
            key = self.trigger_listbox.get(selected_index).split(": ", 1)[1]
            logger.debug("Deleting trigger: %s", key)
            del TRIGGERS[key]
            self.update_list()
            self.update_file()
        else:
            messagebox.showerror("Error", "No trigger selected for deletion")
            
    def edit_trigger(self):
        selected_index = self.trigger_listbox.curselection()
        if selected_index:
            key = self.trigger_listbox.get(selected_index).split(": ", 1)[1]
            value = TRIGGERS[key]

            
            edit_window = Toplevel(self)
            edit_window.title("Edit Trigger")

            edit_window.geometry("300x150")
            ttk.Label(edit_window, text="Trigger:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            key_entry = ttk.Entry(edit_window)
            key_entry.insert(0, key)
            key_entry.grid(row=0, column=1, padx=10, pady=10)

            ttk.Label(edit_window, text="Output:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
            value_entry = ttk.Entry(edit_window)
            value_entry.insert(0, value)
            value_entry.grid(row=1, column=1, padx=10, pady=10)

            # Submit button to save changes
            def save_changes():
                new_key = key_entry.get()
                new_value = value_entry.get()
                if new_key and new_value:
                    
                    if new_key != key:
                        del TRIGGERS[key]
                    TRIGGERS[new_key] = new_value
                    self.update_list()
                    self.update_file()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Both trigger and output must be provided")

            ttk.Button(edit_window, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "No trigger selected for editing")
               
       

    def update_list(self): #clears the current list and updates it with the current triggers from the dictionary
        self.trigger_listbox.delete(0, tk.END)
        self.output_listbox.delete(0, tk.END)
        for index, trigs in enumerate(TRIGGERS): 
            self.trigger_listbox.insert(index, str(index) + ": " + str(trigs)) 
            self.output_listbox.insert(index, str(index) + ": " + str(TRIGGERS[trigs]))   

    def start_macro(self):
        # Start the macro in a separate thread
        logger.debug("Starting keyboard listener")
        def run_macro():
            try:
                lazytype.main(TRIGGERS,logger)
            finally:
                # Re-enable the button when lazytype.main ends
                self.enablelistener.config(state="normal")
                self.enablelistener.config(text="Enable Keyboard Listener")
                logger.debug("Keyboard listener stopped, button re-enabled")


        self.keyboard_listener = threading.Thread(target=run_macro, daemon=True)
        self.keyboard_listener.start()
# TODO enable the button when the listener on and change it to a turn off macro button
        self.enablelistener.config(state="disabled")
        self.enablelistener.config(text="Keyboard Listener Enabled")
if __name__ == "__main__":
    
    app = TypingMacroApp()
    app.mainloop()

    
