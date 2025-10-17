import tkinter as tk
from tkinter import ttk, messagebox
from ui_base import BaseWindow, BaseFrame
from services import TrafficViolationService
from config import AppConfig


class HeaderFrame(BaseFrame):
    
    def create(self):
        header = tk.Frame(self.parent, bg=self.get_color('teal'), height=60)
        header.pack(side="top", fill="x")
        tk.Label(header, text="Traffic Violations Management", 
                 bg=self.get_color('teal'), fg=self.get_color('white'),
                 font=("Arial", 18, "bold")).pack(side="left", padx=20)
        return header


class SearchFrame(BaseFrame):
    
    def __init__(self, parent, on_search_callback, on_clear_callback):
        super().__init__(parent)
        self.on_search_callback = on_search_callback
        self.on_clear_callback = on_clear_callback
        self.search_entry = None
    
    def create(self):
        search_frame = tk.Frame(self.parent, bg=self.get_color('white'), pady=10)
        search_frame.pack(fill="x")
        
        tk.Label(search_frame, text="Search (Plate / Driver):", 
                 bg=self.get_color('white'), fg=self.get_color('dark'), 
                 font=("Arial", 12)).pack(side="left", padx=10)
        
        self.search_entry = tk.Entry(search_frame, bg=self.get_color('light_cyan'), 
                                     fg=self.get_color('dark'), font=("Arial", 12))
        self.search_entry.pack(side="left", padx=5, ipadx=30, ipady=3)
        
        tk.Button(search_frame, text="Search", bg=self.get_color('light_teal'), 
                  fg=self.get_color('white'), font=("Arial", 11),
                  command=self.on_search_callback).pack(side="left", padx=5)
        tk.Button(search_frame, text="Clear", bg=self.get_color('dark'), 
                  fg=self.get_color('white'), font=("Arial", 11),
                  command=self.on_clear_callback).pack(side="left", padx=5)
        
        return search_frame
    
    def get_search_term(self):
        return self.search_entry.get()
    
    def clear(self):
        self.search_entry.delete(0, tk.END)


class TableFrame(BaseFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = None
    
    def create(self):
        frame_table = tk.Frame(self.parent)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        x_scroll = tk.Scrollbar(frame_table, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(frame_table, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(frame_table, columns=self.config.columns, show="headings",
                                 xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        
        for col in self.config.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)
        
        return frame_table
    
    def load_data(self, records):
        self.clear_data()
        for record in records:
            self.tree.insert("", "end", values=record)
    
    def clear_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
    
    def get_selected_record(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected, "values")


class ActionButtonsFrame(BaseFrame):
    
    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks
    
    def create(self):
        btn_frame = tk.Frame(self.parent, bg=self.get_color('white'), pady=10)
        btn_frame.pack(fill="x")
        
        buttons = [
            ("Add", 'light_teal', self.callbacks['add']),
            ("Edit", 'light_teal', self.callbacks['edit']),
            ("Delete", 'light_teal', self.callbacks['delete']),
            ("Refresh", 'light_teal', self.callbacks['refresh'])
        ]
        
        for text, color, command in buttons:
            tk.Button(btn_frame, text=text, bg=self.get_color(color), 
                     fg=self.get_color('white'), font=("Arial", 12), width=10,
                     command=command).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Logout", bg=self.get_color('dark'), 
                 fg=self.get_color('white'), font=("Arial", 12), width=10,
                 command=self.callbacks['logout']).pack(side="right", padx=10)
        
        return btn_frame


class ManagementPage(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.service = TrafficViolationService()
        
        self.header_frame = None
        self.search_frame = None
        self.table_frame = None
        self.buttons_frame = None
        
        self.window = tk.Tk()
        self.window.title("Traffic Violations Management")
        self.window.state("zoomed")
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        self.header_frame = HeaderFrame(self.window)
        self.header_frame.create()
        
        self.search_frame = SearchFrame(self.window, self.handle_search, self.handle_clear_search)
        self.search_frame.create()
        
        self.table_frame = TableFrame(self.window)
        self.table_frame.create()
        
        callbacks = {
            'add': self.handle_add,
            'edit': self.handle_edit,
            'delete': self.handle_delete,
            'refresh': self.load_data,
            'logout': self.handle_logout
        }
        self.buttons_frame = ActionButtonsFrame(self.window, callbacks)
        self.buttons_frame.create()
    
    def load_data(self):
        try:
            records = self.service.get_all_violations()
            self.table_frame.load_data(records)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")
    
    def handle_search(self):
        try:
            search_term = self.search_frame.get_search_term()
            records = self.service.search_violations(search_term)
            self.table_frame.load_data(records)
        except Exception as e:
            messagebox.showerror("Error", f"Search failed:\n{e}")
    
    def handle_clear_search(self):
        try:
            self.search_frame.clear()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear search:\n{e}")
    
    def handle_add(self):
        try:
            from ui_dialog import RecordDialog
            RecordDialog(self, mode="add")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open add window:\n{e}")
    
    def handle_edit(self):
        try:
            record = self.table_frame.get_selected_record()
            if not record:
                messagebox.showerror("Error", "Select a record to edit")
                return
            from ui_dialog import RecordDialog
            RecordDialog(self, mode="edit", record_values=record)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open edit window:\n{e}")
    
    def handle_delete(self):
        try:
            record = self.table_frame.get_selected_record()
            if not record:
                messagebox.showerror("Error", "Select a record to delete")
                return
            
            confirm = messagebox.askyesno("Confirm", "Delete this record?")
            if confirm:
                if self.service.delete_violation(record[0]):
                    self.load_data()
                    messagebox.showinfo("Success", "Record deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record:\n{e}")
    
    def handle_logout(self):
        self.close()
        login_page = __import__("ui_login").ui_login.LoginPage()
        login_page.run()
