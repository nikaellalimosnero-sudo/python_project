import tkinter as tk
from tkinter import messagebox, ttk
from ui_base import BaseWindow, BaseFrame
from services import AuthenticationService
from config import AppConfig


class LoginLogoFrame(BaseFrame):

    def create(self):
        left_frame = tk.Frame(self.parent, bg=self.get_color('teal'), width=400)
        left_frame.pack(side="left", fill="y")
        
        logo_frame = tk.Frame(left_frame, bg=self.get_color('teal'))
        logo_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self._create_traffic_light(logo_frame)
        
        tk.Label(logo_frame, text="Traffic Violation\nSystem", 
                 bg=self.get_color('teal'), fg=self.get_color('white'), 
                 font=("Arial", 20, "bold")).pack(pady=10)
        
        return left_frame
    
    def _create_traffic_light(self, parent):
        canvas = tk.Canvas(parent, width=100, height=220, bg=self.get_color('teal'), 
                          highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(40, 20, 70, 220, fill=self.get_color('dark'), outline="")
        canvas.create_oval(30, 30, 80, 80, fill="red")
        canvas.create_oval(30, 100, 80, 150, fill="yellow")
        canvas.create_oval(30, 170, 80, 220, fill="green")


class LoginFormFrame(BaseFrame):
    
    def __init__(self, parent, on_login_callback):
        super().__init__(parent)
        self.on_login_callback = on_login_callback
        self.username_entry = None
        self.password_entry = None
    
    def create(self):
        right_frame = tk.Frame(self.parent, bg=self.get_color('white'))
        right_frame.pack(side="right", expand=True, fill="both")
        
        tk.Label(right_frame, text="Login", bg=self.get_color('white'), 
                 fg=self.get_color('dark'), font=("Arial", 24, "bold")).pack(pady=40)
        
        self._create_username_field(right_frame)
        self._create_password_field(right_frame)
        self._create_login_button(right_frame)
        
        return right_frame
    
    def _create_username_field(self, parent):
        tk.Label(parent, text="Username", bg=self.get_color('white'), 
                 fg=self.get_color('dark'), font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(parent, bg=self.get_color('light_cyan'), 
                                       fg=self.get_color('dark'), font=("Arial", 14))
        self.username_entry.pack(pady=10, ipadx=30, ipady=8)
    
    def _create_password_field(self, parent):
        tk.Label(parent, text="Password", bg=self.get_color('white'), 
                 fg=self.get_color('dark'), font=("Arial", 14)).pack(pady=10)
        self.password_entry = tk.Entry(parent, bg=self.get_color('light_cyan'), 
                                       fg=self.get_color('dark'), show="*", font=("Arial", 14))
        self.password_entry.pack(pady=10, ipadx=30, ipady=8)
    
    def _create_login_button(self, parent):
        tk.Button(parent, text="Login", bg=self.get_color('light_teal'), 
                  fg=self.get_color('white'), font=("Arial", 14, "bold"),
                  command=self.on_login_callback).pack(pady=40, ipadx=20, ipady=10)
    
    def get_credentials(self):
        return self.username_entry.get(), self.password_entry.get()


class LoginPage(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.auth_service = AuthenticationService()
        self.logo_frame = None
        self.form_frame = None
        
        self.window = tk.Tk()
        self.window.title("Login - Traffic Violation System")
        self.window.state("zoomed")
        
        self.setup_ui()
    
    def setup_ui(self):
        self.logo_frame = LoginLogoFrame(self.window)
        self.logo_frame.create()
        
        self.form_frame = LoginFormFrame(self.window, self.handle_login)
        self.form_frame.create()
    
    def handle_login(self):
        try:
            username, password = self.form_frame.get_credentials()
            
            if self.auth_service.authenticate(username, password):
                self.close()
                from ui_management import ManagementPage
                management_page = ManagementPage()
                management_page.run()
            else:
                messagebox.showerror("Error", "Invalid Username or Password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed:\n{e}")
