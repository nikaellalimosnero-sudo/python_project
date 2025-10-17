from ui_login import LoginPage
from tkinter import messagebox


class TrafficViolationApplication:
    
    def __init__(self):
        self.current_page = None
    
    def start(self):
        try:
            self.current_page = LoginPage()
            self.current_page.run()
        except Exception as e:
            messagebox.showerror("Critical Error", f"Application failed to start:\n{e}")


def main():
    app = TrafficViolationApplication()
    app.start()


if __name__ == "__main__":
    main()
