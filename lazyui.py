import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from ttkthemes import ThemedTk
import logging
import time
import json
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class TypingMacroApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="yaru")

        self.title("Lazy Type UI")
        self.geometry("600x400")
        self.configure(padx=10, pady=10)
     
        self.create_widgets()
        with open("data.json", "r") as f:
            self.TRIGGERS = json.load(f)
        self.update_list()



    def create_widgets(self):
        # Frames for layout
        trigger_frame = ttk.LabelFrame(self, text="Triggers")
        output_frame = ttk.LabelFrame(self, text="Outputs")

        trigger_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Trigger Listbox and Buttons
        self.trigger_listbox = tk.Listbox(trigger_frame, height=10)
        self.trigger_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.add_box = ttk.Entry(trigger_frame)
        self.add_box.pack()
        trigger_btn_frame = tk.Frame(trigger_frame)
        trigger_btn_frame.pack(fill="x", pady=5)

        ttk.Button(trigger_btn_frame, text="Add",command=self.add_trigger).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(trigger_btn_frame, text="Edit").pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(trigger_btn_frame, text="Delete").pack(side="left", expand=True, fill="x", padx=2)

        # Output Listbox and Buttons
        self.output_listbox = tk.Listbox(output_frame, height=10)
        self.output_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.add_outbox=ttk.Entry(output_frame)
        self.add_outbox.pack()
        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill="x", pady=5)


    def add_trigger(self):
       # add_window = Toplevel(self)
        #add_window.title("Add Window")
        #ttk.Button(text="Add",command=self.add_trigger)
        logger.debug("This is a debug message")
        key = self.add_box.get()
        value = self.add_outbox.get()
      
        if key and value:
            self.TRIGGERS[key] = value
            self.update_list()
        else:
            messagebox.showerror("Error", "Both a key and value must be provided")
            #logger.warning("Both key and value must be provided.")
        self.update_file()
    def update_file(self):
        with open("data.json", "w") as f:
            json.dump(self.TRIGGERS, f, indent=4)
        logger.info("File updated successfully.")
        
        

    def update_list(self):
        self.trigger_listbox.delete(0, tk.END)
        for index, trigs in enumerate(self.TRIGGERS): 
            self.trigger_listbox.insert(index, str(index) + ": -" + str(trigs)) 
            self.output_listbox.insert(index, str(index) + ": -" + str(self.TRIGGERS[trigs]))   
           
if __name__ == "__main__":
    
    app = TypingMacroApp()
    app.mainloop()


