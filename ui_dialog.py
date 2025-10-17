import tkinter as tk
from tkinter import messagebox
from config import AppConfig
from services import TrafficViolationService


class RecordDialog:
    def __init__(self, parent, mode="add", record_values=None):
        self.parent = parent
        self.mode = mode
        self.record_values = record_values
        self.service = TrafficViolationService()
        self.config = AppConfig()
        
        self.entries = []
        self.labels = list(self.config.columns[1:])
        
        parent_window = getattr(parent, "window", parent)
        
        self.window = tk.Toplevel(parent_window)
        self.window.title(f"{mode.capitalize()} Record")
        self.window.geometry("500x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        container = tk.Frame(self.window)
        canvas = tk.Canvas(container, width=480, height=550)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self._create_form_fields(scroll_frame)
        self._create_save_button(scroll_frame)
    
    def _create_form_fields(self, parent):
        for i, label in enumerate(self.labels):
            tk.Label(parent, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            ent = tk.Entry(parent, width=40)
            ent.grid(row=i, column=1, padx=10, pady=5)
            
            if self.mode == "edit" and self.record_values:
                ent.insert(0, self.record_values[i+1])
            
            self.entries.append(ent)
    
    def _create_save_button(self, parent):
        tk.Button(parent, text="Save", bg=self.config.colors['light_teal'], 
                  fg=self.config.colors['white'], font=("Arial", 12, "bold"),
                  command=self.handle_save).grid(row=len(self.labels), column=0, 
                                                 columnspan=2, pady=15)
    
    def handle_save(self):
        if self.mode == "add":
            if self.service.create_violation(self.entries, self.labels):
                self.window.destroy()
    
                try:
                    self.parent.load_data()
                except Exception:
                    pass
                messagebox.showinfo("Success", "Record added successfully!")
        elif self.mode == "edit":
            record_id = self.record_values[0]
            if self.service.update_violation(record_id, self.entries, self.labels):
                self.window.destroy()
                try:
                    self.parent.load_data()
                except Exception:
                    pass
                messagebox.showinfo("Success", "Record updated successfully!")
